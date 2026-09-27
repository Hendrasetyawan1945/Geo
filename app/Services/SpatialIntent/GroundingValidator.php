<?php

declare(strict_types=1);

namespace App\Services\SpatialIntent;

/**
 * Algorithmic Grounding Validator (Claim-Level Post-Generation Verifier)
 *
 * Memeriksa narasi teks keluaran LLM terhadap himpunan fakta (F) hasil kueri SQL.
 * Memverifikasi integritas pada tingkat klaim granular (Claim-Level Grounding):
 * 1. Entity Grounding: Memastikan setiap POI yang disebut merupakan anggota himpunan fakta (\forall e \in E, e \in F).
 * 2. Attribute Grounding: Memverifikasi klaim harga tiket (Rp X / gratis) sesuai data basis data.
 * 3. Spatial Grounding: Memverifikasi klaim jarak (X km) selaras dengan hasil komputasi ST_Distance_Sphere.
 * 4. Temporal/Operational Grounding: Memverifikasi jam operasional dan status buka.
 *
 * Prinsip Keamanan:
 * - Fail-Closed: Jika fakta SQL kosong dan LLM menyebut entitas destinasi, status wajib NOT GROUNDED.
 * - Deterministic Fallback: Jika terjadi pelanggaran grounding sekecil apa pun, output LLM dibatalkan.
 */
class GroundingValidator
{
    /** Daftar master nama 22 wisata Kota Padang untuk deteksi entitas */
    public const MASTER_POI_NAMES = [
        'Pantai Air Manis',
        'Pantai Padang',
        'Pantai Nirwana',
        'Pantai Carolina',
        'Pantai Pasir Jambak',
        'Pulau Sikuai',
        'Pulau Setan Lokang',
        'Pulau Pisang Gantung',
        'Lubuk Hitam',
        'Bukit Nobita',
        'Bukit Lampu',
        'Taman Hutan Raya Bung Hatta',
        'Museum Adityawarman',
        'Museum Situs Rumah Bersejarah',
        'Rumah Gadang Pallindo',
        'Jembatan Siti Nurbaya',
        'Masjid Raya Ganting',
        'Tugu Adipura',
        'Rumah Makan Sederhana',
        'Warung Soto Padang',
        'Pondok Mie Kocok Bandung',
        'Pasar Raya Padang',
    ];

    /** Kategori resmi */
    public const VALID_CATEGORIES = [
        'Pantai',
        'Pulau',
        'Alam',
        'Museum',
        'Sejarah',
        'Kuliner',
    ];

    /**
     * Validasi claim-level grounding respons teks terhadap himpunan fakta SQL.
     *
     * @param string $llmResponse
     * @param array<int, array<string, mixed>> $retrievedFacts
     * @return array{
     *     isGrounded: bool,
     *     violations: list<string>,
     *     fabricatedEntities: list<string>,
     *     claimStats: array{totalClaims: int, supportedClaims: int, fidelity: float}
     * }
     */
    public function validate(string $llmResponse, array $retrievedFacts): array
    {
        $violations = [];
        $fabricated = [];
        $totalClaims = 0;
        $supportedClaims = 0;

        $mentionedPois = $this->extractMentionedPois($llmResponse);

        // 1. Fail-Closed Invariant: Penanganan Kondisi Fakta SQL Kosong
        if (empty($retrievedFacts)) {
            if (!empty($mentionedPois)) {
                // LLM merekomendasikan destinasi padahal basis data tidak menemukan hasil
                foreach ($mentionedPois as $poi) {
                    $violations[] = sprintf("Fakta basis data kosong, namun narasi merekomendasikan entitas '%s'.", $poi);
                    $fabricated[] = $poi;
                    $totalClaims++;
                }
                return [
                    'isGrounded'         => false,
                    'violations'         => $violations,
                    'fabricatedEntities' => $fabricated,
                    'claimStats'         => ['totalClaims' => $totalClaims, 'supportedClaims' => 0, 'fidelity' => 0.0],
                ];
            }

            // Jika fakta kosong dan respons tidak menyebut POI apa pun (misal penolakan jujur)
            return [
                'isGrounded'         => true,
                'violations'         => [],
                'fabricatedEntities' => [],
                'claimStats'         => ['totalClaims' => 0, 'supportedClaims' => 0, 'fidelity' => 100.0],
            ];
        }

        // 2. Pemetaan Fakta Basis Data Berdasarkan Nama Kanonikal
        /** @var array<string, array<string, mixed>> $factsByName */
        $factsByName = [];
        foreach ($retrievedFacts as $row) {
            $nameKey = strtolower(trim((string) ($row['nama'] ?? '')));
            if ($nameKey !== '') {
                $factsByName[$nameKey] = $row;
            }
        }

        // 3. Verifikasi Granular per-Entitas dan Atribut (Claim-Level Verification)
        $sentences = $this->splitIntoSentences($llmResponse);

        foreach ($mentionedPois as $poi) {
            $lowerPoi = strtolower($poi);
            $totalClaims++; // Klaim eksistensi entitas

            if (!isset($factsByName[$lowerPoi])) {
                // Pelanggaran Entity Grounding (Entitas Fiktif / Luar Hasil Kueri)
                $violations[] = sprintf("Entitas '%s' disebut dalam respons namun tidak terdapat dalam himpunan fakta kueri SQL.", $poi);
                $fabricated[] = $poi;
                continue;
            }

            $supportedClaims++; // Entitas terverifikasi ada dalam himpunan fakta
            $factRow = $factsByName[$lowerPoi];

            // Isolasi konteks segmen khusus untuk POI ini (mencegah kontaminasi antarentitas dalam satu kalimat)
            $contextText = $this->extractContextForPoi($llmResponse, $poi, $mentionedPois);

            // A. Verifikasi Klaim Harga (Price Claim Grounding)
            $this->verifyPriceClaim($contextText, $factRow, $poi, $violations, $totalClaims, $supportedClaims);

            // B. Verifikasi Klaim Jarak Spasial (Spatial Distance Claim Grounding)
            $this->verifyDistanceClaim($contextText, $factRow, $poi, $violations, $totalClaims, $supportedClaims);

            // C. Verifikasi Klaim Jam Operasional (Operational Hours Claim Grounding)
            $this->verifyOperationalClaim($contextText, $factRow, $poi, $violations, $totalClaims, $supportedClaims);
        }

        $fidelity = $totalClaims > 0 ? round(($supportedClaims / $totalClaims) * 100.0, 2) : 100.0;
        $isGrounded = empty($violations);

        return [
            'isGrounded'         => $isGrounded,
            'violations'         => $violations,
            'fabricatedEntities' => $fabricated,
            'claimStats'         => [
                'totalClaims'     => $totalClaims,
                'supportedClaims' => $supportedClaims,
                'fidelity'        => $fidelity,
            ],
        ];
    }

    /**
     * Ekstraksi seluruh nama POI yang disebut dalam respons (format tebal **Nama** maupun kamus master).
     *
     * @param string $text
     * @return list<string>
     */
    public function extractMentionedPois(string $text): array
    {
        $found = [];
        $lowerText = strtolower($text);

        // 1. Ekstraksi dari markdown bold (**Nama POI**)
        if (preg_match_all('/\*\*([^*]+)\*\*/', $text, $matches)) {
            foreach ($matches[1] as $boldPhrase) {
                $trimmed = trim($boldPhrase);
                foreach (self::MASTER_POI_NAMES as $masterPoi) {
                    if (strcasecmp($trimmed, $masterPoi) === 0 && !in_array($masterPoi, $found, true)) {
                        $found[] = $masterPoi;
                    }
                }
            }
        }

        // 2. Pencocokan langsung terhadap daftar master 22 POI
        foreach (self::MASTER_POI_NAMES as $masterPoi) {
            if (str_contains($lowerText, strtolower($masterPoi)) && !in_array($masterPoi, $found, true)) {
                $found[] = $masterPoi;
            }
        }

        return $found;
    }

    /**
     * Verifikasi klaim harga tiket masuk.
     */
    private function verifyPriceClaim(
        string $context,
        array $fact,
        string $poi,
        array &$violations,
        int &$totalClaims,
        int &$supportedClaims
    ): void {
        $actualPrice = isset($fact['harga_tiket']) ? (int) $fact['harga_tiket'] : null;
        if ($actualPrice === null) {
            return;
        }

        // Deteksi klaim gratis
        if (preg_match('/\b(gratis|tanpa biaya|free)\b/i', $context)) {
            $totalClaims++;
            if ($actualPrice === 0) {
                $supportedClaims++;
            } else {
                $violations[] = sprintf(
                    "Klaim harga untuk '%s' menyimpang: dinyatakan gratis, tetapi data faktual adalah Rp%s.",
                    $poi,
                    number_format($actualPrice, 0, ',', '.')
                );
            }
            return;
        }

        // Deteksi klaim harga eksplisit (Rp10.000 atau 10.000 rupiah atau 10 ribu)
        if (preg_match('/(?:rp\.?\s*|tiket\s*(?:masuk\s*)?(?:sebesar\s*)?)([0-9.]+)/i', $context, $m)) {
            $rawNumber = str_replace('.', '', $m[1]);
            $claimedPrice = (int) $rawNumber;
            if ($claimedPrice > 0) {
                $totalClaims++;
                if ($claimedPrice === $actualPrice) {
                    $supportedClaims++;
                } else {
                    $violations[] = sprintf(
                        "Klaim harga untuk '%s' menyimpang: dinyatakan Rp%s, data faktual adalah Rp%s.",
                        $poi,
                        number_format($claimedPrice, 0, ',', '.'),
                        number_format($actualPrice, 0, ',', '.')
                    );
                }
            }
        } elseif (preg_match('/([0-9]+)\s*ribu/i', $context, $m)) {
            $claimedPrice = ((int) $m[1]) * 1000;
            $totalClaims++;
            if ($claimedPrice === $actualPrice) {
                $supportedClaims++;
            } else {
                $violations[] = sprintf(
                    "Klaim harga untuk '%s' menyimpang: dinyatakan Rp%s, data faktual adalah Rp%s.",
                    $poi,
                    number_format($claimedPrice, 0, ',', '.'),
                    number_format($actualPrice, 0, ',', '.')
                );
            }
        }
    }

    /**
     * Verifikasi klaim jarak geografis (km).
     */
    private function verifyDistanceClaim(
        string $context,
        array $fact,
        string $poi,
        array &$violations,
        int &$totalClaims,
        int &$supportedClaims
    ): void {
        $actualDist = isset($fact['jarak_km']) ? (float) $fact['jarak_km'] : null;
        if ($actualDist === null) {
            return;
        }

        if (preg_match('/([0-9]+(?:[.,][0-9]+)?)\s*km\b/i', $context, $m)) {
            $claimedDist = (float) str_replace(',', '.', $m[1]);
            $totalClaims++;

            // Toleransi pembulatan teks narasi sebesar 0.6 km
            if (abs($claimedDist - $actualDist) <= 0.6) {
                $supportedClaims++;
            } else {
                $violations[] = sprintf(
                    "Klaim jarak spasial untuk '%s' menyimpang: dinyatakan %.2f km, hasil komputasi ST_Distance_Sphere adalah %.2f km.",
                    $poi,
                    $claimedDist,
                    $actualDist
                );
            }
        }
    }

    /**
     * Verifikasi klaim jam operasional dan status buka.
     */
    private function verifyOperationalClaim(
        string $context,
        array $fact,
        string $poi,
        array &$violations,
        int &$totalClaims,
        int &$supportedClaims
    ): void {
        if (preg_match('/\b24\s*jam\b/i', $context)) {
            $totalClaims++;
            $is24h = ($fact['jam_buka'] ?? '') === '00:00:00' && ($fact['jam_tutup'] ?? '') >= '23:59:00';
            if ($is24h) {
                $supportedClaims++;
            } else {
                $violations[] = sprintf(
                    "Klaim jam operasional 24 jam untuk '%s' menyimpang dari jadwal basis data (%s - %s).",
                    $poi,
                    $fact['jam_buka'] ?? '-',
                    $fact['jam_tutup'] ?? '-'
                );
            }
        }
    }

    /**
     * Pisahkan teks ke dalam array kalimat.
     *
     * @param string $text
     * @return list<string>
     */
    private function splitIntoSentences(string $text): array
    {
        $parts = preg_split('/(?<=[.!?\n])\s+/', $text, -1, PREG_SPLIT_NO_EMPTY);
        return is_array($parts) ? $parts : [$text];
    }

    /**
     * Mengisolasi segmen klaim teks yang relevan khusus untuk POI target.
     * Mencegah kontaminasi silang atribut antarentitas dalam satu kalimat majemuk.
     *
     * @param string $text
     * @param string $targetPoi
     * @param list<string> $allPois
     * @return string
     */
    private function extractContextForPoi(string $text, string $targetPoi, array $allPois): string
    {
        $lowerText = strtolower($text);
        $lowerTarget = strtolower($targetPoi);

        $pos = strpos($lowerText, $lowerTarget);
        if ($pos === false) {
            return '';
        }

        // Cari batas akhir kemunculan POI berikutnya
        $endPos = strlen($text);
        foreach ($allPois as $otherPoi) {
            if (strcasecmp($otherPoi, $targetPoi) === 0) {
                continue;
            }
            $otherPos = strpos($lowerText, strtolower($otherPoi));
            if ($otherPos !== false && $otherPos > $pos && $otherPos < $endPos) {
                $endPos = $otherPos;
            }
        }

        return substr($text, $pos, $endPos - $pos);
    }
}

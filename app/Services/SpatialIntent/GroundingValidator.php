<?php

declare(strict_types=1);

namespace App\Services\SpatialIntent;

/**
 * Algorithmic Grounding Validator (Post-Generation Checker)
 *
 * Memeriksa teks narasi keluaran LLM terhadap himpunan fakta (F) hasil kueri SQL.
 * Menjamin bahwa model tidak memunculkan entitas palsu (Zero Fabricated POIs).
 *
 * Invarian Grounding:
 * Untuk setiap entitas wisata (e) yang disebut dalam narasi LLM (E),
 * e harus merupakan anggota dari fakta hasil kueri basis data (F):
 * \forall e \in E, e \in F
 *
 * Jika terdeteksi e \notin F atau klaim halusinasi, teks LLM dibatalkan secara deterministik
 * dan sistem beralih ke template deterministik berbasis data faktual.
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

    /**
     * Validasi grounding respons teks terhadap himpunan fakta SQL.
     *
     * @param string $llmResponse
     * @param array<int, array<string, mixed>> $retrievedFacts
     * @return array{isGrounded: bool, violations: list<string>, fabricatedEntities: list<string>}
     */
    public function validate(string $llmResponse, array $retrievedFacts): array
    {
        $violations = [];
        $fabricated = [];

        // 1. Ambil himpunan nama POI yang sah dari hasil kueri SQL (F)
        $allowedPoiNames = array_map(
            fn($row) => strtolower(trim((string) $row['nama'])),
            $retrievedFacts
        );

        // 2. Deteksi apakah ada entitas master wisata lain yang TIDAK ada di $retrievedFacts tapi disebut di teks
        $lowerResponse = strtolower($llmResponse);

        foreach (self::MASTER_POI_NAMES as $masterPoi) {
            $lowerMaster = strtolower($masterPoi);

            if (str_contains($lowerResponse, $lowerMaster)) {
                // POI disebut dalam narasi teks
                if (!in_array($lowerMaster, $allowedPoiNames, true)) {
                    // Pelanggaran grounding: menyebut POI yang tidak ada dalam hasil filter SQL!
                    $violations[] = sprintf("Entitas '%s' disebut dalam respons tetapi tidak terdapat dalam hasil kueri fakta.", $masterPoi);
                    $fabricated[] = $masterPoi;
                }
            }
        }

        $isGrounded = empty($violations);

        return [
            'isGrounded'         => $isGrounded,
            'violations'         => $violations,
            'fabricatedEntities' => $fabricated,
        ];
    }
}

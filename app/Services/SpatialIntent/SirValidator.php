<?php

declare(strict_types=1);

namespace App\Services\SpatialIntent;

/**
 * Deterministic SIR Validator (6-Dimensional Invariant Enforcer)
 *
 * Mengimplementasikan 6 lapisan validasi invarian deterministik untuk mengontrol
 * dan membatasi kewenangan LLM sebelum SIR diizinkan masuk ke SQL Compiler:
 *
 * Dimensi 1: Schema & Type Integrity (integritas atribut, sanitasi XSS/tag)
 * Dimensi 2: Spatial Domain Validity (verifikasi rentang nilai radius > 0 tanpa abs())
 * Dimensi 3: Spatial Operator Validity (verifikasi ontologi operator tanpa auto-cast ke 'none')
 * Dimensi 4: Reference Coordinate Bounds (verifikasi batas geodesik WGS84)
 * Dimensi 5: Operational & Price Constraints (aturan konsistensi non-negatif & anti-kontradiksi)
 * Dimensi 6: Domain Scope & Ontological Boundary (verifikasi kategori resmi & penolakan out-of-scope)
 *
 * Prinsip Rekayasa (Safety Invariant - No Intent Alteration):
 * Validator TIDAK BOLEH mengubah niat pengguna secara diam-diam (misal: radius -5 km diubah jadi 5 km,
 * atau operator salah diubah jadi 'none'). Jika batasan melanggar invarian, SIR ditandai isValid = false
 * dengan daftar error eksplisit untuk memicu klarifikasi/penolakan jujur, BUKAN eksekusi sembarangan.
 */
class SirValidator
{
    /** Batas ambang atas radius operasional Kota Padang (km) */
    public const MAX_OPERATIONAL_RADIUS_KM = 50.0;

    /** Daftar kata kunci entitas di luar domain yurisdiksi pariwisata Kota Padang */
    public const OUT_OF_SCOPE_KEYWORDS = [
        'salju',
        'ski',
        'kasino',
        'casino',
        'judi',
        'candi',
        'candi hindu',
        'candi buddha',
        'borobudur',
        'prambanan',
        'gunung es',
        'kereta gantung',
        'monorail',
        'disneyland',
        'dufan',
        'trans studio',
    ];

    /**
     * Jalankan validasi 6-dimensi terhadap objek SpatialIntent.
     *
     * @param SpatialIntent $sir
     * @return array{sir: SpatialIntent, isValid: bool, errors: list<string>, executionPolicy: string}
     */
    public function validate(SpatialIntent $sir): array
    {
        $errors = [];

        // 1. Dimensi 1: Schema & Type Integrity
        $this->validateSchemaAndTypes($sir);

        // 2. Dimensi 2: Spatial Domain Validity (No Intent Alteration!)
        $this->validateSpatialDomain($sir, $errors);

        // 3. Dimensi 3: Spatial Operator Validity (No Silently Casting to 'none'!)
        $this->validateSpatialOperator($sir, $errors);

        // 4. Dimensi 4: Reference Coordinate Bounds
        $this->validateSpatialReference($sir, $errors);

        // 5. Dimensi 5: Operational & Price Constraints (Consistency Rules)
        $this->validateOperationalConstraints($sir, $errors);

        // 6. Dimensi 6: Domain Scope & Ontological Boundary
        $this->validateOntologicalScope($sir, $errors);

        // Finalisasi status Canonical SIR (CSIR)
        $isValid = empty($errors);
        $sir->isValid = $isValid;
        $sir->validationErrors = $errors;

        if ($sir->isOutOfScope) {
            $sir->validationStatus = 'out_of_scope';
            $sir->executionPolicy = 'reject_out_of_scope';
        } elseif (!$isValid) {
            $sir->validationStatus = 'rejected';
            $sir->executionPolicy = 'clarify_user';
        } else {
            $sir->validationStatus = 'validated';
            $sir->executionPolicy = 'execute_sql';
        }

        return [
            'sir'             => $sir,
            'isValid'         => $isValid,
            'errors'          => $errors,
            'executionPolicy' => $sir->executionPolicy,
        ];
    }

    /**
     * Dimensi 1: Schema & Type Integrity.
     * Sanitasi teks bebas untuk mencegah XSS/tag injection.
     */
    private function validateSchemaAndTypes(SpatialIntent $sir): void
    {
        if ($sir->targetName !== null) {
            $cleaned = trim(strip_tags($sir->targetName));
            $sir->targetName = $cleaned !== '' ? $cleaned : null;
        }

        if ($sir->keyword !== null) {
            $cleaned = trim(strip_tags($sir->keyword));
            $sir->keyword = $cleaned !== '' ? $cleaned : null;
        }

        if ($sir->adminArea !== null) {
            $cleaned = trim(strip_tags($sir->adminArea));
            $sir->adminArea = $cleaned !== '' ? $cleaned : null;
        }

        if ($sir->sort !== null) {
            $allowedSorts = ['termurah', 'termahal', 'terdekat', 'terbaik'];
            if (!in_array(strtolower($sir->sort), $allowedSorts, true)) {
                $sir->sort = null;
            }
        }
    }

    /**
     * Dimensi 2: Spatial Domain Validity.
     * Memastikan nilai radius bernilai positif (> 0).
     * PENTING: Dilarang menggunakan abs() karena akan memanipulasi maksud user secara diam-diam!
     */
    private function validateSpatialDomain(SpatialIntent $sir, array &$errors): void
    {
        if ($sir->radius !== null) {
            if ($sir->radius <= 0) {
                // Menolak radius negatif/nol tanpa mengubah via abs()
                $errors[] = sprintf('Radius pencarian tidak valid: %.2f km (harus berupa bilangan positif > 0).', $sir->radius);
            } elseif ($sir->radius > 100.0) {
                // Jika radius di luar jangkauan wajar perkotaan, normalisasi ke batas maksimum operasional
                $sir->radius = self::MAX_OPERATIONAL_RADIUS_KM;
            }
        }
    }

    /**
     * Dimensi 3: Spatial Operator Validity.
     * Operator harus terdaftar dalam ontologi spasial.
     * PENTING: Dilarang mengubah operator tak dikenal menjadi 'none' diam-diam!
     */
    private function validateSpatialOperator(SpatialIntent $sir, array &$errors): void
    {
        if (!in_array($sir->spatialOperator, SpatialIntent::VALID_OPERATORS, true)) {
            $errors[] = sprintf("Operator spasial '%s' tidak terdaftar dalam ontologi spasial sistem.", $sir->spatialOperator);
        }

        // Operator within_admin_area wajib memiliki nama wilayah
        if ($sir->spatialOperator === 'within_admin_area' && empty($sir->adminArea)) {
            $errors[] = "Operator 'within_admin_area' memerlukan parameter nama wilayah/kecamatan.";
        }
    }

    /**
     * Dimensi 4: Reference Coordinate Bounds.
     * Memeriksa rentang koordinat geografis WGS84 (-90 <= lat <= 90, -180 <= lng <= 180).
     */
    private function validateSpatialReference(SpatialIntent $sir, array &$errors): void
    {
        if ($sir->latitude !== null) {
            if ($sir->latitude < -90.0 || $sir->latitude > 90.0) {
                $errors[] = sprintf('Koordinat latitude di luar batas WGS84: %f', $sir->latitude);
            }
        }

        if ($sir->longitude !== null) {
            if ($sir->longitude < -180.0 || $sir->longitude > 180.0) {
                $errors[] = sprintf('Koordinat longitude di luar batas WGS84: %f', $sir->longitude);
            }
        }
    }

    /**
     * Dimensi 5: Operational & Price Constraints.
     * Validasi batasan harga dan penyelesaian kontradiksi logika.
     */
    private function validateOperationalConstraints(SpatialIntent $sir, array &$errors): void
    {
        if ($sir->maxPrice !== null) {
            if ($sir->maxPrice < 0) {
                $errors[] = sprintf('Batas harga maksimum tidak boleh bernilai negatif (diterima: %d).', $sir->maxPrice);
            }
        }

        // Kontradiksi: meminta tiket gratis namun menetapkan batas harga > 0
        if ($sir->isFree && $sir->maxPrice !== null && $sir->maxPrice > 0) {
            $errors[] = sprintf('Kontradiksi batasan anggaran: meminta tiket gratis (is_free = true) namun membatasi harga Rp%s.', number_format($sir->maxPrice, 0, ',', '.'));
        }
    }

    /**
     * Dimensi 6: Domain Scope & Ontological Boundary.
     * Memeriksa keselarasan kategori dengan ontologi resmi dan mendeteksi kueri luar lingkup.
     */
    private function validateOntologicalScope(SpatialIntent $sir, array &$errors): void
    {
        // 1. Periksa kategori resmi
        if ($sir->category !== null) {
            $matched = false;
            foreach (SpatialIntent::VALID_CATEGORIES as $validCat) {
                if (strcasecmp($sir->category, $validCat) === 0) {
                    $sir->category = $validCat; // Preservasi huruf kapital kanonikal
                    $matched = true;
                    break;
                }
            }
            if (!$matched) {
                $errors[] = sprintf("Kategori '%s' tidak dikenal dalam ontologi pariwisata Kota Padang.", $sir->category);
            }
        }

        // 2. Deteksi kueri di luar yurisdiksi pariwisata Padang (Out-of-Scope)
        $textToCheck = strtolower($sir->rawQuery . ' ' . ($sir->keyword ?? '') . ' ' . ($sir->targetName ?? ''));
        foreach (self::OUT_OF_SCOPE_KEYWORDS as $outKeyword) {
            if (str_contains($textToCheck, $outKeyword)) {
                $sir->isOutOfScope = true;
                $sir->outOfScopeReason = sprintf("Permintaan '%s' berada di luar lingkup domain pariwisata Kota Padang.", $outKeyword);
                $errors[] = $sir->outOfScopeReason;
                break;
            }
        }
    }
}

<?php

declare(strict_types=1);

namespace App\Services\SpatialIntent;

/**
 * Spatial Intent Representation (SIR) & Canonical Spatial Intent Representation (CSIR)
 *
 * DTO formal yang merepresentasikan maksud spasial pengguna hasil ekstraksi semantik LLM.
 * Berperan sebagai typed compiler IR (intermediate representation) antara bahasa alami
 * dan eksekusi komputasi spasial deterministik pada MySQL 8.0 Spatial Engine.
 *
 * Dipartisi secara formal menjadi 3 kelompok semantik inti + 1 kelompok control metadata:
 * 1. Intent Semantics (maksud utama, kategori, target POI, kata kunci)
 * 2. Spatial Constraints (operator spasial ontologis, titik acuan, radius, wilayah)
 * 3. Operational Constraints (harga, jam operasional, status buka, sorting)
 * 4. Control Metadata / CSIR (status validasi, error list, kebijakan eksekusi, penanda out-of-scope)
 */
class SpatialIntent
{
    /** Kategori wisata Kota Padang yang sah dalam ontologi sistem */
    public const VALID_CATEGORIES = [
        'Pantai',
        'Pulau',
        'Alam',
        'Museum',
        'Sejarah',
        'Kuliner',
    ];

    /** Operator spasial resmi yang terdefinisi dalam ontologi spasial */
    public const VALID_OPERATORS = [
        'nearest',           // Cari terdekat dari titik acuan (ORDER BY distance ASC LIMIT k)
        'within_radius',     // Dalam radius lingkaran (ST_Distance_Sphere <= radius)
        'within_admin_area', // Dalam wilayah/kecamatan administratif tertentu (alamat LIKE %)
        'none',              // Tidak ada batasan spasial eksplisit
    ];

    /** Tipe titik acuan spasial */
    public const VALID_REFERENCES = [
        'gps',         // Koordinat GPS langsung dari perangkat pengguna
        'city_center', // Pusat Kota Padang (-0.9471, 100.4174)
        'poi',         // Mengacu pada nama POI tertentu
        'unknown',
    ];

    public function __construct(
        // === 1. Intent Semantics ===
        public string $intent = 'spatial_recommendation', // spatial_recommendation, entity_lookup, general_inquiry
        public string $entity = 'tourism_object',
        public ?string $category = null,
        public ?string $targetName = null,
        public ?string $keyword = null,

        // === 2. Spatial Constraints ===
        public string $spatialOperator = 'none',
        public string $referenceType = 'unknown',
        public ?string $referenceEntity = null,
        public ?float $latitude = null,
        public ?float $longitude = null,
        public ?float $radius = 20.0, // Default radius 20.0 km jika radius query
        public string $distanceUnit = 'km',
        public ?string $adminArea = null,

        // === 3. Operational Constraints ===
        public bool $isFree = false,
        public ?int $maxPrice = null,
        public bool $openNow = false,
        public bool $open24h = false,
        public ?string $sort = null, // termurah, termahal, terdekat, terbaik

        // === 4. Control Metadata & CSIR (Hasil Validasi Sistem) ===
        public string $rawQuery = '',
        public bool $isValid = true,
        public string $validationStatus = 'pending', // pending, validated, rejected, out_of_scope
        /** @var list<string> */
        public array $validationErrors = [],
        public string $executionPolicy = 'execute_sql', // execute_sql, reject_out_of_scope, clarify_user
        public bool $isOutOfScope = false,
        public ?string $outOfScopeReason = null,
        public bool $fallbackApplied = false,
        public ?string $fallbackNotice = null,
    ) {}

    /**
     * Instansiasi Raw SIR dari array hasil parsing LLM.
     *
     * @param array<string, mixed> $data
     * @param string $rawQuery
     * @return self
     */
    public static function fromArray(array $data, string $rawQuery = ''): self
    {
        // Normalisasi kategori
        $category = null;
        $rawCat = $data['category'] ?? $data['kategori'] ?? null;
        if (is_string($rawCat) && trim($rawCat) !== '') {
            $category = trim($rawCat);
        }

        // Normalisasi nama target / keyword
        $targetName = null;
        $rawTarget = $data['target_name'] ?? $data['nama_wisata'] ?? null;
        if (is_string($rawTarget) && trim($rawTarget) !== '') {
            $targetName = trim($rawTarget);
        }

        $keyword = null;
        $rawKw = $data['keyword'] ?? $data['kata_kunci'] ?? null;
        if (is_string($rawKw) && trim($rawKw) !== '') {
            $keyword = trim($rawKw);
        }

        // Operator spasial
        $spatialOp = (string) ($data['spatial_operator'] ?? 'none');
        if ($spatialOp === 'none') {
            if (isset($data['urutan']) && $data['urutan'] === 'terdekat') {
                $spatialOp = 'nearest';
            } elseif (!empty($data['radius']) || !empty($data['distance'])) {
                $spatialOp = 'within_radius';
            } elseif (!empty($data['admin_area']) || !empty($data['wilayah'])) {
                $spatialOp = 'within_admin_area';
            }
        }

        // Radius / Distance
        $radiusVal = null;
        if (isset($data['radius']) && is_numeric($data['radius'])) {
            $radiusVal = (float) $data['radius'];
        } elseif (isset($data['distance']) && is_numeric($data['distance'])) {
            $radiusVal = (float) $data['distance'];
        }

        // Harga
        $maxPrice = null;
        if (isset($data['max_price']) && is_numeric($data['max_price'])) {
            $maxPrice = (int) $data['max_price'];
        } elseif (isset($data['harga_maksimal']) && is_numeric($data['harga_maksimal'])) {
            $maxPrice = (int) $data['harga_maksimal'];
        }

        $isFree = (bool) ($data['is_free'] ?? $data['gratis'] ?? false);
        $openNow = (bool) ($data['open_now'] ?? $data['buka_sekarang'] ?? false);
        $open24h = (bool) ($data['open_24h'] ?? $data['buka_24jam'] ?? false);

        $sort = isset($data['sort']) && is_string($data['sort']) ? $data['sort'] : ($data['urutan'] ?? null);

        $adminArea = isset($data['admin_area']) && is_string($data['admin_area'])
            ? trim($data['admin_area'])
            : (isset($data['wilayah']) && is_string($data['wilayah']) ? trim($data['wilayah']) : null);

        $refType = (string) ($data['reference_type'] ?? 'unknown');
        if ($refType === 'unknown') {
            if (isset($data['latitude'], $data['longitude']) && is_numeric($data['latitude']) && is_numeric($data['longitude'])) {
                $refType = 'gps';
            }
        }

        return new self(
            intent: (string) ($data['intent'] ?? 'spatial_recommendation'),
            entity: (string) ($data['entity'] ?? 'tourism_object'),
            category: $category,
            targetName: $targetName,
            keyword: $keyword,
            spatialOperator: $spatialOp,
            referenceType: $refType,
            referenceEntity: isset($data['reference_entity']) ? (string) $data['reference_entity'] : null,
            latitude: isset($data['latitude']) && is_numeric($data['latitude']) ? (float) $data['latitude'] : null,
            longitude: isset($data['longitude']) && is_numeric($data['longitude']) ? (float) $data['longitude'] : null,
            radius: $radiusVal ?? ($spatialOp === 'within_radius' ? 20.0 : null),
            distanceUnit: (string) ($data['distance_unit'] ?? $data['unit'] ?? 'km'),
            adminArea: $adminArea,
            isFree: $isFree,
            maxPrice: $maxPrice,
            openNow: $openNow,
            open24h: $open24h,
            sort: is_string($sort) ? trim($sort) : null,
            rawQuery: $rawQuery,
        );
    }

    /**
     * Konversi ke Canonical SIR (CSIR) format array terstandarisasi.
     */
    public function toCanonicalArray(): array
    {
        return [
            'semantics' => [
                'intent'      => $this->intent,
                'entity'      => $this->entity,
                'category'    => $this->category,
                'target_name' => $this->targetName,
                'keyword'     => $this->keyword,
            ],
            'spatial_constraints' => [
                'operator'         => $this->spatialOperator,
                'reference_type'   => $this->referenceType,
                'reference_entity' => $this->referenceEntity,
                'latitude'         => $this->latitude,
                'longitude'        => $this->longitude,
                'radius'           => $this->radius,
                'distance_unit'    => $this->distanceUnit,
                'admin_area'       => $this->adminArea,
            ],
            'operational_constraints' => [
                'is_free'   => $this->isFree,
                'max_price' => $this->maxPrice,
                'open_now'  => $this->openNow,
                'open_24h'  => $this->open24h,
                'sort'      => $this->sort,
            ],
            'control_metadata' => [
                'is_valid'          => $this->isValid,
                'validation_status' => $this->validationStatus,
                'validation_errors' => $this->validationErrors,
                'execution_policy'  => $this->executionPolicy,
                'is_out_of_scope'   => $this->isOutOfScope,
                'out_of_scope_reason' => $this->outOfScopeReason,
                'fallback_applied'  => $this->fallbackApplied,
                'fallback_notice'   => $this->fallbackNotice,
            ],
        ];
    }
}

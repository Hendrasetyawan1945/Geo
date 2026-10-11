<?php

declare(strict_types=1);

namespace App\Commands;

use App\Controllers\ChatController;
use App\Models\WisataModel;
use App\Services\BenchmarkDataset;
use App\Services\SpatialIntent\GroundingValidator;
use App\Services\SpatialIntent\SirValidator;
use App\Services\SpatialIntent\SpatialIntent;
use App\Services\SpatialIntent\SpatialPolicyHandler;
use CodeIgniter\CLI\BaseCommand;
use CodeIgniter\CLI\CLI;

/**
 * RisetEvaluasi Command
 *
 * Evaluator empiris berlapis 4-tingkat (Layer A: Semantic Extraction, Layer B: Deterministic Validation,
 * Layer C: Spatial Execution, Layer D: Grounded Generation) untuk benchmark 40 skenario
 * sistem rekomendasi pariwisata cerdas Kota Padang.
 *
 * Memisahkan secara ketat pengujian keandalan komputasi spasial deterministik
 * dengan kinerja inferensi semantik LLM (DeepSeek vs Heuristic Mock).
 */
class RisetEvaluasi extends BaseCommand
{
    protected $group       = 'Riset';
    protected $name        = 'riset:evaluasi';
    protected $description = 'Menjalankan evaluasi empiris 4-lapisan sistem Web GIS pariwisata Padang.';
    protected $usage       = 'riset:evaluasi [options]';
    protected $arguments   = [];
    protected $options     = [
        '--limit' => 'Batasi jumlah skenario pengujian',
        '--mock'  => 'Jalankan mode deterministik in-memory untuk pipeline benchmark',
        '--live'  => 'Jalankan mode live LLM inference (DeepSeek API)',
        '--json'  => 'Tampilkan output JSON murni ke stdout',
    ];

    /** Seluruh 19 atribut formal Canonical Spatial Intent Representation (CSIR) */
    public const CSIR_FIELDS = [
        'intent',
        'entity',
        'category',
        'target_name',
        'keyword',
        'spatial_operator',
        'reference_type',
        'reference_entity',
        'latitude',
        'longitude',
        'radius',
        'distance_unit',
        'admin_area',
        'is_free',
        'max_price',
        'open_now',
        'open_24h',
        'sort',
        'is_out_of_scope',
    ];

    /** Atribut wajib yang selalu dievaluasi pada setiap skenario */
    public const REQUIRED_FIELDS = [
        'intent',
        'entity',
        'category',
        'spatial_operator',
        'reference_type',
        'is_out_of_scope',
    ];

    /** Sub-dimensi Semantik */
    public const SEMANTIC_FIELDS = ['intent', 'entity', 'category', 'target_name', 'keyword'];

    /** Sub-dimensi Spasial */
    public const SPATIAL_FIELDS = ['spatial_operator', 'reference_type', 'reference_entity', 'latitude', 'longitude', 'radius', 'distance_unit', 'admin_area'];

    /** Sub-dimensi Operasional */
    public const OPERATIONAL_FIELDS = ['is_free', 'max_price', 'open_now', 'open_24h', 'sort'];

    /** Sub-dimensi Kontrol */
    public const CONTROL_FIELDS = ['is_out_of_scope'];

    public function run(array $params)
    {
        $isJsonOnly = isset($params['json']) || CLI::getOption('json') !== null;
        $isMock = isset($params['mock']) || CLI::getOption('mock') !== null;
        $isLive = isset($params['live']) || CLI::getOption('live') !== null;

        // Default ke mock jika tidak ada flag live
        $mode = $isLive ? 'LIVE' : 'MOCK';

        if (!$isJsonOnly) {
            CLI::write("==================================================================", 'green');
            CLI::write("  EVALUASI EMPIRIS BERLAPIS SISTEM SPASIAL PARIWISATA PADANG", 'yellow');
            CLI::write("  Teknologi: CodeIgniter 4.7.4 • MySQL 8.0 Spatial (ST_Distance_Sphere)", 'cyan');
            CLI::write("  Evaluasi: 4-Layer Architecture (Semantic, Validation, Spatial, Grounding)", 'cyan');
            CLI::write("==================================================================\n", 'green');
            CLI::write("Evaluation mode : " . ($mode === 'LIVE' ? 'LIVE (DeepSeek API)' : 'MOCK (Deterministic Pipeline)'), 'white');
        }

        $dataset = BenchmarkDataset::all();
        $limit = $params['limit'] ?? CLI::getOption('limit');
        if ($limit !== null && is_numeric($limit)) {
            $dataset = array_slice($dataset, 0, (int) $limit);
        }

        $totalTest = count($dataset);
        if (!$isJsonOnly) {
            CLI::write("Dataset size    : {$totalTest} standardized scenarios\n", 'white');
        }

        $chatController = new ChatController();
        $groundingValidator = new GroundingValidator();

        if ($mode === 'MOCK') {
            $chatController->setMockMode(true);
        } else {
            $chatController->setMockMode(false);
        }

        $scenarioResults = [];
        $fieldMatchesAccumulator = [];
        foreach (self::CSIR_FIELDS as $f) {
            $fieldMatchesAccumulator[$f] = ['applicable' => 0, 'correct' => 0];
        }

        $timings = [
            'intent' => [],
            'sql'    => [],
            'nlg'    => [],
            'total'  => [],
        ];

        $validationMatches = 0;
        $spatialPredicateMatches = 0;
        $pureSpatialMatches = 0;
        $totalSpatialCases = 0;
        $chitchatMatches = 0;
        $totalChitchatCases = 0;
        $honestRejectionCount = 0;
        $totalOutOfScopeCases = 0;
        $totalVerifiableClaims = 0;
        $totalSupportedClaims = 0;
        $totalMentionedEntities = 0;
        $totalGroundedEntities = 0;
        $totalFabricatedEntities = 0;
        $exactCsirMatches = 0;
        $executionEnvelopeMatches = 0;

        foreach ($dataset as $case) {
            $caseId = $case['id'];
            $prompt = $case['prompt'];
            $lat = isset($case['lat']) && is_numeric($case['lat']) ? (float) $case['lat'] : null;
            $lng = isset($case['lng']) && is_numeric($case['lng']) ? (float) $case['lng'] : null;
            $history = $case['riwayat'] ?? [];
            $expectedCsir = $case['expected_csir'] ?? $this->buildFallbackExpectedCsir($case);

            // Eksekusi Pipeline
            $res = $chatController->processCore($prompt, $lat, $lng, $history);

            /** @var SpatialIntent $sir */
            $sir = $res['sir'];
            $reply = $res['replyText'];
            $places = $res['places'];
            $timing = $res['timings'];

            $timings['intent'][] = $timing['intent_ms'];
            $timings['sql'][]    = $timing['sql_ms'];
            $timings['nlg'][]    = $timing['nlg_ms'];
            $timings['total'][]  = $timing['total_ms'];

            // === 1. LAYER A: Field-Level Semantic CSIR Comparison ===
            // Ekstraksi niat murni pengguna (Pre-fallback Intent CSIR - No Intent Alteration)
            $actualCsirArray = $this->extractActualCsirArray($sir);
            $fieldMatches = $this->compareCsirFields($expectedCsir, $actualCsirArray, $case);
            $isExactCsir = $this->isExactCsirMatch($fieldMatches);
            if ($isExactCsir) {
                $exactCsirMatches++;
            }

            // Envelope eksekusi: memperhitungkan resolusi kebijakan batas operasional (Post-policy resolution)
            $actualEnvelopeArray = $this->extractActualExecutionEnvelopeArray($sir);
            $envelopeFieldMatches = $this->compareCsirFields($expectedCsir, $actualEnvelopeArray, $case);
            $isEnvelopeMatch = $this->isExactCsirMatch($envelopeFieldMatches);
            if ($isEnvelopeMatch) {
                $executionEnvelopeMatches++;
            }

            foreach ($fieldMatches as $field => $status) {
                if ($status !== 'NOT_APPLICABLE') {
                    $fieldMatchesAccumulator[$field]['applicable']++;
                    if ($status === 'MATCH') {
                        $fieldMatchesAccumulator[$field]['correct']++;
                    }
                }
            }

            // === 2. LAYER B: Deterministic Validation Evaluation ===
            $expectedValid = $case['expected_valid'] ?? (!$expectedCsir['is_out_of_scope']);
            $expectedPolicy = $case['expected_policy'] ?? ($expectedCsir['is_out_of_scope'] ? 'reject_out_of_scope' : 'execute_sql');

            $validationMatch = ($sir->isValid === $expectedValid && $sir->executionPolicy === $expectedPolicy);
            if ($validationMatch) {
                $validationMatches++;
            }

            $isOutOfScopeCase = ($expectedCsir['is_out_of_scope'] === true);
            $honestRejectionSuccess = false;
            if ($isOutOfScopeCase) {
                $totalOutOfScopeCases++;
                if ($sir->isOutOfScope && $sir->executionPolicy === 'reject_out_of_scope' && count($places) === 0) {
                    $honestRejectionSuccess = true;
                    $honestRejectionCount++;
                }
            }

            // Klasifikasi Tipe Skenario Pengujian
            $isChitchatCase = ($case['is_sapaan'] ?? false) || ($expectedCsir['intent'] === 'general_inquiry');
            $isPureSpatialCase = !$isChitchatCase && !$isOutOfScopeCase;

            if ($isPureSpatialCase) {
                $totalSpatialCases++;
            } elseif ($isChitchatCase) {
                $totalChitchatCases++;
            }

            // === 3. LAYER C: Spatial Execution & Predicate Correctness ===
            $spatialPredicateCorrect = $this->evaluateSpatialPredicate($case, $sir, $places);
            if ($spatialPredicateCorrect) {
                $spatialPredicateMatches++;
                if ($isPureSpatialCase) {
                    $pureSpatialMatches++;
                } elseif ($isChitchatCase) {
                    $chitchatMatches++;
                }
            }

            // === 4. LAYER D: Grounded Generation Evaluation ===
            $groundingEvaluation = $this->evaluateGrounding($reply, $places, $groundingValidator, $sir, $case);
            $totalVerifiableClaims  += $groundingEvaluation['verifiable_claims'];
            $totalSupportedClaims   += $groundingEvaluation['supported_claims'];
            $totalMentionedEntities += $groundingEvaluation['mentioned_entities'];
            $totalGroundedEntities  += $groundingEvaluation['grounded_entities'];
            $totalFabricatedEntities += $groundingEvaluation['fabricated_entities'];

            // Simpan Data Per-Kasus
            $scenarioResults[] = [
                'id'                            => $caseId,
                'grup'                          => $case['grup'],
                'prompt'                        => $prompt,
                'scenario_type'                 => $isPureSpatialCase ? 'pure_spatial' : ($isChitchatCase ? 'chit_chat' : 'out_of_scope'),
                'expected'                      => $expectedCsir,
                'predicted_intent_csir'         => $actualCsirArray,
                'resolved_execution_envelope'   => $actualEnvelopeArray,
                'field_matches'                 => $fieldMatches,
                'envelope_field_matches'        => $envelopeFieldMatches,
                'exact_csir_match'              => $isExactCsir,
                'envelope_match'                => $isEnvelopeMatch,
                'validation_match'              => $validationMatch,
                'spatial_predicate_match'       => $spatialPredicateCorrect,
                'grounding'                     => $groundingEvaluation,
                'places_count'                  => count($places),
                'fallback_applied'              => $sir->fallbackApplied,
                'fallback_notice'               => $sir->fallbackNotice,
                'timings'                       => $timing,
            ];

            if (!$isJsonOnly) {
                $mismatchCount = 0;
                foreach ($fieldMatches as $st) {
                    if ($st === 'MISMATCH') {
                        $mismatchCount++;
                    }
                }

                $statusLabel = $isExactCsir ? 'EXACT_OK' : ($mismatchCount === 0 ? 'OK' : "MISMATCH({$mismatchCount})");
                CLI::write(sprintf(
                    "[%02d/%02d] %-30s | CSIR: %-12s | Valid: %-3s | SpatPred: %-3s | Claims: %02d/%02d | %5.1f ms",
                    $caseId,
                    $totalTest,
                    substr($case['grup'], 0, 30),
                    $statusLabel,
                    $validationMatch ? 'YES' : 'NO',
                    $spatialPredicateCorrect ? 'YES' : 'NO',
                    $groundingEvaluation['supported_claims'],
                    $groundingEvaluation['verifiable_claims'],
                    $timing['total_ms']
                ));
            }
        }

        // Agregasi Metrik
        $aggregated = $this->aggregateMetrics(
            $scenarioResults,
            $fieldMatchesAccumulator,
            $totalTest,
            $exactCsirMatches,
            $executionEnvelopeMatches,
            $validationMatches,
            $spatialPredicateMatches,
            $pureSpatialMatches,
            $totalSpatialCases,
            $chitchatMatches,
            $totalChitchatCases,
            $honestRejectionCount,
            $totalOutOfScopeCases,
            $totalSupportedClaims,
            $totalVerifiableClaims,
            $totalGroundedEntities,
            $totalMentionedEntities,
            $totalFabricatedEntities,
            $timings,
            $mode
        );

        if ($isJsonOnly) {
            CLI::write(json_encode($aggregated, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
            return;
        }

        // Tampilkan Laporan Konsol Rinci
        $this->renderConsoleReport($aggregated, $scenarioResults);

        // Simpan Hasil JSON ke disk
        $reportPath = WRITEPATH . 'riset_evaluasi_mysql.json';
        file_put_contents($reportPath, json_encode($aggregated, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

        // Buat dan simpan matriks audit traceability per-kasus (Markdown & JSON)
        $traceabilityMd = $this->generateTraceabilityMatrix($scenarioResults);
        file_put_contents(WRITEPATH . 'csir_case_traceability_matrix.md', $traceabilityMd);
        file_put_contents(WRITEPATH . 'csir_case_traceability_matrix.json', json_encode($scenarioResults, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

        $projectRoot = dirname(__DIR__, 2);
        if (is_dir($projectRoot . '/benchmark')) {
            file_put_contents($projectRoot . '/benchmark/csir_case_traceability_matrix.md', $traceabilityMd);
            file_put_contents($projectRoot . '/benchmark/csir_case_traceability_matrix.json', json_encode($scenarioResults, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        }
        if (is_dir($projectRoot . '/jurnal')) {
            file_put_contents($projectRoot . '/jurnal/TABEL_TRACEABILITY_CSIR_40_KASUS.md', $traceabilityMd);
        }

        CLI::write("\n[✓] Laporan evaluasi berhasil disimpan ke: {$reportPath}", 'cyan');
        CLI::write("[✓] Matriks audit per-kasus disimpan ke: benchmark/csir_case_traceability_matrix.md\n", 'cyan');
    }

    /**
     * Membandingkan setiap field CSIR antara expected dan predicted.
     *
     * @param array<string, mixed> $expected
     * @param array<string, mixed> $actual
     * @param array<string, mixed> $case
     * @return array<string, string> 'MATCH'|'MISMATCH'|'NOT_APPLICABLE'
     */
    private function compareCsirFields(array $expected, array $actual, array $case): array
    {
        $result = [];
        foreach (self::CSIR_FIELDS as $field) {
            if (!$this->isFieldApplicable($field, $expected, $case)) {
                $result[$field] = 'NOT_APPLICABLE';
                continue;
            }

            $expVal = $expected[$field] ?? null;
            if ($field === 'latitude' && !empty($case['lat'])) {
                $expVal = (float) $case['lat'];
            } elseif ($field === 'longitude' && !empty($case['lng'])) {
                $expVal = (float) $case['lng'];
            }
            $actVal = $actual[$field] ?? null;

            $result[$field] = $this->compareField($field, $expVal, $actVal);
        }

        return $result;
    }

    /**
     * Menentukan apakah suatu field relevan/berlaku untuk dievaluasi pada skenario ini.
     */
    private function isFieldApplicable(string $field, array $expected, array $case): bool
    {
        // Field wajib selalu berlaku
        if (in_array($field, self::REQUIRED_FIELDS, true)) {
            return true;
        }

        // Jika ground truth memiliki nilai non-null eksplisit, field tersebut berlaku
        if (array_key_exists($field, $expected) && $expected[$field] !== null) {
            return true;
        }

        // Jika field berupa boolean konstrain dan expected bernilai true, field berlaku
        if (in_array($field, ['is_free', 'open_now', 'open_24h'], true)) {
            return !empty($expected[$field]);
        }

        // Koordinat berlaku jika case menyediakan koordinat GPS
        if (in_array($field, ['latitude', 'longitude'], true)) {
            return !empty($case['lat']) || !empty($case['lng']);
        }

        return false;
    }

    /**
     * Membandingkan nilai field tunggal sesuai tipe datanya.
     */
    private function compareField(string $field, $expected, $actual): string
    {
        return match (true) {
            in_array($field, ['radius', 'latitude', 'longitude'], true)
                => $this->compareFloat($expected, $actual),
            in_array($field, ['max_price'], true)
                => $this->compareNumeric($expected, $actual),
            in_array($field, ['is_free', 'open_now', 'open_24h', 'is_out_of_scope'], true)
                => $this->compareBoolean($expected, $actual),
            default
                => $this->compareNormalized($field, $expected, $actual),
        };
    }

    /**
     * Perbandingan float dengan toleransi numerik.
     */
    private function compareFloat($expected, $actual, float $tolerance = 0.001): string
    {
        if ($expected === null && $actual === null) {
            return 'MATCH';
        }
        if ($expected === null || $actual === null) {
            return 'MISMATCH';
        }
        return abs((float) $expected - (float) $actual) <= $tolerance ? 'MATCH' : 'MISMATCH';
    }

    /**
     * Perbandingan numerik integer/float eksak.
     */
    private function compareNumeric($expected, $actual): string
    {
        if ($expected === null && $actual === null) {
            return 'MATCH';
        }
        if ($expected === null || $actual === null) {
            return 'MISMATCH';
        }
        return ((float) $expected === (float) $actual) ? 'MATCH' : 'MISMATCH';
    }

    /**
     * Perbandingan boolean ketat.
     */
    private function compareBoolean($expected, $actual): string
    {
        if ($expected === null && $actual === null) {
            return 'MATCH';
        }
        if ($expected === null || $actual === null) {
            return 'MISMATCH';
        }
        return ((bool) $expected === (bool) $actual) ? 'MATCH' : 'MISMATCH';
    }

    /**
     * Perbandingan string/enum ternormalisasi.
     */
    private function compareNormalized(string $field, $expected, $actual): string
    {
        $normExp = $this->normalizeValue($field, $expected);
        $normAct = $this->normalizeValue($field, $actual);

        if ($normExp === null && $normAct === null) {
            return 'MATCH';
        }
        if ($normExp === null || $normAct === null) {
            return 'MISMATCH';
        }

        return (strcasecmp((string) $normExp, (string) $normAct) === 0) ? 'MATCH' : 'MISMATCH';
    }

    /**
     * Normalisasi nilai semantik untuk mencegah kesalahan trivial format string.
     */
    private function normalizeValue(string $field, $value)
    {
        if ($value === null) {
            return null;
        }
        if (is_string($value)) {
            $value = trim($value);
            if ($value === '') {
                return null;
            }
        }

        return match ($field) {
            'spatial_operator' => str_replace(' ', '_', strtolower((string) $value)),
            'reference_type'   => strtolower((string) $value),
            'distance_unit'    => strtolower((string) $value),
            'sort'             => strtolower((string) $value),
            default            => $value,
        };
    }

    /**
     * Exact CSIR Match: bernilai true jika seluruh applicable field berstatus MATCH (tanpa satupun MISMATCH).
     */
    private function isExactCsirMatch(array $fieldMatches): bool
    {
        foreach ($fieldMatches as $status) {
            if ($status === 'MISMATCH') {
                return false;
            }
        }
        return true;
    }

    /**
     * Ekstraksi atribut CSIR dari objek SpatialIntent menjadi array asosiatif 19-field.
     *
     * @param SpatialIntent $sir
     * @return array<string, mixed>
     */
    private function extractActualCsirArray(SpatialIntent $sir): array
    {
        return [
            'intent'           => $sir->intent,
            'entity'           => $sir->entity,
            'category'         => $sir->category,
            'target_name'      => $sir->targetName,
            'keyword'          => $sir->keyword,
            'spatial_operator' => $sir->spatialOperator,
            'reference_type'   => $sir->referenceType,
            'reference_entity' => $sir->referenceEntity,
            'latitude'         => $sir->latitude,
            'longitude'        => $sir->longitude,
            'radius'           => $sir->radius,
            'distance_unit'    => $sir->distanceUnit,
            'admin_area'       => $sir->adminArea,
            'is_free'          => $sir->isFree,
            'max_price'        => $sir->maxPrice,
            'open_now'         => $sir->openNow,
            'open_24h'         => $sir->open24h,
            'sort'             => $sir->sort,
            'is_out_of_scope'  => $sir->isOutOfScope,
        ];
    }

    /**
     * Evaluasi Spatial Predicate Correctness (Layer C).
     */
    private function evaluateSpatialPredicate(array $case, SpatialIntent $sir, array $places): bool
    {
        // 1. Kasus Out-of-Scope / Expect Empty
        if (($case['expect_empty'] ?? false) || ($case['expected_csir']['is_out_of_scope'] ?? false)) {
            return count($places) === 0;
        }

        // 2. Verifikasi Konsistensi Kebijakan Fallback Lokasi Luar Jangkauan (> 35 km)
        if ($sir->latitude !== null && $sir->longitude !== null) {
            $distFromCenter = $this->calculateDistanceKm(
                $sir->latitude,
                $sir->longitude,
                SpatialPolicyHandler::PADANG_CENTER_LAT,
                SpatialPolicyHandler::PADANG_CENTER_LNG
            );
            if ($distFromCenter > SpatialPolicyHandler::SERVICE_AREA_THRESHOLD_KM && !$sir->fallbackApplied) {
                return false;
            }
        }

        // 3. Verifikasi Predikat Operator Radius: d <= R
        if ($sir->spatialOperator === 'within_radius' && $sir->radius !== null) {
            if (empty($places)) {
                return true;
            }
            foreach ($places as $p) {
                if (isset($p['jarak_km']) && is_numeric($p['jarak_km'])) {
                    if ((float) $p['jarak_km'] > ($sir->radius + 0.1)) {
                        return false;
                    }
                }
            }
        }

        // 4. Verifikasi Predikat Wilayah Administratif: POI.admin_area == expected_admin_area
        if ($sir->spatialOperator === 'within_admin_area' && !empty($sir->adminArea)) {
            if (empty($places)) {
                return true;
            }
            $targetArea = strtolower($sir->adminArea);
            foreach ($places as $p) {
                $addr = strtolower($p['alamat'] ?? '');
                if (!str_contains($addr, $targetArea)) {
                    return false;
                }
            }
        }

        // 5. Verifikasi Predikat Urutan Terdekat: returned POI == argmin(distance)
        if ($sir->spatialOperator === 'nearest' || $sir->sort === 'terdekat') {
            if (count($places) >= 1) {
                $firstDist = isset($places[0]['jarak_km']) ? (float) $places[0]['jarak_km'] : null;
                $prevDist = -1.0;
                foreach ($places as $p) {
                    if (isset($p['jarak_km']) && is_numeric($p['jarak_km'])) {
                        $currDist = (float) $p['jarak_km'];
                        // Verifikasi POI pertama adalah argmin jarak
                        if ($firstDist !== null && $currDist < ($firstDist - 0.01)) {
                            return false;
                        }
                        // Verifikasi urutan monotonik naik
                        if ($prevDist >= 0.0 && $currDist < ($prevDist - 0.01)) {
                            return false;
                        }
                        $prevDist = $currDist;
                    }
                }
            }
        }

        // 6. Verifikasi Predikat Tiket Gratis Murni
        if ($sir->isFree && ($sir->maxPrice === null || $sir->maxPrice === 0)) {
            foreach ($places as $p) {
                if (isset($p['harga_tiket']) && (int) $p['harga_tiket'] !== 0) {
                    return false;
                }
            }
        }

        // 7. Verifikasi Predikat Batas Anggaran Maksimum
        if ($sir->maxPrice !== null && $sir->maxPrice > 0) {
            foreach ($places as $p) {
                if (isset($p['harga_tiket']) && (int) $p['harga_tiket'] > $sir->maxPrice) {
                    return false;
                }
            }
        }

        // 8. Verifikasi Predikat Kategori: POI.category == expected_category
        $expectedCategory = $case['expected_kategori'] ?? $case['expected_csir']['category'] ?? $sir->category;
        if ($expectedCategory !== null && !empty($places)) {
            foreach ($places as $p) {
                if (isset($p['kategori']) && strcasecmp(trim($p['kategori']), trim($expectedCategory)) !== 0) {
                    return false;
                }
            }
        }

        return true;
    }

    /**
     * Hitung jarak lingkaran besar (Great-Circle Distance) dalam kilometer.
     */
    private function calculateDistanceKm(float $lat1, float $lon1, float $lat2, float $lon2): float
    {
        $radLat1 = deg2rad($lat1);
        $radLat2 = deg2rad($lat2);
        $radDeltaLon = deg2rad($lon2 - $lon1);

        $cosVal = sin($radLat1) * sin($radLat2) + cos($radLat1) * cos($radLat2) * cos($radDeltaLon);
        $cosVal = max(-1.0, min(1.0, $cosVal));

        return 6371.0 * acos($cosVal);
    }

    /**
     * Evaluasi Grounded NLG Synthesis & Algorithmic Grounding Validation (Layer D).
     */
    private function evaluateGrounding(string $reply, array $places, GroundingValidator $validator, SpatialIntent $sir, array $case): array
    {
        // Kasus out-of-scope yang ditolak jujur
        if (($case['expected_csir']['is_out_of_scope'] ?? false) && $sir->executionPolicy === 'reject_out_of_scope') {
            return [
                'is_grounded'         => true,
                'verifiable_claims'   => 0,
                'supported_claims'    => 0,
                'claim_fidelity'      => 100.0,
                'mentioned_entities'  => 0,
                'grounded_entities'   => 0,
                'entity_fidelity'     => 100.0,
                'fabricated_entities' => 0,
                'violations'          => [],
            ];
        }

        $res = $validator->validate($reply, $places);
        $claimStats = $res['claimStats'];
        $fabEntities = $res['fabricatedEntities'];

        $validPoisInDb = array_column($places, 'nama');
        $mentionedCount = 0;
        $groundedCount = 0;

        foreach ($validPoisInDb as $poi) {
            if (stripos($reply, $poi) !== false) {
                $mentionedCount++;
                $groundedCount++;
            }
        }
        $mentionedCount += count($fabEntities);

        $entityFidelity = $mentionedCount > 0 ? (100.0 * $groundedCount / $mentionedCount) : 100.0;

        return [
            'is_grounded'         => $res['isGrounded'],
            'verifiable_claims'   => $claimStats['totalClaims'],
            'supported_claims'    => $claimStats['supportedClaims'],
            'claim_fidelity'      => $claimStats['fidelity'],
            'mentioned_entities'  => $mentionedCount,
            'grounded_entities'   => $groundedCount,
            'entity_fidelity'     => $entityFidelity,
            'fabricated_entities' => count($fabEntities),
            'violations'          => $res['violations'],
        ];
    }

    /**
     * Fallback penyusun expected CSIR dari struktur lama jika field expected_csir belum ada.
     */
    private function buildFallbackExpectedCsir(array $case): array
    {
        $filters = $case['expected_filters'] ?? [];
        $isOutOfScope = !empty($case['is_out_of_scope']) 
            || (!empty($case['expected_policy']) && $case['expected_policy'] === 'reject_out_of_scope')
            || (isset($case['grup']) && str_contains(strtolower((string) $case['grup']), 'out-of-scope'));

        return [
            'intent'           => $case['is_sapaan'] ? 'general_inquiry' : (!empty($case['expected_nama']) ? 'entity_lookup' : 'spatial_recommendation'),
            'entity'           => 'tourism_object',
            'category'         => $case['expected_kategori'] ?? null,
            'target_name'      => $case['expected_nama'] ?? null,
            'keyword'          => $filters['kata_kunci'] ?? null,
            'spatial_operator' => isset($filters['urutan']) && $filters['urutan'] === 'terdekat' ? 'nearest' : (isset($filters['wilayah']) ? 'within_admin_area' : 'none'),
            'reference_type'   => isset($case['lat'], $case['lng']) && $case['lat'] !== null ? 'gps' : 'unknown',
            'reference_entity' => null,
            'latitude'         => isset($case['lat']) && is_numeric($case['lat']) ? (float) $case['lat'] : null,
            'longitude'        => isset($case['lng']) && is_numeric($case['lng']) ? (float) $case['lng'] : null,
            'radius'           => null,
            'distance_unit'    => 'km',
            'admin_area'       => $filters['wilayah'] ?? null,
            'is_free'          => $filters['gratis'] ?? false,
            'max_price'        => $filters['max_harga'] ?? null,
            'open_now'         => $filters['jam_sekarang'] ?? false,
            'open_24h'         => $filters['buka_24_jam'] ?? false,
            'sort'             => $filters['urutan'] ?? null,
            'is_out_of_scope'  => $isOutOfScope,
        ];
    }

    /**
     * Ekstraksi atribut envelope eksekusi (setelah resolusi batas kebijakan spasial).
     *
     * @param SpatialIntent $sir
     * @return array<string, mixed>
     */
    private function extractActualExecutionEnvelopeArray(SpatialIntent $sir): array
    {
        $arr = $this->extractActualCsirArray($sir);
        if ($sir->fallbackApplied) {
            $arr['reference_type'] = $sir->getExecutionReferenceType();
            $arr['latitude'] = $sir->getExecutionLatitude();
            $arr['longitude'] = $sir->getExecutionLongitude();
        }
        return $arr;
    }

    /**
     * Agregasi seluruh metrik pengujian.
     */
    private function aggregateMetrics(
        array $scenarioResults,
        array $fieldMatchesAccumulator,
        int $totalTest,
        int $exactCsirMatches,
        int $executionEnvelopeMatches,
        int $validationMatches,
        int $spatialPredicateMatches,
        int $pureSpatialMatches,
        int $totalSpatialCases,
        int $chitchatMatches,
        int $totalChitchatCases,
        int $honestRejectionCount,
        int $totalOutOfScopeCases,
        int $totalSupportedClaims,
        int $totalVerifiableClaims,
        int $totalGroundedEntities,
        int $totalMentionedEntities,
        int $totalFabricatedEntities,
        array $timings,
        string $mode
    ): array {
        $fieldAccuracies = [];
        foreach ($fieldMatchesAccumulator as $field => $data) {
            $acc = $data['applicable'] > 0 ? (100.0 * $data['correct'] / $data['applicable']) : null;
            $fieldAccuracies[$field] = [
                'applicable' => $data['applicable'],
                'correct'    => $data['correct'],
                'accuracy'   => $acc !== null ? round($acc, 2) : 100.0,
            ];
        }

        // Sub-dimensi
        $calcSubDim = function(array $fields) use ($fieldAccuracies) {
            $app = 0;
            $corr = 0;
            foreach ($fields as $f) {
                if (isset($fieldAccuracies[$f])) {
                    $app += $fieldAccuracies[$f]['applicable'];
                    $corr += $fieldAccuracies[$f]['correct'];
                }
            }
            return $app > 0 ? round(100.0 * $corr / $app, 2) : 100.0;
        };

        $exactCsirAcc = $totalTest > 0 ? round(100.0 * $exactCsirMatches / $totalTest, 2) : 0.0;
        $envelopeAcc  = $totalTest > 0 ? round(100.0 * $executionEnvelopeMatches / $totalTest, 2) : 0.0;
        $valDecisionAcc = $totalTest > 0 ? round(100.0 * $validationMatches / $totalTest, 2) : 0.0;
        $spatialPredAcc = $totalTest > 0 ? round(100.0 * $spatialPredicateMatches / $totalTest, 2) : 0.0;
        $pureSpatialAcc = $totalSpatialCases > 0 ? round(100.0 * $pureSpatialMatches / $totalSpatialCases, 2) : 100.0;
        $chitchatAcc    = $totalChitchatCases > 0 ? round(100.0 * $chitchatMatches / $totalChitchatCases, 2) : 100.0;
        $hrr = $totalOutOfScopeCases > 0 ? round(100.0 * $honestRejectionCount / $totalOutOfScopeCases, 2) : 100.0;
        $cgf = $totalVerifiableClaims > 0 ? round(100.0 * $totalSupportedClaims / $totalVerifiableClaims, 2) : 100.0;
        $egf = $totalMentionedEntities > 0 ? round(100.0 * $totalGroundedEntities / $totalMentionedEntities, 2) : 100.0;
        $efr = $totalTest > 0 ? round(100.0 * $totalFabricatedEntities / $totalTest, 2) : 0.0;

        $meanTotal = count($timings['total']) > 0 ? array_sum($timings['total']) / count($timings['total']) : 0.0;
        $meanSql   = count($timings['sql']) > 0 ? array_sum($timings['sql']) / count($timings['sql']) : 0.0;
        $meanIntent = count($timings['intent']) > 0 ? array_sum($timings['intent']) / count($timings['intent']) : 0.0;
        $meanNlg   = count($timings['nlg']) > 0 ? array_sum($timings['nlg']) / count($timings['nlg']) : 0.0;

        return [
            'meta' => [
                'framework'  => 'CodeIgniter 4.7.4',
                'database'   => 'MySQL 8.0 Spatial',
                'mode'       => $mode,
                'timestamp'  => date('c'),
                'total_test' => $totalTest,
            ],
            'layer_a_semantic_csir' => [
                'exact_csir_match_rate'         => $exactCsirAcc,
                'exact_csir_count'              => "{$exactCsirMatches}/{$totalTest}",
                'execution_envelope_match_rate' => $envelopeAcc,
                'execution_envelope_count'      => "{$executionEnvelopeMatches}/{$totalTest}",
                'semantic_subdimension_accuracy'    => $calcSubDim(self::SEMANTIC_FIELDS),
                'spatial_subdimension_accuracy'     => $calcSubDim(self::SPATIAL_FIELDS),
                'operational_subdimension_accuracy' => $calcSubDim(self::OPERATIONAL_FIELDS),
                'control_subdimension_accuracy'     => $calcSubDim(self::CONTROL_FIELDS),
                'field_accuracies'                  => $fieldAccuracies,
            ],
            'layer_b_deterministic_validation' => [
                'validation_decision_accuracy' => $valDecisionAcc,
                'validation_matches_count'     => "{$validationMatches}/{$totalTest}",
                'honest_rejection_rate'        => $hrr,
                'honest_rejection_count'       => "{$honestRejectionCount}/{$totalOutOfScopeCases}",
            ],
            'layer_c_spatial_execution' => [
                'pure_spatial_predicate_correctness'   => $pureSpatialAcc,
                'pure_spatial_matches'                => "{$pureSpatialMatches}/{$totalSpatialCases}",
                'chitchat_handling_accuracy'          => $chitchatAcc,
                'chitchat_matches'                    => "{$chitchatMatches}/{$totalChitchatCases}",
                'overall_execution_compliance_rate'   => $spatialPredAcc,
                'overall_execution_matches'           => "{$spatialPredicateMatches}/{$totalTest}",
                'spatial_predicate_correctness'       => $spatialPredAcc, // retained for backward compatibility
            ],
            'layer_d_grounded_generation' => [
                'claim_grounding_fidelity_cgf' => $cgf,
                'supported_claims'             => $totalSupportedClaims,
                'verifiable_claims'            => $totalVerifiableClaims,
                'entity_grounding_fidelity_egf'=> $egf,
                'grounded_entities'            => $totalGroundedEntities,
                'mentioned_entities'           => $totalMentionedEntities,
                'entity_fabrication_rate'      => $efr,
                'total_fabricated_pois'        => $totalFabricatedEntities,
            ],
            'latencies_ms' => [
                'mean_intent_parsing' => round($meanIntent, 2),
                'mean_mysql_spatial'  => round($meanSql, 3),
                'mean_grounded_nlg'   => round($meanNlg, 2),
                'mean_total'          => round($meanTotal, 2),
            ],
            'cases' => $scenarioResults,
        ];
    }

    /**
     * Render ringkasan hasil evaluasi ke konsol CLI.
     */
    private function renderConsoleReport(array $aggregated, array $scenarioResults): void
    {
        $la = $aggregated['layer_a_semantic_csir'];
        $lb = $aggregated['layer_b_deterministic_validation'];
        $lc = $aggregated['layer_c_spatial_execution'];
        $ld = $aggregated['layer_d_grounded_generation'];
        $lat = $aggregated['latencies_ms'];

        CLI::write("\n==================================================================", 'green');
        CLI::write("           RINGKASAN HASIL EVALUASI EMPIRIS 4-LAPISAN", 'yellow');
        CLI::write("==================================================================", 'green');

        CLI::write("1. LAYER A: CSIR SEMANTIC EXTRACTION ACCURACY", 'cyan');
        CLI::write(sprintf("   • Exact CSIR Match Rate (Pre-Fallback)     : %6.2f%% (%s skenario)", $la['exact_csir_match_rate'], $la['exact_csir_count']));
        CLI::write(sprintf("   • Execution Envelope Alignment (Post-Policy): %6.2f%% (%s skenario)", $la['execution_envelope_match_rate'], $la['execution_envelope_count']));
        CLI::write(sprintf("   • Subdimensi 1: Intensi & Entitas          : %6.2f%%", $la['semantic_subdimension_accuracy']));
        CLI::write(sprintf("   • Subdimensi 2: Kendala Spasial            : %6.2f%%", $la['spatial_subdimension_accuracy']));
        CLI::write(sprintf("   • Subdimensi 3: Kendala Operasional        : %6.2f%%", $la['operational_subdimension_accuracy']));
        CLI::write(sprintf("   • Subdimensi 4: Kontrol & Boundary         : %6.2f%%", $la['control_subdimension_accuracy']));

        CLI::write("\n   Rincian Akurasi Field-Level CSIR:");
        foreach ($la['field_accuracies'] as $field => $stat) {
            CLI::write(sprintf("     - %-18s : %6.2f%% (%d/%d kasus)", $field, $stat['accuracy'], $stat['correct'], $stat['applicable']));
        }

        CLI::write("\n2. LAYER B: DETERMINISTIC VALIDATION & SAFETY (SirValidator)", 'cyan');
        CLI::write(sprintf("   • Validation Decision Accuracy    : %6.2f%% (%s skenario)", $lb['validation_decision_accuracy'], $lb['validation_matches_count']));
        CLI::write(sprintf("   • Honest Rejection Rate (HRR)     : %6.2f%% (%s out-of-scope)", $lb['honest_rejection_rate'], $lb['honest_rejection_count']));

        CLI::write("\n3. LAYER C: SPATIAL QUERY EXECUTION (MySQL 8.0 ST_Distance_Sphere)", 'cyan');
        CLI::write(sprintf("   • Pure Spatial Predicate Correctness (N=36): %6.2f%% (%s skenario)", $lc['pure_spatial_predicate_correctness'], $lc['pure_spatial_matches']));
        CLI::write(sprintf("   • Conversational Chit-Chat Handling  (N=2) : %6.2f%% (%s skenario)", $lc['chitchat_handling_accuracy'], $lc['chitchat_matches']));
        CLI::write(sprintf("   • Overall Scenario Execution Compliance(N=40): %6.2f%% (%s skenario)", $lc['overall_execution_compliance_rate'], $lc['overall_execution_matches']));

        CLI::write("\n4. LAYER D: EVIDENCE GROUNDING & ANTI-HALLUCINATION", 'cyan');
        CLI::write(sprintf("   • Claim Grounding Fidelity (CGF)  : %6.2f%% (%d/%d klaim terverifikasi)", $ld['claim_grounding_fidelity_cgf'], $ld['supported_claims'], $ld['verifiable_claims']));
        CLI::write(sprintf("   • Entity Grounding Fidelity (EGF) : %6.2f%% (%d/%d sebutan POI)", $ld['entity_grounding_fidelity_egf'], $ld['grounded_entities'], $ld['mentioned_entities']));
        CLI::write(sprintf("   • Fabricated POI Entities         : %d entitas teramati (Rate: %4.2f%%)", $ld['total_fabricated_pois'], $ld['entity_fabrication_rate']));

        CLI::write("------------------------------------------------------------------");
        CLI::write("                 PROFIL LATENSI KOMPUTASI (ms)");
        CLI::write("------------------------------------------------------------------");
        CLI::write(sprintf("• Intent Extraction (LLM -> CSIR)     : %7.2f ms (%5.2f%%)", $lat['mean_intent_parsing'], $lat['mean_total'] > 0 ? ($lat['mean_intent_parsing'] / $lat['mean_total']) * 100 : 0));
        CLI::write(sprintf("• MySQL 8.0 Spatial (ST_Distance_Sphere): %7.2f ms (%5.2f%%)", $lat['mean_mysql_spatial'], $lat['mean_total'] > 0 ? ($lat['mean_mysql_spatial'] / $lat['mean_total']) * 100 : 0));
        CLI::write(sprintf("• Grounded NLG Synthesis (LLM -> Text): %7.2f ms (%5.2f%%)", $lat['mean_grounded_nlg'], $lat['mean_total'] > 0 ? ($lat['mean_grounded_nlg'] / $lat['mean_total']) * 100 : 0));
        CLI::write(sprintf("• TOTAL LATENSI PERCAKAPAN SERVER     : %7.2f ms (~%4.2f detik)", $lat['mean_total'], $lat['mean_total'] / 1000.0));
        CLI::write("==================================================================", 'green');

        // Tampilkan diagnostik kasus mismatch jika ada
        $mismatches = [];
        foreach ($scenarioResults as $r) {
            if (!$r['exact_csir_match']) {
                $mismatches[] = $r;
            }
        }

        if (!empty($mismatches)) {
            CLI::write("\n[DIAGNOSTIK KASUS MISMATCH CSIR (PRE-FALLBACK EXTRACTION)]", 'yellow');
            foreach ($mismatches as $m) {
                CLI::write(sprintf("  • CASE #%02d [%s] - Prompt: \"%s\"", $m['id'], $m['grup'], $m['prompt']), 'red');
                foreach ($m['field_matches'] as $fld => $st) {
                    if ($st === 'MISMATCH') {
                        $expVal = $m['expected'][$fld] ?? null;
                        $actVal = $m['predicted_intent_csir'][$fld] ?? null;
                        $exp = is_bool($expVal) ? ($expVal ? 'true' : 'false') : ($expVal ?? 'null');
                        $act = is_bool($actVal) ? ($actVal ? 'true' : 'false') : ($actVal ?? 'null');
                        CLI::write(sprintf("      - Field '%s' MISMATCH: Expected [%s] vs Predicted [%s]", $fld, (string)$exp, (string)$act), 'yellow');
                    }
                }
            }
        } else {
            CLI::write("\n[DIAGNOSTIK] Seluruh 40 skenario lulus Exact CSIR Match tanpa mismatch semantik!", 'green');
        }
    }

    /**
     * Menyusun tabel matriks audit per-kasus (40 skenario) dalam format Markdown.
     */
    private function generateTraceabilityMatrix(array $scenarioResults): string
    {
        $md = "# MATRIKS AUDIT KESELARASAN PER-KASUS (40 SKENARIO BENCHMARK)\n\n";
        $md .= "Matriks ini mendokumentasikan nilai acuan (*ground truth*), nilai prediksi ekstraksi semantik (*Raw CSIR*),\n";
        $md .= "resolusi batas kebijakan spasial (*Execution Envelope*), perbandingan atribut, dan status kelulusan tiap skenario.\n\n";
        $md .= "| ID | Grup Skenario | Prompt Pengguna | Tipe Skenario | Expected (Acuan) | Extracted CSIR | Envelope Eksekusi | Status CSIR | Predikat Spasial | Catatan Deviasi / Kebijakan |\n";
        $md .= "|:---:|---|---|:---:|---|---|---|:---:|:---:|---|\n";

        foreach ($scenarioResults as $r) {
            $id = $r['id'];
            $grup = $r['grup'];
            $prompt = str_replace('|', '/', $r['prompt']);
            $type = $r['scenario_type'];
            
            // Expected summary
            $exp = $r['expected'];
            $expSum = sprintf("intent: %s, cat: %s, op: %s, ref: %s", $exp['intent'] ?? '-', $exp['category'] ?? 'null', $exp['spatial_operator'] ?? '-', $exp['reference_type'] ?? '-');
            if ($exp['is_out_of_scope'] ?? false) $expSum .= " (OOS)";

            // Pred CSIR summary
            $act = $r['predicted_intent_csir'];
            $actSum = sprintf("intent: %s, cat: %s, op: %s, ref: %s", $act['intent'] ?? '-', $act['category'] ?? 'null', $act['spatial_operator'] ?? '-', $act['reference_type'] ?? '-');

            // Envelope summary
            $env = $r['resolved_execution_envelope'];
            $envSum = sprintf("ref: %s, lat: %s, lng: %s", $env['reference_type'] ?? '-', $env['latitude'] ?? 'null', $env['longitude'] ?? 'null');

            $csirStatus = $r['exact_csir_match'] ? '✅ EXACT' : '⚠️ MISMATCH';
            $spatStatus = $r['spatial_predicate_match'] ? '✅ PASS' : '❌ FAIL';

            // Catatan
            $notes = [];
            foreach ($r['field_matches'] as $fld => $st) {
                if ($st === 'MISMATCH') {
                    $notes[] = sprintf("%s: exp=[%s] vs act=[%s]", $fld, $exp[$fld] ?? 'null', $act[$fld] ?? 'null');
                }
            }
            if (!empty($r['fallback_applied'])) {
                $notes[] = "Fallback diterapkan (Domain Boundary Notice: Pusat Padang)";
            }
            $noteStr = empty($notes) ? "Sempurna (100% Cocok)" : implode('; ', $notes);
            $noteStr = str_replace('|', '/', $noteStr);

            $md .= sprintf("| **%02d** | %s | *\"%s\"* | `%s` | `%s` | `%s` | `%s` | %s | %s | %s |\n",
                $id, $grup, $prompt, $type, $expSum, $actSum, $envSum, $csirStatus, $spatStatus, $noteStr
            );
        }

        return $md;
    }
}

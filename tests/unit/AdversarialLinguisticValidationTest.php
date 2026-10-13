<?php

declare(strict_types=1);

namespace Tests\Unit;

use App\Services\LlmService;
use App\Services\SpatialIntent\FactTableBuilder;
use App\Services\SpatialIntent\GroundingValidator;
use App\Services\SpatialIntent\SirValidator;
use App\Services\SpatialIntent\SpatialIntent;
use App\Services\SpatialIntent\SpatialPolicyHandler;
use App\Services\SpatialIntent\SpatialQueryCompiler;
use CodeIgniter\Test\CIUnitTestCase;

class AdversarialLinguisticValidationTest extends CIUnitTestCase
{
    protected SirValidator $sirValidator;
    protected SpatialQueryCompiler $compiler;
    protected GroundingValidator $groundingValidator;
    protected LlmService $llmService;

    protected function setUp(): void
    {
        parent::setUp();
        $this->sirValidator = new SirValidator();
        $this->compiler = new SpatialQueryCompiler();
        $this->groundingValidator = new GroundingValidator();
        $this->llmService = new LlmService();
        $this->llmService->mockMode = true;
    }

    // =========================================================================
    // BAGIAN 1: PENGUJIAN ADVERSARIAL & BATASAN KEAMANAN (ADVERSARIAL SECURITY)
    // =========================================================================

    /**
     * Uji Serangan SQL Injection Kompleks: Memastikan muatan UNION SELECT dan DDL
     * tidak pernah dieksekusi secara raw dan di-bind secara aman sebagai parameter literal.
     */
    public function testAdversarialSqlInjectionPayloadsAreNeutralized(): void
    {
        $payloads = [
            "' UNION SELECT username, password FROM users --",
            "1; DROP TABLE wisata; SELECT * FROM wisata WHERE '1'='1",
            "admin' OR 1=1 #",
            "') OR EXISTS(SELECT * FROM information_schema.tables) --",
        ];

        foreach ($payloads as $payload) {
            $sir = new SpatialIntent(
                intent: 'spatial_recommendation',
                category: 'Pantai',
                keyword: $payload,
                isValid: true
            );

            $compiled = $this->compiler->compile($sir);

            $this->assertTrue($compiled['isExecutable']);
            $this->assertStringNotContainsString('DROP TABLE', $compiled['sql']);
            $this->assertStringNotContainsString('UNION SELECT', $compiled['sql']);
            $this->assertStringContainsString('wisata.nama LIKE ?', $compiled['sql']);
            $this->assertContains('%' . $payload . '%', $compiled['params']);
        }
    }

    /**
     * Uji Koordinat Ekstrem / Di Luar Planet Bumi:
     * Koordinat tidak valid (latitude > 90 atau longitude > 180) harus ditolak oleh validator.
     */
    public function testExtremeNonEarthCoordinatesMustBeRejected(): void
    {
        $extremeCoords = [
            ['lat' => 999.0, 'lng' => 100.35],
            ['lat' => -150.0, 'lng' => 100.35],
            ['lat' => -0.94, 'lng' => 500.0],
            ['lat' => -0.94, 'lng' => -250.0],
        ];

        foreach ($extremeCoords as $coord) {
            $sir = new SpatialIntent(
                spatialOperator: 'nearest',
                referenceType: 'gps',
                latitude: $coord['lat'],
                longitude: $coord['lng']
            );

            $res = $this->sirValidator->validate($sir);

            $this->assertFalse($res['isValid'], "Koordinat ({$coord['lat']}, {$coord['lng']}) harus ditolak.");
            $this->assertSame('rejected', $sir->validationStatus);
            $this->assertSame('clarify_user', $sir->executionPolicy);
        }
    }

    /**
     * Uji Radius Absurd & Ekstrem:
     * Radius negatif atau radius ribuan kilometer harus ditolak tanpa konversi diam-diam (No Intent Alteration).
     */
    public function testAbsurdRadiusValuesMustBeRejectedWithoutClamping(): void
    {
        $absurdRadii = [-50.0, -0.001, 1000.0, 50000.0];

        foreach ($absurdRadii as $radius) {
            $sir = new SpatialIntent(
                spatialOperator: 'within_radius',
                radius: $radius
            );

            $res = $this->sirValidator->validate($sir);

            $this->assertFalse($res['isValid'], "Radius {$radius} harus ditolak.");
            $this->assertSame('clarify_user', $sir->executionPolicy);
        }
    }

    /**
     * Uji Kontradiksi Operasional:
     * Kueri yang memadukan gratis (is_free = true) dan batas harga non-nol harus ditangani secara logis.
     */
    public function testOperationalConstraintConsistency(): void
    {
        $sir = new SpatialIntent(
            category: 'Pantai',
            isFree: true,
            maxPrice: 20000,
            isValid: true
        );

        $compiled = $this->compiler->compile($sir);

        // Kueri harus tetap aman dan mengikat predikat gratis harga_tiket = 0
        $this->assertTrue($compiled['isExecutable']);
        $this->assertStringContainsString('wisata.harga_tiket = 0', $compiled['sql']);
    }

    // =========================================================================
    // BAGIAN 2: VARIASI LINGUISTIK & DIALEK/SLANG MINANGKABAU (LINGUISTIC SUITE)
    // =========================================================================

    /**
     * Uji Slang Minang: "pantai nan rancak dakek siko"
     * Harus terpetakan ke Kategori 'Pantai', Operator 'nearest', dan Titik Acuan 'gps'.
     */
    public function testMinangSlangPantaiNanRancakDakekSiko(): void
    {
        $prompt = "pantai nan rancak dakek siko";
        $sir = $this->llmService->extractSir($prompt);

        $this->assertSame('Pantai', $sir->category);
        $this->assertSame('nearest', $sir->spatialOperator);
        $this->assertSame('gps', $sir->referenceType);
        $this->assertTrue($sir->isValid);
    }

    /**
     * Uji Slang Minang: "tampek makan lamak di padang"
     * Harus terpetakan ke Kategori 'Kuliner'.
     */
    public function testMinangSlangTampekMakanLamak(): void
    {
        $prompt = "tampek makan lamak di padang";
        $sir = $this->llmService->extractSir($prompt);

        $this->assertSame('Kuliner', $sir->category);
        $this->assertTrue($sir->isValid);
    }

    /**
     * Uji Slang Minang: "aia tajun nan free"
     * Harus terpetakan ke Kategori 'Alam' dengan is_free = true.
     */
    public function testMinangSlangAiaTajunFree(): void
    {
        $prompt = "rekomendasi aia tajun nan free di padang";
        $sir = $this->llmService->extractSir($prompt);

        $this->assertSame('Alam', $sir->category);
        $this->assertTrue($sir->isFree);
        $this->assertTrue($sir->isValid);
    }

    /**
     * Uji Slang Minang: "pulau untuak snorkeling"
     * Harus terpetakan ke Kategori 'Pulau'.
     */
    public function testMinangSlangPulauSnorkeling(): void
    {
        $prompt = "a se pulau nan rancak untuak snorkeling di padang";
        $sir = $this->llmService->extractSir($prompt);

        $this->assertSame('Pulau', $sir->category);
        $this->assertTrue($sir->isValid);
    }

    // =========================================================================
    // BAGIAN 3: AUDIT GROUNDING KETAT & MITIGASI HALUSINASI (GROUNDING INTEGRITY)
    // =========================================================================

    /**
     * Uji Deteksi Entitas Fiktif / Objek Wisata Palsu:
     * Menolak narasi yang memuat objek wisata yang tidak ada di Kota Padang (Fabricated POIs).
     */
    public function testFabricatedPOIsInNarrativeAreDeterministicallyBlocked(): void
    {
        $facts = [
            ['nama' => 'Pantai Padang', 'harga_tiket' => 0, 'jarak_km' => 2.5],
        ];

        $hallucinatedNarratives = [
            'Saya sarankan mengunjungi **Pantai Salju Minang** dan **Pantai Padang**.',
            'Selain Pantai Padang, ada juga **Candi Padang Roco** yang indah.',
            'Kunjungi **Disneyland Padang** yang memiliki wahana terlengkap.',
        ];

        foreach ($hallucinatedNarratives as $narrative) {
            $validation = $this->groundingValidator->validate($narrative, $facts);

            $this->assertFalse($validation['isGrounded'], "Narasi halusinasi harus dinyatakan tidak grounded: {$narrative}");
            $this->assertNotEmpty($validation['fabricatedEntities']);
        }
    }

    /**
     * Uji Klaim Tarif Menyimpang:
     * Menolak jika objek gratis diklaim berbayar, atau tiket Rp10.000 diklaim Rp100.000.
     */
    public function testDistortedTicketPriceIsFlaggedAsViolation(): void
    {
        $facts = [
            ['nama' => 'Pantai Air Manis', 'harga_tiket' => 10000, 'jarak_km' => 5.0],
        ];

        // DB harga Rp10.000, tetapi diklaim Rp100.000
        $deviantNarrative = "Kunjungi **Pantai Air Manis** dengan harga tiket Rp100.000 per orang.";
        $validation = $this->groundingValidator->validate($deviantNarrative, $facts);

        $this->assertFalse($validation['isGrounded']);
        $this->assertNotEmpty($validation['violations']);
        $this->assertStringContainsString('Klaim harga', $validation['violations'][0]);
    }

    /**
     * Uji Kepatuhan Kueri Out-of-Scope (Honest Rejection Invariant):
     * Memastikan kueri di luar lingkup geospasial Padang secara jujur ditolak.
     */
    public function testOutOfScopeQueriesAreHonestRejections(): void
    {
        $outOfScopeQueries = [
            'Rekomendasi tempat main salju dan ski es di Padang',
            'Wisata candi peninggalan kerajaan Hindu di Kota Padang',
        ];

        foreach ($outOfScopeQueries as $query) {
            $sir = $this->llmService->extractSir($query);

            $this->assertTrue($sir->isOutOfScope);
            $this->assertSame('reject_out_of_scope', $sir->executionPolicy);
            $this->assertFalse($sir->isValid);
        }
    }
}

<?php

namespace Tests\Unit;

use App\Services\SpatialIntent\GroundingValidator;
use CodeIgniter\Test\CIUnitTestCase;

class GroundingValidatorTest extends CIUnitTestCase
{
    protected GroundingValidator $validator;

    protected function setUp(): void
    {
        parent::setUp();
        $this->validator = new GroundingValidator();
    }

    /**
     * Uji respons yang mematuhi fakta (grounded).
     */
    public function testGroundedResponsePasses()
    {
        $facts = [
            ['nama' => 'Pantai Padang', 'harga_tiket' => 0, 'jarak_km' => 3.2],
            ['nama' => 'Pantai Air Manis', 'harga_tiket' => 10000, 'jarak_km' => 7.8],
        ];

        $llmResponse = 'Berikut rekomendasi: **Pantai Padang** yang gratis dengan jarak 3.2 km, dan **Pantai Air Manis** dengan tiket Rp10.000 berjarak 7.8 km.';

        $res = $this->validator->validate($llmResponse, $facts);

        $this->assertTrue($res['isGrounded']);
        $this->assertEmpty($res['violations']);
        $this->assertEmpty($res['fabricatedEntities']);
        $this->assertEquals(100.0, $res['claimStats']['fidelity']);
    }

    /**
     * Uji respons yang menyebut entitas di luar hasil fakta (halusinasi terdeteksi & tertangkap).
     */
    public function testFabricatedEntityIsCaught()
    {
        $facts = [
            ['nama' => 'Pantai Padang', 'harga_tiket' => 0],
        ];

        // Model berhalusinasi menambahkan Pantai Carolina padahal tidak ada di hasil query
        $llmResponse = 'Saya merekomendasikan **Pantai Padang** dan juga **Pantai Carolina** untuk bersantai.';

        $res = $this->validator->validate($llmResponse, $facts);

        $this->assertFalse($res['isGrounded']);
        $this->assertNotEmpty($res['violations']);
        $this->assertContains('Pantai Carolina', $res['fabricatedEntities']);
    }

    /**
     * Uji klaim harga tiket yang menyimpang (Claim-level Grounding Violation).
     * Contoh dari reviewer: DB Rp10.000 tapi LLM mengklaim Rp50.000.
     */
    public function testPriceClaimDeviationIsCaught()
    {
        $facts = [
            ['nama' => 'Pantai Air Manis', 'harga_tiket' => 10000, 'jarak_km' => 7.82],
        ];

        // LLM mengklaim tiket Rp50.000 padahal faktanya Rp10.000
        $llmResponse = 'Destinasi yang kami temukan adalah **Pantai Air Manis** dengan tiket Rp50.000.';

        $res = $this->validator->validate($llmResponse, $facts);

        $this->assertFalse($res['isGrounded']);
        $this->assertNotEmpty($res['violations']);
        $this->assertStringContainsString('Klaim harga untuk \'Pantai Air Manis\' menyimpang', $res['violations'][0]);
    }

    /**
     * Uji klaim jarak spasial yang menyimpang (Spatial Grounding Violation).
     * Contoh dari reviewer: DB 7.82 km tapi LLM mengklaim 2 km.
     */
    public function testDistanceClaimDeviationIsCaught()
    {
        $facts = [
            ['nama' => 'Pantai Air Manis', 'harga_tiket' => 10000, 'jarak_km' => 7.82],
        ];

        // LLM mengklaim jarak 2 km padahal faktanya 7.82 km
        $llmResponse = 'Objek wisata **Pantai Air Manis** berjarak 2 km dari lokasi Anda.';

        $res = $this->validator->validate($llmResponse, $facts);

        $this->assertFalse($res['isGrounded']);
        $this->assertNotEmpty($res['violations']);
        $this->assertStringContainsString('Klaim jarak spasial untuk \'Pantai Air Manis\' menyimpang', $res['violations'][0]);
    }

    /**
     * Uji prinsip Fail-Closed ketika fakta SQL kosong tapi LLM mengklaim entitas rekomendasi.
     */
    public function testEmptyFactsWithEntityClaimFailsClosed()
    {
        $facts = []; // Hasil kueri SQL kosong (0 record)

        // LLM tetap mengarang destinasi
        $llmResponse = 'Berikut tempat wisata yang bisa Anda kunjungi: **Pantai Padang** yang sangat indah.';

        $res = $this->validator->validate($llmResponse, $facts);

        $this->assertFalse($res['isGrounded']);
        $this->assertNotEmpty($res['violations']);
        $this->assertStringContainsString('Fakta basis data kosong, namun narasi merekomendasikan entitas', $res['violations'][0]);
    }

    /**
     * Uji fakta SQL kosong dengan respons penolakan jujur (Honest Rejection) -> Lolos.
     */
    public function testEmptyFactsWithHonestRejectionPasses()
    {
        $facts = [];

        $llmResponse = 'Mohon maaf, tidak ditemukan objek wisata yang memenuhi kriteria pencarian Anda di Kota Padang.';

        $res = $this->validator->validate($llmResponse, $facts);

        $this->assertTrue($res['isGrounded']);
        $this->assertEmpty($res['violations']);
    }
}

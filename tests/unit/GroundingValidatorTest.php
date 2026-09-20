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
            ['nama' => 'Pantai Padang', 'harga_tiket' => 0],
            ['nama' => 'Pantai Air Manis', 'harga_tiket' => 10000],
        ];

        $llmResponse = 'Berikut rekomendasi pantai: **Pantai Padang** yang gratis dan **Pantai Air Manis** dengan tiket Rp10.000.';

        $res = $this->validator->validate($llmResponse, $facts);

        $this->assertTrue($res['isGrounded']);
        $this->assertEmpty($res['violations']);
        $this->assertEmpty($res['fabricatedEntities']);
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
}

<?php

namespace Tests\Unit;

use App\Services\SpatialIntent\SirValidator;
use App\Services\SpatialIntent\SpatialIntent;
use CodeIgniter\Test\CIUnitTestCase;

class SirValidatorTest extends CIUnitTestCase
{
    protected SirValidator $validator;

    protected function setUp(): void
    {
        parent::setUp();
        $this->validator = new SirValidator();
    }

    /**
     * Uji Dimensi 1: Schema & Type sanitasi XSS.
     */
    public function testSchemaSanitization()
    {
        $sir = new SpatialIntent(
            targetName: '<script>alert("hack")</script>Pantai Padang',
            keyword: '<b>pasir putih</b>'
        );

        $res = $this->validator->validate($sir);

        $this->assertTrue($res['isValid']);
        $this->assertSame('alert("hack")Pantai Padang', $sir->targetName);
        $this->assertSame('pasir putih', $sir->keyword);
    }

    /**
     * Uji Dimensi 2: No Intent Alteration - Radius negatif harus DITOLAK, bukan di-abs()!
     */
    public function testNegativeRadiusMustBeRejectedWithoutAbs()
    {
        $sir = new SpatialIntent(
            spatialOperator: 'within_radius',
            radius: -5.0
        );

        $res = $this->validator->validate($sir);

        $this->assertFalse($res['isValid']);
        $this->assertSame('rejected', $sir->validationStatus);
        $this->assertSame('clarify_user', $sir->executionPolicy);
        $this->assertNotEmpty($sir->validationErrors);
        $this->assertStringContainsString('Radius pencarian tidak valid', $sir->validationErrors[0]);
    }

    /**
     * Uji Dimensi 3: Operator tak dikenal harus GAGAL, bukan diam-diam dialihkan ke 'none'!
     */
    public function testUnknownOperatorMustFail()
    {
        $sir = new SpatialIntent(
            spatialOperator: 'around_me'
        );

        $res = $this->validator->validate($sir);

        $this->assertFalse($res['isValid']);
        $this->assertStringContainsString('Operator spasial \'around_me\' tidak terdaftar', $sir->validationErrors[0]);
    }

    /**
     * Uji Dimensi 4: Koordinat di luar batas bola bumi WGS84 harus ditolak.
     */
    public function testCoordinateBounds()
    {
        $sir = new SpatialIntent(
            latitude: 120.0, // Invalid latitude (> 90)
            longitude: 100.35
        );

        $res = $this->validator->validate($sir);

        $this->assertFalse($res['isValid']);
        $this->assertStringContainsString('Koordinat latitude di luar batas WGS84', $sir->validationErrors[0]);
    }

    /**
     * Uji Dimensi 5: Kontradiksi aturan operasional (is_free = true tapi max_price > 0).
     */
    public function testContradictionBudgetConstraint()
    {
        $sir = new SpatialIntent(
            isFree: true,
            maxPrice: 25000
        );

        $res = $this->validator->validate($sir);

        $this->assertFalse($res['isValid']);
        $this->assertStringContainsString('Kontradiksi batasan anggaran', $sir->validationErrors[0]);
    }

    /**
     * Uji Dimensi 6: Permintaan luar lingkup (Out-of-Scope) harus ditolak secara jujur.
     */
    public function testOutOfScopeDetection()
    {
        $sir = new SpatialIntent(
            rawQuery: 'Saya mau main ski salju dan kasino di Padang'
        );

        $res = $this->validator->validate($sir);

        $this->assertFalse($res['isValid']);
        $this->assertTrue($sir->isOutOfScope);
        $this->assertSame('out_of_scope', $sir->validationStatus);
        $this->assertSame('reject_out_of_scope', $sir->executionPolicy);
    }
}

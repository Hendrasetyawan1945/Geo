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
     * Uji Dimensi 2: No Intent Alteration - Radius melebihi batas operasional (> 50 km) harus DITOLAK, bukan di-clamp!
     */
    public function testExcessiveRadiusMustBeRejectedWithoutClamping()
    {
        $sir = new SpatialIntent(
            spatialOperator: 'within_radius',
            radius: 150.0
        );

        $res = $this->validator->validate($sir);

        $this->assertFalse($res['isValid']);
        $this->assertSame('rejected', $sir->validationStatus);
        $this->assertSame('clarify_user', $sir->executionPolicy);
        $this->assertStringContainsString('melebihi batas operasional Kota Padang', $sir->validationErrors[0]);
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
     * Uji Dimensi 3: No Silent Spatial Assumption - within_radius tanpa radius (null) harus DITOLAK via clarify_user, bukan diasumsikan 20 km!
     */
    public function testWithinRadiusWithoutRadiusMustBeRejected()
    {
        $sir = new SpatialIntent(
            spatialOperator: 'within_radius',
            radius: null
        );

        $res = $this->validator->validate($sir);

        $this->assertFalse($res['isValid']);
        $this->assertSame('rejected', $sir->validationStatus);
        $this->assertSame('clarify_user', $sir->executionPolicy);
        $this->assertNotEmpty($sir->validationErrors);
        $this->assertStringContainsString('memerlukan spesifikasi radius pencarian', $sir->validationErrors[0]);
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
     * Uji Dimensi 5: Harmonisasi preferensi anggaran (is_free = true dan max_price > 0 bukan kontradiksi).
     * Secara relasional {harga = 0} ⊆ {harga <= P}, sehingga kueri harus VALID.
     */
    public function testInclusiveBudgetConstraintIsValid()
    {
        $sir = new SpatialIntent(
            isFree: true,
            maxPrice: 25000
        );

        $res = $this->validator->validate($sir);

        $this->assertTrue($res['isValid']);
        $this->assertEmpty($res['errors']);
        $this->assertSame('execute_sql', $res['executionPolicy']);
    }

    /**
     * Uji Dimensi 5: Harga maksimum negatif harus ditolak secara tegas.
     */
    public function testNegativePriceMustFail()
    {
        $sir = new SpatialIntent(
            maxPrice: -5000
        );

        $res = $this->validator->validate($sir);

        $this->assertFalse($res['isValid']);
        $this->assertStringContainsString('tidak boleh bernilai negatif', $sir->validationErrors[0]);
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

    /**
     * Uji Formal Multi-Turn Semantic State Merging: CSIR_{t+1} = Merge(CSIR_t, \Delta CSIR_{t+1})
     */
    public function testMultiTurnSemanticStateMerging()
    {
        // Turn 1: Inisiasi spasial Pantai Padang
        $csir1 = new SpatialIntent(
            category: 'Pantai',
            referenceType: 'gps',
            latitude: -0.958742,
            longitude: 100.354128,
            spatialOperator: 'nearest',
            rawQuery: 'Cari pantai dekat saya'
        );
        $this->validator->validate($csir1);

        // Turn 2: Delta batasan harga (ujaran eliptik tanpa menyebut ulang 'pantai' atau GPS)
        $delta2 = new SpatialIntent(
            maxPrice: 15000,
            rawQuery: 'Yang tiketnya di bawah 15 ribu'
        );
        $this->validator->validate($delta2);

        // State transition: CSIR_2 = Merge(CSIR_1, Delta_2)
        $csir2 = $csir1->mergeWith($delta2);

        $this->assertSame('Pantai', $csir2->category);
        $this->assertSame('gps', $csir2->referenceType);
        $this->assertSame(-0.958742, $csir2->latitude);
        $this->assertSame('nearest', $csir2->spatialOperator);
        $this->assertSame(15000, $csir2->maxPrice);

        // Turn 3: Delta batasan jam operasional
        $delta3 = new SpatialIntent(
            openNow: true,
            rawQuery: 'Yang buka sekarang'
        );
        $this->validator->validate($delta3);

        // State transition: CSIR_3 = Merge(CSIR_2, Delta_3)
        $csir3 = $csir2->mergeWith($delta3);

        $this->assertSame('Pantai', $csir3->category);
        $this->assertSame(-0.958742, $csir3->latitude);
        $this->assertSame(15000, $csir3->maxPrice);
        $this->assertTrue($csir3->openNow);
    }
}

<?php

namespace Tests\Unit;

use App\Services\SpatialIntent\SpatialIntent;
use App\Services\SpatialIntent\SpatialQueryCompiler;
use CodeIgniter\Test\CIUnitTestCase;

class SpatialQueryCompilerTest extends CIUnitTestCase
{
    protected SpatialQueryCompiler $compiler;

    protected function setUp(): void
    {
        parent::setUp();
        $this->compiler = new SpatialQueryCompiler();
    }

    /**
     * Safety Invariant: Kueri tidak valid dilarang dieksekusi!
     */
    public function testInvalidSirIsNotExecutable()
    {
        $sir = new SpatialIntent(isValid: false);
        $res = $this->compiler->compile($sir);

        $this->assertFalse($res['isExecutable']);
        $this->assertSame('', $res['sql']);
        $this->assertEmpty($res['params']);
    }

    /**
     * Uji kompilasi kueri terdekat dengan ST_Distance_Sphere pada MySQL 8.0.
     */
    public function testNearestSpatialQueryCompilation()
    {
        $sir = new SpatialIntent(
            category: 'Pantai',
            spatialOperator: 'nearest',
            latitude: -0.9489,
            longitude: 100.3572,
            isValid: true
        );

        $res = $this->compiler->compile($sir, 5);

        $this->assertTrue($res['isExecutable']);
        $this->assertStringContainsString('ST_Distance_Sphere', $res['sql']);
        $this->assertStringContainsString('kategori.nama = ?', $res['sql']);
        $this->assertStringContainsString('ORDER BY ST_Distance_Sphere', $res['sql']);
        $this->assertContains('Pantai', $res['params']);
        $this->assertContains(5, $res['params']);
    }

    /**
     * Uji kompilasi kueri radius dengan batas ST_Distance_Sphere.
     */
    public function testWithinRadiusSpatialQueryCompilation()
    {
        $sir = new SpatialIntent(
            spatialOperator: 'within_radius',
            latitude: -0.9489,
            longitude: 100.3572,
            radius: 10.0,
            isValid: true
        );

        $res = $this->compiler->compile($sir, 10);

        $this->assertTrue($res['isExecutable']);
        $this->assertStringContainsString('(ST_Distance_Sphere(POINT(wisata.lng, wisata.lat), POINT(?, ?)) / 1000.0) <= ?', $res['sql']);
        $this->assertContains(10.0, $res['params']);
    }

    /**
     * Security Test: Injeksi SQL berbahaya via kata kunci (' OR 1=1 --).
     * Memastikan string injeksi selalu di-bind sebagai nilai parameter literal (PDO binding),
     * tidak pernah memodifikasi struktur pohon sintaksis kueri SQL.
     */
    public function testSqlInjectionAttemptIsParameterizedAsLiteral()
    {
        $maliciousPayload = "' OR 1=1 --";
        $sir = new SpatialIntent(
            keyword: $maliciousPayload,
            isValid: true
        );

        $res = $this->compiler->compile($sir);

        $this->assertTrue($res['isExecutable']);
        $this->assertStringNotContainsString("' OR 1=1 --", $res['sql']);
        $this->assertStringContainsString('wisata.nama LIKE ?', $res['sql']);
        $this->assertContains('%' . $maliciousPayload . '%', $res['params']);
    }
}

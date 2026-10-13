<?php

declare(strict_types=1);

namespace Tests\Unit;

use App\Services\SpatialIntent\SpatialIntent;
use App\Services\SpatialIntent\SpatialQueryCompiler;
use CodeIgniter\Test\CIUnitTestCase;
use mysqli;

/**
 * SpatialDatabaseIntegrationTest
 *
 * Pengujian integrasi basis data spasial independen terhadap kernel MySQL 8.0 (geo_db).
 * Memverifikasi:
 * 1. Integritas dataset 22 POI terstandarisasi Kota Padang.
 * 2. Presisi komputasi jarak geodesik native ST_Distance_Sphere terhadap rumus Haversine independen PHP.
 * 3. Batas spasial radius (Spatial Radius Boundary Enforcement).
 * 4. Keterurutan jarak monotonik terdekat (Monotonic Proximity Ordering).
 * 5. Kompilasi dan eksekusi kueri terparameter SpatialQueryCompiler.
 * 6. Penanganan koordinat di luar batas wilayah (Out-of-bounds coordinate clipping).
 */
class SpatialDatabaseIntegrationTest extends CIUnitTestCase
{
    protected ?mysqli $mysqli = null;
    protected SpatialQueryCompiler $compiler;

    protected function setUp(): void
    {
        parent::setUp();
        $this->compiler = new SpatialQueryCompiler();

        $this->mysqli = @new mysqli('127.0.0.1', 'geo_user', 'GeoSecurePass2026_db', 'geo_db');
        if ($this->mysqli->connect_error) {
            $this->markTestSkipped('Koneksi basis data MySQL geo_db tidak tersedia: ' . $this->mysqli->connect_error);
        }
    }

    protected function tearDown(): void
    {
        if ($this->mysqli && !$this->mysqli->connect_error) {
            $this->mysqli->close();
        }
        parent::tearDown();
    }

    /**
     * Verifikasi integritas dataset acuan 22 POI terdistribusi pada 6 kategori.
     */
    public function testDatabaseConnectivityAndKnownPoiCount(): void
    {
        $res = $this->mysqli->query('SELECT COUNT(*) as total FROM wisata');
        $row = $res->fetch_assoc();
        $this->assertSame(22, (int) $row['total'], 'Basis data geo_db harus memiliki tepat 22 POI acuan.');

        $catRes = $this->mysqli->query('SELECT COUNT(DISTINCT nama) as total_cat FROM kategori');
        $catRow = $catRes->fetch_assoc();
        $this->assertGreaterThanOrEqual(6, (int) $catRow['total_cat'], 'Harus terdapat minimal 6 kategori wisata.');
    }

    /**
     * Buktikan akurasi native ST_Distance_Sphere terhadap perhitungan Haversine independen PHP (< 0.1% selisih).
     */
    public function testNativeDistanceSphereVsHaversineGeodesicAccuracy(): void
    {
        // Titik acuan Pusat Kota Padang
        $userLat = -0.9471;
        $userLng = 100.4174;

        // Ambil koordinat Pantai Padang dari basis data (kolom lat, lng)
        $stmt = $this->mysqli->prepare("SELECT nama, lat, lng FROM wisata WHERE nama LIKE '%Pantai Padang%' LIMIT 1");
        $stmt->execute();
        $result = $stmt->get_result()->fetch_assoc();
        $stmt->close();

        $this->assertNotNull($result, 'Pantai Padang harus ada di basis data.');
        $poiLat = (float) $result['lat'];
        $poiLng = (float) $result['lng'];

        // 1. Hitung menggunakan MySQL ST_Distance_Sphere native
        $sqlNative = "SELECT ST_Distance_Sphere(POINT(?, ?), POINT(?, ?)) as distance_meters";
        $stmtNative = $this->mysqli->prepare($sqlNative);
        $stmtNative->bind_param('dddd', $userLng, $userLat, $poiLng, $poiLat);
        $stmtNative->execute();
        $nativeRow = $stmtNative->get_result()->fetch_assoc();
        $stmtNative->close();
        $nativeDist = (float) $nativeRow['distance_meters'];

        // 2. Hitung menggunakan rumus Haversine murni dalam PHP
        // R = 6371008.8 meter (radius speroid rata-rata WGS 84 MySQL)
        $earthRadius = 6371008.8;
        $lat1Rad = deg2rad($userLat);
        $lat2Rad = deg2rad($poiLat);
        $dLatRad = deg2rad($poiLat - $userLat);
        $dLngRad = deg2rad($poiLng - $userLng);

        $a = sin($dLatRad / 2) ** 2 + cos($lat1Rad) * cos($lat2Rad) * (sin($dLngRad / 2) ** 2);
        $c = 2 * atan2(sqrt($a), sqrt(1 - $a));
        $haversineDist = $earthRadius * $c;

        // Verifikasi selisih relatif < 0.05%
        $diffMeters = abs($nativeDist - $haversineDist);
        $relError = $diffMeters / $nativeDist;

        $this->assertLessThan(0.0005, $relError, "Selisih geodesik ({$diffMeters} m) harus di bawah toleransi 0.05%.");
        $this->assertGreaterThan(0, $nativeDist);
    }

    /**
     * Verifikasi batas spasial radius: Semua POI yang dikembalikan harus berada di dalam radius R.
     */
    public function testSpatialRadiusBoundaryEnforcement(): void
    {
        // Koordinat user di sekitar Pantai Padang
        $userLat = -0.9234;
        $userLng = 100.3621;
        $radiusKm = 3.0;
        $radiusMeters = $radiusKm * 1000.0;

        $query = "SELECT nama, lat, lng,
                         ST_Distance_Sphere(POINT(?, ?), POINT(lng, lat)) as dist_meters
                  FROM wisata
                  WHERE ST_Distance_Sphere(POINT(?, ?), POINT(lng, lat)) <= ?
                  ORDER BY dist_meters ASC";

        $stmt = $this->mysqli->prepare($query);
        $stmt->bind_param('ddddd', $userLng, $userLat, $userLng, $userLat, $radiusMeters);
        $stmt->execute();
        $res = $stmt->get_result();

        $rows = [];
        while ($row = $res->fetch_assoc()) {
            $rows[] = $row;
            $dist = (float) $row['dist_meters'];
            $this->assertLessThanOrEqual(
                $radiusMeters,
                $dist,
                "POI '{$row['nama']}' berjarak {$dist}m melebihi batas radius {$radiusMeters}m."
            );
        }
        $stmt->close();

        // Harus ada POI yang terjangkau dalam 3 km dari pantai Padang
        $this->assertNotEmpty($rows, 'Harus ada POI yang terdeteksi dalam radius 3 km.');

        // Pastikan POI yang jauh (misal Pulau Pasumpahan > 15 km) TIDAK masuk dalam hasil
        $names = array_column($rows, 'nama');
        $this->assertNotContains('Pulau Pasumpahan', $names, 'Pulau Pasumpahan tidak boleh lolos filter radius 3 km.');
    }

    /**
     * Verifikasi monotonic proximity ordering: Urutan hasil kueri 'nearest' wajib monoton naik.
     */
    public function testMonotonicProximityOrdering(): void
    {
        $userLat = -0.9471;
        $userLng = 100.4174;
        $limit = 5;

        $query = "SELECT nama, ST_Distance_Sphere(POINT(?, ?), POINT(lng, lat)) as dist_meters
                  FROM wisata
                  ORDER BY dist_meters ASC
                  LIMIT ?";

        $stmt = $this->mysqli->prepare($query);
        $stmt->bind_param('ddi', $userLng, $userLat, $limit);
        $stmt->execute();
        $res = $stmt->get_result();

        $prevDist = -1.0;
        $count = 0;
        while ($row = $res->fetch_assoc()) {
            $currentDist = (float) $row['dist_meters'];
            $this->assertGreaterThanOrEqual(
                $prevDist,
                $currentDist,
                "Urutan jarak harus monoton naik: sebelumnya {$prevDist}m, sekarang {$currentDist}m."
            );
            $prevDist = $currentDist;
            $count++;
        }
        $stmt->close();

        $this->assertSame($limit, $count, "Harus mengembalikan tepat {$limit} POI terdekat.");
    }

    /**
     * Verifikasi eksekusi SQL yang dihasilkan SpatialQueryCompiler terhadap database langsung.
     */
    public function testSpatialQueryCompilerExecutionIntegrity(): void
    {
        $sir = new SpatialIntent(
            category: 'Pantai',
            spatialOperator: 'within_radius',
            latitude: -0.9234,
            longitude: 100.3621,
            radius: 5.0,
            distanceUnit: 'km',
            isValid: true
        );

        $compiled = $this->compiler->compile($sir, 10);
        $this->assertTrue($compiled['isExecutable']);

        $stmt = $this->mysqli->prepare($compiled['sql']);
        $this->assertNotFalse($stmt, 'SQL hasil kompilasi compiler harus valid pada MySQL 8.0: ' . $this->mysqli->error);

        // Bind parameter dinamis
        $types = '';
        $bindArgs = [];
        foreach ($compiled['params'] as $p) {
            if (is_int($p)) {
                $types .= 'i';
            } elseif (is_float($p)) {
                $types .= 'd';
            } else {
                $types .= 's';
            }
            $bindArgs[] = $p;
        }

        $stmt->bind_param($types, ...$bindArgs);
        $stmt->execute();
        $res = $stmt->get_result();

        $results = [];
        while ($row = $res->fetch_assoc()) {
            $results[] = $row;
            // Verifikasi kategori adalah Pantai
            $this->assertStringContainsStringIgnoringCase('Pantai', $row['kategori'] ?? $row['nama']);
            // Verifikasi jarak <= 5.0 km
            $distKm = (float) $row['jarak_km'];
            $this->assertLessThanOrEqual(5.0, $distKm);
        }
        $stmt->close();

        $this->assertNotEmpty($results, 'Kueri terkompilasi harus menghasilkan data wisata yang sesuai.');
    }

    /**
     * Verifikasi penanganan koordinat jauh di luar cakupan Kota Padang (misal Jakarta / Kutub).
     * Dengan radius 5 km, basis data harus mengembalikan 0 baris (empty set) tanpa error sintaks.
     */
    public function testOutOfBoundsCoordinateHandling(): void
    {
        // Koordinat Monas Jakarta (-6.1754, 106.8272)
        $farLat = -6.1754;
        $farLng = 106.8272;
        $radiusMeters = 5000.0;

        $query = "SELECT id, nama
                  FROM wisata
                  WHERE ST_Distance_Sphere(POINT(?, ?), POINT(lng, lat)) <= ?";

        $stmt = $this->mysqli->prepare($query);
        $stmt->bind_param('ddd', $farLng, $farLat, $radiusMeters);
        $stmt->execute();
        $res = $stmt->get_result();

        $this->assertSame(0, $res->num_rows, 'Koordinat di luar Kota Padang harus menghasilkan 0 POI dalam radius 5 km.');
        $stmt->close();
    }
}

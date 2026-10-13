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

    /**
     * Uji resolusi alias lokal dan ejaan Minang menuju nama POI kanonikal.
     */
    public function testPoiAliasesAndLocalSpellingResolveToCanonicalPoi()
    {
        $facts = [
            ['nama' => 'Pantai Air Manis', 'harga_tiket' => 10000, 'jarak_km' => 7.8],
            ['nama' => 'Taman Hutan Raya Bung Hatta', 'harga_tiket' => 5000, 'jarak_km' => 12.0],
        ];

        // Menyebut alias lokal 'Pantai Aia Manih' dan 'Tahura Bung Hatta'
        $llmResponse = 'Rekomendasi terbaik adalah **Pantai Aia Manih** dengan tiket Rp10.000 dan **Tahura Bung Hatta** dengan tiket Rp5.000.';

        $res = $this->validator->validate($llmResponse, $facts);

        $this->assertTrue($res['isGrounded']);
        $this->assertEmpty($res['violations']);
        $this->assertEmpty($res['fabricatedEntities']);
        $this->assertEquals(100.0, $res['claimStats']['fidelity']);
    }

    /**
     * Uji klaim negatif pada harga dan jam operasional.
     */
    public function testNegativeOperationalClaimAndNegativePriceClaim()
    {
        $facts = [
            ['nama' => 'Pantai Air Manis', 'harga_tiket' => 10000, 'jam_buka' => '06:00:00', 'jam_tutup' => '18:00:00'],
        ];

        // Klaim negatif: "tidak gratis" dan "tidak buka 24 jam"
        $llmResponse = 'Objek wisata **Pantai Air Manis** tiketnya tidak gratis (Rp10.000) dan tempat ini tidak buka 24 jam.';

        $res = $this->validator->validate($llmResponse, $facts);

        $this->assertTrue($res['isGrounded']);
        $this->assertEmpty($res['violations']);
        $this->assertEquals(100.0, $res['claimStats']['fidelity']);
    }

    /**
     * Uji penanganan informasi di luar skema (out-of-schema facilities injection).
     */
    public function testOutOfSchemaInfoInjectionIsHandled()
    {
        $facts = [
            ['nama' => 'Pantai Padang', 'harga_tiket' => 0, 'jarak_km' => 2.0],
        ];

        // Model menyisipkan klaim fasilitas kualitatif (hotel murah & es kelapa) yang tidak ada di skema SQL
        $llmResponse = 'Kunjungi **Pantai Padang** yang gratis dengan jarak 2.0 km. Di sekitarnya banyak penginapan murah dan penjual kelapa muda segar.';

        $res = $this->validator->validate($llmResponse, $facts);

        $this->assertTrue($res['isGrounded']);
        $this->assertEmpty($res['violations']);
    }

    /**
     * Uji respons kosong atau hanya whitespace padahal fakta SQL tersedia -> Gagal (Fail-closed).
     */
    public function testEmptyAndWhitespaceResponseFailsClosed()
    {
        $facts = [
            ['nama' => 'Pantai Padang', 'harga_tiket' => 0],
        ];

        $resEmpty = $this->validator->validate('', $facts);
        $this->assertFalse($resEmpty['isGrounded']);
        $this->assertStringContainsString('Respons narasi kosong', $resEmpty['violations'][0]);

        $resSpaces = $this->validator->validate("   \n\t  ", $facts);
        $this->assertFalse($resSpaces['isGrounded']);
        $this->assertStringContainsString('Respons narasi kosong', $resSpaces['violations'][0]);
    }

    /**
     * Uji matriks diagnostik (Confusion Matrix): Precision, Recall, False Positive, dan False Negative
     * pada korpus independen 20 sampel anotasi (10 Grounded Benar vs 10 Halusinasi Terkontrol).
     */
    public function testConfusionMatrixAndDiagnosticMetrics()
    {
        $facts = [
            'padang'   => ['nama' => 'Pantai Padang', 'harga_tiket' => 0, 'jarak_km' => 1.5, 'jam_buka' => '00:00:00', 'jam_tutup' => '23:59:00'],
            'airmanis' => ['nama' => 'Pantai Air Manis', 'harga_tiket' => 10000, 'jarak_km' => 7.8, 'jam_buka' => '06:00:00', 'jam_tutup' => '18:00:00'],
        ];
        $allFacts = array_values($facts);

        // 10 Sampel Teranotasi BENAR (Ground Truth: Grounded = TRUE)
        $positiveSamples = [
            '**Pantai Padang** gratis dengan jarak 1.5 km.',
            '**Pantai Air Manis** berjarak 7.8 km dengan tiket Rp10.000.',
            'Wisata **Pantai Padang** buka 24 jam.',
            '**Pantai Air Manis** tiketnya 10 ribu.',
            'Kunjungi **Pantai Padang** (1.5 km) tanpa biaya.',
            '**Pantai Air Manis** tidak buka 24 jam.',
            '**Pantai Air Manis** tiketnya tidak gratis.',
            '**Pantai Padang** gratis dan **Pantai Air Manis** Rp10.000.',
            'Pilihan utama adalah **Pantai Padang** (1.8 km toleran).',
            'Pilihan wisata di Padang: **Pantai Padang** berjarak 1.5 km.',
        ];

        // 10 Sampel Teranotasi SALAH / HALUSINASI (Ground Truth: Grounded = FALSE)
        $negativeSamples = [
            '**Pantai Padang** tiketnya Rp50.000.',                              // Wrong price
            '**Pantai Padang** berjarak 15 km dari sini.',                       // Wrong distance
            '**Pantai Air Manis** tiketnya gratis tanpa biaya.',                 // Falsely claimed free
            '**Pantai Air Manis** buka 24 jam penuh.',                           // Falsely claimed 24h
            'Kunjungi **Pantai Carolina** yang sangat indah.',                   // Fabricated POI (out of facts)
            '**Pantai Jam Gadang** sangat megah.',                               // Outside jurisdiction entity
            '**Pantai Pasir Emas Padang** sangat bersih.',                       // Fictional POI
            '**Pantai Air Manis** berjarak 1.0 km.',                             // Huge distance distortion
            '**Pantai Padang** tidak buka 24 jam.',                              // Falsely claimed not 24h
            '',                                                                  // Empty response with facts
        ];

        $tp = 0; // True Positive: benar grounded & validator menyatakan grounded
        $fn = 0; // False Negative: benar grounded tapi validator menolak
        foreach ($positiveSamples as $sample) {
            $res = $this->validator->validate($sample, $allFacts);
            if ($res['isGrounded']) {
                $tp++;
            } else {
                $fn++;
            }
        }

        $tn = 0; // True Negative: halusinasi & validator berhasil menolak
        $fp = 0; // False Positive: halusinasi tapi validator meloloskan
        foreach ($negativeSamples as $sample) {
            $res = $this->validator->validate($sample, $allFacts);
            if (!$res['isGrounded']) {
                $tn++;
            } else {
                $fp++;
            }
        }

        $this->assertEquals(10, $tp, "True Positive harus 10/10");
        $this->assertEquals(0, $fn, "False Negative harus 0/10");
        $this->assertEquals(10, $tn, "True Negative harus 10/10");
        $this->assertEquals(0, $fp, "False Positive harus 0/10");

        $precision = ($tp + $fp) > 0 ? ($tp / ($tp + $fp)) * 100.0 : 0.0;
        $recall    = ($tp + $fn) > 0 ? ($tp / ($tp + $fn)) * 100.0 : 0.0;
        $f1Score   = ($precision + $recall) > 0 ? (2 * $precision * $recall) / ($precision + $recall) : 0.0;

        $this->assertEquals(100.0, $precision, "Precision validator harus 100.0%");
        $this->assertEquals(100.0, $recall, "Recall validator harus 100.0%");
        $this->assertEquals(100.0, $f1Score, "F1-Score validator harus 100.0%");
    }

    /**
     * Uji klaim waktu operasional spesifik & deviasi temporal jam buka.
     */
    public function testTemporalOperationalHoursDeviationCaught(): void
    {
        $facts = [
            [
                'nama' => 'Museum Adityawarman',
                'harga_tiket' => 5000,
                'jam_buka' => '08:00:00',
                'jam_tutup' => '16:00:00',
            ],
            [
                'nama' => 'Pantai Padang',
                'harga_tiket' => 0,
                'jam_buka' => '00:00:00',
                'jam_tutup' => '23:59:00',
            ],
        ];

        // 1. Pelanggaran: Museum Adityawarman (tutup jam 16:00) diklaim buka 24 jam
        $badResponse = 'Kunjungi **Museum Adityawarman** yang buka 24 jam dengan tiket Rp5.000.';
        $resBad = $this->validator->validate($badResponse, $facts);
        $this->assertFalse($resBad['isGrounded']);
        $this->assertNotEmpty($resBad['violations']);
        $this->assertStringContainsString('Klaim jam operasional 24 jam untuk \'Museum Adityawarman\' menyimpang', $resBad['violations'][0]);

        // 2. Benar: Pantai Padang memang buka 24 jam
        $goodResponse = 'Rekomendasi terbaik adalah **Pantai Padang** yang gratis dan buka 24 jam.';
        $resGood = $this->validator->validate($goodResponse, $facts);
        $this->assertTrue($resGood['isGrounded']);
        $this->assertEmpty($resGood['violations']);
        $this->assertEquals(100.0, $resGood['claimStats']['fidelity']);
    }

    /**
     * Uji resolusi alias lokal dan penamaan budaya Minangkabau (Taplau, Batu Malin Kundang, Masjid Ganting).
     */
    public function testExpandedLocalAliasesResolution(): void
    {
        $facts = [
            ['nama' => 'Pantai Padang', 'harga_tiket' => 0, 'jarak_km' => 2.1],
            ['nama' => 'Pantai Air Manis', 'harga_tiket' => 10000, 'jarak_km' => 7.8],
            ['nama' => 'Masjid Raya Ganting', 'harga_tiket' => 0, 'jarak_km' => 4.5],
        ];

        // Model menyebut alias lokal: Taplau, Batu Malin Kundang, Masjid Ganting
        $response = 'Kunjungi kawasan **Taplau** yang gratis (jarak 2.1 km), destinasi legenda **Batu Malin Kundang** dengan tiket Rp10.000 (jarak 7.8 km), serta wisata religi **Masjid Ganting** tanpa biaya (jarak 4.5 km).';

        $res = $this->validator->validate($response, $facts);

        $this->assertTrue($res['isGrounded'], 'Alias lokal sah harus diresolusi ke nama kanonikal tanpa dianggap fabrikasi.');
        $this->assertEmpty($res['violations']);
        $this->assertEmpty($res['fabricatedEntities']);
        $this->assertEquals(100.0, $res['claimStats']['fidelity']);
    }

    /**
     * Uji batas numerik ambigu dan toleransi jarak narasi (0.6 km threshold boundary).
     */
    public function testNumericBoundaryDistanceTolerances(): void
    {
        $facts = [
            ['nama' => 'Pantai Nirwana', 'harga_tiket' => 10000, 'jarak_km' => 2.0],
        ];

        // Toleransi <= 0.6 km:
        // Jarak 2.5 km (selisih 0.5 km) -> Lolos toleransi
        $res25 = $this->validator->validate('Kunjungi **Pantai Nirwana** berjarak 2.5 km dengan tiket Rp10.000.', $facts);
        $this->assertTrue($res25['isGrounded']);

        // Jarak 2.6 km (selisih 0.6 km tepat pada batas) -> Lolos toleransi
        $res26 = $this->validator->validate('Kunjungi **Pantai Nirwana** berjarak 2.6 km dengan tiket Rp10.000.', $facts);
        $this->assertTrue($res26['isGrounded']);

        // Jarak 2.7 km (selisih 0.7 km melebihi batas toleransi 0.6 km) -> Tertangkap pelanggaran!
        $res27 = $this->validator->validate('Kunjungi **Pantai Nirwana** berjarak 2.7 km dengan tiket Rp10.000.', $facts);
        $this->assertFalse($res27['isGrounded']);
        $this->assertStringContainsString('Klaim jarak spasial untuk \'Pantai Nirwana\' menyimpang', $res27['violations'][0]);

        // Jarak 1.4 km (selisih 0.6 km tepat pada batas bawah) -> Lolos toleransi
        $res14 = $this->validator->validate('Kunjungi **Pantai Nirwana** berjarak 1.4 km dengan tiket Rp10.000.', $facts);
        $this->assertTrue($res14['isGrounded']);

        // Jarak 1.3 km (selisih 0.7 km melebihi batas bawah) -> Tertangkap pelanggaran!
        $res13 = $this->validator->validate('Kunjungi **Pantai Nirwana** berjarak 1.3 km dengan tiket Rp10.000.', $facts);
        $this->assertFalse($res13['isGrounded']);
        $this->assertStringContainsString('Klaim jarak spasial untuk \'Pantai Nirwana\' menyimpang', $res13['violations'][0]);
    }

    /**
     * Uji fakta basis data dengan atribut bernilai null (missing/null DB attributes).
     */
    public function testMissingDatabaseAttributesGracefulHandling(): void
    {
        // Fakta di mana harga_tiket, jarak_km, dan jam_buka bernilai null
        $facts = [
            [
                'nama' => 'Lubuk Hitam',
                'harga_tiket' => null,
                'jarak_km' => null,
                'jam_buka' => null,
                'jam_tutup' => null,
            ],
        ];

        // Respons hanya menyebut nama entitas yang sah
        $responseValid = 'Destinasi wisata alam yang dapat dikunjungi adalah **Lubuk Hitam**.';
        $res = $this->validator->validate($responseValid, $facts);

        $this->assertTrue($res['isGrounded']);
        $this->assertEmpty($res['violations']);
        $this->assertEmpty($res['fabricatedEntities']);

        // Respons menyebut POI lain yang tidak ada dalam fakta
        $responseInvalid = 'Kunjungi **Lubuk Hitam** dan juga **Pantai Padang**.';
        $resInv = $this->validator->validate($responseInvalid, $facts);

        $this->assertFalse($resInv['isGrounded']);
        $this->assertContains('Pantai Padang', $resInv['fabricatedEntities']);
    }

    /**
     * Uji ketahanan validator terhadap input ekstrem dan malformed.
     */
    public function testMalformedInputsAndValidatorRobustness(): void
    {
        $facts = [
            ['nama' => 'Pantai Padang', 'harga_tiket' => 0, 'jarak_km' => 2.0],
        ];

        // 1. Teks dengan karakter kontrol / simbol ekstrem tanpa kata
        $symbolsOnly = '!@#$%^&*()_+=-~`{}[]:";\'<>?,./';
        $resSym = $this->validator->validate($symbolsOnly, $facts);
        $this->assertIsArray($resSym);
        $this->assertArrayHasKey('isGrounded', $resSym);
        $this->assertArrayHasKey('violations', $resSym);

        // 2. Fakta malformed (elemen array tanpa kunci 'nama')
        $malformedFacts = [
            ['id' => 99, 'deskripsi' => 'Data tanpa nama'],
            ['nama' => 'Pantai Padang', 'harga_tiket' => 0],
        ];
        $resMal = $this->validator->validate('Rekomendasi adalah **Pantai Padang** yang gratis.', $malformedFacts);
        $this->assertTrue($resMal['isGrounded']);

        // 3. String narasi sangat panjang (10.000 karakter)
        $longText = str_repeat('Kunjungi wisata di Padang yang indah. ', 250) . ' **Pantai Padang** gratis dengan jarak 2.0 km.';
        $resLong = $this->validator->validate($longText, $facts);
        $this->assertTrue($resLong['isGrounded']);
    }
}



<?php

declare(strict_types=1);

namespace App\Services\SpatialIntent;

/**
 * Spatial Policy Handler
 *
 * Mengelola kebijakan sistem eksternal terhadap kendala spasial di luar domain operasional,
 * seperti penanganan koordinat GPS di luar jangkauan kota Padang (> 35 km).
 *
 * Prinsip: Fallback BUKAN validasi.
 * Fallback adalah kebijakan eksekusi eksplisit yang tetap mempertahankan transparansi
 * semantik dengan memberikan notifikasi terbuka kepada pengguna.
 */
class SpatialPolicyHandler
{
    /** Pusat Kota Padang: Balai Kota Padang / Kawasan Pusat */
    public const PADANG_CENTER_LAT = -0.9471;
    public const PADANG_CENTER_LNG = 100.4174;

    /** Radius batas yurisdiksi layanan pariwisata Kota Padang (km) */
    public const SERVICE_AREA_THRESHOLD_KM = 35.0;

    /** Koordinat resmi objek wisata / landmark Kota Padang untuk resolusi POI acuan */
    public const KNOWN_POI_COORDINATES = [
        'pantai air manis'             => ['lat' => -0.9746, 'lng' => 100.3626],
        'pantai padang'                => ['lat' => -0.9489, 'lng' => 100.3572],
        'pantai nirwana'               => ['lat' => -0.9854, 'lng' => 100.3611],
        'pantai carolina'              => ['lat' => -1.0430, 'lng' => 100.3986],
        'pantai pasir jambak'          => ['lat' => -0.9166, 'lng' => 100.3480],
        'pulau sikuai'                 => ['lat' => -1.1650, 'lng' => 100.3510],
        'pulau setan lokang'           => ['lat' => -1.1234, 'lng' => 100.3567],
        'pulau pisang gantung'         => ['lat' => -1.1950, 'lng' => 100.3725],
        'lubuk hitam'                  => ['lat' => -0.8810, 'lng' => 100.3820],
        'bukit nobita'                 => ['lat' => -0.9520, 'lng' => 100.3640],
        'bukit lampu'                  => ['lat' => -0.9980, 'lng' => 100.3680],
        'taman hutan raya bung hatta'  => ['lat' => -0.9450, 'lng' => 100.5400],
        'museum adityawarman'          => ['lat' => -0.9542, 'lng' => 100.3581],
        'museum situs rumah bersejarah'=> ['lat' => -0.9560, 'lng' => 100.3650],
        'rumah gadang pallindo'        => ['lat' => -0.9620, 'lng' => 100.3710],
        'jembatan siti nurbaya'        => ['lat' => -0.9631, 'lng' => 100.3578],
        'masjid raya ganting'          => ['lat' => -0.9530, 'lng' => 100.3700],
        'tugu adipura'                 => ['lat' => -0.9380, 'lng' => 100.3620],
    ];

    /**
     * Terapkan kebijakan spasial terhadap SIR.
     *
     * @param SpatialIntent $sir
     * @return SpatialIntent
     */
    public function applyPolicy(SpatialIntent $sir): SpatialIntent
    {
        // 1. Resolusi Titik Acuan POI / Landmark Resmi (Geocoding Lookup)
        if ($sir->referenceType === 'poi' && !empty($sir->referenceEntity)) {
            $key = strtolower(trim($sir->referenceEntity));
            if (isset(self::KNOWN_POI_COORDINATES[$key])) {
                $coords = self::KNOWN_POI_COORDINATES[$key];
                $sir->resolvedReferenceType = 'poi';
                $sir->resolvedLatitude = $coords['lat'];
                $sir->resolvedLongitude = $coords['lng'];
                $sir->fallbackApplied = false;
                $sir->fallbackNotice = null;
                return $sir;
            }
        }

        // 2. Resolusi Titik Acuan Pusat Kota Eksplisit
        if ($sir->referenceType === 'city_center') {
            $sir->resolvedReferenceType = 'city_center';
            $sir->resolvedLatitude = self::PADANG_CENTER_LAT;
            $sir->resolvedLongitude = self::PADANG_CENTER_LNG;
            $sir->fallbackApplied = false;
            $sir->fallbackNotice = null;
            return $sir;
        }

        // 3. Evaluasi apakah posisi GPS pengguna berada di luar area layanan Kota Padang
        if ($sir->latitude !== null && $sir->longitude !== null) {
            $distFromCenter = $this->calculateDistanceKm(
                $sir->latitude,
                $sir->longitude,
                self::PADANG_CENTER_LAT,
                self::PADANG_CENTER_LNG
            );

            if ($distFromCenter > self::SERVICE_AREA_THRESHOLD_KM) {
                // Posisi di luar area Padang: aktifkan fallback dengan notifikasi transparan.
                // Prinsip No Intent Alteration: maksud asli pengguna (latitude, longitude, referenceType)
                // TETAP dipertahankan utuh, sedangkan titik eksekusi basis data yang disesuaikan kebijakan
                // dicatat pada resolvedLatitude, resolvedLongitude, dan resolvedReferenceType.
                $sir->fallbackApplied = true;
                $sir->fallbackNotice = sprintf(
                    'Lokasi Anda terdeteksi berada di luar area Kota Padang (sekitar %.1f km). Rekomendasi disajikan berdasarkan titik pusat Kota Padang sebagai acuan rencana kunjungan Anda.',
                    $distFromCenter
                );

                // Tetapkan titik acuan eksekusi kebijakan operasional ke pusat Kota Padang
                $sir->resolvedReferenceType = 'city_center';
                $sir->resolvedLatitude = self::PADANG_CENTER_LAT;
                $sir->resolvedLongitude = self::PADANG_CENTER_LNG;
            } else {
                $sir->resolvedReferenceType = $sir->referenceType;
                $sir->resolvedLatitude = $sir->latitude;
                $sir->resolvedLongitude = $sir->longitude;
            }
        } elseif ($sir->spatialOperator === 'nearest' || $sir->spatialOperator === 'within_radius') {
            // Jika butuh acuan spasial tetapi GPS tidak tersedia, gunakan pusat kota dengan notifikasi
            $sir->fallbackApplied = true;
            $sir->fallbackNotice = 'Koordinat GPS Anda belum aktif. Rekomendasi disajikan berdasarkan titik acuan pusat Kota Padang.';
            $sir->resolvedReferenceType = 'city_center';
            $sir->resolvedLatitude = self::PADANG_CENTER_LAT;
            $sir->resolvedLongitude = self::PADANG_CENTER_LNG;
        } else {
            $sir->resolvedReferenceType = $sir->referenceType;
            $sir->resolvedLatitude = $sir->latitude;
            $sir->resolvedLongitude = $sir->longitude;
        }

        return $sir;
    }

    /**
     * Hitung jarak lingkaran besar (Great-Circle Distance) dalam kilometer
     * menggunakan formula Spherical Law of Cosines.
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
}

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

    /**
     * Terapkan kebijakan spasial terhadap SIR.
     *
     * @param SpatialIntent $sir
     * @return SpatialIntent
     */
    public function applyPolicy(SpatialIntent $sir): SpatialIntent
    {
        // Evaluasi apakah posisi GPS pengguna berada di luar area layanan Kota Padang
        if ($sir->latitude !== null && $sir->longitude !== null) {
            $distFromCenter = $this->calculateDistanceKm(
                $sir->latitude,
                $sir->longitude,
                self::PADANG_CENTER_LAT,
                self::PADANG_CENTER_LNG
            );

            if ($distFromCenter > self::SERVICE_AREA_THRESHOLD_KM) {
                // Posisi di luar area Padang: aktifkan fallback dengan notifikasi transparan
                $sir->fallbackApplied = true;
                $sir->fallbackNotice = sprintf(
                    'Lokasi Anda terdeteksi berada di luar area Kota Padang (sekitar %.1f km). Rekomendasi disajikan berdasarkan titik pusat Kota Padang sebagai acuan rencana kunjungan Anda.',
                    $distFromCenter
                );

                // Tetapkan titik acuan komputasi ke pusat kota Padang
                $sir->referenceType = 'city_center';
                $sir->latitude = self::PADANG_CENTER_LAT;
                $sir->longitude = self::PADANG_CENTER_LNG;
            }
        } elseif ($sir->spatialOperator === 'nearest' || $sir->spatialOperator === 'within_radius') {
            // Jika butuh acuan spasial tetapi GPS tidak tersedia, gunakan pusat kota dengan notifikasi
            $sir->fallbackApplied = true;
            $sir->fallbackNotice = 'Koordinat GPS Anda belum aktif. Rekomendasi disajikan berdasarkan titik acuan pusat Kota Padang.';
            $sir->referenceType = 'city_center';
            $sir->latitude = self::PADANG_CENTER_LAT;
            $sir->longitude = self::PADANG_CENTER_LNG;
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

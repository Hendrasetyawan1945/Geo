<?php

declare(strict_types=1);

namespace App\Services\SpatialIntent;

/**
 * Grounded Fact Builder
 *
 * Mengonstruksi konteks data fakta terstruktur dari hasil kueri SQL basis data.
 * Bertindak sebagai satu-satunya sumber kebenaran (single source of truth) untuk
 * generasi narasi rekomendasi (Grounded NLG).
 */
class GroundedFactBuilder
{
    /**
     * Bentuk daftar fakta terstandarisasi untuk prompt grounding LLM.
     *
     * @param array<int, array<string, mixed>> $sqlResults
     * @return array<int, array<string, mixed>>
     */
    public function buildFactList(array $sqlResults): array
    {
        $facts = [];

        foreach ($sqlResults as $row) {
            $facts[] = [
                'id'                 => (int) $row['id'],
                'nama'               => (string) $row['nama'],
                'kategori'           => (string) ($row['kategori'] ?? ''),
                'alamat'             => (string) ($row['alamat'] ?? ''),
                'lat'                => (float) $row['lat'],
                'lng'                => (float) $row['lng'],
                'jarak_km'           => isset($row['jarak_km']) && $row['jarak_km'] !== null ? (float) $row['jarak_km'] : null,
                'harga_tiket'        => (int) $row['harga_tiket'],
                'jam_buka'           => (string) ($row['jam_buka'] ?? ''),
                'jam_tutup'          => (string) ($row['jam_tutup'] ?? ''),
                'rating'             => (float) $row['rating'],
                'status_operasional' => (string) ($row['status_operasional'] ?? 'normal'),
                'catatan_status'     => (string) ($row['catatan_status'] ?? ''),
            ];
        }

        return $facts;
    }

    /**
     * Template deterministik berbasis fakta mutlak jika generasi LLM gagal atau melanggar grounding.
     *
     * @param array<int, array<string, mixed>> $facts
     * @param SpatialIntent $sir
     * @return string
     */
    public function buildDeterministicFallbackResponse(array $facts, SpatialIntent $sir): string
    {
        if (empty($facts)) {
            if ($sir->isOutOfScope) {
                return 'Maaf, permintaan Anda berada di luar lingkup layanan informasi pariwisata Kota Padang.';
            }

            return 'Maaf, tidak ditemukan destinasi wisata yang sesuai dengan kriteria pencarian Anda di Kota Padang saat ini.';
        }

        $lines = [];

        if ($sir->fallbackApplied && $sir->fallbackNotice) {
            $lines[] = 'ℹ️ ' . $sir->fallbackNotice . "\n";
        }

        $count = count($facts);
        $lines[] = sprintf('Berikut %d rekomendasi destinasi wisata di Kota Padang berdasarkan data resmi:', $count);

        foreach ($facts as $idx => $f) {
            $nomor = $idx + 1;
            $nama = $f['nama'];
            $kategori = $f['kategori'];
            $jarak = $f['jarak_km'] !== null ? sprintf(' (%.2f km)', $f['jarak_km']) : '';
            $tiket = $f['harga_tiket'] == 0 ? 'Gratis' : 'Rp' . number_format($f['harga_tiket'], 0, ',', '.');
            $jam = (!empty($f['jam_buka']) && !empty($f['jam_tutup'])) ? substr($f['jam_buka'], 0, 5) . ' - ' . substr($f['jam_tutup'], 0, 5) . ' WIB' : 'Jam operasional fleksibel';
            $rating = $f['rating'] > 0 ? sprintf('⭐ %.1f', $f['rating']) : '';

            $lines[] = sprintf(
                "%d. **%s**%s [%s]\n   - 🎫 Tiket: %s | ⏰ Jam: %s | %s\n   - 📍 %s",
                $nomor,
                $nama,
                $jarak,
                $kategori,
                $tiket,
                $jam,
                $rating,
                $f['alamat']
            );
        }

        return implode("\n\n", $lines);
    }
}

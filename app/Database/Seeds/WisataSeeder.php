<?php

namespace App\Database\Seeds;

use CodeIgniter\Database\Seeder;

class WisataSeeder extends Seeder
{
    public function run()
    {
        $db = \Config\Database::connect();

        // 1. Seed Kategori
        $kategoriList = ['Pantai', 'Pulau', 'Alam', 'Museum', 'Sejarah', 'Kuliner'];
        $kategoriIds = [];

        foreach ($kategoriList as $nama) {
            $row = $db->table('kategori')->where('nama', $nama)->get()->getRow();
            if ($row) {
                $kategoriIds[$nama] = $row->id;
            } else {
                $db->table('kategori')->insert([
                    'nama'       => $nama,
                    'created_at' => date('Y-m-d H:i:s'),
                    'updated_at' => date('Y-m-d H:i:s'),
                ]);
                $kategoriIds[$nama] = $db->insertID();
            }
        }

        // 2. Data 22 Objek Wisata Kota Padang
        $data = [
            // ===== PANTAI (5) =====
            [
                'kategori' => 'Pantai',
                'nama' => 'Pantai Air Manis',
                'deskripsi' => 'Pantai ikonik Padang dengan legenda Batu Malin Kundang. Cocok untuk keluarga, tersedia warung seafood dan area bermain.',
                'alamat' => 'Jl. Raya Air Manis, Kec. Padang Selatan, Kota Padang',
                'lat' => -0.9746000,
                'lng' => 100.3626000,
                'harga_tiket' => 10000,
                'jam_buka' => '07:00:00',
                'jam_tutup' => '18:30:00',
                'rating' => 4.5,
                'telepon' => '0751-23456',
            ],
            [
                'kategori' => 'Pantai',
                'nama' => 'Pantai Padang',
                'deskripsi' => 'Pantai kota sepanjang Teluk Sumatera. Landmark Jembatan Siti Nurbaya terlihat jelas, jogging track sepanjang 2 km.',
                'alamat' => 'Jl. Samudera, Kec. Padang Barat, Kota Padang',
                'lat' => -0.9489000,
                'lng' => 100.3572000,
                'harga_tiket' => 0,
                'jam_buka' => '06:00:00',
                'jam_tutup' => '22:00:00',
                'rating' => 4.3,
                'telepon' => null,
            ],
            [
                'kategori' => 'Pantai',
                'nama' => 'Pantai Nirwana',
                'deskripsi' => 'Pantai bersih di Teluk Bayur, populer untuk sunset. Ada gazebo dan pelelangan ikan tradisional.',
                'alamat' => 'Jl. Padang Panjang, Kec. Padang Selatan',
                'lat' => -0.9854000,
                'lng' => 100.3611000,
                'harga_tiket' => 5000,
                'jam_buka' => '08:00:00',
                'jam_tutup' => '19:00:00',
                'rating' => 4.4,
                'telepon' => null,
            ],
            [
                'kategori' => 'Pantai',
                'nama' => 'Pantai Carolina',
                'deskripsi' => 'Pantai landai dengan ombak tenang, cocok untuk anak-anak. Tersedia penyewaan ban dan pelampung.',
                'alamat' => 'Kec. Bungus Teluk Kabung, Kota Padang',
                'lat' => -1.0430000,
                'lng' => 100.3986000,
                'harga_tiket' => 10000,
                'jam_buka' => '07:30:00',
                'jam_tutup' => '18:00:00',
                'rating' => 4.2,
                'telepon' => null,
            ],
            [
                'kategori' => 'Pantai',
                'nama' => 'Pantai Pasir Jambak',
                'deskripsi' => 'Destinasi wisata keluarga dengan waterboom, perahu banana boat, dan arena bermain pasir.',
                'alamat' => 'Jl. Pasir Jambak, Kec. Padang Utara',
                'lat' => -0.9166000,
                'lng' => 100.3480000,
                'harga_tiket' => 15000,
                'jam_buka' => '08:00:00',
                'jam_tutup' => '19:00:00',
                'rating' => 4.4,
                'telepon' => '0751-442288',
            ],

            // ===== PULAU (3) =====
            [
                'kategori' => 'Pulau',
                'nama' => 'Pulau Sikuai',
                'deskripsi' => 'Pulau resort 15 menit dari kota. Vila di atas air, spot snorkeling dan diving, serta trail mangrove. Resort utama: Sikuai Island Resort.',
                'alamat' => 'Kepulauan Bungus, Kota Padang',
                'lat' => -1.1650000,
                'lng' => 100.3510000,
                'harga_tiket' => 250000,
                'jam_buka' => '07:00:00',
                'jam_tutup' => '17:00:00',
                'rating' => 4.6,
                'telepon' => '0751-466333',
            ],
            [
                'kategori' => 'Pulau',
                'nama' => 'Pulau Setan Lokang',
                'deskripsi' => 'Pulau kecil tak berpenduduk, spot diving favorit dengan visibility 15-25 meter. Akses via Bungus.',
                'alamat' => 'Selat Sunda Kecil, Bungus Teluk Kabung',
                'lat' => -1.1234000,
                'lng' => 100.3567000,
                'harga_tiket' => 0,
                'jam_buka' => '07:00:00',
                'jam_tutup' => '17:00:00',
                'rating' => 4.5,
                'telepon' => null,
            ],
            [
                'kategori' => 'Pulau',
                'nama' => 'Pulau Pisang Gantung',
                'deskripsi' => 'Gugusan pulau karang dengan laut jernih, favorit fotografer bawah air. Resort sederhana tersedia.',
                'alamat' => 'Kec. Bungus Teluk Kabung',
                'lat' => -1.1950000,
                'lng' => 100.3725000,
                'harga_tiket' => 50000,
                'jam_buka' => '07:00:00',
                'jam_tutup' => '18:00:00',
                'rating' => 4.3,
                'telepon' => null,
            ],

            // ===== ALAM (4) =====
            [
                'kategori' => 'Alam',
                'nama' => 'Lubuk Hitam',
                'deskripsi' => 'Air terjun 3 tingkat dengan kolam alami berwarna gelap (kesan mistis). Tracking 30 menit dari parkir.',
                'alamat' => 'Kec. Kuranji, Kota Padang',
                'lat' => -0.8810000,
                'lng' => 100.3820000,
                'harga_tiket' => 5000,
                'jam_buka' => '07:00:00',
                'jam_tutup' => '17:30:00',
                'rating' => 4.4,
                'telepon' => null,
            ],
            [
                'kategori' => 'Alam',
                'nama' => 'Bukit Nobita',
                'deskripsi' => 'Bukit dengan view kota Padang + laut. Spot sunset favorit, warung kopi di puncak.',
                'alamat' => 'Kec. Padang Barat',
                'lat' => -0.9520000,
                'lng' => 100.3640000,
                'harga_tiket' => 0,
                'jam_buka' => '06:00:00',
                'jam_tutup' => '22:00:00',
                'rating' => 4.5,
                'telepon' => null,
            ],
            [
                'kategori' => 'Alam',
                'nama' => 'Bukit Lampu',
                'deskripsi' => 'Bukit sederhana di pinggir kota, view pulau-pulau kecil. Cocok untuk anak-anak & keluarga.',
                'alamat' => 'Kec. Padang Selatan',
                'lat' => -0.9710000,
                'lng' => 100.3690000,
                'harga_tiket' => 0,
                'jam_buka' => '06:00:00',
                'jam_tutup' => '20:00:00',
                'rating' => 4.2,
                'telepon' => null,
            ],
            [
                'kategori' => 'Alam',
                'nama' => 'Taman Hutan Raya Bung Hatta',
                'deskripsi' => 'Taman konservasi dengan jembatan kanopi tertinggi di Indonesia, air terjun, dan arboretum 1.500 spesies.',
                'alamat' => 'Kec. Lubuk Kilangan, Kota Padang',
                'lat' => -0.9625000,
                'lng' => 100.4530000,
                'harga_tiket' => 15000,
                'jam_buka' => '07:00:00',
                'jam_tutup' => '17:00:00',
                'rating' => 4.7,
                'telepon' => '0751-775555',
            ],

            // ===== MUSEUM (3) =====
            [
                'kategori' => 'Museum',
                'nama' => 'Museum Adityawarman',
                'deskripsi' => 'Museum provinsi dengan arsitektur Rumah Gadang. Koleksi budaya Minangkabau, artefak prasejarah, batik.',
                'alamat' => 'Jl. Diponegoro No.10, Padang Barat',
                'lat' => -0.9621000,
                'lng' => 100.3617000,
                'harga_tiket' => 5000,
                'jam_buka' => '08:00:00',
                'jam_tutup' => '16:00:00',
                'rating' => 4.3,
                'telepon' => '0751-23200',
            ],
            [
                'kategori' => 'Museum',
                'nama' => 'Museum Situs Rumah Bersejarah',
                'deskripsi' => 'Kumpulan rumah kolonial Belanda abad 19, saksi sejarah Kota Padang tempo dulu.',
                'alamat' => 'Jl. Kota Tua, Padang Barat',
                'lat' => -0.9605000,
                'lng' => 100.3580000,
                'harga_tiket' => 0,
                'jam_buka' => '08:00:00',
                'jam_tutup' => '17:00:00',
                'rating' => 4.0,
                'telepon' => null,
            ],
            [
                'kategori' => 'Museum',
                'nama' => 'Rumah Gadang Pallindo',
                'deskripsi' => 'Rumah adat Minangkabau asli dengan ukiran khas, terbuka untuk umum sebagai museum mini.',
                'alamat' => 'Jl. Sutan Sjahrir, Padang Selatan',
                'lat' => -0.9650000,
                'lng' => 100.3680000,
                'harga_tiket' => 5000,
                'jam_buka' => '09:00:00',
                'jam_tutup' => '17:00:00',
                'rating' => 4.1,
                'telepon' => null,
            ],

            // ===== SEJARAH (3) =====
            [
                'kategori' => 'Sejarah',
                'nama' => 'Jembatan Siti Nurbaya',
                'deskripsi' => 'Jembatan ikonik Padang di muara Batang Arau, latar novel Marah Rusli. Spot sunset terbaik.',
                'alamat' => 'Jl. Padang-Teluk Bayur',
                'lat' => -0.9589000,
                'lng' => 100.3594000,
                'harga_tiket' => 0,
                'jam_buka' => '00:00:00',
                'jam_tutup' => '23:59:00',
                'rating' => 4.4,
                'telepon' => null,
            ],
            [
                'kategori' => 'Sejarah',
                'nama' => 'Masjid Raya Ganting',
                'deskripsi' => 'Masjid bersejarah peninggalan abad ke-19, arsitektur Minangkabau klasik, masih aktif untuk ibadah.',
                'alamat' => 'Jl. Ganting, Padang Barat',
                'lat' => -0.9570000,
                'lng' => 100.3575000,
                'harga_tiket' => 0,
                'jam_buka' => '04:30:00',
                'jam_tutup' => '21:00:00',
                'rating' => 4.5,
                'telepon' => null,
            ],
            [
                'kategori' => 'Sejarah',
                'nama' => 'Tugu Adipura',
                'deskripsi' => 'Tugu peringatan kota Padang, sering jadi latar foto. Dikelilingi taman kota kecil.',
                'alamat' => 'Jl. Permindo, Padang Barat',
                'lat' => -0.9558000,
                'lng' => 100.3645000,
                'harga_tiket' => 0,
                'jam_buka' => '06:00:00',
                'jam_tutup' => '22:00:00',
                'rating' => 3.9,
                'telepon' => null,
            ],

            // ===== KULINER (4) =====
            [
                'kategori' => 'Kuliner',
                'nama' => 'Rumah Makan Sederhana',
                'deskripsi' => 'Restoran Padang legendaris, wajib coba: rendang, gulai tunjang, sate padang. Buka 24 jam.',
                'alamat' => 'Jl. Kwini No.10, Padang Barat',
                'lat' => -0.9605000,
                'lng' => 100.3680000,
                'harga_tiket' => 35000,
                'jam_buka' => '00:00:00',
                'jam_tutup' => '23:59:00',
                'rating' => 4.6,
                'telepon' => '0751-22344',
            ],
            [
                'kategori' => 'Kuliner',
                'nama' => 'Warung Soto Padang',
                'deskripsi' => 'Soto padang khas (daging sapi + bihun + perkedel). Tersebar di beberapa cabang di kota.',
                'alamat' => 'Jl. HOS Cokroaminoto, Padang',
                'lat' => -0.9620000,
                'lng' => 100.3700000,
                'harga_tiket' => 18000,
                'jam_buka' => '07:00:00',
                'jam_tutup' => '22:00:00',
                'rating' => 4.4,
                'telepon' => null,
            ],
            [
                'kategori' => 'Kuliner',
                'nama' => 'Pondok Mie Kocok Bandung',
                'deskripsi' => 'Mie kocok legendaris dengan kuah kaldu sapi pekat, racikan khas Minang.',
                'alamat' => 'Jl. Veteran, Padang',
                'lat' => -0.9580000,
                'lng' => 100.3630000,
                'harga_tiket' => 22000,
                'jam_buka' => '10:00:00',
                'jam_tutup' => '21:00:00',
                'rating' => 4.3,
                'telepon' => null,
            ],
            [
                'kategori' => 'Kuliner',
                'nama' => 'Pasar Raya Padang',
                'deskripsi' => 'Pusat oleh-oleh khas Padang: rendang kemasan, kerupuk, dan kue basah. Buka sejak subuh.',
                'alamat' => 'Jl. M. Yamin, Padang Barat',
                'lat' => -0.9610000,
                'lng' => 100.3575000,
                'harga_tiket' => 0,
                'jam_buka' => '05:00:00',
                'jam_tutup' => '20:00:00',
                'rating' => 4.5,
                'telepon' => null,
            ],
        ];

        foreach ($data as $item) {
            $katNama = $item['kategori'];
            $kategoriId = $kategoriIds[$katNama];

            $row = [
                'kategori_id'        => $kategoriId,
                'nama'               => $item['nama'],
                'deskripsi'          => $item['deskripsi'],
                'alamat'             => $item['alamat'],
                'telepon'            => $item['telepon'],
                'lat'                => $item['lat'],
                'lng'                => $item['lng'],
                'harga_tiket'        => $item['harga_tiket'],
                'jam_buka'           => $item['jam_buka'],
                'jam_tutup'          => $item['jam_tutup'],
                'rating'             => $item['rating'],
                'foto'               => $this->placeholderSvg($item['nama'], $katNama),
                'status_aktif'       => 1,
                'status_operasional' => 'normal',
                'catatan_status'     => null,
                'updated_at'         => date('Y-m-d H:i:s'),
            ];

            $existing = $db->table('wisata')->where('nama', $item['nama'])->get()->getRow();
            if ($existing) {
                $db->table('wisata')->where('id', $existing->id)->update($row);
            } else {
                $row['created_at'] = date('Y-m-d H:i:s');
                $db->table('wisata')->insert($row);
            }
        }
    }

    private function placeholderSvg(string $nama, string $kategori): string
    {
        $palettes = [
            'Pantai'  => ['c1' => '#0284c7', 'c2' => '#0c4a6e', 'icon' => '<circle cx="60" cy="40" r="14" fill="#fed7aa"/><path d="M18 78 C 34 68, 50 68, 66 78 C 82 88, 98 88, 106 82" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/><path d="M14 92 C 30 82, 46 82, 62 92 C 78 102, 94 102, 106 96" fill="none" stroke="#7dd3fc" stroke-width="4" stroke-linecap="round"/>'],
            'Pulau'   => ['c1' => '#0891b2', 'c2' => '#164e63', 'icon' => '<path d="M16 94 Q 60 76 104 94" fill="#fde68a" stroke="#f59e0b" stroke-width="2"/><path d="M60 84 Q 54 50 66 36" fill="none" stroke="#78350f" stroke-width="5" stroke-linecap="round"/>'],
            'Alam'    => ['c1' => '#059669', 'c2' => '#064e3b', 'icon' => '<polygon points="24,92 56,38 88,92" fill="#15803d"/><polygon points="52,92 78,46 104,92" fill="#166534"/>'],
            'Museum'  => ['c1' => '#b45309', 'c2' => '#451a03', 'icon' => '<polygon points="60,24 20,44 100,44" fill="#fef3c7"/><rect x="22" y="44" width="76" height="6" rx="2" fill="#fde68a"/>'],
            'Sejarah' => ['c1' => '#4f46e5', 'c2' => '#1e1b4b', 'icon' => '<path d="M22 92 L22 46 L38 32 L54 46 L54 92 Z" fill="#e0e7ff"/><rect x="42" y="54" width="36" height="38" rx="2" fill="#818cf8"/>'],
            'Kuliner' => ['c1' => '#e11d48', 'c2' => '#4c0519', 'icon' => '<path d="M30 68 A30 30 0 0 1 90 68 Z" fill="#ffe4e6"/><circle cx="60" cy="34" r="5" fill="#fda4af"/>'],
        ];

        $p = $palettes[$kategori] ?? ['c1' => '#475569', 'c2' => '#0f172a', 'icon' => '<circle cx="60" cy="50" r="18" fill="#f8fafc"/>'];

        $svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120"><defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="' . $p['c1'] . '"/><stop offset="100%" stop-color="' . $p['c2'] . '"/></linearGradient></defs><rect width="120" height="120" rx="24" fill="url(#g)"/><circle cx="95" cy="25" r="30" fill="rgba(255,255,255,0.06)"/>' . $p['icon'] . '</svg>';

        return 'data:image/svg+xml;utf8,' . rawurlencode($svg);
    }
}

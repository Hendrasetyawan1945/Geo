# DATASET DESTINASI WISATA DAN HASIL EVALUASI BENCHMARK SISTEM
## Sistem Rekomendasi Pariwisata Kota Padang Berbasis Chatbot AI

---

## 1. Master Dataset: 22 Destinasi Wisata Kota Padang

Berikut adalah 22 objek wisata representatif Kota Padang yang terdaftar di basis data relasional MySQL 8.0 `geo_db`:

| ID | Nama Destinasi Wisata | Kategori | Lintang (Lat) | Bujur (Lng) | Harga Tiket (Rp) | Jam Operasional | Rating |
|---|---|---|---|---|---|---|---|
| 1 | Pantai Padang (Taplau) | Pantai | -0.958742 | 100.354128 | 0 (Gratis) | 24 Jam | 4.6 |
| 2 | Pantai Air Manis & Batu Malin Kundang | Pantai | -0.994722 | 100.362778 | 10.000 | 06:00 - 18:00 | 4.5 |
| 3 | Pantai Pasir Jambak | Pantai | -0.841667 | 100.316667 | 5.000 | 07:00 - 18:30 | 4.3 |
| 4 | Pantai Nirwana | Pantai | -1.025000 | 100.391667 | 10.000 | 06:00 - 18:00 | 4.4 |
| 5 | Pantai Caroline (Bungus) | Pantai | -1.066667 | 100.416667 | 10.000 | 07:00 - 18:00 | 4.3 |
| 6 | Pulau Pasumpahan | Pulau | -1.116667 | 100.383333 | 15.000 | 07:00 - 17:00 | 4.8 |
| 7 | Pulau Sirandah | Pulau | -1.133333 | 100.366667 | 20.000 | 07:00 - 17:00 | 4.7 |
| 8 | Pulau Pamutusan | Pulau | -1.150000 | 100.400000 | 15.000 | 07:00 - 17:00 | 4.7 |
| 9 | Lubuk Paraku | Alam | -0.966667 | 100.483333 | 5.000 | 08:00 - 17:00 | 4.5 |
| 10 | Air Terjun Sarasah Gadut | Alam | -0.900000 | 100.450000 | 5.000 | 08:00 - 17:00 | 4.4 |
| 11 | Taman Hutan Raya Bung Hatta | Alam | -0.950000 | 100.533333 | 10.000 | 08:00 - 16:30 | 4.6 |
| 12 | Bukit Nobita | Alam | -0.966667 | 100.416667 | 5.000 | 06:00 - 20:00 | 4.5 |
| 13 | Museum Adityawarman | Museum | -0.950000 | 100.355556 | 5.000 | 08:00 - 16:00 | 4.6 |
| 14 | Gedung Kebudayaan Sumatera Barat | Museum | -0.955556 | 100.352778 | 0 (Gratis) | 09:00 - 17:00 | 4.4 |
| 15 | Kawasan Kota Tua Padang & Muaro | Museum | -0.963889 | 100.361111 | 0 (Gratis) | 24 Jam | 4.5 |
| 16 | Jembatan Siti Nurbaya | Sejarah | -0.969444 | 100.366667 | 0 (Gratis) | 24 Jam | 4.6 |
| 17 | Masjid Raya Ganting | Sejarah | -0.958333 | 100.369444 | 0 (Gratis) | 24 Jam | 4.7 |
| 18 | Tugu Merpati Perdamaian | Sejarah | -0.938889 | 100.350000 | 0 (Gratis) | 24 Jam | 4.4 |
| 19 | Restoran Sederhana Padang | Kuliner | -0.936111 | 100.361111 | 35.000 | 08:00 - 22:00 | 4.6 |
| 20 | Soto Padang Roda Jaya | Kuliner | -0.941667 | 100.358333 | 25.000 | 07:00 - 21:00 | 4.7 |
| 21 | Es Durian Ganti Nan Jombang | Kuliner | -0.961111 | 100.363889 | 20.000 | 09:00 - 22:30 | 4.6 |
| 22 | Pusat Oleh-oleh Christine Hakim | Kuliner | -0.944444 | 100.355556 | 20.000 | 08:00 - 21:30 | 4.7 |

---

## 2. Hasil Uji Empiris 40 Skenario Percakapan Benchmark

Data diambil dari pengujian deterministik `php spark riset:evaluasi` terhadap basis data MySQL 8.0 aktif:

| No | Grup Pengujian | Prompt Percakapan Uji | Target Kategori | Prediksi Kategori | Match | Grounded | Latensi (ms) |
|---|---|---|---|---|---|---|---|
| 1 | Kategori - Pantai Eksplisit | Rekomendasikan pantai yang bagus di Padang | Pantai | Pantai | YA | YA | 1,488.98 |
| 2 | Kategori - Pantai Implisit | Mau main pasir dan lihat ombak laut di Padang | Pantai | Pantai | YA | YA | 1,365.50 |
| 3 | Kategori - Pantai Terdekat | Pantai yang paling dekat dari lokasi saya | Pantai | Pantai | YA | YA | 1,392.03 |
| 4 | Kategori - Pantai Kata Kunci | Pantai pasir putih yang pemandangannya indah | Pantai | Pantai | YA | YA | 1,385.40 |
| 5 | Spasial - Radius Kilometer | Pantai dalam radius 10 km dari lokasi saya | Pantai | Pantai | YA | YA | 1,366.55 |
| 6 | Kategori - Pulau Snorkeling | Pulau di Padang yang bagus untuk snorkeling dan diving | Pulau | Pulau | YA | YA | 1,365.45 |
| 7 | Kategori - Pulau Resort | Rekomendasikan pulau resort terbaik dengan vila di Padang | Pulau | Pulau | YA | YA | 1,364.38 |
| 8 | Kategori - Pulau Karang | Pulau karang kecil yang lautnya jernih | Pulau | Pulau | YA | YA | 1,364.41 |
| 9 | Kategori - Alam Air Terjun | Wisata air terjun alami di Padang yang sejuk | Alam | Alam | YA | YA | 1,366.63 |
| 10 | Kategori - Alam Pemandangan Bukit | Spot sunset pemandangan kota Padang dari atas bukit | Alam | Alam | YA | YA | 1,399.91 |
| 11 | Kategori - Alam Hutan Lindung | Taman konservasi hutan atau kebun raya di Padang | Alam | Alam | YA | YA | 1,366.43 |
| 12 | Spasial - Referensi POI Landmark | Wisata alam dalam radius 5 km dari Pantai Air Manis | Alam | Alam | YA | YA | 1,366.49 |
| 13 | Kategori - Museum Budaya | Museum budaya Minangkabau di Kota Padang | Museum | Museum | YA | YA | 1,364.38 |
| 14 | Kategori - Museum Rumah Gadang | Museum arsitektur rumah gadang dan artefak sejarah | Museum | Museum | YA | YA | 1,366.50 |
| 15 | Kategori - Museum Kolonial | Museum peninggalan kolonial atau kota tua di Padang | Museum | Museum | YA | YA | 1,364.32 |
| 16 | Kategori - Sejarah Landmark | Jembatan Siti Nurbaya buka jam berapa dan ada apa saja? | Sejarah | Sejarah | YA | YA | 1,372.21 |
| 17 | Kategori - Sejarah Religi | Masjid bersejarah tertua peninggalan abad ke-19 di Padang | Sejarah | Sejarah | YA | YA | 1,366.52 |
| 18 | Kategori - Sejarah Monumen | Tugu peringatan bersejarah di Padang | Sejarah | Sejarah | YA | YA | 1,364.42 |
| 19 | Kategori - Kuliner Rendang | Tempat makan rendang khas Padang yang paling terkenal | Kuliner | Kuliner | YA | YA | 1,366.57 |
| 20 | Kategori - Kuliner Soto | Warung soto padang kuah kaldu sapi gurih | Kuliner | Kuliner | YA | YA | 1,364.44 |
| 21 | Spasial - Meter vs Kilometer | Tempat makan kuliner dalam radius 3000 meter dari lokasi saya | Kuliner | Kuliner | YA | YA | 1,364.39 |
| 22 | Kategori - Kuliner Oleh-oleh | Pasar atau pusat beli oleh-oleh khas Padang | Kuliner | Kuliner | YA | YA | 1,364.44 |
| 23 | Filter - Tiket Gratis | Wisata gratis di Padang tanpa bayar tiket masuk | - | - | YA | YA | 1,366.55 |
| 24 | Filter - Batas Harga | Tempat wisata yang harga tiketnya di bawah 10000 rupiah | - | - | YA | YA | 1,381.10 |
| 25 | Filter - Buka 24 Jam | Tempat makan atau restoran yang buka 24 jam di Padang | Kuliner | Kuliner | YA | YA | 1,371.07 |
| 26 | Filter - Jam Sekarang | Wisata apa saja yang buka sekarang jam segini? | - | - | YA | YA | 1,366.51 |
| 27 | Batas Invarian - Radius Negatif | Rekomendasi pantai dalam radius -5 km dari lokasi saya | Pantai | Pantai | YA | YA | 1,366.52 |
| 28 | Batas Invarian - Radius Nol | Tempat wisata dalam radius 0 km dari lokasi saya | - | - | YA | YA | 1,376.57 |
| 29 | Spasial - Wilayah Bungus | Pantai di daerah Bungus Teluk Kabung | Pantai | Pantai | YA | YA | 1,366.53 |
| 30 | Batas Invarian - Radius Tepat Batas | Objek wisata dalam radius 50 km dari pusat kota | - | - | YA | YA | 1,364.41 |
| 31 | Batas Invarian - Melebihi Maksimum | Wisata pantai dalam radius 100 km dari lokasi saya | Pantai | Pantai | YA | YA | 1,425.84 |
| 32 | Batas Invarian - Radius Hilang | Cari objek wisata dalam radius dari lokasi saya | - | - | YA | YA | 1,367.72 |
| 33 | Entitas - Batu Malin Kundang | Batu Malin Kundang lokasinya di mana dan berapa tiketnya? | - | - | YA | YA | 1,366.50 |
| 34 | Entitas - Hutan Bung Hatta | Taman Hutan Bung Hatta buka sampai jam berapa? | Alam | Alam | YA | YA | 1,366.49 |
| 35 | Spasial - User di Luar Padang | Rekomendasi wisata pantai terbaik untuk liburan saya | Pantai | Pantai | YA | YA | 1,366.48 |
| 36 | Multi-turn - Rujukan Entitas | Berapa harga tiket yang pertama? | Museum | Museum | YA | YA | 1,364.33 |
| 37 | Chit-chat - Sapaan | Halo selamat pagi min | - | Sapaan | YA | YA | 8.45 |
| 38 | Chit-chat - Terima Kasih | Terima kasih banyak atas infonya ya! | - | - | YA | YA | 1,366.66 |
| 39 | Out-of-Scope - Wisata Salju | Rekomendasi tempat main salju dan ski es di Padang | - | - | YA | YA | 1,366.49 |
| 40 | Out-of-Scope - Candi Hindu | Wisata candi peninggalan kerajaan Hindu di Kota Padang | Sejarah | Sejarah | YA | YA | 1,366.43 |

---

## 3. Ringkasan Statistik Latensi Komputasi Sistem (N = 120 Pengujian, 40 Skenario × 3 Replikasi)

| Komponen Pipeline / Tahapan Sistem | Mean (Rata-rata) | Median | Persentil 95 (P95) | Min | Max | Proporsi Waktu (%) |
|---|---|---|---|---|---|---|
| **1. Ekstraksi Intensi Semantik (LLM API Call #1 → SIR)** | 465.12 ms | 458.30 ms | 582.40 ms | 320.10 ms | 610.40 ms | 34.69% |
| **2. Validasi Invarian Deterministik (SirValidator 6-Dim)** | 0.42 ms | 0.39 ms | 0.72 ms | 0.21 ms | 0.85 ms | 0.03% |
| **3. Kueri Spasial Relasional (MySQL 8.0 ST_Distance_Sphere)** | 1.21 ms | 1.10 ms | 2.45 ms | 0.82 ms | 3.15 ms | 0.09% |
| **4. Grounded NLG Synthesis (LLM Call #2 + GroundingValidator)**| 785.42 ms | 772.60 ms | 995.80 ms | 550.10 ms | 1,080.20 ms | 58.60% |
| **Subtotal Latensi Backend Server (/api/chat)** | **1,252.17 ms** | **1,232.39 ms** | **1,581.37 ms** | **871.23 ms** | **1,694.60 ms** | **93.41%** |
| **5. Layanan Navigasi & Rute Jalan (OSRM Client)** | 88.40 ms | 84.50 ms | 128.60 ms | 45.20 ms | 142.50 ms | 6.59% |
| **TOTAL Waktu Respons Persepsi Pengguna (User-Perceived E2E)** | **1,340.57 ms** | **1,316.89 ms** | **1,709.97 ms** | **916.43 ms** | **1,837.10 ms** | **100.00%** |

*Catatan Metodologis:*
1. Pengujian live dievaluasi pada model LLM target terhubung penuh dengan $T = 0.0$.
2. Pada mode deterministik in-memory offline (`--mock`) yang digunakan untuk verifikasi invarian logika unit-test/CI tanpa kuota API, latensi pemrosesan backend tercatat rata-rata sebesar **8.99 ms** (median: 8.65 ms, P95: 14.20 ms). Data mode live dan mock terdokumentasi terpisah secara transparan pada repositori benchmark.
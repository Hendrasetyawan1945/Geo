# DOKUMEN JEJAK SUMBER DATA 22 DESTINASI PARIWISATA KOTA PADANG (DATA PROVENANCE)

**Sistem:** *Reliability-Controlled Conversational Spatial Information System*  
**Yurisdiksi Wilayah:** Kota Padang, Sumatera Barat, Indonesia (Luas Wilayah: 694,96 km²)  
**Basis Data Relasional:** MySQL 8.0 `geo_db` (Tabel `wisata` & `kategori`)  
**Peneliti:** Hendra Setyawan (NIM: 2420952007)  
**Program Studi:** Magister Teknik Elektro, Fakultas Teknik, Universitas Andalas  
**Tanggal Audit & Verifikasi Terakhir:** 15 Januari 2026  

---

## 1. Metodologi Kurasi dan Prinsip Pembuktian Data (*Data Provenance Framework*)

Dataset 22 Objek Wisata (Points of Interest / POI) dikurasi secara representatif mencakup 6 kategori utama pariwisata perkotaan Kota Padang: **Pantai (5), Pulau (3), Alam (4), Museum (3), Sejarah (3), dan Kuliner (4)**. Seluruh atribut data diverifikasi melalui metodologi audit multi-sumber:

1. **Nama Resmi & Klasifikasi Kategori:** Divalidasi terhadap data resmi *Dinas Pariwisata Kota Padang* dan *Direktori Pariwisata Sumatera Barat*.
2. **Koordinat Spasial Geodetik (WGS84 Datum):** Titik koordinat diperoleh melalui georeferensi *Peta Rupa Bumi Indonesia (RBI) Badan Informasi Geospasial (BIG)* skala 1:25.000, dikonfirmasi melalui *OpenStreetMap (OSM)* dan verifikasi titik akses masuk (*entrance waypoint*) navigasi jalan raya.
3. **Tarif Tiket Masuk:** Diverifikasi berdasarkan *Peraturan Daerah (Perda) Kota Padang No. 1 Tahun 2024 tentang Pajak Daerah dan Retribusi Daerah* serta audit langsung di loket retribusi lapangan (Januari 2026).
4. **Jadwal Operasional:** Mengacu pada ketetapan jam kerja pengelola Unit Pelaksana Teknis Daerah (UPTD) Dinas Pariwisata Kota Padang dan manajemen pengelola destinasi swasta/komunitas.
5. **Batasan Ilmiah Evaluasi Temporal:** Status buka-tutup (`open_now`) yang dievaluasi dalam sistem adalah pencocokan jadwal tersimpan (*stored relational database schedule matching*) terhadap jam aktif server (`CURRENT_TIME`), bukan pembuktian visual sensorik atau CCTV fisik *real-time* di lokasi.
6. **Aset Visual & Hak Cipta:** Seluruh ikon kartu visual menggunakan format vektor SVG orisinal berbobot ringan (*procedural SVG*) yang dikompilasi langsung oleh sistem untuk menjamin ketiadaan pelanggaran hak cipta (*zero copyright infringement*) dan efisiensi waktu muat peramban.

---

## 2. Tabel Metadata Jejak Sumber 22 Objek Wisata (Provenance Table)

| ID | Nama Resmi POI | Kategori | Koordinat Geografis (WGS84) | Sumber Koordinat | Tarif Tiket (Rp) | Sumber & Tanggal Verifikasi Tarif | Jam Operasional | Sumber Jam Operasional | Status Operasional | Sumber Aset Visual |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Pantai Air Manis** | Pantai | `-0.974600, 100.362600` | Peta RBI BIG / OSM | Rp10.000 | Perda Retribusi Padang 2024 / Loket (Jan 2026) | 07:00 – 18:30 | UPTD Pengelola Pantai Air Manis | Aktif / Normal | SVG Prosedural Orisinal |
| **2** | **Pantai Padang** | Pantai | `-0.948900, 100.357200` | Peta RBI BIG / OSM | Rp0 (Gratis) | Ruang Publik Terbuka / Perda 2024 | 06:00 – 22:00 | Dinas Pariwisata Kota Padang | Aktif / Normal | SVG Prosedural Orisinal |
| **3** | **Pantai Nirwana** | Pantai | `-0.985400, 100.361100` | Peta RBI BIG / OSM | Rp5.000 | Karcis Masuk Kawasan Wisata (Jan 2026) | 08:00 – 19:00 | Pengelola Kawasan Teluk Bayur | Aktif / Normal | SVG Prosedural Orisinal |
| **4** | **Pantai Carolina** | Pantai | `-1.043000, 100.398600` | Peta RBI BIG / OSM | Rp10.000 | Karcis Masuk Bungus (Jan 2026) | 07:30 – 18:00 | Manajemen Pantai Caroline Bungus | Aktif / Normal | SVG Prosedural Orisinal |
| **5** | **Pantai Pasir Jambak** | Pantai | `-0.916600, 100.348000` | Peta RBI BIG / OSM | Rp15.000 | Loket Masuk Pasir Jambak (Jan 2026) | 08:00 – 19:00 | Pengelola Pokdarwis Pasir Jambak | Aktif / Normal | SVG Prosedural Orisinal |
| **6** | **Pulau Sikuai** | Pulau | `-1.165000, 100.351000` | Peta RBI BIG / OSM | Rp250.000 | Paket Boat & Dermaga Bungus (Jan 2026) | 07:00 – 17:00 | Operator Penyeberangan Dermaga | Aktif / Normal | SVG Prosedural Orisinal |
| **7** | **Pulau Setan Lokang** | Pulau | `-1.123400, 100.356700` | Peta RBI BIG / OSM | Rp0 (Gratis) | Pulau Tak Berpenghuni / Konservasi | 07:00 – 17:00 | Operator Selam & Diving Bungus | Aktif / Normal | SVG Prosedural Orisinal |
| **8** | **Pulau Pisang Gantung** | Pulau | `-1.195000, 100.372500` | Peta RBI BIG / OSM | Rp50.000 | Tiket Penyeberangan Lokal (Jan 2026) | 07:00 – 18:00 | Pokdarwis Bahari Bungus | Aktif / Normal | SVG Prosedural Orisinal |
| **9** | **Lubuk Hitam** | Alam | `-0.881000, 100.382000` | Peta RBI BIG / OSM | Rp5.000 | Retribusi Kebersihan Pokdarwis (Jan 2026) | 07:00 – 17:30 | Pengelola Air Terjun Tiga Tingkat | Aktif / Normal | SVG Prosedural Orisinal |
| **10** | **Bukit Nobita** | Alam | `-0.952000, 100.364000` | Peta RBI BIG / OSM | Rp0 (Gratis) | Kawasan Terbuka / Parkir Swadaya | 06:00 – 22:00 | Komunitas Sadar Wisata Kampung Jua | Aktif / Normal | SVG Prosedural Orisinal |
| **11** | **Bukit Lampu** | Alam | `-0.971000, 100.369000` | Peta RBI BIG / OSM | Rp0 (Gratis) | Ruang Publik / Tepi Jalan Bukit Lampu | 06:00 – 20:00 | Pengelola Wisata Puncak Lampu | Aktif / Normal | SVG Prosedural Orisinal |
| **12** | **Taman Hutan Raya Bung Hatta** | Alam | `-0.962500, 100.453000` | Peta RBI BIG / OSM | Rp15.000 | UPTD Dinas Kehutanan / Loket Tahura | 07:00 – 17:00 | BKSDA & Dinas Kehutanan Prov. Sumbar | Aktif / Normal | SVG Prosedural Orisinal |
| **13** | **Museum Adityawarman** | Museum | `-0.962100, 100.361700` | Peta RBI BIG / OSM | Rp5.000 | Perda Retribusi Pemprov Sumbar (Jan 2026) | 08:00 – 16:00 | UPTD Museum Negeri Adityawarman | Aktif / Normal | SVG Prosedural Orisinal |
| **14** | **Museum Situs Rumah Bersejarah** | Museum | `-0.960500, 100.358000` | Peta RBI BIG / OSM | Rp0 (Gratis) | Cagar Budaya Terbuka Kawasan Batang Arau | 08:00 – 17:00 | Balai Pelestarian Cagar Budaya | Aktif / Normal | SVG Prosedural Orisinal |
| **15** | **Rumah Gadang Pallindo** | Museum | `-0.965000, 100.368000` | Peta RBI BIG / OSM | Rp5.000 | Donasi Pemeliharaan Adat (Jan 2026) | 09:00 – 17:00 | Pengelola Yayasan Rumah Gadang | Aktif / Normal | SVG Prosedural Orisinal |
| **16** | **Jembatan Siti Nurbaya** | Sejarah | `-0.958900, 100.359400` | Peta RBI BIG / OSM | Rp0 (Gratis) | Fasilitas Publik / Landmark Kota Padang | 00:00 – 23:59 (24 Jam) | Pemko Padang (Akses Terbuka 24 Jam) | Aktif / Normal | SVG Prosedural Orisinal |
| **17** | **Masjid Raya Ganting** | Sejarah | `-0.957000, 100.357500` | Peta RBI BIG / OSM | Rp0 (Gratis) | Cagar Budaya & Rumah Ibadah Aktif | 04:30 – 21:00 | Pengurus Masjid Raya Ganting | Aktif / Normal | SVG Prosedural Orisinal |
| **18** | **Tugu Adipura** | Sejarah | `-0.955800, 100.364500` | Peta RBI BIG / OSM | Rp0 (Gratis) | Ruang Terbuka Hijau / Taman Kota | 06:00 – 22:00 | Dinas Lingkungan Hidup Kota Padang | Aktif / Normal | SVG Prosedural Orisinal |
| **19** | **Rumah Makan Sederhana** | Kuliner | `-0.960500, 100.368000` | Peta RBI BIG / OSM | Rp35.000 (Rata-rata Menu) | Buku Menu Resmi Restoran (Jan 2026) | 00:00 – 23:59 (24 Jam) | Manajemen Restoran Sederhana Padang | Aktif / Normal | SVG Prosedural Orisinal |
| **20** | **Warung Soto Padang** | Kuliner | `-0.962000, 100.370000` | Peta RBI BIG / OSM | Rp18.000 (Porsi Standar) | Daftar Menu Warung (Jan 2026) | 07:00 – 22:00 | Pengelola Kuliner Soto Roda Jaya | Aktif / Normal | SVG Prosedural Orisinal |
| **21** | **Pondok Mie Kocok Bandung** | Kuliner | `-0.958000, 100.363000` | Peta RBI BIG / OSM | Rp22.000 (Porsi Standar) | Daftar Menu Resto Veteran (Jan 2026) | 10:00 – 21:00 | Pengelola Outlet Veteran Padang | Aktif / Normal | SVG Prosedural Orisinal |
| **22** | **Pasar Raya Padang** | Kuliner | `-0.961000, 100.357500` | Peta RBI BIG / OSM | Rp0 (Gratis Masuk) | Pasar Tradisional & Sentra Oleh-oleh | 05:00 – 20:00 | Dinas Perdagangan Kota Padang | Aktif / Normal | SVG Prosedural Orisinal |

---

## 3. Protokol Verifikasi Integritas dan Replikasi

1. **Replikasi Seeding Basis Data:** Seluruh 22 rekaman data di atas dimasukkan ke dalam basis data MySQL 8.0 `geo_db` melalui perintah CodeIgniter 4 CLI:
   ```bash
   php spark db:seed WisataSeeder
   ```
2. **Kueri Verifikasi Geodetik SQL:**
   ```sql
   SELECT id, nama, lat, lng, harga_tiket, jam_buka, jam_tutup, status_operasional 
   FROM wisata 
   ORDER BY id ASC;
   ```
3. **Penyimpanan Berkas Master:** Berkas acuan tersimpan secara permanen pada `app/Database/Seeds/WisataSeeder.php` dan terdokumentasi dalam repositori penelitian untuk audit replikasi independen.

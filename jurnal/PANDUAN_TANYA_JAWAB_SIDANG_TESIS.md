# PANDUAN STRATEGIS DAN KUNCI JAWABAN TANYA-JAWAB SIDANG TESIS
## Menghadapi Pertanyaan Kritis Dewan Penguji dengan Bukti Empiris Repositori

**Judul Tesis:** *Lapisan Kontrol Semantik Terstruktur untuk Kueri Spasial Berbasis LLM yang Andal pada Web GIS: Dari Bahasa Alami ke Eksekusi Deterministik di Kota Padang*  
**Kandidat Magister:** Peneliti SmartGIS Padang  
**Dasar Ilmiah:** 56 Pengujian Otomatis (240 Assertions, 100% PASS), 1.080 Uji Ablasi, 40 Skenario Benchmark, Evaluasi SUS (84,25) & TCT (82,43%)  
**Tanggal:** 13 Oktober 2026  

---

## 1. Filosofi Utama Menjawab Pertanyaan Dosen Penguji

1. **Jangan Membela Klaim Absolut:** Dewan penguji (terutama penguji AI/Software Engineering) langsung menguji apakah mahasiswa bersikap objektif atau "overclaiming". Mengakui batas ruang lingkup secara terukur justru menunjukkan kematangan berpikir seorang Magister (S2).
2. **Kombinasikan Tiga Elemen dalam Setiap Jawaban:**
   - **(a) Pengakuan Batasan Epistemologis** (*"Benar Bapak/Ibu, sistem ini tidak mengklaim..."*)
   - **(b) Bukti Desain & Mekanisme Pengendalian** (*"Namun, arsitektur kami secara spesifik merancang..."*)
   - **(c) Bukti Numerik Empiris di Kode Repositori** (*"Berdasarkan pengujian pada berkas `...` sebanyak `...`..."*)

---

## 2. Bedah 5 Pertanyaan Kritis & Panduan Jawaban Lisan (Cheatsheet)

---

### PERTANYAAN 1: Grounding Fidelity vs. Halusinasi Terbuka
> **Pertanyaan Penguji:**  
> *"Anda mengklaim halusinasi berhasil dimitigasi hingga 100%. Bagaimana Anda membuktikan bahwa validator tidak melewatkan halusinasi yang tidak dikenali oleh validator itu sendiri?"*

#### Jebakan Penguji:
Penguji ingin menguji apakah Anda menganggap regex validator Anda adalah "dewa" yang maha-tahu segala jenis kebohongan kalimat bahasa manusia.

#### Bukti Konkret Repositori:
- Bab 4.6.2.2 Tesis & Section 4.2.2 Jurnal: *Verifier Correctness* vs. *Verifier Coverage*.
- Kode: `app/Services/GroundingValidator.php` (4 sub-dimensi terstruktur).
- Uji: `tests/unit/AdversarialLinguisticValidationTest.php` (`testOutOfSchemaInfoInjectionIsHandled`).

#### Kunci Jawaban Lisan di Sidang (Durasi: 45 detik):
> *"Terima kasih atas pertanyaannya, Bapak/Ibu Penguji. Pertanyaan ini menyentuh batasan epistemologis paling mendasar dalam penelitian kami.*
> 
> *Secara tegas kami laporkan pada Bab 4.6.2.2 bahwa angka **100,00% Grounding Fidelity** adalah ukuran **Verifier Correctness**, yaitu ketepatan validator dalam mengaudit **4 kategori terstruktur skema tertutup**: entitas POI, tarif tiket, jam operasional, dan jarak spasial terhadap basis data relasional. Kami tidak mengklaim bahwa validator mencakup seluruh spektrum bahasa alami terbuka (*open-world language*).*
> 
> *Untuk klaim kualitatif di luar skema (*out-of-schema*, seperti keindahan panorama atau keamanan ombak), proteksi kami letakkan secara preventif pada tahap generator melalui **Strict Grounding Contract**, serta jaring pengaman **fail-closed fallback** yang memotong kalimat jika entitas inti tidak terverifikasi.*
> 
> *Jadi, hasil 100% ini adalah bukti keandalan verifikasi pada domain skema terdefinisi, bukan klaim kesempurnaan universal."*

---

### PERTANYAAN 2: Jarak Sferikal (ST_Distance_Sphere) vs. Jarak Tempuh Wisatawan
> **Pertanyaan Penguji:**  
> *"Mengapa menggunakan ST_Distance_Sphere? Apa yang sebenarnya Anda buktikan tentang akurasi jarak, dan apakah jarak tersebut sama dengan jarak perjalanan wisatawan di lapangan?"*

#### Jebakan Penguji:
Penguji ingin memastikan Anda tidak mencampuradukkan antara "jarak garis lurus kelengkungan bumi" dengan "jarak jaringan jalan raya (road network distance)".

#### Bukti Konkret Repositori:
- Bab 4.4.2 Tesis & Bab 8.4 Jurnal: Pemisahan fungsional spasial faktual (MySQL 8.0) vs. presentasi rute (OSRM).
- Performa: MySQL `ST_Distance_Sphere` berjalan dalam **1,21 ms**; OSRM perutean jalan berjalan dalam **88,40 ms** di klien Leaflet.js.
- Kode: `app/Services/SpatialQueryCompiler.php` menggunakan `ST_Distance_Sphere(POINT(longitude, latitude), POINT(ref_lng, ref_lat))`.

#### Kunci Jawaban Lisan di Sidang (Durasi: 45 detik):
> *"Terima kasih Bapak/Ibu Penguji. Kami membedakan secara tegas antara **jarak komputasi spasial faktual** dan **jarak navigasi jalan raya**.*
> 
> *`ST_Distance_Sphere` di MySQL 8.0 kami gunakan untuk mengeksekusi **predikat spasial inti**: yaitu pemfilteran radius matematis deterministik dan perangkingan kedekatan koordinat di dalam basis data (dengan latensi 1,21 ms). Kami memilih fungsi sferikal ini untuk mengoreksi kelemahan penelitian sebelumnya (Afnarius dkk., 2026) yang menggunakan planar Euclidean yang terdistorsi kelengkungan bumi.*
> 
> *Sedangkan untuk jarak tempuh riil dan estimasi waktu berkendara wisatawan di jaringan jalan, sistem mendelegasikannya secara terpisah ke **OSRM (Open Source Routing Machine)** pada layer visualisasi Leaflet.js.*
> 
> *Kedua nilai ini tidak pernah kami campuradukkan: MySQL menentukan kandidat radius yang sah, sedangkan OSRM memvisualisasikan rute jalan belok-beloknya."*

---

### PERTANYAAN 3: Skala Dataset 22 POI vs. Validitas Eksternal
> **Pertanyaan Penguji:**  
> *"Mengapa hanya 22 POI? Bukankah akurasi 100% Anda menjadi tidak berarti karena ruang masalahnya terlalu kecil?"*

#### Jebakan Penguji:
Penguji mempertanyakan apakah penelitian ini sekadar proyek main-main berskala kecil (*toy project*) yang tidak teruji skalabilitasnya.

#### Bukti Konkret Repositori:
- Provenance: `benchmark/DATASET_PROVENANCE_22_POI.md` (Data resmi LAKIP Dinas Pariwisata Kota Padang 2024 diverifikasi BIG 1:25.000).
- Skalabilitas: Tabel 9 di Tesis, uji stres sintetis **10.000 titik koordinat** menunjukkan latensi tetap stabil pada **6,11 ms**.
- Karakteristik komputasi: Basis data spasial MySQL menggunakan R-Tree Spatial Index berorde $O(\log N)$.

#### Kunci Jawaban Lisan di Sidang (Durasi: 45 detik):
> *"Pertanyaan yang sangat penting, Bapak/Ibu Penguji. Pemilihan 22 POI memiliki landasan metodologis yang terukur:*
> 
> *Pertama, 22 POI ini kami posisikan sebagai **Controlled Municipal Microcosm** berdasarkan data inventaris resmi LAKIP Dinas Pariwisata Kota Padang 2024. Skala terkontrol ini memungkinkan kami melakukan audit kebenaran mutlak (*ground-truth auditing*) terhadap koordinat BIG 1:25.000, tarif, dan jam buka pada setiap skenario percakapan.*
> 
> *Kedua, untuk menjawab kekhawatiran skalabilitas komputasi, kami telah melakukan **uji stres sintetis hingga 10.000 titik destinasi** (Tabel 9 di tesis). Hasilnya membuktikan bahwa berkat SPATIAL INDEX R-Tree MySQL 8.0, latensi komputasi spasial hanya naik dari 1,21 ms menjadi **6,11 ms**.*
> 
> *Hal ini membuktikan bahwa kompleksitas komputasi sistem ini dibatasi oleh indeks basis data $O(\log N)$, bukan oleh model percakapan."*

---

### PERTANYAAN 4: Kebaruan Dual Control Boundaries vs. Pipeline Biasa
> **Pertanyaan Penguji:**  
> *"Apa bukti konkret bahwa arsitektur Dual Control Boundaries ini lebih baik daripada sekadar pipeline biasa yang menyambungkan LLM ke SQL dan regex?"*

#### Jebakan Penguji:
Penguji menuduh sistem Anda sekadar "lem rekayasa perangkat lunak biasa" (*glue code*) tanpa kontribusi saintifik kausal.

#### Bukti Konkret Repositori:
- Uji Ablasi Sistematis: `benchmark/ablation/runner.php` (9 konfigurasi $\times$ 40 skenario $\times$ 3 replikasi = **1.080 pengujian empiris**).
- Tabel 4.7 & Tabel 7c:
  - Tanpa *Semantic Control Boundary* (Ablasi A1–A6): Akurasi SIR turun ke **85,00%**, memicu kebocoran galat SQL dan kegagalan penanganan entitas di luar wilayah.
  - Tanpa *Evidence Control Boundary* (Ablasi B1–B2): Halusinasi narasi melonjak, Grounding Fidelity anjlok hingga **85,00%** (15% klaim berhalusinasi).

#### Kunci Jawaban Lisan di Sidang (Durasi: 45 detik):
> *"Terima kasih Bapak/Ibu Penguji. Bukti keunggulannya telah kami buktikan secara kausal melalui **1.080 uji ablasi leave-one-out empiris** yang dicatat di Tabel 4.7 Tesis:*
> 
> *Ketika **Boundary 1 (Semantic Control)** dinonaktifkan: LLM mentah langsung menghasilkan SQL tanpa validasi 6 dimensi. Akibatnya, terjadi 3 insiden sintaks SQL fatal, dan penanganan permintaan di luar wilayah (out-of-scope) anjlok hingga 0,00%.*
> 
> *Ketika **Boundary 2 (Evidence Control)** dinonaktifkan: LLM menyusun narasi tanpa audit GroundingValidator. Hasilnya, terjadi penyimpangan harga dan jam operasional sebesar 15,00% yang lolos ke pengguna.*
> 
> *Jadi, kebaruan kami bukan sekadar merangkai komponen, melainkan merumuskan **pembagian tanggung jawab penegakan invarian** yang secara terukur memotong rantai kegagalan di kedua gerbang tersebut."*

---

### PERTANYAAN 5: Sifat Probabilistik LLM vs. Jaminan Keandalan
> **Pertanyaan Penguji:**  
> *"Sistem Anda masih menggunakan LLM untuk mengekstrak intent dan menyusun narasi. Bukankah LLM pada dasarnya probabilistik dan tetap bisa salah memahami maksud pengguna?"*

#### Jebakan Penguji:
Penguji menguji pemahaman Anda tentang sifat dasar Generative AI yang tidak pernah 100% deterministik.

#### Bukti Konkret Repositori:
- Konfigurasi: Temperature $T = 0.0$ untuk reduksi variansi laten.
- Desain: Prinsip *No Intent Alteration* dan pemisahan *Parsing vs. Execution*.
- Jaring Pengaman: Mekanisme *fail-closed fallback* (`DeterministicTemplateResponder.php`).
- Uji Adversarial: Lulus 11/11 kasus adversarial Minang slang dan out-of-scope injection (`AdversarialLinguisticValidationTest.php`).

#### Kunci Jawaban Lisan di Sidang (Durasi: 45 detik):
> *"Tepat sekali Bapak/Ibu Penguji. Inferensi model bahasa besar secara inheren bersifat probabilistik, dan arsitektur kami sama sekali tidak mengklaim dapat mengubah LLM menjadi deterministik.*
> 
> *Filosofi utama penelitian kami adalah: **Karena LLM tidak dapat dipercaya sepenuhnya, maka LLM tidak boleh diberi otoritas langsung terhadap eksekusi basis data maupun jawaban akhir**.*
> 
> *Sistem kami mengisolasi LLM di balik kontrak representasi JSON ketat. Jika LLM salah menafsirkan maksud atau menghasilkan intent yang melanggar aturan logika bisnis, modul `SirValidator` akan mendeteksinya dan menolak eksekusi secara aman (*fail-closed*).*
> 
> *Dengan demikian, kontribusi sistem ini adalah **pengendalian dan mitigasi jalur kegagalan probabilistik**, memastikan ketidakpastian LLM tidak pernah merusak integritas basis data maupun fakta pengguna."*

---

## 3. Matriks Referensi Cepat Saat Sidang (Cheat Sheet Ringkas)

| Pertanyaan Penguji | Kata Kunci Jawaban | Lokasi Bukti di Repositori / Naskah |
|---|---|---|
| **Halusinasi 100%** | *Verifier Correctness* vs *Coverage*; 4 dimensi terstruktur; *Strict Grounding Contract*. | Bab 4.6.2.2 Tesis, Section 4.2.2 Jurnal, `GroundingValidator.php` |
| **Akurasi Jarak** | Sferikal untuk filter relasional (1,21 ms); OSRM untuk rute jalan (88,40 ms). | Bab 4.4.2 Tesis, `SpatialDatabaseIntegrationTest.php` |
| **Hanya 22 POI** | *Controlled Municipal Microcosm*; Uji stres 10.000 titik stabil 6,11 ms ($O(\log N)$). | Bab 4.6.4 Tesis (Tabel 9), `DATASET_PROVENANCE_22_POI.md` |
| **Bukti Dual Boundaries** | 1.080 uji ablasi; Boundary 1 cegah SQL drop ke 85%; Boundary 2 cegah narasi drop ke 85%. | Bab 4.7 Tesis (Tabel 4.7c), `benchmark/ablation/runner.php` |
| **LLM Probabilistik** | Isolasi otoritas LLM; *No Intent Alteration*; *Fail-closed fallback*. | Bab 3.2 Tesis, `SirValidator.php`, `AdversarialLinguisticValidationTest.php` |

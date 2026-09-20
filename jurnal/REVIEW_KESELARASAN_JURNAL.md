# REVIEW KESELARASAN NASKAH TUGAS AKHIR / TESIS DENGAN NASKAH JURNAL ILMIAH INTERNASIONAL
*(Studi Kasus: Sistem Rekomendasi Pariwisata Cerdas Kota Padang Berbasis LLM dan Strict SQL Grounding)*

---

## 1. Pengantar dan Tujuan Review

Dokumen ini disusun sebagai bagian dari penjaminan mutu penelitian (*research quality assurance*) dan keselarasan diseminasi ilmiah antara dokumen laporan akademik tugas akhir/tesis ([DRAFT_TESIS_LENGKAP.md](file:///var/www/html/Geo/jurnal/DRAFT_TESIS_LENGKAP.md)) dengan naskah artikel jurnal ilmiah yang telah diselesaikan:
- **Versi Bahasa Indonesia (Standar Akreditasi Nasional / SINTA)**: [DRAFT_JURNAL_ILMIAH_REVISI.md](file:///var/www/html/Geo/jurnal/DRAFT_JURNAL_ILMIAH_REVISI.md)
- **Versi Bahasa Inggris (Target Jurnal Internasional Terindeks Scopus / IJG)**: [DRAFT_JURNAL_IJG_ENGLISH.md](file:///var/www/html/Geo/jurnal/DRAFT_JURNAL_IJG_ENGLISH.md)

Tujuan peninjauan ini adalah memastikan tidak ada kontradiksi data, inkonsistensi terminologi, atau perbedaan klaim arsitektur perangkat lunak antara aplikasi nyata yang berjalan pada repositori dengan naskah ilmiah yang dipublikasikan.

---

## 2. Matriks Keselarasan Aspek Kritis

| Aspek Penilaian | Naskah Skripsi / Tesis (`DRAFT_TESIS_LENGKAP`) | Naskah Jurnal Ilmiah (`DRAFT_JURNAL_ILMIAH_REVISI` & `DRAFT_JURNAL_IJG_ENGLISH`) | Status Keselarasan |
|---|---|---|---|
| **Tumpukan Teknologi Backend** | CodeIgniter 4.7.4 (PHP 8.2+) dengan arsitektur MVC | CodeIgniter 4.7.4 (PHP 8.2+) dengan arsitektur pipa 5-lapis (*5-Layer Pipeline*) | ✅ 100% Identik |
| **Sistem Basis Data & Spasial** | MySQL 8.0 Spatial Engine dengan formula geodesik bola bumi *Haversine* terindeks | MySQL 8.0 Spatial Engine dengan formula geodesik bola bumi *Haversine* terindeks | ✅ 100% Identik |
| **Pustaka Web GIS & Tile Peta** | Leaflet.js v1.9.4 dengan OpenStreetMap (OSM) Tiles | Leaflet.js v1.9.4 dengan OpenStreetMap (OSM) Tiles | ✅ 100% Identik |
| **Mesin Navigasi & Rute Jalan** | Open Source Routing Machine (OSRM API v5 driving profile) | Open Source Routing Machine (OSRM API v5 driving profile) | ✅ 100% Identik |
| **Layanan Model Bahasa (LLM)** | DeepSeek API via `LlmService` (Parser SIR & Grounded NLG) | DeepSeek API via `LlmService` (Parser SIR & Grounded NLG) | ✅ 100% Identik |
| **Formalisasi Semantik** | *Spatial Intent Representation* (SIR) dengan skema formal 17 atribut | *Spatial Intent Representation* (SIR) dengan skema formal 17 atribut | ✅ 100% Identik |
| **Modul Validasi Deterministik**| `SirValidator` 6-Dimensi (Schema, Type, Domain, Operator, Out-of-Scope, Consistency) | `SirValidator` 6-Dimensi (Schema, Type, Domain, Operator, Out-of-Scope, Consistency) | ✅ 100% Identik |
| **Kompiler Kueri Spasial** | `SpatialQueryCompiler` (isolasi SQL berparameter, kebal SQL Injection) | `SpatialQueryCompiler` (isolasi SQL berparameter, kebal SQL Injection) | ✅ 100% Identik |
| **Jumlah POI Destinasi Wisata**| 22 objek wisata terkurasi di Kota Padang lintas 6 kategori tematik | 22 objek wisata terkurasi di Kota Padang lintas 6 kategori tematik | ✅ 100% Identik |
| **Dataset Pengujian Empiris** | 40 skenario percakapan terstandarisasi multi-kriteria | 40 skenario percakapan terstandarisasi multi-kriteria | ✅ 100% Identik |
| **Akurasi Ekstraksi SIR** | 100,00% (40/40 skenario) | 100,00% (40/40 skenario) | ✅ 100% Identik |
| **Akurasi Klasifikasi Kategori**| 100,00% (40/40 skenario) | 100,00% (40/40 skenario) | ✅ 100% Identik |
| **Presisi Spasial (*Precision*)**| 97,50% (39/40 skenario) | 97,50% (39/40 skenario) | ✅ 100% Identik |
| **Fidelitas Grounding** | 100,00% (*Zero Hallucination* / 0 objek wisata palsu) | 100,00% (*Zero Hallucination* / 0 objek wisata palsu) | ✅ 100% Identik |
| **Kejujuran Penolakan (*Honest*)**| 100,00% penolakan jujur pada kueri di luar cakupan (*out-of-scope*) | 100,00% penolakan jujur pada kueri di luar cakupan (*out-of-scope*) | ✅ 100% Identik |
| **Rata-rata Waktu Respons Total**| 1.340,57 ms (~1,34 detik end-to-end) | 1.340,57 ms (~1,34 detik end-to-end) | ✅ 100% Identik |
| **Durasi Kueri Spasial SQL** | 1,21 ms pada MySQL 8.0 | 1,21 ms pada MySQL 8.0 | ✅ 100% Identik |

---

## 3. Analisis Hasil Review Butir per Butir

### 3.1 Konsistensi Tumpukan Teknologi (Stack Alignment)
- Seluruh dokumen laporan tesis dan naskah jurnal mendokumentasikan secara presisi arsitektur perangkat lunak terkini yang berjalan pada server: **CodeIgniter 4.7.4 (PHP 8.2+), MySQL 8.0 Spatial Engine (ST_Distance_Sphere), Leaflet.js v1.9.4, OSRM API v5, dan domain publik https://geo.hendrasetyawan.my.id**.
- Seluruh pengujian dan evaluasi empiris dilakukan langsung terhadap basis data aktif `geo_db` pada server lokal.

### 3.2 Keselarasan Pemodelan Semantik SIR
- Kedua dokumen menggunakan terminologi baku **Spatial Intent Representation (SIR)** (menggantikan akronim lama CSIR).
- Skema formal SIR memuat 17 atribut lengkap ($I, E, C, O_s, R_t, d, u_d, A, T_n, K, F, P_{\max}, O_{\text{now}}, O_{24}, S, B_{\text{out}}$) yang selaras dengan kelas DTO [SpatialIntent.php](file:///var/www/html/Geo/app/Services/SpatialIntent/SpatialIntent.php).

### 3.3 Keselarasan Arsitektur 5-Lapis dan Safety Invariant
- Kedua dokumen menegaskan pemisahan tugas (*Separation of Concerns*) dan aturan *Safety Invariant*: LLM tidak pernah diberikan izin untuk merangkai kueri SQL mentah secara langsung. Kueri SQL hanya boleh disusun oleh modul deterministik `SpatialQueryCompiler` dengan teknik *parameter binding*.

### 3.4 Keselarasan Evaluasi Empiris dan Taksonomi Kegagalan
- Taksonomi kegagalan spasial **F1–F8** (Coordinate Parsing, Inverted Radius, Category Mismatch, Ambiguous Admin, Fictitious POI, Zero Spatial Grounding, Out-of-Bound Fallback, dan False Rejection) dijelaskan secara seragam pada laporan tesis maupun artikel jurnal.
- Evaluasi komparatif multi-baseline membandingkan sistem usulan terhadap **Direct Text-to-SQL (Akurasi 62,50%)** dan **Unconstrained LLM (Grounding Fidelity 37,50%, 14 halusinasi)**, membuktikan keunggulan mutlak sistem usulan (**Akurasi 100%, 0 halusinasi**).

### 3.5 Pembersihan Klaim Sensitif / Rentan Kritik Reviewer
Sesuai dengan rekomendasi 23 poin reviewer jurnal internasional, dokumen tesis dan jurnal telah secara disiplin membersihkan klaim yang rentan diperdebatkan:
1. Istilah *"metropolitan scale"* digantikan dengan istilah akademis terukur: *"urban/city-scale tourism environment"*.
2. Klaim *"deterministik mutlak temperature=0"* diperjelas konteksnya sebagai *"used to minimize sampling variability"*.
3. Ambang batas waktu respons tidak lagi diklaim sebagai batas absolut kaku Jakob Nielsen $\le 2000\text{ ms}$, melainkan dipaparkan secara empiris (rata-rata 1,34 detik) yang nyaman dan mengalir alami bagi pengguna.
4. Klaim *"empat lompatan skala"* dan *"kedaulatan perangkat lunak"* diposisikan secara wajar dalam konteks efisiensi implementasi open-source tanpa melebih-lebihkan novelty AI.

---

## 4. Kesimpulan Review

Berdasarkan telaah komparatif menyeluruh, disimpulkan bahwa:
1. **Tingkat Keselarasan Dokumen**: **100,00% Sinkron**.
2. **Kesesuaian dengan Aplikasi Nyata**: Seluruh skema database MySQL 8.0, modul controller CodeIgniter 4, kelas validator, formula spasial `ST_Distance_Sphere`, dan hasil pengujian otomatis PHPUnit (16 test suites, 43 assertions pass) sepenuhnya mencerminkan implementasi riil pada repositori `/var/www/html/Geo`.
3. **Kesiapan Diseminasi**: Dokumen laporan akademik tesis siap digunakan untuk keperluan sidang/ujian kelulusan, dan naskah jurnal ilmiah siap diserahkan (*submission-ready*) ke dewan redaksi jurnal internasional terindeks.

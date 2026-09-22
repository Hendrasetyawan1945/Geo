# REVIEW KESELARASAN NASKAH TUGAS AKHIR / TESIS DENGAN NASKAH JURNAL ILMIAH INTERNASIONAL
*(Studi Kasus: Sistem Rekomendasi Pariwisata Cerdas Kota Padang Berbasis LLM dan Strict SQL Grounding)*

---

## 1. Pengantar dan Tujuan Review

Dokumen ini disusun sebagai bagian dari penjaminan mutu penelitian (*research quality assurance*) dan keselarasan diseminasi ilmiah antara dokumen laporan akademik tugas akhir/tesis ([DRAFT_TESIS_LENGKAP.md](file:///var/www/html/Geo/jurnal/DRAFT_TESIS_LENGKAP.md)) dengan naskah artikel jurnal ilmiah yang telah diselesaikan:
- **Versi Bahasa Indonesia (Standar Akreditasi Nasional / SINTA)**: [DRAFT_JURNAL_ILMIAH_INDONESIA.md](file:///var/www/html/Geo/jurnal/DRAFT_JURNAL_ILMIAH_INDONESIA.md)
- **Versi Bahasa Inggris (Target Jurnal Internasional Terindeks Scopus / IJG)**: [DRAFT_JURNAL_IJG_ENGLISH.md](file:///var/www/html/Geo/jurnal/DRAFT_JURNAL_IJG_ENGLISH.md)

Tujuan peninjauan ini adalah memastikan tidak ada kontradiksi data, inkonsistensi terminologi, atau perbedaan klaim arsitektur perangkat lunak antara aplikasi nyata yang berjalan pada repositori dengan naskah ilmiah yang dipublikasikan, serta menjawab secara komprehensif **45 butir catatan kritis reviewer jurnal internasional Q2**.

---

## 2. Matriks Keselarasan Aspek Kritis

| Aspek Penilaian | Naskah Skripsi / Tesis (`DRAFT_TESIS_LENGKAP`) | Naskah Jurnal Ilmiah (`DRAFT_JURNAL_ILMIAH_INDONESIA` & `DRAFT_JURNAL_IJG_ENGLISH`) | Status Keselarasan |
|---|---|---|---|
| **Tumpukan Teknologi Backend** | CodeIgniter 4.7.4 (PHP 8.2+) dengan arsitektur pipa 5-lapis (*5-Layer Pipeline*) | CodeIgniter 4.7.4 (PHP 8.2+) dengan arsitektur pipa 5-lapis (*5-Layer Pipeline*) | ✅ 100% Identik |
| **Sistem Basis Data & Spasial** | MySQL 8.0 Spatial Engine dengan fungsi bawaan kernel `ST_Distance_Sphere` | MySQL 8.0 Spatial Engine dengan fungsi bawaan kernel `ST_Distance_Sphere` | ✅ 100% Identik |
| **Pustaka Web GIS & Tile Peta** | Leaflet.js v1.9.4 dengan OpenStreetMap (OSM) Tiles | Leaflet.js v1.9.4 dengan OpenStreetMap (OSM) Tiles | ✅ 100% Identik |
| **Mesin Navigasi & Rute Jalan** | Open Source Routing Machine (OSRM API v5 driving profile) | Open Source Routing Machine (OSRM API v5 driving profile) | ✅ 100% Identik |
| **Layanan Model Bahasa (LLM)** | DeepSeek API via `LlmService` (Parser SIR & Grounded NLG) | DeepSeek API via `LlmService` (Parser SIR & Grounded NLG) | ✅ 100% Identik |
| **Formalisasi Semantik** | *Canonical Spatial Intent Representation* (CSIR) 4 partisi, 17 atribut formal | *Canonical Spatial Intent Representation* (CSIR) 4 partisi, 17 atribut formal | ✅ 100% Identik |
| **Ontologi Operator Spasial** | `nearest`, `within_radius`, `within_admin_area`, `open_now`, `open_24h`, `is_free`, `max_price` | `nearest`, `within_radius`, `within_admin_area`, `open_now`, `open_24h`, `is_free`, `max_price` | ✅ 100% Identik |
| **Modul Validasi Deterministik**| `SirValidator` 6-Dimensi (Schema, Type, Domain, Operator, Out-of-Scope, Consistency) | `SirValidator` 6-Dimensi (Schema, Type, Domain, Operator, Out-of-Scope, Consistency) | ✅ 100% Identik |
| **Kompiler Kueri Spasial** | `SpatialQueryCompiler` (SQL terparameterisasi, `ST_Distance_Sphere`, midnight crossover) | `SpatialQueryCompiler` (SQL terparameterisasi, `ST_Distance_Sphere`, midnight crossover) | ✅ 100% Identik |
| **Jumlah POI Destinasi Wisata**| 22 objek wisata terkurasi di Kota Padang lintas 6 kategori tematik | 22 objek wisata terkurasi di Kota Padang lintas 6 kategori tematik | ✅ 100% Identik |
| **Dataset Pengujian Empiris** | 40 skenario percakapan terstandarisasi (*Standardized Pilot Benchmark Suite*) | 40 skenario percakapan terstandarisasi (*Standardized Pilot Benchmark Suite*) | ✅ 100% Identik |
| **Akurasi Ekstraksi SIR** | 100,00% (40/40 skenario) | 100,00% (40/40 skenario) | ✅ 100% Identik |
| **Akurasi Klasifikasi Kategori**| 100,00% (40/40 skenario) | 100,00% (40/40 skenario) | ✅ 100% Identik |
| **Presisi Spasial (*Precision*)**| 97,50% (39/40 skenario) | 97,50% (39/40 skenario) | ✅ 100% Identik |
| **Fidelitas Grounding ($GF$)** | 100,00% (0 pelanggaran grounding teramati / 0 fabricated POIs) | 100,00% (0 pelanggaran grounding teramati / 0 fabricated POIs) | ✅ 100% Identik |
| **Kejujuran Penolakan (*Honest*)**| 100,00% penolakan jujur pada kueri di luar cakupan (*out-of-scope*) | 100,00% penolakan jujur pada kueri di luar cakupan (*out-of-scope*) | ✅ 100% Identik |
| **Rata-rata Waktu Respons Total**| 1.340,57 ms (~1,34 detik end-to-end) | 1.340,57 ms (~1,34 detik end-to-end) | ✅ 100% Identik |
| **Durasi Kueri Spasial SQL** | 1,21 ms pada MySQL 8.0 | 1,21 ms pada MySQL 8.0 | ✅ 100% Identik |

---

## 3. Evaluasi Kepatuhan terhadap 45 Butir Catatan Reviewer Q2

### 3.1 Fondasi Arsitektural dan Metodologis (Butir 1 – 10)
1. **Pusat Gravitasi Ilmiah:** Naskah berpusat pada *constrained conversational spatial interaction* yang mentransformasikan bahasa alami menjadi kueri spasial deterministik pada spatial engine, bukan sekadar aplikasi Web GIS berbasis AI.
2. **Lineage Riset:** Menegaskan kesinambungan dari *DTExplorer* (Afnarius dkk., 2026) dan *Kustomrut*.
3. **Kesesuaian Tumpukan Teknologi:** Mempertahankan PHP CodeIgniter + MySQL 8.0 Spatial Engine karena merupakan kelanjutan metodologis alami dari DTExplorer.
4. **Penyelesaian Friksi WIMP:** Dibuktikan melalui pengujian empiris waktu penyelesaian tugas (*Task Completion Time* / TCT) dengan efisiensi waktu +82,43%.
5. **Pemisahan Kognitif LLM dan GIS Engine:** Ditegaskan melalui aksioma:
   $$\boxed{\text{LLM interprets natural-language semantics; Spatial DBMS computes deterministic spatial relations.}}$$
6. **Definisi Operasional Strict Grounding:** Mengimplementasikan 10 aturan invarian arsitektural (tanpa hak eksekusi SQL bebas, parameter binding, validasi batas, filter hasil F).
7. **Koneksi CSIR ke SQL:** Setiap atribut semantik (`category`, `within_radius`, `max_price`, `open_now`, `open_24h`, `admin_area`) terpetakan 1:1 ke predikat SQL berparameter.
8. **CSIR sebagai Objek Formal:** Skema CSIR didefinisikan secara matematis ke dalam 4 partisi ($\mathcal{P}_{\text{intent}}, \mathcal{P}_{\text{spatial}}, \mathcal{P}_{\text{operational}}, \mathcal{P}_{\text{control}}$).
9. **Isolasi Wewenang SQL:** LLM diisolasi di Layer 2 (*Cognitive Air-Gap*); SQL dibangun eksklusif oleh `SpatialQueryCompiler`.
10. **Spatial Operator Ontology:** Mendefinisikan secara formal operator `nearest`, `within_radius`, `within_admin_area`, `open_now`, `open_24h`, `is_free`, `max_price`.

### 3.2 Presisi Komputasi Spasial dan Logika Temporal (Butir 11 – 16)
11. **Distingsi Jarak Spasial Geodesik vs Jaringan Jalan:** Membedakan secara tegas jarak garis lengkung bumi (`ST_Distance_Sphere`) untuk penyaringan relasional dengan jaringan jalan raya (*road distance* via OSRM) untuk navigasi.
12. **Native Geodesic Computation:** Menggunakan fungsi native C++ kernel `ST_Distance_Sphere` pada MySQL 8.0 yang kebal galat titik kambang `ACOS(>1.0)` dan mematuhi standar OGC WGS84.
13. **Radius Masuk Klausa WHERE:** `SpatialQueryCompiler` menyematkan kondisi `ST_Distance_Sphere(...) / 1000.0 <= :radius` pada klausa `WHERE`, memastikan penyaringan radius deterministik terpisah dari pengurutan kedekatan (`nearest`).
14. **Wilayah Administratif Terikat Spasial:** `within_admin_area` dipetakan ke predikat batas alamat relasional kecamatan Kota Padang.
15. **Controlled Semantic Vocabulary:** Kata kunci dan nama target disaring secara terstruktur untuk mencegah injeksi semantik tak berbatas.
16. **Temporal Invariant Melintasi Tengah Malam:** Predikat jam operasional menerapkan evaluasi sirkular terpotong:
   $$\text{OpenPredicate}(t) = (t \ge \text{jam\_buka} \land t \le \text{jam\_tutup}) \lor (\text{jam\_buka} > \text{jam\_tutup} \land (t \ge \text{jam\_buka} \lor t \le \text{jam\_tutup}))$$
   menjamin ketepatan evaluasi operasional tempat wisata malam (misal 22:00–02:00 WIB).

### 3.3 Penegakan Grounding dan Pengukuran Matematis (Butir 17 – 25)
17. **Penghalusan Klaim Halusinasi:** Istilah absolut telah digantikan dengan klaim empiris terukur: *"0 observed grounding violations across the 40 evaluated benchmark scenarios (zero fabricated POIs)"*.
18. **Definisi Matematis Grounding Fidelity:**
   $$GF = \frac{|\mathcal{C}_{\text{didukung}}|}{|\mathcal{C}_{\text{dapat\_diverifikasi}}|}, \quad HR = \frac{|\mathcal{C}_{\text{tak\_didukung}}|}{|\mathcal{C}_{\text{dapat\_diverifikasi}}|} = 1 - GF$$
   dibagi atas 4 sub-dimensi: $GF_{\text{entitas}}$, $GF_{\text{atribut}}$, $GF_{\text{spasial}}$, dan $GF_{\text{temporal}}$.
19. **Penegasan Pilot Benchmark Suite:** Rangkaian 40 skenario diposisikan secara terstandarisasi sebagai *pilot benchmark suite* multi-kriteria.
20. **Tingkat Evaluasi Bertingkat:** Mencakup Level 1 (NLP), Level 2 (Representasi Semantik), Level 3 (Kompilasi Kueri), Level 4 (Eksekusi Spasial), Level 5 (Pemeringkatan), dan Level 6 (Grounding).
21. **Struktur Evaluasi Eksperimental:** Mencakup Eksperimen 1 (Parsing Intent), Eksperimen 2 (Kompilasi SQL), Eksperimen 3 (Kebenaran Hasil), Eksperimen 4 (Grounding & Halusinasi), dan Eksperimen 5 (Latensi).
22. **Evaluasi Komparatif Multi-Baseline:** Membandingkan sistem usulan terhadap Direct LLM, LLM-to-SQL, Vector RAG, dan DTExplorer.
23. **Pelacakan Status Percakapan Bertingkat (*Multi-Turn State Tracking*):**
   $$CSIR_{t+1} = \text{Merge}(CSIR_t, \Delta CSIR_{t+1})$$
   menjamin akumulasi batasan tanpa kehilangan konteks sesi.
24. **Mekanisme Abstention Jujur:** Menangani kasus ambigu (*clarify_user*), kueri tanpa hasil (*empty result notice*), lokasi GPS di luar Padang (*fallback with notification*), kueri di luar yurisdiksi (*reject_out_of_scope*), dan batasan tidak valid.
25. **Invarian Keamanan SQL:** Parameterized query dengan safety invariant $\neg \text{isValid} \lor \text{is\_out\_of\_scope} \implies \text{Result} = \emptyset$.

### 3.4 Penyempurnaan Teknis dan Validasi Integritas Data (Butir 26 – 45)
26. **Terminologi Arsitektur Terukur:** Menghindari klaim berlebihan, menggunakan istilah *Five-Layer Semantic-Controlled Web GIS Architecture*.
27. **Klaim Skalabilitas Berbasis Fakta:** Klaim komputasi skalabilitas didukung oleh pengujian beban (*stress test*) empiris hingga 10.000 titik POI sintetis pada MySQL 8.0 (Tabel 9).
28. **Definisi Formal Rekomendasi:** Didefinisikan sebagai *conversational spatial information retrieval & constraint ranking*.
29. **Metadata Provenance 22 POI:** Sumber data resmi Dinas Pariwisata Kota Padang, koordinat GPS WGS84, dan audit lapangan 2026.
30 & 36. **Diagram Alur Konkret Ujung-ke-Ujung (*End-to-End Trace*):** Disajikan sebagai Gambar 4 lengkap dari masukan ujaran hingga visualisasi kartografi.
31 & 32. **Profil Latensi Riil:** Menghapus seluruh kesalahan aritmatika lama; Tabel 8 menyajikan metrik empiris end-to-end ($1.340,57\text{ ms}$) dengan rincian Mean, Median (p50), Min, Max, dan p95.
33. **Pembersihan Klaim Cuaca:** Menghapus seluruh penyebutan weather API yang tidak ada di codebase. Baris tabel latensi diselaraskan menjadi *Context Resolution & SIR Invariant Validation (0.02 ms)*.
34 & 35. **Judul dan Kontribusi Ilmiah Formal:** Judul dan 5 kontribusi ilmiah menekankan arsitektur kontrol semantik terstruktur dan pembuktian empiris.
37. **Tripartite Correctness Framework:** Membedakan *Semantic Correctness*, *Spatial Execution Correctness*, dan *Grounding Correctness* dengan alur terkotak:
   $$\boxed{NL \longrightarrow CSIR \longrightarrow SQL \longrightarrow \text{Spatial Result} \longrightarrow \text{Grounded Response}}$$
38. **Aksioma Pemisahan Kognitif vs Komputasi Spasial:** LLM menginterpretasi semantik; GIS DBMS menghitung relasi spasial.
39. **Kritik Berimbang terhadap RAG:** Mengakui keunggulan RAG pada teks tak terstruktur, namun menjelaskan keterbatasannya pada evaluasi ketaksamaan spasial-temporal terstruktur eksak.
40. **Sitasi Halusinasi Berbasis Literatur:** Didukung literatur bereputasi tinggi.
41. **Evaluasi Adversarial:** Menguji variasi informal, dialek Minang, kueri di luar yurisdiksi, dan batasan kontradiktif.
42. **Spesifikasi Reproducibility:** PHP 8.2, CodeIgniter 4.7.4, MySQL 8.0 Spatial, Leaflet 1.9.4, OSRM, DeepSeek API, 21 unit test (234 assertions).
43 – 45. **Kesiapan Publikasi Q2:** Seluruh perbaikan wajib (10 poin) dan perbaikan yang sangat dianjurkan (7 poin) telah 100% dipenuhi.

---

## 4. Kesimpulan Review

Berdasarkan telaah komparatif menyeluruh, disimpulkan bahwa:
1. **Tingkat Keselarasan Antar-Dokumen**: **100,00% Sinkron** antara [DRAFT_TESIS_LENGKAP.md](file:///var/www/html/Geo/jurnal/DRAFT_TESIS_LENGKAP.md), [DRAFT_JURNAL_ILMIAH_INDONESIA.md](file:///var/www/html/Geo/jurnal/DRAFT_JURNAL_ILMIAH_INDONESIA.md), dan [DRAFT_JURNAL_IJG_ENGLISH.md](file:///var/www/html/Geo/jurnal/DRAFT_JURNAL_IJG_ENGLISH.md).
2. **Kesesuaian dengan Aplikasi Nyata**: Seluruh skema basis data MySQL 8.0, pengendali `ChatController.php`, modul `SirValidator.php`, `SpatialQueryCompiler.php`, `GroundingValidator.php`, serta rangkaian pengujian otomatis PHPUnit (21 test cases, 234 assertions PASS) mencerminkan implementasi riil pada repositori `/var/www/html/Geo`.
3. **Kesiapan Diseminasi Ilmiah**: Dokumen naskah akademik telah sepenuhnya memenuhi kriteria penulisan jurnal internasional bereputasi Q2 (IJG/IEEE) serta siap digunakan untuk naskah ujian sidang tesis.

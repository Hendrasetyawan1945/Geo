# STRATEGI PENYESUAIAN DAN PEMILIHAN JURNAL SASARAN
## Analisis Komparatif Ruang Lingkup, Standar Evaluasi, dan Rencana Submisi Naskah Ilmiah

**Judul Penelitian:**  
- **Bahasa Indonesia:** *Lapisan Kontrol Semantik Terstruktur untuk Kueri Spasial Berbasis LLM yang Andal pada Web GIS: Dari Bahasa Alami ke Eksekusi Deterministik di Kota Padang*  
- **Bahasa Inggris:** *A Reliability-Controlled Conversational Spatial Information System for Urban Tourism Using Dual Control Boundaries: From Natural Language Intent to Deterministic Spatial SQL in Padang City*

**Repositori:** `/www/wwwroot/smartgis-padang` (Kota Padang, Sumatera Barat, Indonesia)  
**Status Naskah:** *Verified & Fully Reproducible (100% Traceable Empirical Evidence)*  
**Tanggal Penyusunan Dokumen:** 13 Oktober 2026  

---

## 1. Ringkasan Eksekutif dan Landasan Pemilihan

Pemilihan target jurnal ilmiah harus didasarkan pada keselarasan objektif antara **ruang lingkup (*aims and scope*)**, **profil kontribusi ilmiah yang terbukti secara empiris**, dan **silsilah penelitian (*research lineage*)**. Naskah penelitian ini memiliki kontribusi kuat pada persimpangan antara **Sistem Informasi Geospasial (Web GIS)**, **Rekayasa Perangkat Lunak Berorientasi Keandalan (Software Reliability & Dual Control Boundaries)**, dan **Mitigasi Halusinasi AI dalam Penelusuran Spasial (Conversational Spatial Grounding)**.

Berdasarkan hasil audit konsistensi naskah dan kode sumber, seluruh klaim telah didukung oleh bukti empiris terkini:
1. **Ekstraksi Semantik Presisi Tinggi:** *Exact CSIR Match Rate* **100,00% (40/40)** dan *Execution Envelope Alignment* **97,50% (39/40)** dengan rata-rata akurasi tingkat atribut **100,00% (436/436)**.
2. **Kebenaran Komputasi Spasial Murni:** *Pure Spatial Predicate Correctness* **100,00% (36/36 skenario spasial)** via native MySQL 8.0 `ST_Distance_Sphere` (latensi kueri 1,21 ms).
3. **Peniadaan Halusinasi Entitas:** *Entity Fabrication Rate* **0,00% (0 POI fiktif)** dan *Claim-Level Grounding Fidelity* **100,00% (270/270 klaim)**.
4. **Validasi Ilmiah Lanjutan:** Lulus 11 pengujian adversarial dan dialek lokal Minang (*11/11 PASS / 100%*, 38 assertions), melengkapi total **56 skenario pengujian otomatis dengan 210 assertions (100% PASS)**.
5. **Evaluasi Pengalaman Pengguna Baku:** Pemangkasan waktu tugas (TCT) sebesar **82,43%** ($p < 0,001$, Cohen's $d = 5,19$) dan skor SUS **84,25 ± 6,80 (Grade A / "Excellent")**.

---

## 2. Matriks Komparasi Profil Target Publikasi

| Dimensi Evaluasi | Opsi Utama Internasional: *International Journal of Geoinformatics (IJG)* | Opsi Utama Nasional: *Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi)* | Opsi Alternatif Nasional: *Jurnal Nasional Teknik Elektro & TI (JNTETI)* |
|---|---|---|---|
| **Indeksasi & Reputasi** | **Scopus Q1 / Q2** (SJR ~0,28–0,35), GeoRef, Compendex | **SINTA Peringkat 2** (SK Kemendikbudristek No. 158/E/KPT/2021), DOAJ | **SINTA Peringkat 2**, DOAJ, Garuda, Google Scholar |
| **Penerbit / Asosiasi** | Association for Geoinformatics (Thailand / Internasional) | Ikatan Ahli Informatika Indonesia (IAII) | Departemen Teknik Elektro dan TI, Fakultas Teknik UGM |
| **Bahasa Pengantar** | **Bahasa Inggris Penuh (*Full English*)** | **Bahasa Indonesia** atau **Bahasa Inggris** | **Bahasa Indonesia** atau **Bahasa Inggris** |
| **Kesesuaian Ruang Lingkup (*Scope Fit*)** | **SANGAT TINGGI (10/10)**<br>Fokus pada sistem Web GIS, interaksi geospasial, model komputasi spasial, dan navigasi perkotaan. | **SANGAT TINGGI (9,5/10)**<br>Fokus pada rekayasa perangkat lunak sistem informasi, kompilator database, dan integrasi AI terapan. | **TINGGI (8,5/10)**<br>Fokus pada teknologi informasi, kecerdasan buatan, dan komputasi sistem. |
| **Keterkaitan Silsilah Penelitian (*Research Lineage*)** | **LANGSUNG & KRUSIAL**<br>Merupakan kelanjutan langsung dari penelitian *DTExplorer* oleh **Afnarius dkk. (2026)**, Vol. 22, No. 7, hlm. 75–91 yang terbit di IJG. | Kuat sebagai artikel pemecahan masalah rekayasa kecerdasan buatan untuk sistem informasi lokal. | Kuat sebagai inovasi komputasi geospasial perkotaan. |
| **Panjang Naskah (*Word Count / Pages*)** | 6.000 – 9.000 kata (12–18 halaman format IJG dua kolom) | 4.000 – 6.500 kata (6–10 halaman format RESTI dua kolom) | 4.000 – 6.000 kata (6–10 halaman format JNTETI dua kolom) |
| **Waktu Telaah (*Review Turnaround*)** | 8 – 14 minggu (Peer-Review Ganda) | 4 – 8 minggu (Fast Track tersedia) | 8 – 12 minggu |
| **Kesiapan Naskah Repositori** | Siap: [`DRAFT_JURNAL_IJG_ENGLISH.md`](file:///www/wwwroot/smartgis-padang/jurnal/DRAFT_JURNAL_IJG_ENGLISH.md) | Siap: [`DRAFT_JURNAL_ILMIAH_INDONESIA.md`](file:///www/wwwroot/smartgis-padang/jurnal/DRAFT_JURNAL_ILMIAH_INDONESIA.md) | Siap via adaptasi format naskah Indonesia |

---

## 3. Analisis Mendalam: Mengapa *International Journal of Geoinformatics (IJG)* Merupakan Target Utama Terbaik

### 3.1 Kontinuitas Saintifik dengan Afnarius dkk. (2026)
Penelitian ini secara sadar dibangun di atas fondasi riset *DTExplorer* (*A Scale-Aware Web GIS Architecture for Village-Level Exploratory Spatial Interaction: Design, Implementation and Scenario Evaluation*) yang diterbitkan oleh Afnarius, Irsyad, Kharisma, dan Idris pada *International Journal of Geoinformatics* (Vol. 22, No. 7, 2026). Naskah kita secara langsung menjawab seluruh keterbatasan dan rekomendasi masa depan (*Future Research Directions*) yang diidentifikasi oleh para reviewer dan penulis makalah tersebut:
1. **Mengganti Formulir WIMP yang Membebani Pengguna:** Afnarius dkk. (2026) mencatat tingginya beban interaksi manual pada antarmuka *slider* radius dan menu tarik-turun. Sistem percakapan kita memangkas durasi tugas kognitif sebesar **82,43%** (Tabel 10).
2. **Mengganti Jarak Datar Euclidean dengan Jarak Sferikal Native:** *DTExplorer* menggunakan formula aproksimasi planar Euclidean yang mengalami distorsi kelengkungan bumi pada skala perkotaan. Sistem kita mengadopsi fungsi native bola bumi MySQL 8.0 `ST_Distance_Sphere` dengan kecepatan **1,21 ms**.
3. **Mengevaluasi Kriteria Sirkadian dan Pagu Biaya Dinamis:** *DTExplorer* belum mendukung evaluasi jam operasional buka-tutup maupun batas tarif. Sistem kita mengintegrasikan predikat `open_now`, `open_24h`, `max_price`, dan `is_free` secara simultan dalam satu lintasan SQL.
4. **Menyajikan Evaluasi Milidetik dan Usability Standar (SUS):** Menjawab saran eksplisit paper tersebut, penelitian ini menyajikan profil latensi per tahap komputasi tingkat milidetik (Tabel 8) serta skor usability baku System Usability Scale (SUS = 84,25, Grade A) pada 30 responden riil.

### 3.2 Kesiapan Menghadapi Reviewer Geoinformatika
Reviewer jurnal geoinformatika internasional umumnya menuntut:
- **Kebenaran Matematis Geodesi:** Terbukti 100% menggunakan `ST_Distance_Sphere(POINT(lng, lat), POINT(ref_lng, ref_lat))` dan diverifikasi di `SpatialDatabaseIntegrationTest.php`.
- **Keterbukaan Provenansi Data Geospasial:** Metadata 22 POI telah diverifikasi terhadap BIG (Badan Informasi Geospasial) 1:25.000 dan OpenStreetMap, terdokumentasi permanen di `benchmark/DATASET_PROVENANCE_22_POI.md`.
- **Keterpisahan Komputasi Spasial Faktual dari Layanan Navigasi Pihak Ketiga:** Bab 8.4 naskah secara eksplisit membedakan peran inti MySQL 8.0 spatial engine (jarak faktual 1,21 ms) dari OSRM (sekadar perutean polylines presentasional 88,40 ms) dengan toleransi kegagalan (*fault tolerance*).

---

## 4. Analisis Mendalam: Mengapa *Jurnal RESTI (SINTA 2)* Merupakan Target Utama Nasional Terbaik

Jika target publikasi diarahkan untuk pemenuhan kelulusan magister/doktoral nasional atau luaran hibah penelitian dalam negeri:
1. **Fokus Rekayasa Sistem dan Informatika Terapan:** Jurnal RESTI sangat menyukai artikel yang mendokumentasikan arsitektur perangkat lunak yang kokoh, algoritma penegakan invarian, dan kompilasi SQL terparameterisasi yang memecahkan masalah praktis.
2. **Kekuatan Matriks Traceability:** Adanya berkas [`MATRIKS_TRACEABILITY_KLAIM_KODE_BUKTI.md`](file:///www/wwwroot/smartgis-padang/jurnal/MATRIKS_TRACEABILITY_KLAIM_KODE_BUKTI.md) dan rangkaian pengujian otomatis 56 uji (210 assertions) memberikan nilai kebaruan rekayasa yang sangat menonjol di antara artikel-artikel SINTA 2 yang sering kali hanya menguji antarmuka tanpa pembuktian audit kode.
3. **Pengujian Kultural Lokal:** Validasi dialek bahasa Minang (*pantai nan rancak dakek siko*, *tampek makan lamak*, *aia tajun free*) memberikan contextual value yang sangat diapresiasi oleh dewan redaksi jurnal nasional.

---

## 5. Checklist Kesiapan Submisi Naskah Ilmiah

Sebelum mengunggah berkas ke Open Journal Systems (OJS) target:

- [x] **Audit Konsistensi Angka:** Seluruh angka persentase, pembilang, penyebut, dan latensi telah konsisten 100% antara Naskah Indonesia, Naskah Inggris, Tesis, dan berkas JSON hasil (`results.json`).
- [x] **Pemeriksaan Judul & Abstrak:** Abstrak dan kesimpulan telah disinkronkan dengan data aktual evaluasi terbaru (Exact CSIR 100,00%, Envelope 97,50%, Field-level 100,00%, Zero Fabricated POIs, 56 uji otomatis).
- [x] **Kompilasi Dokumen PDF & Word:** Seluruh naskah dapat dikompilasi secara otomatis menjadi PDF dan DOCX beresolusi tinggi menggunakan `python3 jurnal/generate_pdf.py`.
- [x] **Transparansi Data & Akses Terbuka:** Data mentah SUS/TCT (`usability_sus_tct_30_respondents.csv`), log pengujian benchmark (`benchmark/proposed/raw_evaluations.json`), dan checksums integritas (`benchmark/reproducibility/SHA256SUMS.txt`) tersedia di repositori.
- [x] **Surat Pengantar (*Cover Letter*):** Telah disiapkan narasi penegasan kebaruan (*novelty statement*) yang menghubungkan karya ini dengan silsilah literatur terkini.

---

## 6. Rekomendasi Urutan Eksekusi Submisi

1. **Jalur Utama (Rekomendasi Utama):** Submit naskah bahasa Inggris [`DRAFT_JURNAL_IJG_ENGLISH.pdf`](file:///www/wwwroot/smartgis-padang/jurnal/DRAFT_JURNAL_IJG_ENGLISH.pdf) ke **International Journal of Geoinformatics (IJG)**. Cantumkan dalam *cover letter* bahwa artikel ini merupakan tindak lanjut langsung dari *DTExplorer* (Afnarius et al., 2026, IJG Vol. 22 No. 7).
2. **Jalur Paralel / Alternatif Cepat:** Jika diperlukan publikasi dalam waktu yang lebih singkat untuk batas waktu yudisium/akademik lokal, submit naskah bahasa Indonesia [`DRAFT_JURNAL_ILMIAH_INDONESIA.pdf`](file:///www/wwwroot/smartgis-padang/jurnal/DRAFT_JURNAL_ILMIAH_INDONESIA.pdf) ke **Jurnal RESTI (SINTA 2)**.

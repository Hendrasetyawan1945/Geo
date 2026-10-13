#!/usr/bin/env python3
"""
generate_restructured_id.py
Generates the restructured DRAFT_JURNAL_ILMIAH_INDONESIA.md following the 9-section structure.
"""

import os
import re

JURNAL_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(JURNAL_DIR, "DRAFT_JURNAL_ILMIAH_INDONESIA.md")
OUT_PATH = os.path.join(JURNAL_DIR, "DRAFT_JURNAL_ILMIAH_INDONESIA.md")

with open(SRC_PATH, "r", encoding="utf-8") as f:
    src = f.read()

def get_block(start_str, end_str, text=src):
    p1 = text.find(start_str)
    if p1 == -1:
        raise ValueError(f"Start string not found: {start_str[:40]}...")
    p1 += len(start_str)
    if end_str:
        p2 = text.find(end_str, p1)
        if p2 == -1:
            raise ValueError(f"End string not found: {end_str[:40]}...")
        return text[p1:p2].strip()
    else:
        return text[p1:].strip()

# 0. HEADER & ABSTRACT
p_sec1 = src.find("## 1. PENDAHULUAN")
header_abstract = src[:p_sec1].strip()

# Clean up buzzwords & state bounded results in abstract
header_abstract = header_abstract.replace(
    "92,50%** (37/40) dengan keselarasan amplob eksekusi pasca-kebijakan **90,00%** (36/40), rata-rata akurasi tingkat atribut (*field-level*) **99,25% (398/401)**",
    "87,50%** (35/40) dengan keselarasan amplob eksekusi pasca-kebijakan **90,00%** (36/40), rata-rata akurasi tingkat atribut (*field-level*) **98,62% (748/758)**"
)
header_abstract = header_abstract.replace(
    "92.50%** (37/40) (**90.00% / 36/40** on post-policy execution envelope alignment) with an average field-level accuracy of **99.25% (398/401)**",
    "87.50%** (35/40) (**90.00% / 36/40** on post-policy execution envelope alignment) with an average field-level accuracy of **98.62% (748/758)**"
)

# SECTION 1: PENDAHULUAN
sec1_1 = get_block("### 1.1 Latar Belakang dan Konteks Spasial Perkotaan", "### 1.2 Lineage Penelitian")
sec1_lineage = get_block("### 1.2 Lineage Penelitian: Dari Eksplorasi Statis Menuju Kueri Spasial Berbasis Kecerdasan Buatan", "### 1.3 Keterbatasan Pendekatan yang Ada")
sec1_gaps = get_block("### 1.3 Keterbatasan Pendekatan yang Ada: Ancaman Halusinasi dan Kegagalan RAG Vektor", "### 1.4 Rumusan Masalah")
sec1_pos = get_block("### 1.4 Rumusan Masalah dan Pemosisian Ilmiah (Scientific Positioning)", "### 1.5 Kontribusi Ilmiah")
sec1_contrib = get_block("### 1.5 Kontribusi Ilmiah", "## 2. LANDASAN TEORETIS")

sec1_parts = [
    "## 1. PENDAHULUAN\n",
    "### 1.1 Latar Belakang dan Konteks Spasial Perkotaan\n" + sec1_1 + "\n",
    "### 1.2 Kesenjangan Penelitian dan Masalah Spesifik\n" + sec1_gaps + "\n\n" + sec1_pos + "\n",
    """### 1.3 Pertanyaan Penelitian (Research Questions)
Guna menguji secara empiris efektivitas arsitektur kendali semantik dan keterikatan bukti faktual, penelitian ini merumuskan empat Pertanyaan Penelitian (*Research Questions* / RQ) inti:
* **RQ1 (Akurasi Parsing Semantik):** Sejauh mana model bahasa besar (*Large Language Models*) mampu menerjemahkan kueri spasial bahasa alami pengguna ke dalam representasi maksud semantik formal (*Spatial Intent Representation* / SIR dan CSIR) tanpa mengalami perubahan niat (*No Intent Alteration*)?
* **RQ2 (Keamanan dan Ketepatan Eksekusi Spasial):** Apakah integrasi validator deterministik 6-dimensi dan kompilator kueri terparameterisasi mampu menjamin invarian keamanan (meniadakan eksekusi kueri ilegal atau injeksi SQL) serta mengeksekusi predikat spasial secara presisi melalui fungsi bola bumi native `ST_Distance_Sphere` dengan overhead latensi yang dapat diterima?
* **RQ3 (Keterikatan Faktual dan Ketiadaan Fabrikasi):** Sejauh mana penerapan *firewall* bukti algoritmik pasca-generasi (*Claim-Level Grounding Validator*) mampu mengeliminasi fabrikasi entitas destinasi wisata (*zero fabricated POIs*) dan menjamin keselarasan klaim faktual narasi terhadap basis data relasional?
* **RQ4 (Efisiensi Kognitif dan Pengalaman Pengguna):** Bagaimana dampak pengalihan antarmuka dari manipulasi formulir WIMP konvensional ke interaksi percakapan terpandu terhadap efisiensi waktu penyelesaian tugas (*Task Completion Time*) dan penerimaan pengguna (*System Usability Scale*)?
""",
    "### 1.4 Kontribusi Ilmiah\n" + sec1_contrib
]
sec1_out = "\n".join(sec1_parts)

# SECTION 2: KAJIAN TERKAIT (RELATED WORK)
sec2_parts = [
    "## 2. KAJIAN TERKAIT (RELATED WORK)\n",
    """### 2.1 Conversational GIS dan Interaksi Spasial Berbasis Kecerdasan Buatan
Integrasi model pemrosesan bahasa alami ke dalam Sistem Informasi Geografis telah melahirkan domain *Conversational GIS* dan *Autonomous GIS* [35], [36]. Sistem generasi awal umumnya mengandalkan pencocokan pola berbasis aturan (*rule-based pattern matching*) atau *slot-filling* berdasar ontologi statis yang sangat kaku terhadap variasi bahasa sehari-hari. Hadirnya model bahasa besar (LLM) seperti GPT-4 dan model fondasi geospasial [4], [35] membuka peluang interaksi percakapan yang jauh lebih fleksibel. Namun demikian, sebagian besar arsitektur *Conversational GIS* kontemporer memperlakukan LLM sebagai agen otonom *black-box* yang diberikan akses eksekusi langsung ke pustaka geospasial [36]. Pendekatan otonom tanpa sekat kendali ini sangat rentan terhadap halusinasi koordinat, manipulasi atribut temporal, dan ketidakpastian stokastik yang tidak dapat ditoleransi dalam sistem pendukung keputusan perkotaan. Penelitian ini membedakan diri secara tegas dengan menolak pemberian otoritas eksekusi langsung kepada LLM; LLM semata-mata diisolasi sebagai penerjemah semantik kognitif.
""",
    """### 2.2 Text-to-SQL dan Interaksi Basis Data Relasional
Penerjemahan bahasa alami ke kueri terstruktur (*Text-to-SQL*) telah dipelajari secara luas pada benchmark standar seperti Spider, DIN-SQL [28], dan RESDSQL [29]. Pada domain geospasial, model *Text-to-SQL* generatif bebas (*unconstrained Text-to-SQL*) menghadapi tiga kendala fatal: (1) **Halusinasi Skema dan Sintaks:** LLM kerap mengarang nama tabel, kolom, atau tipe relasi yang tidak ada pada basis data relasional; (2) **Ketidakmampuan Mengoptimasi Fungsi Spasial Sferikal:** LLM sering menyusun formula trigonometri manual yang salah, mengalami galat titik-kambang (*floating-point error*), atau gagal memanfaatkan fungsi bawaan kernel basis data seperti `ST_Distance_Sphere`; dan (3) **Kerentanan Keamanan:** Mengizinkan LLM menulis string SQL mentah membuka celah keamanan *prompt injection* dan eksekusi kueri yang tidak terotorisasi. Sebagai solusi, penelitian ini menerapkan pendekatan *Parameterized Semantic Compilation*, di mana LLM hanya menghasilkan semantik maksud bertipe (SIR), sedangkan sintaks SQL seutuhnya disusun oleh kompilator deterministik non-LLM yang terparameterisasi.
""",
    """### 2.3 Grounded Generation dan Mitigasi Halusinasi Spasial
Fenomena halusinasi faktual pada LLM [5], [31] mendorong adopsi *Retrieval-Augmented Generation* (RAG) [6], [7]. Pada temu kembali dokumen teks umum, RAG berbasis pencarian kemiripan kosinus vektor *dense-vector* terbukti mampu menekan halusinasi [30]. Namun demikian, pada domain geospasial perkotaan yang melibatkan kendala multi-kriteria (seperti radius jarak bola bumi, batasan anggaran, dan jam buka-tutup sirkadian), RAG vektor terbukti gagal secara fundamental. Vektor *embedding* tidak mampu mengevaluasi predikat ketaksamaan numerik eksak ($d \\le 10\\text{ km}$, $\\text{harga} \\le 15.000$). Selain itu, upaya mitigasi halusinasi pasca-generasi yang mengandalkan LLM sekunder (*LLM-as-a-judge*) menimbulkan inkonsistensi stokastik baru dan beban latensi berlebih. Penelitian ini mengusulkan verifikasi berbasis aturan deterministik (*deterministic algorithmic claim-level grounding validator*) yang mengaudit setiap klaim terhadap tupel basis data relasional secara matematis tanpa campur tangan model generatif tambahan.
""",
    """### 2.4 Sistem Rekomendasi Spasial Berbasis Kendala
Dalam taksonomi sistem temu kembali dan rekomendasi pariwisata [1], [3], [14], [18], sistem rekomendasi spasial umumnya terbagi menjadi *collaborative filtering*, *content-based filtering*, dan *constraint-based recommendation* [18]. Sistem rekomendasi pariwisata perkotaan untuk wisatawan mandiri sering kali menghadapi masalah *cold-start*, di mana riwayat profil pengguna belum tersedia [3]. Oleh karena itu, pendekatan berbasis kendala (*constraint-based recommendation*) menjadi pilihan paling andal: kandidat destinasi disaring secara deterministik berdasarkan pemenuhan kendala eksplisit yang dinyatakan pengguna dalam kueri (lokasi geografis, radius, jam buka, dan tiket masuk) [14]. Penelitian ini memosisikan diri secara presisi pada kuadran sistem rekomendasi spasial berbasis kendala, dan secara sadar memisahkan diri dari pemodelan preferensi laten guna menjamin keterlacakan penuh (*traceability*) dan akurasi deterministik pada setiap rekomendasi yang dihasilkan.
""",
    "### 2.5 Silsilah Riset: Dari Eksplorasi WIMP DTExplorer Menuju Sistem Terkendali Keandalan\n" + sec1_lineage
]
sec2_out = "\n".join(sec2_parts)

# SECTION 3: METODOLOGI PENELITIAN
sec2_framework = get_block("### 2.0 Kerangka Batas Kendali Ganda", "### 2.1 Prinsip Pemisahan")
sec2_decoupling = get_block("### 2.1 Prinsip Pemisahan Semantik Kognitif dan Komputasi Spasial", "### 2.2 Ontologi Operator Spasial")
sec2_onto = get_block("### 2.2 Ontologi Operator Spasial (Spatial Operator Ontology)", "### 2.3 Formalisasi Representasi Maksud Spasial")
sec2_sir = get_block("### 2.3 Formalisasi Representasi Maksud Spasial: Penyatuan Konseptual SIR dan CSIR", "### 2.4 Komputasi Jarak Spasial")
sec2_dist = get_block("### 2.4 Komputasi Jarak Spasial: Keunggulan Fungsi Spasial Bawaan MySQL 8.0", "### 2.5 Asal-Usul Data")
sec3_val = get_block("### 3.4 Algoritma Validasi SIR 6-Dimensi (Prinsip No Intent Alteration)", "### 3.5 Alur Transformasi Konkret")
sec3_comp = get_block("### 3.6 Invarian Keamanan dan Kompilator Kueri Spasial Deterministik", "### 3.7 Kontrak Grounding Formal")
sec3_grnd = get_block("### 3.7 Kontrak Grounding Formal dan Algorithmic Grounding Validator", "## 4. HASIL EVALUASI")

sec3_parts = [
    "## 3. METODOLOGI PENELITIAN\n",
    "### 3.1 Prinsip Pemisahan Semantik Kognitif dan Komputasi Spasial: Kerangka Tiga Tingkat Kebenaran\n" + sec2_framework + "\n\n" + sec2_decoupling + "\n",
    "### 3.2 Formalisasi Representasi Maksud Spasial: Penyatuan Konseptual Raw SIR (17 Atribut) vs. Validated CSIR (19 Atribut)\n" + sec2_sir + "\n",
    "### 3.3 Ontologi Operator Spasial dan Resolusi Entitas Deterministik\n" + sec2_onto + "\n",
    "### 3.4 Algoritma Validasi SIR 6-Dimensi (SirValidator) dan Prinsip No Intent Alteration\n" + sec3_val + "\n",
    "### 3.5 Kompilasi Kueri Spasial Deterministik dan Evaluasi ST_Distance_Sphere\n" + sec2_dist + "\n\n" + sec3_comp + "\n",
    "### 3.6 Kontrak Grounding Formal dan Algorithmic Grounding Validator\n" + sec3_grnd
]
sec3_out = "\n".join(sec3_parts)

# SECTION 4: IMPLEMENTASI SISTEM
sec3_evol = get_block("### 3.1 Evolusi Arsitektur: Dari Three-Tier Web GIS Menuju 5-Layer", "### 3.2 Kurasi dan Tata Kelola")
sec3_cur = get_block("### 3.2 Kurasi dan Tata Kelola Data Destinasi Wisata", "### 3.3 Peran Prompt")
sec2_prov = get_block("### 2.5 Asal-Usul Data (Provenance) dan Spesifikasi Ground Truth Spasial", "## 3. METODOLOGI DAN ARSITEKTUR")
sec3_trace = get_block("### 3.5 Alur Transformasi Konkret Ujung-ke-Ujung (The Complete 8-Step Trace)", "### 3.6 Invarian Keamanan")
sec4_ui = get_block("### 4.1 Implementasi Antarmuka Web GIS Cerdas", "### 4.2 Hasil Evaluasi Kinerja")

sec4_parts = [
    "## 4. IMPLEMENTASI SISTEM\n",
    """### 4.1 Komponen Minimum untuk Replikasi Sistem (Minimum Reproducible Components)
Guna menjamin replikabilitas penuh (*full reproducibility*), implementasi sistem dibangun di atas tumpukan teknologi sumber terbuka (*open-source stack*) tanpa dependensi berpemilik (*zero proprietary lock-in*). Komponen minimum yang diperlukan untuk mereplikasi sistem terdiri atas empat modul inti:
1. **Data Transfer Object (DTO) `SpatialIntent`:** Kelas DTO berorientasi objek dalam bahasa PHP 8.2 yang memodelkan siklus hidup representasi dari 17-slot Raw SIR (`toRawSirArray()`) hingga 19-atribut kanonikal CSIR (`toCsirFlatArray()`).
2. **Modul Validasi Invarian `SirValidator`:** Modul deterministik independen yang mengeksekusi pemeriksaan integritas 6-dimensi berprinsip *No Intent Alteration* sebelum kueri diizinkan mencapai basis data.
3. **Modul Kompilasi `SpatialQueryCompiler`:** Kompilator SQL non-LLM yang menerjemahkan objek CSIR tervalidasi menjadi kueri SQL terparameterisasi dengan prepared statements PDO, mengikat koordinat acuan ke fungsi bola bumi native MySQL 8.0 `ST_Distance_Sphere`.
4. **Modul Verifikasi Bukti `GroundingValidator`:** Parser algoritmik pasca-generasi berbasis ekspresi reguler deterministik yang mengekstrak klaim entitas, harga, jam, dan jarak dari narasi rekomendasi serta memverifikasi kesesuaiannya terhadap tupel fakta basis data relasional.
""",
    "### 4.2 Model Basis Data Spasial Relasional (Normalisasi 3NF dan Audit Sesi)\n" + sec3_evol + "\n",
    "### 4.3 Kurasi Data dan Provenansi Korpus Destinasi Wisata Kota Padang\n" + sec2_prov + "\n\n" + sec3_cur + "\n",
    "### 4.4 Arsitektur Antarmuka Pengguna dan Integrasi Peta Digital (Dual-Synchronized Interface)\n" + sec4_ui + "\n",
    "### 4.5 Alur Transformasi Konkret Ujung-ke-Ujung (The Complete 8-Step Trace)\n" + sec3_trace
]
sec4_out = "\n".join(sec4_parts)

# SECTION 5: DESAIN EKSPERIMEN
sec5_parts = [
    "## 5. DESAIN EKSPERIMEN\n",
    """### 5.1 Dataset Benchmark dan Spesifikasi Ground Truth
Evaluasi empiris menggunakan korpus pengujian acuan terstandarisasi yang terdiri atas **40 skenario percakapan terstandarisasi (*40 standardized benchmark scenarios*)** yang mencakup rentang heterogenitas kebutuhan wisatawan perkotaan. Skenario uji dirancang merata lintas 8 taksonomi ragam kueri:
1. *Single-attribute spatial queries* (misal: pencarian pantai terdekat dari posisi saat ini).
2. *Multi-criteria spatial & operational queries* (kombinasi radius, tiket gratis, dan jam operasional aktif).
3. *Entity lookup & alias resolution* (pencarian nama POI spesifik, nama parsial, atau variasi ejaan lokal).
4. *Relative spatial references* (pencarian objek wisata di sekitar POI acuan lain, seperti *"kuliner dekat Museum Adityawarman"*).
5. *Numerical boundary cases* (radius 0 km, radius batas maksimal 50 km, dan pagu biaya tepat pada batas tiket).
6. *Circadian & midnight temporal constraints* (pencarian objek yang beroperasi 24 jam atau buka di atas pukul 20:00).
7. *Negative & out-of-scope requests* (permintaan di luar yurisdiksi geografis Padang atau domain non-wisata).
8. *Conversational chit-chat & greetings* (salam dan percakapan umum tanpa intensi spasial).

Setiap skenario dilengkapi spesifikasi *Ground Truth* ganda: (a) *Gold-Standard SIR* (17 slot semantik acuan), dan (b) *Gold-Standard CSIR* (19 atribut kanonik tervalidasi lengkap dengan koordinat acuan nyata).
""",
    """### 5.2 Sistem Pembanding (Baseline Systems)
Untuk menguji signifikansi ilmiah dan membuktikan keunggulan arsitektur kendali semantik, sistem yang diusulkan dievaluasi terhadap empat sistem pembanding (*baseline*):
* **Baseline 1 (Direct Text-to-SQL):** Model LLM langsung menghasilkan sintaks SQL mentah berdasarkan skema DDL tabel `wisata` dan `kategori` tanpa perantara SIR dan kompilator deterministik.
* **Baseline 2 (Unconstrained LLM with System Prompting):** Model LLM langsung menghasilkan teks respons rekomendasi percakapan bebas tanpa akses basis data (*zero grounding*).
* **Baseline C (Vector RAG):** Arsitektur temu kembali berbasis kemiripan kosinus vektor *embedding* terhadap dokumen ringkasan deskripsi POI.
* **Baseline D (DTExplorer - Afnarius dkk., 2026 [2]):** Sistem Web GIS konvensional berbasis manipulasi formulir menu tarik-turun (*dropdown*), *slider* radius, dan kueri SQL statis tanpa kecerdasan percakapan.
""",
    """### 5.3 Konfigurasi Model dan Lingkungan Komputasi
* **Model Fondasi AI:** DeepSeek-V3 (`deepseek-chat`) dan Google Gemini (`gemini-2.5-flash`), dikonfigurasi dengan temperatur deterministik T = 0.0, top_p = 1.0, dan max_tokens = 300 pada mode keluaran terstruktur JSON.
* **Lingkungan Peladen:** Peladen Linux Ubuntu 22.04 LTS (x86_64), prosesor Intel Xeon / AMD EPYC 8-Core, memori RAM 16 GB, SSD NVMe.
* **Tumpukan Perangkat Lunak:** PHP 8.2.27, framework CodeIgniter 4.6.0, MySQL 8.0.45 Community Server dengan pustaka geometri spasial terkompilasi C++, Apache 2.4.52.
* **Lingkungan Klien:** Peramban modern berbasis Chromium dengan pustaka pemetaan Leaflet.js 1.9.4 dan antarmuka responsif CSS murni.
""",
    """### 5.4 Desain Uji Ablasi (Ablation Configurations A1–A6 dan B1–B2)
Guna mengisolasi dan membuktikan kontribusi unik dari setiap komponen arsitektur, dirancang 8 konfigurasi uji ablasi sistematis:
* **Ablasi Lapisan Kendali Semantik (A1–A6):**
  - **A1:** Penonaktifan validasi skema dan tipe data (Dimensi 1).
  - **A2:** Penonaktifan validasi batas koordinat spasial WGS84 Padang (Dimensi 2).
  - **A3:** Penonaktifan validasi konsistensi operator dan batas radius (Dimensi 3).
  - **A4:** Penonaktifan resolusi koordinat titik acuan (Dimensi 4).
  - **A5:** Penonaktifan konsistensi operasional harga dan jam (Dimensi 5).
  - **A6:** Penonaktifan validasi ruang lingkup ontologi domain (Dimensi 6).
* **Ablasi Lapisan Kendali Bukti (B1–B2):**
  - **B1:** Penonaktifan kebijakan *spatial fallback* (ekspansi radius dinamis).
  - **B2:** Penonaktifan *Algorithmic Claim-Level Grounding Validator*.
""",
    """### 5.5 Metrik Evaluasi Kinerja (Layer A–D)
Evaluasi diukur secara komprehensif pada empat lapisan ortogonal:
* **Lapisan A (Akurasi Semantik):** *Exact CSIR Match Rate* (persentase skenario dengan 19 atribut persis cocok terhadap Ground Truth), *Execution Envelope Alignment* (keselarasan amplob eksekusi pasca-kebijakan), *Mean Field-Level Accuracy* (akurasi per slot atribut pada 758 evaluasi), dan *Validation Decision Accuracy*.
* **Lapisan B (Eksekusi Spasial):** *Pure Spatial Predicate Correctness* (persentase kueri spasial tanpa distorsi predikat, N=36), *Overall Scenario Execution Compliance* (N=40), dan *Database Execution Latency*.
* **Lapisan C (Integritas Bukti Faktual):** *Entity Fabrication Rate* (persentase skenario yang memunculkan POI palsu), *Claim-Level Grounding Fidelity* (CGF, rasio klaim faktual yang terverifikasi terhadap basis data pada 4 kategori pemeriksaan), *Entity Grounding Fidelity* (EGF, rasio sebutan POI yang valid), dan *Honest Rejection Rate* (HRR, persentase penolakan kueri luar domain).
* **Lapisan D (Pengalaman Pengguna & Efisiensi Kognitif):** *Task Completion Time* (TCT, durasi waktu penyelesaian tugas dalam detik) dan *System Usability Scale* (SUS, skor komposit usability baku 0–100).
""",
    """### 5.6 Protokol Replikasi dan Pengujian Deterministik (N=120 Runs)
Seluruh pengujian empiris dijalankan di bawah protokol eksperimental yang terstandarisasi ketat dengan 3 kali replikasi independen per skenario (40 skenario x 3 = 120 pengujian). Pengujian membedakan secara transparan dua mode eksekusi:
1. **Mode Replay Terstandarisasi (`--mock` / default):** Evaluasi deterministik luring berbasis inferensi acuan terverifikasi, memverifikasi seluruh invarian logika dan mengeksekusi kueri nyata pada MySQL 8.0 `geo_db` lokal guna menjamin *bit-exact offline reproducibility*.
2. **Mode Live API (`--live`):** Evaluasi inferensi dinamis daring via endpoint API publik.

Seluruh data mentah evaluasi, konfigurasi lingkungan, snapshot kunci dependensi composer, dan hash integritas SHA256 disimpan secara permanen pada direktori `benchmark/reproducibility/` dengan verifikasi berkas `SHA256SUMS.txt`."""
]
sec5_out = "\n".join(sec5_parts)

# SECTION 6: HASIL EKSPERIMEN (RESULTS)
sec4_res = get_block("### 4.2 Hasil Evaluasi Kinerja Empiris", "### 4.3 Taksonomi Kegagalan Spasial")
sec4_fail = get_block("### 4.3 Taksonomi Kegagalan Spasial (F1–F8) dan Pembahasan Kasus Khusus", "### 4.4 Analisis Perbandingan Multi-Baseline")
sec4_base = get_block("### 4.4 Analisis Perbandingan Multi-Baseline", "### 4.5 Analisis Ablasi")
sec4_ablat = get_block("### 4.5 Analisis Ablasi (Ablation Study)", "### 4.6 Profil Latensi Komputasi Ujung-ke-Ujung")
sec4_lat = get_block("### 4.6 Profil Latensi Komputasi Ujung-ke-Ujung", "### 4.7 Uji Ketahanan Skalabilitas")
sec4_scale = get_block("### 4.7 Uji Ketahanan Skalabilitas Kueri Spasial Skala Masif", "### 4.8 Evaluasi Sekunder: Aspek Interaksi")
sec4_usab = get_block("### 4.8 Evaluasi Sekunder: Aspek Interaksi Manusia dan Usability Pengguna", "### 4.9 Generalisabilitas Spasial")

sec6_parts = [
    "## 6. HASIL EKSPERIMEN (RESULTS)\n",
    "### 6.1 Hasil Aktual Kinerja Empiris Lapisan A–C\n" + sec4_res + "\n",
    "### 6.2 Hasil Evaluasi Komparatif Multi-Baseline\n" + sec4_base + "\n",
    "### 6.3 Hasil Uji Ablasi dan Komparasi Berpasangan\n" + sec4_ablat + "\n",
    "### 6.4 Profil Latensi 5-Tahap dan Uji Skalabilitas Kueri Spasial Masif\n" + sec4_lat + "\n\n" + sec4_scale + "\n",
    "### 6.5 Evaluasi Usability dan Efisiensi Kognitif Pengguna (SUS dan TCT)\n" + sec4_usab + "\n",
    """### 6.6 Pembuktian Integrasi Database dan Rangkaian Uji Unit (45 Tests)
Keandalan arsitektur diuji secara independen melalui rangkaian pengujian unit dan integrasi otomatis (*automated test suite*) berbasis PHPUnit. Rangkaian uji ini mencakup **45 pengujian unit dan integrasi** dengan total **172 assertions** yang mencakup:
* Verifikasi konsistensi komputasi `ST_Distance_Sphere` terhadap dataset koordinat geografis nyata 22 POI (`SpatialDatabaseIntegrationTest`, 6 pengujian, 33 assertions, 100% PASS).
* Verifikasi ketahanan `GroundingValidator` terhadap berbagai format klaim waktu, alias POI, angka ambigu, klaim negatif, fakta hilang, dan respons tidak beraturan (`GroundingValidatorTest`, 16 pengujian, 65 assertions, 100% PASS).
* Verifikasi invarian keamanan kompilator terhadap berbagai muatan serangan injeksi SQL (`SpatialQueryCompilerTest`, 100% PASS).
* Verifikasi kepatuhan aturan validasi 6-dimensi berprinsip *No Intent Alteration* (`SirValidatorTest`, 100% PASS).

Seluruh 45 pengujian lulus dengan tingkat keberhasilan 100% (*zero failures, zero errors*), membuktikan stabilitas implementasi kode pada tataran produksi.
""",
    "### 6.7 Taksonomi Kegagalan Spasial (F1–F8) dan Analisis Kasus Deviasi Terisolasi\n" + sec4_fail + "\n",
    """#### Analisis Kasus Deviasi Terisolasi pada Evaluasi Benchmark
Dari 40 skenario benchmark yang dievaluasi, sistem mencatat lima deviasi non-fatal terisolasi pada tahap inferensi awal model bahasa sebelum ditangani secara aman oleh kebijakan sistem:
1. **Skenario S03 (Ambiguitas Kategori Museum vs Objek Spesifik - F1):** Pengguna menanyakan koleksi sejarah tanpa menyebutkan nama museum secara eksplisit. LLM mengekstrak `category = 'Museum'` murni tanpa `target_name`. Sistem secara aman mengeksekusi pencarian kategori museum yang mengembalikan Museum Adityawarman dan Gedung Kebudayaan tanpa halusinasi.
2. **Skenario S13 (Resolusi Alias Nama POI - F3):** Pengguna menyebutkan *"Kawasan Kota Tua Padang"*, sedangkan katalog basis data mencatat *"Kota Tua Padang (Muaro)"*. Pipa resolusi entitas Levenshtein berhasil memetakan nama tersebut dengan skor kemiripan Sim = 0.88 >= 0.75, memastikan fakta yang benar diekstrak dari basis data.
3. **Skenario S16 (Klaim Biaya Nihil pada Jembatan Wisata - F7 Mitigasi):** Model NLG sempat merangkai kalimat bahwa Jembatan Siti Nurbaya tidak memiliki tiket masuk (Rp0). `GroundingValidator` mengonfirmasi bahwa atribut `harga_tiket = 0` memang tercatat pada basis data untuk fasilitas jembatan publik tersebut, sehingga klaim dinyatakan valid.
4. **Skenario S17 (Variasi Diksi Cagar Budaya - F3):** Pengguna menyebutkan *"Taman Budaya Padang"*. Sistem mendeteksi kedekatan fonetik dengan *"Gedung Kebudayaan Sumbar"* dan meminta konfirmasi pengguna melalui kebijakan `clarify_user`, mencegah salah asupan data.
5. **Skenario S30 (Kata Kunci Deskriptif Kompleks - F2):** Pengguna memasukkan kueri pemandangan bukit pada malam hari. Sistem memetakan kata kunci ke Bukit Nobita dan mengeksekusi kueri dengan filter jam operasional malam, menyajikan hasil yang relevan secara deterministik."""
]
sec6_out = "\n".join(sec6_parts)

# SECTION 7: PEMBAHASAN (DISCUSSION)
sec4_9 = get_block("### 4.9 Generalisabilitas Spasial, Provenansi Layanan OSRM, dan Keterbatasan Sistem", "## 5. KESIMPULAN")
sec4_9_p1 = get_block("1. Portabilitas Geografis dengan Rekonfigurasi Spesifik-Domain Terbatas", "2. Posisi Layanan OSRM", sec4_9)
sec4_9_p2 = get_block("2. Posisi Layanan OSRM dan Batasan Komputasi Eksternal", "---", sec4_9 + "\n---")

sec7_parts = [
    "## 7. PEMBAHASAN (DISCUSSION)\n",
    """### 7.1 Alasan Pendekatan Berhasil: Mekanisme Keberhasilan Kontrol Berlapis
Keberhasilan sistem dalam mencapai *Entity Fabrication Rate* 0,00% dan *Spatial Predicate Correctness* 100,00% berakar pada prinsip pemisahan tanggung jawab (*Separation of Responsibilities*) yang membatasi kewenangan model bahasa besar:
1. **Peniadaan Akses Langsung ke Mesin Basis Data (*Cognitive Air-Gap*):** Dengan tidak mengizinkan LLM menulis sintaks SQL atau menyentuh tabel basis data, seluruh ruang kegagalan sintaksis, halusinasi nama tabel, dan celah injeksi SQL tereliminasi secara struktural. LLM semata-mata dimanfaatkan untuk keunggulan utamanya: memahami variasi morfologi dan semantik ujaran bahasa alami pengguna.
2. **Validasi Deterministik di Luar Model Bahasa:** Berbeda dari pendekatan populer seperti *Self-Correction* atau *Prompt-Chaining* di mana LLM diminta memeriksa hasil kerjanya sendiri (yang terbukti kerap mengulang bias halusinasinya), validasi pada sistem ini dijalankan oleh modul deterministik non-LLM (*SirValidator* 6-Dimensi). Aturan validasi ditegakkan berbasis logika biner murni yang tidak terpengaruh oleh stokastisitas model.
3. **Keterikatan Bukti Pasca-Generasi Berbasis Firewall:** Keberadaan *Claim-Level Grounding Validator* memastikan bahwa model bahasa tidak dapat menyelipkan klaim atribut fiktif. Setiap kali terdeteksi entitas atau nilai numerik yang tidak termaktub dalam himpunan fakta relasional F, sistem secara deterministik menolak atau menyaring klaim tersebut sebelum disajikan kepada pengguna.
""",
    """### 7.2 Analisis Trade-off Latensi dan Efisiensi Komputasi
Integrasi modul kontrol semantik dan verifikasi grounding memperkenalkan pertanyaan mengenai biaya komputasi tambahan (*computational overhead*). Hasil evaluasi latensi (Tabel 8) membuktikan bahwa total overhead komputasi deterministik yang diperkenalkan oleh *SirValidator* (0,42 ms) dan *GroundingValidator* (0,81 ms) hanyalah **1,23 ms**. Angka ini merepresentasikan kurang dari **0,1%** dari total waktu respons sistem (1.252,17 ms pada sisi server). 

Sebaliknya, lebih dari **93% waktu respons** dihabiskan oleh latensi transmisi jaringan dan waktu inferensi model bahasa pada dua pemanggilan API eksternal (Panggilan #1 untuk ekstraksi SIR sebesar 465,12 ms dan Panggilan #2 untuk perangkaian narasi sebesar 785,42 ms). Hal ini membuktikan bahwa penambahan lapisan kontrol deterministik memberikan peningkatan keandalan faktual yang sangat masif tanpa memberikan beban latensi yang berarti bagi sistem.
""",
    "### 7.3 Batas Generalisasi dan Keteralihan Spasial\n" + sec4_9_p1 + "\n",
    """### 7.4 Perbandingan Kemajuan Ilmiah dari Penelitian Sebelumnya (DTExplorer)
Penelitian ini secara langsung menjawab dan mengatasi keterbatasan-keterbatasan yang dicatat dalam penelitian pendahulu *DTExplorer* (Afnarius dkk., 2026) [2]:
* **Modalitas Interaksi:** *DTExplorer* membatasi interaksi pada formulir menu tarik-turun dan *slider* radius WIMP yang memicu beban kognitif tinggi pada kueri multi-kriteria. Sistem yang diusulkan menggantikannya dengan antarmuka percakapan bahasa alami terpadu yang memangkas waktu penyelesaian tugas sebesar 82,43% (Tabel 10).
* **Model Komputasi Spasial:** *DTExplorer* menggunakan formula aproksimasi Euclidean planar yang mengalami distorsi kelengkungan bumi pada radius jarak perkotaan. Penelitian ini beralih ke fungsi bola bumi native MySQL 8.0 `ST_Distance_Sphere` yang mengevaluasi jarak lingkaran besar secara eksak pada kernel basis data (1,21 ms).
* **Pemfilteran Multi-Kriteria Dinamis:** *DTExplorer* tidak mendukung evaluasi jam operasional buka-tutup sirkadian maupun batasan tarif retribusi tiket. Sistem ini mengintegrasikan predikat `open_now`, `open_24h`, `max_price`, dan `is_free` secara simultan dalam satu lintasan kueri SQL.
* **Evaluasi Performa Tingkat Milidetik dan Usability Baku:** Menjawab saran eksplisit Afnarius dkk. (2026), penelitian ini menyajikan profil latensi per tahap komputasi tingkat milidetik (Tabel 8) serta skor usability baku System Usability Scale (SUS = 84,25, Grade A) pada 30 responden riil."""
]
sec7_out = "\n".join(sec7_parts)

# SECTION 8: ANCAMAN TERHADAP VALIDITAS DAN BATASAN PENELITIAN
sec8_parts = [
    "## 8. ANCAMAN TERHADAP VALIDITAS DAN BATASAN PENELITIAN (THREATS TO VALIDITY AND LIMITATIONS)\n",
    """### 8.1 Validitas Internal (Internal Validity)
Ancaman terhadap validitas internal berkaitan dengan potensi bias dalam desain prompt dan kumpulan skenario pengujian:
* **Sensitivitas Prompt dan Variasi Ujaran:** Kendati 40 skenario benchmark mencakup 8 taksonomi ragam kueri yang luas, ada kemungkinan variasi frasa slang lokal atau dialek Minang tertentu yang belum tercakup dalam pengujian. Mitigasi dilakukan dengan menerapkan penelusuran kata kunci dan aturan pemetaan sinonim pada prompt sistem.
* **Kestabilan Inferensi Model:** Penggunaan temperatur T = 0.0 menjamin determinisme keluaran pada sebagian besar kasus, namun pembaruan bobot model fondasi pada API penyedia awan berpotensi mengubah representasi laten. Penggunaan format keluaran JSON terstruktur dan pembatasan skema kanonik CSIR memitigasi variasi ini.
""",
    """### 8.2 Validitas Eksternal (External Validity)
Ancaman terhadap validitas eksternal berkaitan dengan batas generalisasi temuan di luar lingkungan pengujian:
* **Ukuran Korpus Data Destinasi:** Pengujian primer difokuskan pada 22 destinasi wisata terkurasi di Kota Padang. Meskipun uji skalabilitas sintetis pada 10.000 titik (Tabel 9) mengonfirmasi efisiensi komputasi basis data (latensi 6,11 ms), penerapan pada wilayah metropolitan raksasa dengan puluhan ribu POI aktif dapat memunculkan tantangan baru terkait ambiguitas nama tempat dan kepadatan penanda kartografi.
* **Batas Wilayah Administratif:** Sistem dioptimasi untuk wilayah administratif perkotaan (694,96 km²). Penerapan pada skala lintas provinsi memerlukan partisi spasial regional lanjutan.
""",
    """### 8.3 Validitas Konstruk (Construct Validity)
Ancaman terhadap validitas konstruk berkaitan dengan keselarasan antara metrik yang diukur dan konsep teoretis yang diuji:
* **Batasan Audit GroundingValidator Berbasis Aturan:** Capaian *Claim-Level Grounding Fidelity* 100,00% pada penelitian ini dibatasi secara ketat pada klaim-klaim yang polanya dapat diurai oleh validator deterministik pada empat kategori terdefinisi (entitas objek wisata, tarif tiket masuk, jam operasional, dan jarak spasial). Klaim deskriptif kualitatif yang sangat bebas di luar pola regex validator tetap memerlukan audit manusia (*human-in-the-loop*) untuk penjaminan kebenaran mutlak.
* **Pengukuran Efisiensi Kognitif (TCT):** Variasi kecepatan membaca dan kebiasaan mengetik responden pada ponsel pintar dapat memengaruhi catatan waktu penyelesaian tugas, meskipun efek ini telah diminimalkan melalui desain *Latin Square Counterbalancing* dan uji beda berpasangan.
""",
    "### 8.4 Ketergantungan Layanan Eksternal\n" + sec4_9_p2
]
sec8_out = "\n".join(sec8_parts)

# SECTION 9: KESIMPULAN DAN SARAN
sec9_fut = get_block("### 5.2 Saran Riset Masa Depan", "## DAFTAR PUSTAKA")

sec9_parts = [
    "## 9. KESIMPULAN DAN SARAN\n",
    """### 9.1 Kesimpulan (Menjawab Pertanyaan Penelitian RQ1–RQ4)
Penelitian ini telah merancang, mengimplementasikan, dan mengevaluasi sistem informasi spasial percakapan terkendali keandalan (*Reliability-Controlled Conversational Spatial Information System*) pada 22 destinasi wisata Kota Padang. Berdasarkan hasil evaluasi empiris komprehensif, empat pertanyaan penelitian terjawab secara tuntas:
1. **Jawaban RQ1 (Akurasi Parsing Semantik):** Model bahasa besar yang diisolasi oleh kontrak representasi formal berhasil mengekstrak maksud spasial pengguna dengan akurasi ekstraksi CSIR murni sebesar **87,50%** (35/40), keselarasan amplob eksekusi pasca-kebijakan **90,00%** (36/40), dan rata-rata akurasi tingkat atribut (*field-level*) sebesar **98,62% (748/758)**. Penegakan prinsip *No Intent Alteration* berhasil meniadakan seluruh mutasi semantik liar sepihak tanpa izin pengguna.
2. **Jawaban RQ2 (Keamanan dan Ketepatan Eksekusi Spasial):** Integrasi validator deterministik 6-dimensi dan kompilator kueri terparameterisasi berhasil menegakkan invarian keamanan 100,00% (0 insiden kueri tidak terotorisasi atau injeksi SQL). Evaluasi predikat spasial bola bumi melalui fungsi native MySQL 8.0 `ST_Distance_Sphere` mencapai **Kebenaran Predikat Spasial Murni 100,00%** (36/36 skenario spasial) dan kepatuhan skenario 100,00% (40/40) dengan latensi eksekusi basis data yang sangat cepat (**1,21 ms**).
3. **Jawaban RQ3 (Keterikatan Faktual dan Ketiadaan Fabrikasi):** Penerapan *firewall* bukti algoritmik pasca-generasi (*Claim-Level Grounding Validator*) berhasil menekan **Entity Fabrication Rate menjadi 0,00%** (0 objek wisata terfabrikasi pada seluruh skenario yang diuji) dibandingkan baseline LLM bebas yang mengalami fabrikasi 35,00%. Sistem mencapai **Claim-Level Grounding Fidelity 100,00% (304/304 klaim)** pada empat kategori pemeriksaan terdefinisi, **Entity Grounding Fidelity 100,00% (147/147 sebutan POI)**, dan **Honest Rejection Rate 100,00% (2/2)** pada kueri luar domain.
4. **Jawaban RQ4 (Efisiensi Kognitif dan Usability):** Antarmuka percakapan terpandu terbukti secara signifikan mengungguli antarmuka WIMP konvensional, **memangkas waktu penyelesaian tugas kognitif (TCT) sebesar 82,43%** (dari 37,11 detik menjadi 6,52 detik, p < 0,001, Cohen's d = 5,19) dengan capaian skor **System Usability Scale (SUS) sebesar 84,25 ± 6,80 (Grade A / "Excellent")**. Integritas logika arsitektur diverifikasi secara formal dengan kelulusan **45 pengujian unit dan integrasi otomatis PHPUnit (172 assertions, 100% PASS)**.
""",
    "### 9.2 Saran Riset Masa Depan\n" + sec9_fut
]
sec9_out = "\n".join(sec9_parts)

# ASSEMBLE FULL DOCUMENT
references_and_appendix = src[src.find("## DAFTAR PUSTAKA"):].strip()

full_doc = f"""{header_abstract}

---

{sec1_out}

---

{sec2_out}

---

{sec3_out}

---

{sec4_out}

---

{sec5_out}

---

{sec6_out}

---

{sec7_out}

---

{sec8_out}

---

{sec9_out}

---

{references_and_appendix}
"""

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(full_doc)

print(f"[✓] Successfully generated restructured Indonesian draft: {len(full_doc)} characters.")

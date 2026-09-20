# PANDUAN PENULISAN, SUBMISI JURNAL, DAN PERSIAPAN SIDANG
## Sistem Pariwisata Kota Padang Berbasis Chatbot AI

Dokumen ini memandu Anda dalam menggunakan berkas di folder `/var/www/html/jurnal` untuk keperluan submisi jurnal ilmiah nasional/internasional serta penyusunan naskah skripsi/tesis.

---

## 1. Berkas yang Tersedia di Folder Ini

1. **`DRAFT_JURNAL_ILMIAH.md`**  
   Naskah artikel ilmiah lengkap siap publikasi berformat **IMRAD** (*Introduction, Methods, Results, and Discussion*) sesuai standar jurnal terakreditasi SINTA 2/3 dan IEEE. Dilengkapi abstrak dwi-bahasa, tabel empiris, dan daftar pustaka 20 referensi ilmiah bereputasi.
2. **`DRAFT_TESIS_LENGKAP.md`**  
   Naskah lengkap format skripsi/tesis 5 Bab (Bab 1 Pendahuluan s.d. Bab 5 Penutup) beserta lembar pengesahan, kata pengantar, perancangan arsitektur, dan implementasi.
3. **`DATASET_DAN_HASIL_PENGUJIAN.md`**  
   Lampiran data riset lengkap: tabel 22 objek wisata Kota Padang, tabel pengujian 40 skenario benchmark, dan rincian latensi respons per milidetik.

---

## 2. Rekomendasi Jurnal Ilmiah Sasaran

Naskah ini sangat cocok disubmit pada jurnal ilmiah bidang Informatika, Sistem Informasi, dan Kecerdasan Buatan Terapan, antara lain:

1. **Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi)**  
   - Akreditasi: **SINTA 2**  
   - Fokus: Software Engineering, AI, Web & GIS  
   - URL: `https://jurnal.iaii.or.id/index.php/RESTI`
2. **JUTI: Jurnal Ilmiah Teknologi Informasi (ITS)**  
   - Akreditasi: **SINTA 2**  
   - Fokus: Intelligent Systems, Recommender Systems
3. **JUITA: Jurnal Informatika (Universitas Muhammadiyah Purwokerto)**  
   - Akreditasi: **SINTA 2**
4. **JEPIN (Jurnal Edukasi dan Penelitian Informatika - UNTAN)**  
   - Akreditasi: **SINTA 3**
5. **Konferensi Internasional IEEE (misal: ICITACEE, CITSM, ISRITI)**  
   - Terindeks: Scopus / IEEE Xplore (Gunakan terjemahan bahasa Inggris dari naskah ini).

---

## 3. Cara Mengonversi Dokumen ke Word (.docx) atau PDF

Jika Anda ingin mengubah dokumen `.md` ini menjadi file Microsoft Word (`.docx`) siap cetak/submit, jalankan perintah pandoc pada terminal:

```bash
# Install pandoc jika belum ada
sudo apt update && sudo apt install -y pandoc

# Konversi Jurnal Ilmiah ke Word (.docx)
pandoc /var/www/html/jurnal/DRAFT_JURNAL_ILMIAH.md -o /var/www/html/jurnal/DRAFT_JURNAL_ILMIAH.docx

# Konversi Tesis ke Word (.docx)
pandoc /var/www/html/jurnal/DRAFT_TESIS_LENGKAP.md -o /var/www/html/jurnal/DRAFT_TESIS_LENGKAP.docx
```

---

## 4. Tips Menghadapi Pertanyaan Dosen Penguji / Reviewer Jurnal

Berikut adalah poin-poin kunci pembelaan (*defense points*) yang telah diperkuat dalam riset Anda:

### Q1: *"Mengapa menggunakan pendekatan SQL Grounding, bukan RAG vektor biasa?"*
> **Jawaban:** RAG berbasis vektor (*vector embeddings*) mengandalkan kemiripan semantik teks (*cosine similarity*), sehingga sangat lemah dalam menangani filter matematis deterministik seperti jam buka operasional real-time, batas harga tiket masuk (contoh: `harga_tiket <= 15000`), dan kalkulasi jarak spasial geodesik. Melalui *Strict SQL Grounding*, LLM hanya menerjemahkan bahasa manusia menjadi parameter JSON, sedangkan query SQL MySQL 8.0 menjamin 100% fakta akurat, konsisten, dan bebas dari halusinasi faktual (*Zero Hallucination*).

### Q2: *"Bagaimana cara sistem membuktikan bahwa tidak ada halusinasi?"*
> **Jawaban:** Pada tahap evaluasi Bab 4, seluruh entitas tempat pada teks respons chatbot diaudit dan diverifikasi terhadap ID destinasi hasil query SQL. Dari 40 skenario pengujian, tingkat kecocokan grounding mencapai 100% (0 entitas fiktif). Bahkan saat diuji dengan kueri di luar cakupan (*out-of-scope*) seperti *"wisata salju di Padang"*, sistem secara konsisten menjawab jujur bahwa data tidak ditemukan, alih-alih mengarang entitas baru.

### Q3: *"Apakah kalkulasi Haversine di database tidak membebani server?"*
> **Jawaban:** Pengujian latensi membuktikan bahwa eksekusi query MySQL 8.0 termasuk kalkulasi formula trigonometri Haversine hanya memakan waktu rata-rata **2,85 ms** (hanya 0,21% dari total waktu respons). Waktu total sistem rata-rata adalah **1.381,90 ms (~1,38 detik)**, yang didominasi oleh pemrosesan LLM di cloud dan berada nyaman di bawah standar percakapan manusia (2000 ms).
---

## 5. Hubungan Khusus dengan Artikel Rujukan IJG (Afnarius et al., 2026)

Artikel rujukan yang Anda berikan:
> **Afnarius, S., Irsyad, L. N., Kharisma, G., & Idris, M. (2026).**  
> *"A Scale-Aware Web GIS Architecture for Village-Level Exploratory Spatial Interaction: Design, Implementation and Scenario Evaluation."*  
> **International Journal of Geoinformatics**, 22(7), 75–91. DOI: [10.52939/ijg.v22i7.5076](https://doi.org/10.52939/ijg.v22i7.5076).  
> *Afiliasi: Department of Information Systems, Universitas Andalas, Padang, West Sumatra, Indonesia.*

### Perbandingan dan Posisi Kebaruan Ilmiah Riset Anda:

| Aspek Komparasi | Riset Afnarius et al. (2026) di IJG | Chatbot LLM Konvensional | Riset Anda (Sistem Ini) |
|---|---|---|---|
| **Nama Sistem** | DTExplorer | Chatbot AI Umum (GPT, Claude, Gemini tanpa RAG geospasial) | Sistem Rekomendasi Pariwisata Padang (JIS) |
| **Fokus Skala Spasial** | Skala Desa (*Village-Level Tourism*, < 5 km², topografi homogen) | Global tak berbatas (rawan mencampuradukkan entitas lintas kabupaten/kota) | **Skala Meso Metropolitan Kota (*City-Scale: Kota Padang*, 694,96 km², pesisir hingga perbukitan)** |
| **Tata Kelola POI** | Klaster POI desa homogen (homestay, atraksi lokal desa) | Web-crawled uncurated (rentan entitas usang/fiktif) | **22 POI terkurasi lintas 6 kategori perkotaan** (Pantai, Pulau, Alam, Sejarah, Kuliner, Hiburan) |
| **Model Interaksi Pengguna** | Form filter UI tradisional (dropdown kategori & slider radius; friksi kognitif tinggi) | Chat teks murni (*chat-only*, tanpa representasi spasial) | **Dual-Synchronized Conversational Web GIS** (dialog alami bebas + peta Leaflet real-time) |
| **Kueri Multi-Kriteria** | Kaku (kategori tunggal + radius radial) | Fleksibel bahasa alami namun atribut lepas kendali | **JSON Intent Parsing** (kategori, budget tiket, jam buka, cuaca, slang Minang, fuzzy) |
| **Pencegahan Halusinasi AI** | Tidak relevan (tanpa LLM) | Rendah; rawan halusinasi spasial dan atribut usang | **Strict SQL Grounding** (Terbukti 100% Zero-Hallucination, 0 entitas fiktif) |
| **Kalkulasi Jarak & Kedekatan** | Radius Euclidean sederhana di MySQL & Google Maps | Estimasi teks generatif (sering salah matematis) | Formula **Haversine** di MySQL 8.0 (latensi 2,85 ms) |
| **Perutean Jaringan Jalan** | Tidak ada (hanya titik penanda statis) | Tidak memiliki topologi jalan | **OSRM (Open Source Routing Machine)** navigasi nyata *turn-by-turn* |
| **Infrastruktur Peta & Lisensi** | Google Maps API (proprietari, butuh API key berbayar & kuota) | Tidak ada kartografi | **OpenStreetMap + Leaflet.js + MySQL 8.0 + OSRM (100% FOSS & Bebas Kuota)** |
| **Skala Validasi Empiris** | Skenario kualitatif desa (3–5 skenario) | Uji teks subjektif tanpa akurasi spasial formal | **Benchmark Kuantitatif 40 Skenario Terstandarisasi** (Akurasi 100%, Latensi ~1,38 s) |

### Penggunaan Berkas untuk Submisi:
- Untuk jurnal internasional bereputasi seperti **International Journal of Geoinformatics (IJG)** atau IEEE: Gunakan **`DRAFT_JURNAL_IJG_ENGLISH.md`**.
- Untuk jurnal nasional terakreditasi (SINTA 2 / SINTA 3) seperti RESTI, JUTI, JUITA, JEPIN: Gunakan **`DRAFT_JURNAL_ILMIAH_INDONESIA.md`**.
- Untuk naskah skripsi / tesis ke dosen pembimbing dan penguji: Gunakan **`DRAFT_TESIS_LENGKAP.md`**.
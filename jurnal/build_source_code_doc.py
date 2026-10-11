#!/usr/bin/env python3
import os
import re
import html
import subprocess
import time
from pygments import highlight
from pygments.lexers import (
    PhpLexer, PythonLexer, SqlLexer, HtmlLexer,
    JsonLexer, BashLexer, XmlLexer, IniLexer, TextLexer
)
from pygments.formatters import HtmlFormatter

PROJECT_ROOT = "/var/www/html/Geo"
JURNAL_DIR = "/var/www/html/Geo/jurnal"
HTML_OUTPUT = os.path.join(JURNAL_DIR, "DOKUMENTASI_SOURCE_CODE_LENGKAP.html")
PDF_OUTPUT = os.path.join(JURNAL_DIR, "DOKUMENTASI_SOURCE_CODE_LENGKAP.pdf")

CATEGORIES = [
    {
        "id": "part1",
        "num": "I",
        "title": "ENTRY POINT & APPLICATION CONTROLLER LAYER",
        "desc": "Lapisan pengendali permintaan HTTP masuk (Front Controller) dan orkestrasi alur aplikasi web serta antarmuka RESTful API.",
        "files": [
            {
                "rel_path": "public/index.php",
                "lang": "php",
                "role": "Front Controller Entry Point",
                "desc": "Titik masuk tunggal (Single Entry Point) seluruh permintaan HTTP web server (Apache/Nginx) menuju kernel CodeIgniter 4. Bertanggung jawab mendefinisikan konstanta path sistem, menginisialisasi autoloader Composer, dan memicu bootstrapping kernel aplikasi."
            },
            {
                "rel_path": "app/Controllers/BaseController.php",
                "lang": "php",
                "role": "Base Controller Foundation",
                "desc": "Kelas dasar pengontrol yang mewarisi CodeIgniter\\Controller. Menginisialisasi komponen bersama seperti session, request filter, response emitter, dan helper fungsi yang digunakan oleh seluruh controller turunan."
            },
            {
                "rel_path": "app/Controllers/WebGisController.php",
                "lang": "php",
                "role": "WebGIS Presentation Controller",
                "desc": "Controller yang bertugas memuat dan merender antarmuka interaktif WebGIS (webgis.php). Menyediakan konfigurasi awal koordinat tengah Kota Padang (-0.9471, 100.4174) dan menginisialisasi state tampilan awal."
            },
            {
                "rel_path": "app/Controllers/ChatController.php",
                "lang": "php",
                "role": "Conversational AI & Grounding Orchestrator",
                "desc": "Controller utama pengelola endpoint /api/chat dan /api/places. Mengorkestrasi pipeline percakapan dwitunggal: mengelola sesi & riwayat pesan, memanggil LlmService untuk ekstraksi SIR, memvalidasi semantik melalui SirValidator, memicu kompilasi kueri SQL spasial ST_Distance_Sphere, membangun fakta terstruktur, memvalidasi narasi via GroundingValidator, serta mengeksekusi fail-closed fallback."
            },
            {
                "rel_path": "app/Controllers/Home.php",
                "lang": "php",
                "role": "Default Routing Controller",
                "desc": "Controller default instalasi CodeIgniter 4 yang menyediakan fungsi pengarah dasar."
            }
        ]
    },
    {
        "id": "part2",
        "num": "II",
        "title": "DUAL CONTROL BOUNDARIES & AI SPATIAL INTENT SERVICES",
        "desc": "Lapisan inti arsitektur penelitian yang mengimplementasikan Batas Kendali Semantik (Semantic Control Boundary) dan Batas Kendali Bukti (Evidence Control Boundary).",
        "files": [
            {
                "rel_path": "app/Services/SpatialIntent/SpatialIntent.php",
                "lang": "php",
                "role": "SIR & Canonical CSIR Data Transfer Object",
                "desc": "Mendefinisikan struktur data Spatial Intent Representation (SIR) dan Canonical SIR (CSIR). Mengenkapsulasi entitas semantik, batasan spasial (latitude, longitude, operator spasial, radius, unit jarak, tipe acuan referensi), batasan operasional (jam operasional, status buka, filter gratis, tarif maksimal, pengurutan), serta metadata audit kendali."
            },
            {
                "rel_path": "app/Services/SpatialIntent/SirValidator.php",
                "lang": "php",
                "role": "6-Dimensional Deterministic Semantic Validator",
                "desc": "Validator deterministik 6-dimensi yang menegakkan prinsip No Intent Alteration. Melakukan validasi ketat terhadap: (1) validitas format koordinat WGS84, (2) batas geofencing administratif Kota Padang, (3) operator spasial yang diizinkan, (4) batas radius positif, (5) taksonomi 6 kategori resmi wisata, dan (6) logika filter operasional/biaya."
            },
            {
                "rel_path": "app/Services/SpatialIntent/SpatialQueryCompiler.php",
                "lang": "php",
                "role": "Deterministic Spatial SQL Query Compiler",
                "desc": "Kompiler SQL non-LLM yang menerjemahkan objek CSIR tervalidasi secara deterministik menjadi kueri SQL terparameterisasi dengan fungsi spasial bawaan MySQL 8.0 ST_Distance_Sphere. Menjamin tidak terjadi SQL injection dan evaluasi jarak sferikal dilakukan secara matematis eksak."
            },
            {
                "rel_path": "app/Services/SpatialIntent/GroundedFactBuilder.php",
                "lang": "php",
                "role": "Relational Fact Normalizer & Builder",
                "desc": "Mengonversi hasil rekaman relasional basis data menjadi struktur fakta terstandarisasi (Grounded Facts). Fakta mencakup nama resmi, kategori, jarak sferikal, jam buka-tutup, status operasional saat ini, harga tiket, rating, fasilitas, dan alamat lengkap."
            },
            {
                "rel_path": "app/Services/SpatialIntent/GroundingValidator.php",
                "lang": "php",
                "role": "Claim-Level Grounding & Hallucination Auditor",
                "desc": "Validator tingkat klaim (Claim-Level Grounding Validator) yang mengaudit narasi keluaran LLM (Grounded NLG). Memverifikasi bahwa setiap nama destinasi, estimasi jarak, jam buka, dan harga tiket yang diklaim dalam narasi berakar 100% pada fakta basis data, serta memicu fallback penolakan aman jika ditemukan klaim fiktif."
            },
            {
                "rel_path": "app/Services/SpatialIntent/SpatialPolicyHandler.php",
                "lang": "php",
                "role": "Spatial Policy & Safe Fallback Handler",
                "desc": "Mengelola penanganan kebijakan penolakan kueri di luar lingkup domain (out-of-scope rejection), penyusunan respons klarifikasi pengguna (clarification policy), serta fail-closed fallback dengan pesan yang edukatif dan transparan."
            },
            {
                "rel_path": "app/Services/LlmService.php",
                "lang": "php",
                "role": "LLM Inference Client & Prompt Orchestrator",
                "desc": "Klien komunikasi API model bahasa besar (DeepSeek V3 / OpenAI API). Mengelola template system prompt ketat untuk ekstraksi CSIR dan sintesis narasi ramah pengguna (Grounded NLG), serta mendukung mock mode untuk keperluan benchmark deterministik."
            },
            {
                "rel_path": "app/Services/BenchmarkDataset.php",
                "lang": "php",
                "role": "Standardized 40 Benchmark Scenarios Dataset",
                "desc": "Dataset resmi berisi 40 skenario percakapan terstandarisasi untuk evaluasi empiris. Mencakup kueri spasial terdekat, radius berbatas, filter multi-kriteria waktu dan anggaran, kueri di luar lingkup pariwisata, dan penanganan kondisi lokasi ekstrem."
            }
        ]
    },
    {
        "id": "part3",
        "num": "III",
        "title": "DOMAIN DATA MODELS LAYER",
        "desc": "Lapisan model objek dan akses data relasional MySQL 8.0.",
        "files": [
            {
                "rel_path": "app/Models/WisataModel.php",
                "lang": "php",
                "role": "Tourism POI Spatial Model",
                "desc": "Model data relasional untuk entitas objek wisata (tabel wisata). Mengelola kueri CRUD, relasi join ke kategori, pencarian berbasis atribut objek wisata, dan eksekusi kueri spasial terkompilasi."
            },
            {
                "rel_path": "app/Models/KategoriModel.php",
                "lang": "php",
                "role": "Tourism Category Taxonomy Model",
                "desc": "Model data relasional untuk taksonomi kategori wisata (tabel kategori). Mengelola 6 kategori resmi: Pantai, Pulau, Alam/Air Terjun, Museum/Budaya, Sejarah/Religi, dan Kuliner Khas."
            },
            {
                "rel_path": "app/Models/ChatSessionModel.php",
                "lang": "php",
                "role": "User Chat Session & Geolocation Model",
                "desc": "Model data relasional untuk mengelola sesi pengguna (tabel chat_sessions), termasuk pembuatan token unik, penyimpanan koordinat GPS pengguna, dan pembaruan timestamp aktivitas."
            },
            {
                "rel_path": "app/Models/ChatMessageModel.php",
                "lang": "php",
                "role": "Conversation History & Audit Trail Model",
                "desc": "Model data relasional untuk riwayat pesan percakapan (tabel chat_messages). Menyimpan peranan (user/assistant), pesan teks, dan representasi JSON CSIR untuk jejak audit riset ilmiah."
            }
        ]
    },
    {
        "id": "part4",
        "num": "IV",
        "title": "PRESENTATION LAYER (USER INTERFACE & WEBGIS)",
        "desc": "Lapisan antarmuka pengguna interaktif, visualisasi spasial peta digital Leaflet.js, navigasi rute jalan OSRM, dan asisten percakapan cerdas.",
        "files": [
            {
                "rel_path": "app/Views/webgis.php",
                "lang": "html",
                "role": "Interactive WebGIS, Routing & Conversational Assistant View",
                "desc": "Antarmuka terpadu satu jendela dialog yang mengintegrasikan peta interaktif Leaflet.js, layer OpenStreetMap, marker POI kustom, dialog chatbot AI, polyline rute jalan raya nyata via OSRM, pelacakan GPS HTML5 Geolocation API, serta panel kartu informasi detail destinasi."
            }
        ]
    },
    {
        "id": "part5",
        "num": "V",
        "title": "DATABASE ARCHITECTURE, MIGRATIONS & SEED DATA",
        "desc": "Skema basis data relasional MySQL 8.0, migrasi DDL, seeder data 22 objek wisata terkurasi, dan cadangan basis data lengkap.",
        "files": [
            {
                "rel_path": "app/Database/Migrations/2026-09-20-000001_CreateTourismSchema.php",
                "lang": "php",
                "role": "Database Schema DDL Migration",
                "desc": "Skrip migrasi CodeIgniter 4 yang membangun struktur 4 tabel relasional MySQL 8.0: kategori, wisata (lengkap dengan kolom latitude, longitude, dan geom POINT SRID 4326), chat_sessions, dan chat_messages beserta relasi foreign key dan indeks spasial."
            },
            {
                "rel_path": "app/Database/Seeds/WisataSeeder.php",
                "lang": "php",
                "role": "Curated 22 POIs Dataset Seeder",
                "desc": "Seeder data primer yang memasukkan data 6 kategori resmi dan 22 destinasi wisata unggulan Kota Padang dari Dinas Pariwisata Kota Padang lengkap dengan koordinat geospasial presisi, jadwal buka-tutup, harga tiket masuk, rating, dan fasilitas."
            },
            {
                "rel_path": "database_backup_geo_db.sql",
                "lang": "sql",
                "role": "Complete MySQL Database Backup & DDL/DML Dump",
                "desc": "Salinan dump SQL basis data MySQL 8.0 geo_db mencakup definisi struktur tabel (DDL), primary keys, foreign keys, indeks spasial, data kategori, dan inventaris 22 destinasi wisata Kota Padang."
            }
        ]
    },
    {
        "id": "part6",
        "num": "VI",
        "title": "CLI EVALUATION BENCHMARKS & COMMAND RUNNERS",
        "desc": "Perintah antarmuka baris perintah (CLI) untuk eksekusi pengujian otomatis 40 skenario evaluasi dan runner Spark CodeIgniter 4.",
        "files": [
            {
                "rel_path": "app/Commands/RisetEvaluasi.php",
                "lang": "php",
                "role": "Spark CLI Benchmark Evaluation Runner",
                "desc": "Perintah CLI kustom (php spark riset:evaluasi) untuk menjalankan pengujian batch otomatis terhadap 40 skenario benchmark. Mengukur metrik akurasi ekstraksi CSIR, akurasi kategori, kebenaran predikat spasial, grounding fidelity, latensi end-to-end, dan latensi kueri spasial SQL MySQL 8.0."
            },
            {
                "rel_path": "spark",
                "lang": "php",
                "role": "CodeIgniter 4 CLI Executable Runner",
                "desc": "Skrip executable runner untuk antarmuka baris perintah CodeIgniter 4 yang memicu eksekusi perintah kustom, migrasi, dan seeder."
            }
        ]
    },
    {
        "id": "part7",
        "num": "VII",
        "title": "AUTOMATED UNIT & INTEGRATION TESTING SUITE",
        "desc": "Rangkaian pengujian unit otomatis PHPUnit untuk memverifikasi invarian keamanan, validasi SIR, kompilasi kueri SQL spasial, dan mitigasi halusinasi.",
        "files": [
            {
                "rel_path": "tests/unit/SirValidatorTest.php",
                "lang": "php",
                "role": "SirValidator 6D Invariants Unit Test",
                "desc": "Pengujian unit otomatis untuk memverifikasi keandalan SirValidator dalam menangani koordinat invalid, radius negatif, kategori fiktif, kueri di luar lingkup domain, dan penerapan fallback pusat kota."
            },
            {
                "rel_path": "tests/unit/SpatialQueryCompilerTest.php",
                "lang": "php",
                "role": "SpatialQueryCompiler & ST_Distance_Sphere Unit Test",
                "desc": "Pengujian unit otomatis untuk memverifikasi kebenaran sintaks SQL spasial terkompilasi, parameter binding yang aman, dan perhitungan jarak sferikal ST_Distance_Sphere."
            },
            {
                "rel_path": "tests/unit/GroundingValidatorTest.php",
                "lang": "php",
                "role": "Claim Grounding & Fallback Unit Test",
                "desc": "Pengujian unit otomatis untuk memverifikasi kemampuan GroundingValidator dalam menolak klaim tanpa bukti faktual, mendeteksi entitas fiktif (halusinasi), dan memicu penolakan aman."
            },
            {
                "rel_path": "tests/unit/HealthTest.php",
                "lang": "php",
                "role": "System Health & Integration Test",
                "desc": "Pengujian unit otomatis untuk memastikan kesiapan autoloader, environment CI4, dan keterhubungan dependensi framework."
            },
            {
                "rel_path": "phpunit.dist.xml",
                "lang": "xml",
                "role": "PHPUnit Test Suite Configuration",
                "desc": "Berkas konfigurasi resmi XML PHPUnit untuk eksekusi otomatis rangkaian pengujian unit sistem, direktori test, dan pengaturan environment testing."
            }
        ]
    },
    {
        "id": "part8",
        "num": "VIII",
        "title": "SYSTEM CONFIGURATION & DEPLOYMENT INFRASTRUCTURE",
        "desc": "Konfigurasi inti framework, koneksi database, routing, CORS, HTTP client, paket Composer, variabel lingkungan, dan unit service systemd Linux.",
        "files": [
            {
                "rel_path": "app/Config/Routes.php",
                "lang": "php",
                "role": "HTTP URL Routing Configuration",
                "desc": "Pemetaan rute URL aplikasi ke controller yang sesuai, mencakup tampilan WebGIS utama (/), endpoint kirim pesan (/api/chat), dan endpoint katalog objek wisata (/api/places)."
            },
            {
                "rel_path": "app/Config/Database.php",
                "lang": "php",
                "role": "MySQL 8.0 Database Connection Configuration",
                "desc": "Pengaturan koneksi basis data MySQLi, konfigurasi host, kredensial pengguna, basis data geo_db, port 3306, dan pengaturan charset utf8mb4."
            },
            {
                "rel_path": "app/Config/App.php",
                "lang": "php",
                "role": "Application Core Configuration",
                "desc": "Pengaturan URL basis aplikasi, timezone resmi Asia/Jakarta, locale bahasa Indonesia (id), dan penanganan routing index page."
            },
            {
                "rel_path": "app/Config/CURLRequest.php",
                "lang": "php",
                "role": "HTTP Client Configuration",
                "desc": "Konfigurasi HTTP client CodeIgniter 4 untuk koneksi API eksternal (LLM API dan OSRM routing) dengan pengaturan timeout, SSL verification, dan user-agent."
            },
            {
                "rel_path": "app/Config/Cors.php",
                "lang": "php",
                "role": "Cross-Origin Resource Sharing (CORS) Policy",
                "desc": "Konfigurasi kebijakan keamanan CORS untuk mengatur izin akses lintas domain pada endpoint API /api/*."
            },
            {
                "rel_path": "composer.json",
                "lang": "json",
                "role": "Composer Package & Dependency Manifest",
                "desc": "Manifest dependensi pustaka PHP, mencakup paket codeigniter4/framework, ekstensi curl, intl, mbstring, dan autoloader namespace PSR-4."
            },
            {
                "rel_path": "env",
                "lang": "ini",
                "role": "Sanitized Environment Variables Template",
                "desc": "Template berkas konfigurasi variabel lingkungan server (.env) yang telah disanitasi untuk mode produksi/pengembangan, kredensial basis data, dan kunci API."
            },
            {
                "rel_path": "geo-ci4.service",
                "lang": "ini",
                "role": "Systemd Web Server CI4 Service Unit",
                "desc": "Unit service Linux systemd untuk menjalankan proses daemon web server CodeIgniter 4 di latar belakang pada port 8080 secara otomatis saat sistem Linux menyala."
            },
            {
                "rel_path": "geo-tunnel.service",
                "lang": "ini",
                "role": "Systemd External Secure Tunnel Service Unit",
                "desc": "Unit service Linux systemd untuk mengelola reverse tunnel publik aman sehingga sistem WebGIS lokal dapat diakses secara publik via HTTPS untuk kebutuhan demonstrasi."
            }
        ]
    },
    {
        "id": "part9",
        "num": "IX",
        "title": "BENCHMARK REPRODUCIBILITY SUITE & BASELINE RUNNERS",
        "desc": "Paket skrip pengujian komparatif eksperimental, runner baseline Text-to-SQL dan Unconstrained LLM, kontrak skema DDL, serta protokol reproduktibilitas riset independen.",
        "files": [
            {
                "rel_path": "benchmark/run_all.sh",
                "lang": "bash",
                "role": "Master Reproducibility Benchmark Runner Script",
                "desc": "Skrip shell master otomasi untuk mengeksekusi seluruh suite benchmark komparatif (Proposed, Baseline 1, Baseline 2, dan Ablation Study) dalam satu perintah terpadu."
            },
            {
                "rel_path": "benchmark/proposed/evaluator.php",
                "lang": "php",
                "role": "Proposed Full Architecture Evaluator",
                "desc": "Runner evaluasi lengkap arsitektur usulan yang mengeksekusi 40 skenario pengujian dengan Dual Control Boundaries, validasi SIR 6-dimensi, dan kalkulasi akurasi CSIR field-level."
            },
            {
                "rel_path": "benchmark/baseline_text2sql/runner.php",
                "lang": "php",
                "role": "Baseline 1: Text-to-SQL Runner",
                "desc": "Runner pembanding baseline Text-to-SQL tanpa kontrol semantik perantara yang menguji kerentanan halusinasi skema dan kegagalan predicate matching."
            },
            {
                "rel_path": "benchmark/baseline_text2sql/prompt.txt",
                "lang": "text",
                "role": "Baseline 1: DDL Table Schema Prompt Contract",
                "desc": "Kontrak prompt baseline 1 yang menyediakan skema DDL tabel MySQL untuk evaluasi Text-to-SQL langsung."
            },
            {
                "rel_path": "benchmark/baseline_unconstrained/runner.php",
                "lang": "php",
                "role": "Baseline 2: Unconstrained LLM Runner",
                "desc": "Runner pembanding baseline Unconstrained LLM yang mengeksekusi rekomendasi pariwisata secara bebas tanpa basis data verifikasi untuk mengukur fabrikasi entitas POI."
            },
            {
                "rel_path": "benchmark/baseline_unconstrained/prompt.txt",
                "lang": "text",
                "role": "Baseline 2: Direct Tourism Prompt Contract",
                "desc": "Kontrak prompt baseline 2 yang menginstruksikan LLM merekomendasikan destinasi wisata Kota Padang secara mandiri tanpa grounding basis data."
            },
            {
                "rel_path": "benchmark/ablation/runner.php",
                "lang": "php",
                "role": "Ablation Study A1-A6 & B1-B2 Runner",
                "desc": "Runner studi ablasi bertingkat yang mengeksekusi skema leave-one-out invariant ablation pada SirValidator (A1-A6) dan policy ablation (B1-B2) pada 40 skenario benchmark."
            },
            {
                "rel_path": "benchmark/README.md",
                "lang": "text",
                "role": "Benchmark Protocol & Reproducibility Documentation",
                "desc": "Dokumentasi protokol replikasi eksperimen, deskripsi metrik, petunjuk eksekusi CLI spark riset:evaluasi, dan panduan audit reproduktibilitas komparatif."
            }
        ]
    },
    {
        "id": "part10",
        "num": "X",
        "title": "RESEARCH PIPELINE & AUTOMATION UTILITIES",
        "desc": "Skrip Python otomatisasi riset untuk kompilasi dokumen ilmiah PDF, pembuatan diagram arsitektur resolusi tinggi, penelusuran alur eksekusi, dan penyelarasan dataset geospasial.",
        "files": [
            {
                "rel_path": "jurnal/generate_diagrams.py",
                "lang": "python",
                "role": "Scientific Diagram Generator for Research Paper",
                "desc": "Skrip Python berbasis Matplotlib untuk menghasilkan diagram arsitektur kendali ganda, perbandingan latensi eksekusi kueri, dan grafik evaluasi akurasi untuk publikasi jurnal ilmiah."
            },
            {
                "rel_path": "jurnal/generate_thesis_diagrams.py",
                "lang": "python",
                "role": "High-Resolution Thesis Diagrams Generator",
                "desc": "Skrip Python visualisasi khusus untuk menghasilkan set diagram ilmiah berstandar tesis S2 Magister Ilmu Komputer."
            },
            {
                "rel_path": "jurnal/generate_trace_diagram.py",
                "lang": "python",
                "role": "Conversational Request Trace Diagram Generator",
                "desc": "Skrip Python untuk memvisualisasikan alur penelusuran permintaan percakapan langkah demi langkah dari masukan pengguna hingga penyajian rute jalan raya pada peta."
            },
            {
                "rel_path": "jurnal/generate_pdf.py",
                "lang": "python",
                "role": "Academic Document Compiler (Markdown to PDF/DOCX)",
                "desc": "Skrip Python kompilator naskah tesis dan jurnal ilmiah dari format Markdown ke PDF dan DOCX berstandar tipografi akademis A4 menggunakan Pandoc dan Chrome Headless."
            },
            {
                "rel_path": "jurnal/align_geo_stack.py",
                "lang": "python",
                "role": "Geospatial Stack & Dataset Alignment Utility",
                "desc": "Skrip Python utilitas audit integritas untuk menyelaraskan data koordinat geospasial 22 POI wisata antara basis data MySQL, seeder, naskah tesis, dan naskah jurnal internasional."
            }
        ]
    }
]

def sanitize_code(rel_path, content):
    """Sanitize sensitive keys/passwords in config files for academic documentation."""
    # Redact Cloudflare Tunnel token
    content = re.sub(r'(--token\s+)([A-Za-z0-9_\-\.]{20,})', r'\1[REDACTED_CLOUDFLARE_TUNNEL_TOKEN]', content)
    content = re.sub(r'(TUNNEL_TOKEN\s*=\s*["\']?)([^"\'\n]+)(["\']?)', r'\1[REDACTED_CLOUDFLARE_TUNNEL_TOKEN]\3', content)
    
    # Redact LLM API keys
    content = re.sub(r'(sk-[A-Za-z0-9_\-]{15,})', r'sk-[REDACTED_API_KEY]', content)
    content = re.sub(r'(llm\.apiKey\s*=\s*["\'])([^"\']+)(["\'])', r'\1sk-[REDACTED_API_KEY]\3', content)
    content = re.sub(r'(LLM_API_KEY\s*=\s*["\'])([^"\']+)(["\'])', r'\1sk-[REDACTED_API_KEY]\3', content)

    # Redact Database password
    content = re.sub(r'(database\.default\.password\s*=\s*["\'])([^"\']+)(["\'])', r'\1[REDACTED_DB_PASSWORD]\3', content)
    content = re.sub(r'(\'password\'\s*=>\s*["\'])([^"\']+)(["\'])', r'\1[REDACTED_DB_PASSWORD]\3', content)
    content = re.sub(r'(GeoSecurePass[0-9a-zA-Z_]+)', r'[REDACTED_DB_PASSWORD]', content)
    
    # For large SQL dump, format the chat_messages dump so it's clean and doesn't have 40KB single lines
    if rel_path == "database_backup_geo_db.sql":
        lines = content.splitlines()
        clean_lines = []
        for line in lines:
            if line.startswith("INSERT INTO `chat_messages` VALUES"):
                # Cleanly wrap or provide representative records
                clean_lines.append("-- [Catatan Dokumentasi: Data rekaman pesan pengujian sistem (76 baris riwayat percakapan benchmark)]")
                # Format into readable SQL
                formatted_insert = line.replace("),(", "),\n  (")
                clean_lines.append(formatted_insert[:3500] + "\n  -- ... [Riwayat pesan benchmark dipadatkan demi efisiensi cetak dokumen] ...\n;")
            elif line.startswith("INSERT INTO `wisata` VALUES"):
                formatted_insert = line.replace("),(", "),\n  (")
                clean_lines.append(formatted_insert)
            else:
                clean_lines.append(line)
        content = "\n".join(clean_lines)

    return content

def get_lexer(rel_path, lang):
    if lang == "php":
        return PhpLexer(startinline=True)
    elif lang == "python":
        return PythonLexer()
    elif lang == "sql":
        return SqlLexer()
    elif lang == "html":
        return HtmlLexer()
    elif lang == "json":
        return JsonLexer()
    elif lang == "bash":
        return BashLexer()
    elif lang == "xml":
        return XmlLexer()
    elif lang == "ini":
        return IniLexer()
    return TextLexer()

def main():
    print("[*] Menginisialisasi pembuatan Buku Dokumentasi Kode Sumber Lengkap...")
    start_time = time.time()

    # Formatter Pygments dengan inline linenos
    formatter = HtmlFormatter(style='friendly', linenos='inline', cssclass='code-highlight')
    pygments_css = formatter.get_style_defs('.code-highlight')

    # Hitung metrik keseluruhan
    total_files = 0
    total_loc = 0
    total_bytes = 0

    all_file_records = []

    for part in CATEGORIES:
        for f in part["files"]:
            full_path = os.path.join(PROJECT_ROOT, f["rel_path"])
            if os.path.exists(full_path):
                size = os.path.getsize(full_path)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                raw_loc = len(content.splitlines())
                total_files += 1
                total_loc += raw_loc
                total_bytes += size
                all_file_records.append({
                    "part_num": part["num"],
                    "part_id": part["id"],
                    "part_title": part["title"],
                    "rel_path": f["rel_path"],
                    "lang": f["lang"],
                    "role": f["role"],
                    "desc": f["desc"],
                    "loc": raw_loc,
                    "bytes": size,
                    "content": content
                })
            else:
                print(f"[!] Warning: File tidak ditemukan: {f['rel_path']}")

    print(f"[✓] Berhasil mengindeks {total_files} berkas program | Total: {total_loc:,} Baris Kode (LOC) | {total_bytes:,} Bytes")

    # CSS Dokumen Lengkap
    css = f"""
    @page {{
        size: A4 portrait;
        margin: 22mm 16mm 22mm 16mm;
        @top-left {{
            content: "DOKUMENTASI KODE SUMBER LENGKAP SISTEM (SOURCE CODE LISTINGS)";
            font-family: "Liberation Sans", "Helvetica Neue", Arial, sans-serif;
            font-size: 7.2pt;
            font-weight: bold;
            color: #334155;
            border-bottom: 0.5pt solid #cbd5e1;
            padding-bottom: 4px;
        }}
        @top-right {{
            content: "RELIABILITY-CONTROLLED SPATIAL GIS - PADANG";
            font-family: "Liberation Sans", "Helvetica Neue", Arial, sans-serif;
            font-size: 7.2pt;
            color: #64748b;
            border-bottom: 0.5pt solid #cbd5e1;
            padding-bottom: 4px;
        }}
        @bottom-left {{
            content: "Hendra Setyawan (Magister Ilmu Komputer) • CodeIgniter 4 / MySQL 8.0 Spatial";
            font-family: "Liberation Sans", "Helvetica Neue", Arial, sans-serif;
            font-size: 7.2pt;
            color: #64748b;
            border-top: 0.5pt solid #e2e8f0;
            padding-top: 4px;
        }}
        @bottom-right {{
            content: "Halaman " counter(page);
            font-family: "Liberation Sans", "Helvetica Neue", Arial, sans-serif;
            font-size: 7.2pt;
            font-weight: bold;
            color: #0f172a;
            border-top: 0.5pt solid #e2e8f0;
            padding-top: 4px;
        }}
    }}

    @page:first {{
        margin: 0;
        @top-left {{ content: ""; border: none; }}
        @top-right {{ content: ""; border: none; }}
        @bottom-left {{ content: ""; border: none; }}
        @bottom-right {{ content: ""; border: none; }}
    }}

    * {{
        box-sizing: border-box;
    }}

    body {{
        font-family: "Liberation Sans", "Helvetica Neue", Arial, sans-serif;
        font-size: 9pt;
        line-height: 1.45;
        color: #1e293b;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }}

    /* COVER PAGE */
    .cover-container {{
        width: 100%;
        min-height: 297mm;
        height: 297mm;
        padding: 35mm 25mm 25mm 25mm;
        background: linear-gradient(145deg, #091a32 0%, #11294d 45%, #1a3a69 100%);
        color: #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        page-break-after: always;
        break-after: page;
        box-sizing: border-box;
    }}

    .cover-top {{
        border-bottom: 2px solid #38bdf8;
        padding-bottom: 20px;
    }}

    .cover-tagline {{
        font-size: 10pt;
        font-weight: 700;
        letter-spacing: 2px;
        color: #38bdf8;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .cover-title {{
        font-size: 20pt;
        font-weight: 800;
        line-height: 1.25;
        color: #ffffff;
        margin: 0 0 12px 0;
    }}

    .cover-subtitle {{
        font-size: 11pt;
        line-height: 1.5;
        color: #cbd5e1;
        margin: 0 0 15px 0;
    }}

    .cover-paradigm {{
        display: inline-block;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 9.5pt;
        color: #7dd3fc;
        font-weight: 600;
    }}

    .cover-middle {{
        margin: 25px 0;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        border-left: 4px solid #38bdf8;
    }}

    .cover-middle table {{
        width: 100%;
        border-collapse: collapse;
        color: #f1f5f9;
        font-size: 9.5pt;
    }}

    .cover-middle td {{
        padding: 6px 10px;
        vertical-align: top;
    }}

    .cover-middle td.label {{
        width: 25%;
        color: #94a3b8;
        font-weight: 600;
    }}

    .cover-middle td.val {{
        font-weight: 600;
        color: #ffffff;
    }}

    .cover-badges {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 15px;
    }}

    .badge {{
        background: #1e293b;
        color: #e2e8f0;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 8pt;
        font-weight: 600;
        border: 1px solid #334155;
    }}

    .badge.accent {{
        background: #0369a1;
        color: #ffffff;
        border-color: #38bdf8;
    }}

    .cover-bottom {{
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        padding-top: 18px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        font-size: 8.5pt;
        color: #94a3b8;
    }}

    /* SECTIONS */
    .page-break {{
        page-break-before: always;
        break-before: page;
    }}

    h1.section-title {{
        font-size: 14pt;
        font-weight: 800;
        color: #0f172a;
        border-bottom: 2px solid #0284c7;
        padding-bottom: 6px;
        margin-top: 0;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    h2.subsection-title {{
        font-size: 11pt;
        font-weight: 700;
        color: #1e293b;
        margin-top: 14px;
        margin-bottom: 6px;
    }}

    p {{
        margin-top: 0;
        margin-bottom: 8px;
        text-align: justify;
    }}

    /* PREVIEW & SUMMARY BOXES */
    .callout {{
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0284c7;
        padding: 10px 14px;
        margin-bottom: 14px;
        border-radius: 4px;
        font-size: 8.8pt;
    }}

    .callout-title {{
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
    }}

    /* TABLES */
    table.data-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 8pt;
        margin-bottom: 15px;
    }}

    table.data-table th {{
        background-color: #f1f5f9;
        color: #0f172a;
        font-weight: 700;
        text-align: left;
        padding: 6px 8px;
        border: 1px solid #cbd5e1;
        font-size: 8pt;
    }}

    table.data-table td {{
        padding: 5px 8px;
        border: 1px solid #e2e8f0;
        vertical-align: top;
    }}

    table.data-table tr:nth-child(even) {{
        background-color: #f8fafc;
    }}

    table.data-table tr.total-row {{
        background-color: #e2e8f0;
        font-weight: bold;
    }}

    /* FILE BANNER */
    .file-container {{
        margin-bottom: 24px;
        page-break-inside: auto;
    }}

    .file-banner {{
        background: #0f172a;
        color: #ffffff;
        padding: 8px 12px;
        border-radius: 5px 5px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        page-break-after: avoid;
        break-after: avoid;
    }}

    .file-banner-title {{
        font-family: "Liberation Mono", Consolas, monospace;
        font-size: 8.8pt;
        font-weight: 700;
        color: #38bdf8;
    }}

    .file-banner-meta {{
        font-size: 7.5pt;
        color: #cbd5e1;
        display: flex;
        gap: 12px;
    }}

    .file-desc-box {{
        background: #f1f5f9;
        border-left: 1px solid #cbd5e1;
        border-right: 1px solid #cbd5e1;
        border-bottom: 1px solid #cbd5e1;
        padding: 6px 12px;
        font-size: 8.2pt;
        color: #334155;
        page-break-after: avoid;
        break-after: avoid;
    }}

    .file-desc-box strong {{
        color: #0f172a;
    }}

    /* CODE HIGHLIGHT CONTAINER */
    .code-box {{
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-top: none;
        border-radius: 0 0 5px 5px;
        overflow: hidden;
        margin-bottom: 16px;
    }}

    .code-highlight {{
        font-family: "Liberation Mono", Consolas, "Courier New", monospace !important;
        font-size: 7.4pt !important;
        line-height: 1.34 !important;
        margin: 0 !important;
        padding: 8px 10px !important;
        background-color: #ffffff !important;
        white-space: pre-wrap !important;
        word-break: break-all !important;
        tab-size: 4 !important;
    }}

    .code-highlight pre {{
        margin: 0 !important;
        padding: 0 !important;
        font-family: inherit !important;
        font-size: inherit !important;
        line-height: inherit !important;
        white-space: pre-wrap !important;
    }}

    /* LINENO STYLING */
    span.lineno {{
        color: #94a3b8 !important;
        user-select: none !important;
        margin-right: 1.2em !important;
        display: inline-block !important;
        width: 3.2em !important;
        text-align: right !important;
        border-right: 1.5px solid #e2e8f0 !important;
        padding-right: 0.8em !important;
        font-weight: 500 !important;
    }}

    /* DIAGRAM & TREE PRE */
    pre.diagram-box {{
        background: #0f172a;
        color: #38bdf8;
        font-family: "Liberation Mono", monospace;
        font-size: 7.4pt;
        line-height: 1.35;
        padding: 12px;
        border-radius: 6px;
        overflow-x: hidden;
        white-space: pre;
        margin: 10px 0 16px 0;
    }}

    /* TOC STYLING */
    .toc-item {{
        display: flex;
        justify-content: space-between;
        padding: 3px 0;
        border-bottom: 1px dotted #cbd5e1;
        font-size: 8.5pt;
    }}

    .toc-part {{
        font-weight: bold;
        color: #0369a1;
        margin-top: 10px;
        margin-bottom: 4px;
        font-size: 9pt;
        text-transform: uppercase;
    }}

    .toc-path {{
        font-family: "Liberation Mono", monospace;
        color: #1e293b;
        text-decoration: none;
        font-size: 8.2pt;
    }}

    .toc-meta {{
        color: #64748b;
        font-size: 7.8pt;
    }}

    {pygments_css}
    """

    # Mulai rakit dokumen HTML
    html_parts = []
    html_parts.append("<!DOCTYPE html>\n<html lang='id'>\n<head>\n<meta charset='utf-8'>\n")
    html_parts.append(f"<title>Dokumentasi Kode Sumber Lengkap Sistem - {total_files} Berkas ({total_loc:,} LOC)</title>\n")
    html_parts.append(f"<style>\n{css}\n</style>\n</head>\n<body>\n")

    # ==========================================
    # 1. COVER PAGE
    # ==========================================
    html_parts.append(f"""
    <div class="cover-container">
        <div class="cover-top">
            <div class="cover-tagline">Dokumen Lampiran Naskah Tesis & Repositori Kode Sumber Resmi</div>
            <div class="cover-title">DOKUMENTASI KODE SUMBER LENGKAP<br>KESELURUHAN PROGRAM</div>
            <div class="cover-subtitle">
                <strong>Sistem Rekomendasi Pariwisata Berbasis Large Language Model (LLM) dan Strict SQL Grounding untuk Pemberian Saran Destinasi Wisata Cerdas</strong><br>
                <em>(Studi Kasus: Kawasan Pariwisata Kota Padang, Sumatera Barat)</em>
            </div>
            <div class="cover-paradigm">
                Reliability-Controlled Conversational Spatial Information System via Dual Control Boundaries
            </div>
        </div>

        <div class="cover-middle">
            <table>
                <tr>
                    <td class="label">Peneliti / Pengembang</td>
                    <td class="val">: <strong>Hendra Setyawan, S.Kom.</strong></td>
                </tr>
                <tr>
                    <td class="label">Program Studi / Jenjang</td>
                    <td class="val">: Magister Ilmu Komputer (S2)</td>
                </tr>
                <tr>
                    <td class="label">Framework Aplikasi</td>
                    <td class="val">: CodeIgniter 4 (PHP 8.2+ Architecture)</td>
                </tr>
                <tr>
                    <td class="label">Mesin Basis Data & Spasial</td>
                    <td class="val">: MySQL 8.0 Spatial (Fungsi Bawaan <code>ST_Distance_Sphere</code> & Indeks Relasional Komposit (lat, lng))</td>
                </tr>
                <tr>
                    <td class="label">Layanan Inferensi AI</td>
                    <td class="val">: Large Language Model (DeepSeek V3 / OpenAI API) dengan Kontrak SIR/CSIR Deterministik</td>
                </tr>
                <tr>
                    <td class="label">Mesin Pemetaan & Rute</td>
                    <td class="val">: Leaflet.js 1.9.4 + OpenStreetMap Tiles + Open Source Routing Machine (OSRM) Polyline Engine</td>
                </tr>
                <tr>
                    <td class="label">Total Kode Sumber</td>
                    <td class="val">: <strong>{total_files} Berkas Lengkap</strong> | <strong>{total_loc:,} Baris Kode (LOC)</strong> | <strong>{total_bytes/1024:.1f} KB</strong></td>
                </tr>
                <tr>
                    <td class="label">Status Verifikasi Sistem</td>
                    <td class="val">: 100% Lolos Uji PHPUnit Test Suite (29 Unit Tests, 92 Assertions)</td>
                </tr>
            </table>

            <div class="cover-badges">
                <span class="badge accent">CodeIgniter 4.5+</span>
                <span class="badge accent">PHP 8.2 Strict Types</span>
                <span class="badge accent">MySQL 8.0 Spatial</span>
                <span class="badge">ST_Distance_Sphere</span>
                <span class="badge">Leaflet.js 1.9.4</span>
                <span class="badge">OSRM Routing</span>
                <span class="badge">DeepSeek LLM</span>
                <span class="badge">Dual Control Boundaries</span>
                <span class="badge">Strict SQL Grounding</span>
                <span class="badge">Python 3.12 Automation</span>
            </div>
        </div>

        <div class="cover-bottom">
            <div>
                <strong>PROGRAM PASCASARJANA ILMU KOMPUTER</strong><br>
                Padang, Sumatera Barat • Tahun Akademik 2026
            </div>
            <div style="text-align: right;">
                <strong>Repositori:</strong> Hendrasetyawan1945/Geo<br>
                <strong>Build Version:</strong> v1.0.0-Evaluated-Release
            </div>
        </div>
    </div>
    """)

    # ==========================================
    # 2. KATA PENGANTAR & ARSITEKTUR SISTEM
    # ==========================================
    html_parts.append("""
    <div class="page-break"></div>
    <h1 class="section-title">KATA PENGANTAR & SPESIFIKASI ARSITEKTUR PROGRAM</h1>
    
    <div class="callout">
        <div class="callout-title">Tujuan Penyusunan Dokumen</div>
        Dokumen ini menyajikan pencatatan kode sumber lengkap secara menyeluruh (<em>Full Source Code Listing</em>) dari sistem 
        <strong>Reliability-Controlled Conversational Spatial Information System</strong> untuk Kawasan Pariwisata Kota Padang. 
        Dokumen ini disusun sebagai lampiran teknis resmi naskah Tesis dan naskah publikasi ilmiah guna menjamin transparansi riset, 
        keterulangan eksperimen (<em>research reproducibility</em>), dan verifikasi implementasi perangkat lunak berstandar rekayasa 
        perangkat lunak (<em>software engineering</em>).
    </div>

    <h2 class="subsection-title">1. Paradigma Batas Kendali Ganda (Dual Control Boundaries)</h2>
    <p>
        Penerapan model bahasa generatif murni (<em>unconstrained LLM</em>) pada domain geospasial rentan terhadap halusinasi faktual 
        dan distorsi estimasi spasial. Sistem ini mengisolasi sifat probabilistik LLM melalui dua batas kendali deterministik:
    </p>
    <p>
        <strong>1. Batas Kendali Semantik (Semantic Control Boundary):</strong> Menyalurkan inferensi pemahaman bahasa alami pengguna ke dalam 
        skema formal <em>Spatial Intent Representation</em> (SIR). Modul validator deterministik 6-dimensi (<code>SirValidator</code>) 
        menegakkan prinsip <em>No Intent Alteration</em> guna memvalidasi batas administratif Kota Padang, format koordinat WGS84, 
        operator spasial, dan taksonomi kategori sebelum dikompilasi menjadi representasi kanonikal (CSIR).
    </p>
    <p>
        <strong>2. Batas Kendali Bukti (Evidence Control Boundary):</strong> Menolak kewenangan LLM memproduksi kueri basis data. Kompiler 
        kueri non-LLM (<code>SpatialQueryCompiler</code>) secara deterministik mengubah CSIR menjadi SQL terparameterisasi dengan 
        fungsi bawaan MySQL 8.0 <code>ST_Distance_Sphere</code>. Narasi ramah pengguna disintesis di bawah kontrak grounding ketat 
        (<em>Grounded NLG</em>) dan diverifikasi oleh <code>GroundingValidator</code> di tingkat klaim (<em>Claim-Level Grounding</em>) 
        dengan mekanisme <em>fail-closed fallback</em> guna menjamin tidak ada klaim tanpa bukti faktual yang sampai ke pengguna.
    </p>

    <h2 class="subsection-title">2. Diagram Alur Eksekusi Data (Data Flow Architecture)</h2>
    <pre class="diagram-box">
+-------------------------------------------------------------------------------------------------------+
|                                ALUR ARSITEKTUR KENDALI GANDA (DUAL CONTROL BOUNDARIES)                |
+-------------------------------------------------------------------------------------------------------+
 [Pengguna] ---> (Pesan Teks & Koordinat GPS) 
      |
      v
 [WebGisController / ChatController]
      |
      |==== [1. SEMANTIC CONTROL BOUNDARY] =============================================================+
      |  (a) Ekstraksi Semantik Probabilistik : LLM Inference (DeepSeek V3 / OpenAI API)                |
      |      --> Menghasilkan DTO Spatial Intent Representation (SIR)                                   |
      |  (b) Validasi Invarian Deterministik : SirValidator (6-Dimensi, No Intent Alteration)          |
      |      --> Memvalidasi Invarian Koordinat, Geofencing Padang, Operator, Radius, Taksonomi        |
      |      --> Menghasilkan Canonical SIR (CSIR) Tervalidasi                                          |
      +=================================================================================================+
      |
      |==== [2. EVIDENCE CONTROL BOUNDARY] =============================================================+
      |  (a) Kompilasi SQL Deterministik : SpatialQueryCompiler (Non-LLM Parameterized Compiler)        |
      |      --> Menerjemahkan CSIR ke SQL: ST_Distance_Sphere(geom, POINT(lng, lat))                  |
      |  (b) Eksekusi Basis Data Eksak   : MySQL 8.0 Relational Engine (Rata-rata 1.21 ms)             |
      |      --> Menghasilkan Kumpulan Fakta Terverifikasi (Fakta Relasional F)                         |
      |  (c) Pembangun Fakta Terstruktur : GroundedFactBuilder (Normalisasi Atribut Wisata)             |
      |  (d) Sintesis Narasi Terkontrak  : Grounded NLG via LLM Client                                  |
      |  (e) Verifikasi Klaim Deterministik: GroundingValidator (Claim-Level Grounding Validator)      |
      |      --> Evaluasi Klaim Faktual vs Fakta F; Fail-Closed Fallback jika Terdeteksi Halusinasi     |
      +=================================================================================================+
      |
      +---> [Penyajian Respons]: Teks Ter-Grounding 100% + Marker POI + Rute Jalan Raya OSRM Leaflet.js
    </pre>

    <h2 class="subsection-title">3. Ringkasan Metrik Pengujian Empiris (Benchmark Summary)</h2>
    <table class="data-table">
        <tr>
            <th>Metrik Evaluasi</th>
            <th>Hasil Pengujian (40 Skenario)</th>
            <th>Standar Ambang Batas</th>
            <th>Keterangan Evaluasi</th>
        </tr>
        <tr>
            <td>Akurasi Ekstraksi CSIR</td>
            <td><strong>90.00%</strong> (36/40 skenario)<br><small>Field-Level Mean: 98.82%</small></td>
            <td>&ge; 85.00%</td>
            <td>Sangat tinggi; 4 kasus deviasi terisolasi aman oleh validator</td>
        </tr>
        <tr>
            <td>Akurasi Klasifikasi Kategori</td>
            <td><strong>95.00%</strong> (38/40 skenario)</td>
            <td>&ge; 90.00%</td>
            <td>Sangat tinggi; 6 kategori terpetakan presisi</td>
        </tr>
        <tr>
            <td>Kebenaran Predikat Spasial (Spatial Predicate Correctness)</td>
            <td><strong>97.50%</strong> (39/40 skenario)</td>
            <td>&ge; 90.00%</td>
            <td>Tinggi; kalkulasi matematis bola bumi ST_Distance_Sphere</td>
        </tr>
        <tr>
            <td>Claim-Level Grounding Fidelity</td>
            <td><strong>100.00%</strong> (304/304 klaim)</td>
            <td>&ge; 97.50%</td>
            <td>Nol klaim tanpa bukti pada 4 kategori yang diverifikasi</td>
        </tr>
        <tr>
            <td>Entitas POI Fiktif (Hallucination)</td>
            <td><strong>0 Objek</strong> (Rate: 0.00%)</td>
            <td>0 Objek</td>
            <td>Terbukti mitigasi halusinasi efektif secara mutlak</td>
        </tr>
        <tr>
            <td>Latensi Eksekusi Kueri SQL Spasial</td>
            <td><strong>1.21 ms</strong> (Rata-rata MySQL)</td>
            <td>&lt; 50.00 ms</td>
            <td>Sangat cepat berkat indeks komposit terparameterisasi</td>
        </tr>
        <tr>
            <td>Latensi Keseluruhan (End-to-End)</td>
            <td><strong>1,340.57 ms</strong> (Termasuk inferensi LLM)</td>
            <td>&lt; 2,000.00 ms</td>
            <td>Sangat responsif untuk interaksi percakapan manusia</td>
        </tr>
    </table>
    """)

    # ==========================================
    # 3. STRUKTUR DIREKTORI & INVENTARIS KODE
    # ==========================================
    html_parts.append("""
    <div class="page-break"></div>
    <h1 class="section-title">STRUKTUR DIREKTORI & TABEL INVENTARIS KODE SUMBER</h1>

    <h2 class="subsection-title">1. Struktur Hirarki Direktori Proyek (/var/www/html/Geo)</h2>
    <pre class="diagram-box">
/var/www/html/Geo
├── app/
│   ├── Commands/
│   │   └── RisetEvaluasi.php            [CLI Spark Runner Evaluasi 40 Skenario Benchmark]
│   ├── Config/
│   │   ├── App.php                      [Konfigurasi Inti Aplikasi CodeIgniter 4]
│   │   ├── CURLRequest.php              [Konfigurasi HTTP Client untuk LLM & OSRM API]
│   │   ├── Cors.php                     [Konfigurasi Keamanan CORS Endpoint API]
│   │   ├── Database.php                 [Konfigurasi Koneksi MySQL 8.0 & Port 3306]
│   │   └── Routes.php                   [Pemetaan Routing HTTP WebGIS & REST API]
│   ├── Controllers/
│   │   ├── BaseController.php           [Controller Dasar Inisialisasi Komponen CI4]
│   │   ├── ChatController.php           [Controller Utama REST API /api/chat & Orkestrator]
│   │   ├── Home.php                     [Controller Pengarah Default]
│   │   └── WebGisController.php         [Controller Render Antarmuka Peta WebGIS]
│   ├── Database/
│   │   ├── Migrations/
│   │   │   └── 2026-09-20-000001_CreateTourismSchema.php [DDL Skema 4 Tabel & Indeks Spasial]
│   │   └── Seeds/
│   │       └── WisataSeeder.php         [Data Seeder 22 Destinasi Wisata Unggulan Padang]
│   ├── Models/
│   │   ├── ChatMessageModel.php         [Model Relasional Riwayat Pesan & Jejak Audit CSIR]
│   │   ├── ChatSessionModel.php         [Model Relasional Sesi Pengguna & Geolocation Tracker]
│   │   ├── KategoriModel.php            [Model Relasional 6 Kategori Resmi Wisata]
│   │   └── WisataModel.php              [Model Relasional 22 Destinasi Wisata Kota Padang]
│   ├── Services/
│   │   ├── BenchmarkDataset.php         [Dataset 40 Skenario Uji Percakapan Terstandarisasi]
│   │   ├── LlmService.php               [Klien Inferensi LLM DeepSeek/OpenAI & Prompt Engine]
│   │   └── SpatialIntent/
│   │       ├── GroundedFactBuilder.php  [Pembangun Fakta Normalisasi dari Hasil Kueri SQL]
│   │       ├── GroundingValidator.php   [Claim-Level Grounding Validator & Mitigasi Halusinasi]
│   │       ├── SirValidator.php         [Validator Deterministik 6-Dimensi Semantik]
│   │       ├── SpatialIntent.php        [Skema Objek DTO SIR & Representasi Kanonikal CSIR]
│   │       ├── SpatialPolicyHandler.php [Pengendali Kebijakan Penolakan & Safe Fallback]
│   │       └── SpatialQueryCompiler.php [Kompiler SQL Spasial ST_Distance_Sphere Non-LLM]
│   └── Views/
│       └── webgis.php                   [Tampilan WebGIS Leaflet.js, Chat Assistant & OSRM]
├── benchmark/
│   ├── run_all.sh                       [Master Script Eksekusi Seluruh Benchmark]
│   ├── README.md                        [Protokol Replikasi & Panduan Audit Eksperimen]
│   ├── proposed/
│   │   └── evaluator.php                [Runner Evaluasi Komprehensif Arsitektur Usulan]
│   ├── baseline_text2sql/
│   │   ├── prompt.txt                   [Kontrak Prompt Skema DDL Baseline Text-to-SQL]
│   │   └── runner.php                   [Runner Evaluasi Baseline Text-to-SQL]
│   ├── baseline_unconstrained/
│   │   ├── prompt.txt                   [Kontrak Prompt Bebas Baseline Unconstrained LLM]
│   │   └── runner.php                   [Runner Evaluasi Baseline Unconstrained LLM]
│   └── ablation/
│       └── runner.php                   [Runner Pengujian Ablasi Invarian A1-A6 & B1-B2]
├── database_backup_geo_db.sql           [Dump DDL/DML Basis Data MySQL 8.0 geo_db]
├── env                                  [Template Konfigurasi Lingkungan Server .env]
├── geo-ci4.service                      [Systemd Linux Service Unit Web Server CI4]
├── geo-tunnel.service                   [Systemd Linux Service Unit Reverse Tunnel Publik]
├── composer.json                        [Manifest Dependensi Pustaka PHP Composer]
├── phpunit.dist.xml                     [Konfigurasi Test Suite Otomatis PHPUnit]
├── public/
│   └── index.php                        [Titik Masuk Utama HTTP Front Controller]
├── spark                                [Executable Command Runner CLI CodeIgniter 4]
├── tests/
│   └── unit/
│       ├── GroundingValidatorTest.php   [Unit Test Validasi Klaim & Mitigasi Halusinasi]
│       ├── HealthTest.php               [Unit Test Integritas Endpoint & Framework CI4]
│       ├── SirValidatorTest.php         [Unit Test Invarian 6D SirValidator & Geofence]
│       └── SpatialQueryCompilerTest.php [Unit Test Kompiler SQL Spasial ST_Distance_Sphere]
└── jurnal/
    ├── align_geo_stack.py               [Skrip Penyelarasan Dataset Koordinat Geospasial]
    ├── generate_diagrams.py             [Generator Diagram Ilmiah Arsitektur Matplotlib]
    ├── generate_pdf.py                  [Generator Kompilasi Dokumen Ilmiah PDF/DOCX]
    ├── generate_thesis_diagrams.py      [Generator Visualisasi Khusus Tesis S2]
    └── generate_trace_diagram.py        [Generator Diagram Alur Penelusuran Percakapan]
    </pre>

    <h2 class="subsection-title">2. Tabel Rekapitulasi Inventaris {total_files} Berkas Kode Sumber</h2>
    <table class="data-table">
        <tr>
            <th style="width: 5%;">No</th>
            <th style="width: 8%;">Bagian</th>
            <th style="width: 35%;">Path Berkas Sumber</th>
            <th style="width: 27%;">Peran Fungsional Modul</th>
            <th style="width: 8%;">Bahasa</th>
            <th style="width: 9%; text-align: right;">Baris (LOC)</th>
            <th style="width: 8%; text-align: right;">Ukuran</th>
        </tr>
    """)

    for idx, rec in enumerate(all_file_records, 1):
        html_parts.append(f"""
        <tr>
            <td style="text-align: center;">{idx}</td>
            <td style="text-align: center;">Bagian {rec['part_num']}</td>
            <td><code><a href="#{rec['rel_path'].replace('/', '_').replace('.', '_')}" style="color: #0369a1; text-decoration: none;">{rec['rel_path']}</a></code></td>
            <td>{rec['role']}</td>
            <td style="text-transform: uppercase;">{rec['lang']}</td>
            <td style="text-align: right; font-weight: 600;">{rec['loc']:,}</td>
            <td style="text-align: right;">{rec['bytes']/1024:.1f} KB</td>
        </tr>
        """)

    html_parts.append(f"""
        <tr class="total-row">
            <td colspan="5" style="text-align: right;">TOTAL KESELURUHAN ({total_files} BERKAS PROGRAM):</td>
            <td style="text-align: right; color: #0f172a;">{total_loc:,} LOC</td>
            <td style="text-align: right; color: #0f172a;">{total_bytes/1024:.1f} KB</td>
        </tr>
    </table>
    """)

    # ==========================================
    # 4. DAFTAR ISI NAVIGASI SISTEM (TOC)
    # ==========================================
    html_parts.append("""
    <div class="page-break"></div>
    <h1 class="section-title">DAFTAR ISI KODE SUMBER LENGKAP</h1>
    <p>Daftar tautan internal seluruh komponen kode sumber yang disusun secara sistematis per lapisan arsitektur:</p>
    """)

    for part in CATEGORIES:
        html_parts.append(f"<div class='toc-part'>Bagian {part['num']}: {part['title']}</div>\n")
        for f in part["files"]:
            anchor = f["rel_path"].replace('/', '_').replace('.', '_')
            # cari loc
            rec = next((r for r in all_file_records if r["rel_path"] == f["rel_path"]), None)
            loc_str = f"{rec['loc']} baris" if rec else ""
            size_str = f"{rec['bytes']/1024:.1f} KB" if rec else ""
            html_parts.append(f"""
            <div class="toc-item">
                <a class="toc-path" href="#{anchor}"><code>{f['rel_path']}</code> &mdash; {f['role']}</a>
                <span class="toc-meta">{f['lang'].upper()} • {loc_str} • {size_str}</span>
            </div>
            """)

    # ==========================================
    # 5. LISTING KODE SUMBER FILE PER FILE
    # ==========================================
    print(f"[*] Melakukan formatting sintaksis dan penomoran baris untuk {total_files} berkas kode sumber...")

    current_part = None
    for rec in all_file_records:
        if rec["part_num"] != current_part:
            current_part = rec["part_num"]
            part_desc = next((p["desc"] for p in CATEGORIES if p["num"] == current_part), "")
            html_parts.append(f"""
            <div class="page-break"></div>
            <div style="background: #f8fafc; border: 1.5px solid #0284c7; border-radius: 6px; padding: 12px 18px; margin-bottom: 20px;">
                <div style="font-size: 8.5pt; font-weight: 700; color: #0284c7; letter-spacing: 1px; text-transform: uppercase;">
                    LAPISAN ARSITEKTUR PROGRAM &bull; BAGIAN {current_part}
                </div>
                <h1 style="font-size: 13pt; margin: 4px 0 8px 0; color: #0f172a; text-transform: uppercase;">
                    {rec['part_title']}
                </h1>
                <p style="margin: 0; font-size: 8.8pt; color: #475569;">
                    {part_desc}
                </p>
            </div>
            """)

        anchor = rec["rel_path"].replace('/', '_').replace('.', '_')
        clean_content = sanitize_code(rec["rel_path"], rec["content"])
        lexer = get_lexer(rec["rel_path"], rec["lang"])
        highlighted_code = highlight(clean_content, lexer, formatter)

        html_parts.append(f"""
        <div class="file-container" id="{anchor}">
            <div class="file-banner">
                <div class="file-banner-title">
                    Berkas: {rec['rel_path']}
                </div>
                <div class="file-banner-meta">
                    <span><strong>Bahasa:</strong> {rec['lang'].upper()}</span>
                    <span><strong>Peran:</strong> {rec['role']}</span>
                    <span><strong>Baris:</strong> {rec['loc']:,} LOC</span>
                    <span><strong>Ukuran:</strong> {rec['bytes']/1024:.1f} KB</span>
                </div>
            </div>
            <div class="file-desc-box">
                <strong>Deskripsi & Tanggung Jawab Modul:</strong> {rec['desc']}
            </div>
            <div class="code-box">
                {highlighted_code}
            </div>
        </div>
        """)

    html_parts.append("\n</body>\n</html>")

    print(f"[*] Menulis berkas HTML lengkap ke: {HTML_OUTPUT}...")
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write("".join(html_parts))

    html_size_mb = os.path.getsize(HTML_OUTPUT) / (1024 * 1024)
    print(f"[✓] Berkas HTML berhasil dibuat: {html_size_mb:.2f} MB")

    # ==========================================
    # 6. KOMPILASI KE PDF DENGAN GOOGLE CHROME HEADLESS
    # ==========================================
    print(f"[*] Mengompilasi berkas HTML ke PDF resolusi tinggi menggunakan Google Chrome Headless...")
    print(f"    Target PDF: {PDF_OUTPUT}")

    import tempfile
    with tempfile.TemporaryDirectory() as temp_profile_dir:
        cmd_chrome = [
            "google-chrome",
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--no-pdf-header-footer",
            f"--user-data-dir={temp_profile_dir}",
            f"--print-to-pdf={PDF_OUTPUT}",
            HTML_OUTPUT
        ]

        chrome_start = time.time()
        res_chrome = subprocess.run(cmd_chrome, capture_output=True, text=True, cwd=JURNAL_DIR, timeout=300)
        chrome_time = time.time() - chrome_start

    if res_chrome.returncode != 0:
        print(f"[!] Error saat kompilasi Google Chrome: {res_chrome.stderr}")
        return False

    if os.path.exists(PDF_OUTPUT):
        pdf_size_mb = os.path.getsize(PDF_OUTPUT) / (1024 * 1024)
        print(f"[✓] SUKSES! PDF berhasil dikompilasi dalam {chrome_time:.2f} detik.")
        print(f"    File: {PDF_OUTPUT} ({pdf_size_mb:.2f} MB)")

        # Hitung jumlah halaman menggunakan pdfinfo atau pdftotext
        try:
            res_info = subprocess.run(["pdfinfo", PDF_OUTPUT], capture_output=True, text=True)
            for line in res_info.stdout.splitlines():
                if "Pages:" in line:
                    print(f"    Jumlah Halaman PDF: {line.split(':')[1].strip()} halaman")
        except Exception:
            pass

        print(f"\n[SELESAI] Total waktu pemrosesan: {time.time() - start_time:.2f} detik.")
        return True
    else:
        print(f"[!] File PDF tidak ditemukan: {PDF_OUTPUT}")
        return False

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import re
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
HTML_OUTPUT = os.path.join(JURNAL_DIR, "SOURCE_CODE_ONLY.html")
PDF_OUTPUT = os.path.join(JURNAL_DIR, "SOURCE_CODE_ONLY.pdf")
PDF_MAIN = os.path.join(JURNAL_DIR, "DOKUMENTASI_SOURCE_CODE_LENGKAP.pdf")

CATEGORIES = [
    {
        "num": "I",
        "title": "Controller & Entry Point",
        "files": [
            ("public/index.php", "php", "Front Controller Entry Point"),
            ("app/Controllers/ChatController.php", "php", "ChatController (AI & Grounding Orchestrator)"),
            ("app/Controllers/WebGisController.php", "php", "WebGisController (WebGIS Presentation)"),
            ("app/Controllers/BaseController.php", "php", "BaseController (CI4 Controller Base)"),
            ("app/Controllers/Home.php", "php", "Home (Default Route Controller)")
        ]
    },
    {
        "num": "II",
        "title": "Dual Control Boundaries & AI Services",
        "files": [
            ("app/Services/SpatialIntent/SpatialIntent.php", "php", "SpatialIntent DTO (SIR & CSIR Schema)"),
            ("app/Services/SpatialIntent/SirValidator.php", "php", "SirValidator (6D Semantic Validator)"),
            ("app/Services/SpatialIntent/SpatialQueryCompiler.php", "php", "SpatialQueryCompiler (ST_Distance_Sphere Compiler)"),
            ("app/Services/SpatialIntent/GroundedFactBuilder.php", "php", "GroundedFactBuilder (Fact Normalizer)"),
            ("app/Services/SpatialIntent/GroundingValidator.php", "php", "GroundingValidator (Claim-Level Auditor)"),
            ("app/Services/SpatialIntent/SpatialPolicyHandler.php", "php", "SpatialPolicyHandler (Fallback & Scope Policy)"),
            ("app/Services/LlmService.php", "php", "LlmService (DeepSeek/OpenAI Client & NLG)"),
            ("app/Services/BenchmarkDataset.php", "php", "BenchmarkDataset (40 Test Scenarios)")
        ]
    },
    {
        "num": "III",
        "title": "Domain Models Layer",
        "files": [
            ("app/Models/WisataModel.php", "php", "WisataModel (Spatial POI Queries)"),
            ("app/Models/KategoriModel.php", "php", "KategoriModel (Category Taxonomy)"),
            ("app/Models/ChatSessionModel.php", "php", "ChatSessionModel (Sessions & GPS Tracking)"),
            ("app/Models/ChatMessageModel.php", "php", "ChatMessageModel (Audit Trail & CSIR Logs)")
        ]
    },
    {
        "num": "IV",
        "title": "Presentation Layer (WebGIS & UI)",
        "files": [
            ("app/Views/webgis.php", "html", "webgis.php (Leaflet.js Map, Chatbot, OSRM Routing & CSS)")
        ]
    },
    {
        "num": "V",
        "title": "Database Schema & Seeds",
        "files": [
            ("app/Database/Migrations/2026-09-20-000001_CreateTourismSchema.php", "php", "Migration DDL (4 Tables & Spatial Index)"),
            ("app/Database/Seeds/WisataSeeder.php", "php", "WisataSeeder (22 POIs Dataset Seeder)"),
            ("database_backup_geo_db.sql", "sql", "MySQL Database Schema & Data Dump (geo_db.sql)")
        ]
    },
    {
        "num": "VI",
        "title": "CLI Commands & Runner",
        "files": [
            ("app/Commands/RisetEvaluasi.php", "php", "RisetEvaluasi.php (CLI Spark 40 Benchmark Runner)"),
            ("spark", "php", "spark (CodeIgniter 4 CLI Executable)")
        ]
    },
    {
        "num": "VII",
        "title": "Automated Unit Tests",
        "files": [
            ("tests/unit/SirValidatorTest.php", "php", "SirValidatorTest (6D Invariants Unit Test)"),
            ("tests/unit/SpatialQueryCompilerTest.php", "php", "SpatialQueryCompilerTest (Spatial SQL Unit Test)"),
            ("tests/unit/GroundingValidatorTest.php", "php", "GroundingValidatorTest (Grounding Unit Test)"),
            ("tests/unit/HealthTest.php", "php", "HealthTest (System & Health Unit Test)"),
            ("phpunit.dist.xml", "xml", "phpunit.dist.xml (PHPUnit Configuration)")
        ]
    },
    {
        "num": "VIII",
        "title": "Configuration & Infrastructure",
        "files": [
            ("app/Config/Routes.php", "php", "Routes.php (HTTP & REST API Routes)"),
            ("app/Config/Database.php", "php", "Database.php (MySQL 8.0 Connection Config)"),
            ("app/Config/App.php", "php", "App.php (Core Application Config)"),
            ("app/Config/CURLRequest.php", "php", "CURLRequest.php (HTTP Client Config)"),
            ("app/Config/Cors.php", "php", "Cors.php (CORS Security Headers Config)"),
            ("composer.json", "json", "composer.json (PHP Dependencies & Autoload)"),
            ("env", "ini", "env (Environment Config Template)"),
            ("geo-ci4.service", "ini", "geo-ci4.service (Systemd Web Server CI4 Service)"),
            ("geo-tunnel.service", "ini", "geo-tunnel.service (Systemd Secure Tunnel Service)")
        ]
    },
    {
        "num": "IX",
        "title": "Benchmark Suite & Reproducibility Runners",
        "files": [
            ("benchmark/run_all.sh", "bash", "run_all.sh (Master Reproducibility Benchmark Runner)"),
            ("benchmark/proposed/evaluator.php", "php", "evaluator.php (Proposed Full Architecture Evaluator)"),
            ("benchmark/baseline_text2sql/runner.php", "php", "runner.php (Baseline 1: Text-to-SQL Runner)"),
            ("benchmark/baseline_text2sql/prompt.txt", "text", "prompt.txt (Baseline 1: DDL Table Schema Prompt Contract)"),
            ("benchmark/baseline_unconstrained/runner.php", "php", "runner.php (Baseline 2: Unconstrained LLM Runner)"),
            ("benchmark/baseline_unconstrained/prompt.txt", "text", "prompt.txt (Baseline 2: Direct Tourism Prompt Contract)"),
            ("benchmark/ablation/runner.php", "php", "runner.php (Ablation Study A1-A6 & B1-B2 Runner)"),
            ("benchmark/README.md", "text", "README.md (Benchmark Protocol & Reproducibility Documentation)")
        ]
    },
    {
        "num": "X",
        "title": "Research Pipeline & Automation Utilities",
        "files": [
            ("jurnal/generate_pdf.py", "python", "generate_pdf.py (Academic Document Compiler MD to PDF/DOCX)"),
            ("jurnal/generate_diagrams.py", "python", "generate_diagrams.py (Scientific Diagrams Generator)"),
            ("jurnal/generate_thesis_diagrams.py", "python", "generate_thesis_diagrams.py (Thesis Flowchart & Sequence Generator)"),
            ("jurnal/generate_trace_diagram.py", "python", "generate_trace_diagram.py (Execution Trace Diagram Generator)"),
            ("jurnal/align_geo_stack.py", "python", "align_geo_stack.py (Geospatial Dataset Alignment Utility)")
        ]
    }
]

def sanitize_code(rel_path, content):
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
    
    if rel_path == "database_backup_geo_db.sql":
        lines = content.splitlines()
        clean_lines = []
        for line in lines:
            if line.startswith("INSERT INTO `chat_messages` VALUES"):
                clean_lines.append("-- [Data log rekaman pesan pengujian benchmark sistem (dipadatkan)]")
                formatted_insert = line.replace("),(", "),\n  (")
                clean_lines.append(formatted_insert[:3200] + "\n  -- ... [Riwayat pesan benchmark dipadatkan demi kepraktisan cetak] ...\n;")
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

def generate_html(all_file_records, total_files, total_loc, page_numbers=None):
    formatter = HtmlFormatter(style='default', linenos='inline', cssclass='code-highlight')
    pygments_css = formatter.get_style_defs('.code-highlight')

    css = f"""
    @page {{
        size: A4 portrait;
        margin: 18mm 14mm 18mm 14mm;
        @top-left {{
            content: "Lampiran: Kode Sumber Program";
            font-family: Arial, sans-serif;
            font-size: 7.8pt;
            color: #555555;
        }}
        @top-right {{
            content: "CodeIgniter 4 • MySQL 8.0 Spatial";
            font-family: Arial, sans-serif;
            font-size: 7.8pt;
            color: #555555;
        }}
        @bottom-center {{
            content: "- " counter(page) " -";
            font-family: Arial, sans-serif;
            font-size: 8.5pt;
            color: #333333;
        }}
    }}

    * {{
        box-sizing: border-box;
    }}

    body {{
        font-family: Arial, "Helvetica Neue", sans-serif;
        font-size: 8.8pt;
        line-height: 1.4;
        color: #111111;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }}

    /* HEADER & FRAMEWORK INFO */
    .doc-header {{
        border-bottom: 2px solid #222222;
        padding-bottom: 8px;
        margin-bottom: 12px;
    }}

    .doc-header h1 {{
        font-size: 13.5pt;
        font-weight: bold;
        color: #000000;
        margin: 0 0 6px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .framework-card {{
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 3.5px solid #0284c7;
        padding: 7px 12px;
        margin-bottom: 12px;
        font-size: 8.4pt;
        line-height: 1.5;
    }}

    .framework-card table {{
        width: 100%;
        border-collapse: collapse;
    }}

    .framework-card td {{
        padding: 2px 4px;
        vertical-align: top;
    }}

    .framework-card td.lbl {{
        width: 22%;
        font-weight: bold;
        color: #334155;
    }}

    .framework-card td.val {{
        color: #0f172a;
    }}

    /* TOC TABLE */
    .toc-title {{
        font-size: 10pt;
        font-weight: bold;
        text-transform: uppercase;
        color: #000000;
        margin: 10px 0 6px 0;
        border-bottom: 1px solid #333333;
        padding-bottom: 3px;
    }}

    table.toc-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 8pt;
        margin-bottom: 15px;
    }}

    table.toc-table th {{
        border-bottom: 1.5px solid #222222;
        border-top: 1.5px solid #222222;
        padding: 4px 6px;
        text-align: left;
        background: #f1f5f9;
        font-weight: bold;
        color: #0f172a;
    }}

    table.toc-table td {{
        padding: 3.5px 6px;
        border-bottom: 1px solid #e2e8f0;
    }}

    table.toc-table tr:nth-child(even) {{
        background-color: #fafbfc;
    }}

    /* CODE LISTING */
    .file-block {{
        page-break-before: always;
        break-before: page;
        margin-bottom: 15px;
    }}

    .file-header {{
        border-bottom: 1.5px solid #222222;
        border-top: 1.5px solid #222222;
        padding: 4px 2px 5px 2px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        page-break-after: avoid;
        break-after: avoid;
    }}

    .file-name {{
        font-family: Consolas, "Liberation Mono", Courier, monospace;
        font-size: 8.8pt;
        font-weight: bold;
        color: #000000;
    }}

    .file-meta {{
        font-size: 7.8pt;
        color: #444444;
        font-family: Arial, sans-serif;
    }}

    .code-box {{
        background: #ffffff;
        margin: 0;
        padding: 0;
    }}

    .code-highlight {{
        font-family: Consolas, "Liberation Mono", "Courier New", monospace !important;
        font-size: 7.5pt !important;
        line-height: 1.32 !important;
        margin: 0 !important;
        padding: 4px 0 !important;
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

    span.lineno {{
        color: #888888 !important;
        user-select: none !important;
        margin-right: 1.2em !important;
        display: inline-block !important;
        width: 3.2em !important;
        text-align: right !important;
        border-right: 1px solid #cccccc !important;
        padding-right: 0.6em !important;
        font-weight: normal !important;
    }}

    {pygments_css}
    """

    html_parts = []
    html_parts.append("<!DOCTYPE html>\n<html lang='id'>\n<head>\n<meta charset='utf-8'>\n")
    html_parts.append(f"<title>Dokumentasi Kode Sumber ({total_files} Berkas)</title>\n")
    html_parts.append(f"<style>\n{css}\n</style>\n</head>\n<body>\n")

    # ==========================================
    # HALAMAN DAFTAR ISI & INFORMASI FRAMEWORK
    # ==========================================
    html_parts.append(f"""
    <div class="doc-header">
        <h1>KODE SUMBER PROGRAM (SOURCE CODE LISTING)</h1>
        <div style="font-size: 9.5pt; color: #222222; font-weight: normal;">
            Sistem Rekomendasi Pariwisata Berbasis Large Language Model (LLM) dan Strict SQL Grounding Kota Padang
        </div>
    </div>

    <div class="framework-card">
        <table>
            <tr>
                <td class="lbl">Framework Backend</td>
                <td class="val">: <strong>CodeIgniter 4</strong> (PHP 8.2 Strict Types, Architecture MVC/RESTful API)</td>
            </tr>
            <tr>
                <td class="lbl">Basis Data Spasial</td>
                <td class="val">: <strong>MySQL 8.0 Spatial</strong> (Fungsi Spasial <code>ST_Distance_Sphere</code>, Indeks Relasional Komposit (lat, lng))</td>
            </tr>
            <tr>
                <td class="lbl">Peta Digital & Rute</td>
                <td class="val">: <strong>Leaflet.js 1.9.4</strong> &bull; OpenStreetMap Tiles &bull; <strong>OSRM Engine</strong> (Road Navigation Polylines)</td>
            </tr>
            <tr>
                <td class="lbl">Inferensi AI & Kontrak</td>
                <td class="val">: <strong>Large Language Model (DeepSeek V3 / OpenAI API)</strong> &bull; Validasi SIR Deterministik 6-Dimensi</td>
            </tr>
            <tr>
                <td class="lbl">Metode Keandalan</td>
                <td class="val">: <strong>Dual Control Boundaries</strong> (Batas Kendali Semantik & Batas Kendali Bukti / Strict SQL Grounding)</td>
            </tr>
            <tr>
                <td class="lbl">Pengujian & Otomasi</td>
                <td class="val">: <strong>PHPUnit 10.x</strong> &bull; Spark CLI Runner (<code>php spark riset:evaluasi</code>) &bull; Linux Systemd Service</td>
            </tr>
        </table>
    </div>

    <div class="toc-title">
        Daftar Isi Kode Sumber ({total_files} Berkas &bull; {total_loc:,} Baris Kode)
    </div>

    <table class="toc-table">
        <thead>
            <tr>
                <th style="width: 4%; text-align: center;">No</th>
                <th style="width: 8%; text-align: center;">Bagian</th>
                <th style="width: 46%;">Nama Berkas</th>
                <th style="width: 26%;">Komponen / Modul</th>
                <th style="width: 7%; text-align: center;">Bahasa</th>
                <th style="width: 5%; text-align: right;">Baris</th>
                <th style="width: 4%; text-align: right;">Hal.</th>
            </tr>
        </thead>
        <tbody>
    """)

    for idx, rec in enumerate(all_file_records, 1):
        anchor = rec["rel_path"].replace('/', '_').replace('.', '_')
        page_val = page_numbers.get(rec["rel_path"], "-") if page_numbers else "-"
        html_parts.append(f"""
            <tr>
                <td style="text-align: center;">{idx}</td>
                <td style="text-align: center;">Bagian {rec['part_num']}</td>
                <td><code><a href="#{anchor}" style="color: #0284c7; text-decoration: none; font-weight: 600;">{rec['rel_path']}</a></code></td>
                <td>{rec['role']}</td>
                <td style="text-align: center; text-transform: uppercase;">{rec['lang']}</td>
                <td style="text-align: right;">{rec['loc']:,}</td>
                <td style="text-align: right; font-weight: bold;">{page_val}</td>
            </tr>
        """)

    html_parts.append(f"""
            <tr style="border-top: 1.5px solid #333333; font-weight: bold; background: #f1f5f9;">
                <td colspan="5" style="text-align: right;">TOTAL:</td>
                <td style="text-align: right;">{total_loc:,}</td>
                <td style="text-align: right;"></td>
            </tr>
        </tbody>
    </table>
    """)

    # ==========================================
    # KODE SUMBER FILE PER FILE
    # ==========================================
    for rec in all_file_records:
        anchor = rec["rel_path"].replace('/', '_').replace('.', '_')
        clean_content = sanitize_code(rec["rel_path"], rec["content"])
        lexer = get_lexer(rec["rel_path"], rec["lang"])
        highlighted_code = highlight(clean_content, lexer, formatter)

        html_parts.append(f"""
        <div class="file-block" id="{anchor}">
            <div class="file-header">
                <span class="file-name">File: {rec['rel_path']}</span>
                <span class="file-meta">Bagian {rec['part_num']} &bull; {rec['lang'].upper()} &bull; {rec['loc']:,} baris</span>
            </div>
            <div class="code-box">
                {highlighted_code}
            </div>
        </div>
        """)

    html_parts.append("\n</body>\n</html>")
    return "".join(html_parts)

def extract_page_numbers(pdf_path, file_list):
    """Mengekstrak nomor halaman di mana setiap berkas pertama kali muncul di PDF."""
    page_numbers = {}
    try:
        res = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True)
        pages = res.stdout.split("\x0c")
        for page_idx, page_content in enumerate(pages, 1):
            for rel_path in file_list:
                if rel_path not in page_numbers:
                    # Cek kemunculan 'File: rel_path'
                    if f"File: {rel_path}" in page_content:
                        page_numbers[rel_path] = page_idx
    except Exception as e:
        print("[!] Warning extract page numbers:", e)
    return page_numbers

import tempfile

def compile_pdf():
    with tempfile.TemporaryDirectory() as temp_profile_dir:
        cmd = [
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
        return subprocess.run(cmd, capture_output=True, text=True, cwd=JURNAL_DIR, timeout=300)

def main():
    print("[*] Mengompilasi Dokumen Kode Sumber Lengkap dengan Daftar Isi & Informasi Framework...")
    start_time = time.time()

    all_file_records = []
    total_files = 0
    total_loc = 0
    total_bytes = 0
    file_list = []

    for part in CATEGORIES:
        for rel_path, lang, role in part["files"]:
            full_path = os.path.join(PROJECT_ROOT, rel_path)
            if os.path.exists(full_path):
                size = os.path.getsize(full_path)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                raw_loc = len(content.splitlines())
                total_files += 1
                total_loc += raw_loc
                total_bytes += size
                file_list.append(rel_path)
                all_file_records.append({
                    "part_num": part["num"],
                    "rel_path": rel_path,
                    "lang": lang,
                    "role": role,
                    "loc": raw_loc,
                    "bytes": size,
                    "content": content
                })

    print(f"[✓] Teridentifikasi {total_files} berkas | {total_loc:,} LOC")

    # Pass 1: Render awal untuk mendapatkan nomor halaman
    print("[*] Pass 1: Menghasilkan PDF awal untuk penentuan nomor halaman...")
    html_pass1 = generate_html(all_file_records, total_files, total_loc, None)
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html_pass1)

    compile_pdf()

    # Ekstrak nomor halaman
    print("[*] Mengekstrak nomor halaman akurat untuk setiap berkas...")
    page_numbers = extract_page_numbers(PDF_OUTPUT, file_list)
    print(f"[✓] Berhasil memetakan {len(page_numbers)} nomor halaman.")

    # Pass 2: Render final dengan nomor halaman akurat di Daftar Isi
    print("[*] Pass 2: Menghasilkan PDF final dengan nomor halaman presisi pada Daftar Isi...")
    html_pass2 = generate_html(all_file_records, total_files, total_loc, page_numbers)
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html_pass2)

    res = compile_pdf()
    if res.returncode != 0:
        print("[!] Error Chrome:", res.stderr)
        return False

    if os.path.exists(PDF_OUTPUT):

        size_mb = os.path.getsize(PDF_OUTPUT) / (1024 * 1024)
        print(f"[✓] SUKSES! PDF Kode Sumber + Daftar Isi + Framework selesai dibuat!")
        print(f"    File: {PDF_OUTPUT} ({size_mb:.2f} MB)")

        try:
            res_info = subprocess.run(["pdfinfo", PDF_OUTPUT], capture_output=True, text=True)
            for line in res_info.stdout.splitlines():
                if "Pages:" in line:
                    print(f"    Jumlah Halaman: {line.split(':')[1].strip()} halaman")
        except Exception:
            pass

        print(f"[SELESAI] Total waktu pemrosesan: {time.time() - start_time:.2f} detik.")
        return True

    return False

if __name__ == "__main__":
    main()

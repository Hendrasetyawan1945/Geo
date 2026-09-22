#!/usr/bin/env python3
"""
generate_trace_diagram.py
Menghasilkan Diagram Alur Konkret Eksekusi Sistem Ujung-ke-Ujung:
- Gambar 4 (Indonesian): gambar4_alur_eksekusi_konkret.svg / .png
- Figure 4 (English): figure4_concrete_execution_trace.svg / .png
"""

import os
import subprocess

IMG_DIR = "/var/www/html/Geo/jurnal/images"
os.makedirs(IMG_DIR, exist_ok=True)

def escape_xml(s):
    if not isinstance(s, str):
        return str(s)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def make_trace_diagram_svg(lang="id"):
    is_id = (lang == "id")
    W = 1060
    H = 1380
    
    title = "DIAGRAM ALUR KONKRET EKSEKUSI SISTEM UJUNG-KE-UJUNG (END-TO-END TRACE)" if is_id else "CONCRETE END-TO-END SYSTEM EXECUTION TRACE"
    subtitle = "Dari Ujaran Bahasa Alami ke Respons Bernarasi Ter-grounding dan Kartografi Interaktif" if is_id else "From Colloquial Natural Language to Grounded Response and Interactive Cartography"

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    svg.append('''
  <defs>
    <linearGradient id="traceHeader" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f766e"/>
      <stop offset="50%" stop-color="#0369a1"/>
      <stop offset="100%" stop-color="#1e3a8a"/>
    </linearGradient>
    <linearGradient id="codeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
    <filter id="traceShadow" x="-3%" y="-4%" width="106%" height="112%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.09"/>
    </filter>
    <filter id="headerShadow" x="-2%" y="-5%" width="104%" height="118%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.14"/>
    </filter>
    <marker id="arrowDown" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 2 L 5 8 L 10 2 z" fill="#0284c7"/>
    </marker>
  </defs>

  <style>
    .font-base { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .font-mono { font-family: "Courier New", Courier, monospace; }
    .card-title { font-weight: 700; font-size: 13.5px; fill: #0f172a; }
    .badge-text { font-weight: 700; font-size: 9.5px; fill: #ffffff; letter-spacing: 0.4px; }
    .connector-text { font-weight: 600; font-size: 10px; fill: #0369a1; }
    .connector-bg { fill: #ffffff; stroke: #94a3b8; stroke-width: 1.2; rx: 9; }
    .check-pill { rx: 5; fill: #f0fdf4; stroke: #86efac; stroke-width: 1.2; }
    .check-text { font-weight: 700; font-size: 10px; fill: #166534; }
  </style>

  <!-- Background Canvas -->
  <rect width="100%" height="100%" fill="#f8fafc" rx="14"/>
  <rect x="2" y="2" width="''' + str(W-4) + '''" height="''' + str(H-4) + '''" fill="none" stroke="#e2e8f0" stroke-width="2" rx="12"/>

  <!-- Top Header Banner -->
  <g filter="url(#headerShadow)">
    <rect x="25" y="20" width="''' + str(W-50) + '''" height="66" rx="10" fill="url(#traceHeader)"/>
    <text x="''' + str(W/2) + '''" y="46" text-anchor="middle" class="font-base" font-weight="800" font-size="16px" fill="#ffffff" letter-spacing="0.3px">''' + escape_xml(title) + '''</text>
    <text x="''' + str(W/2) + '''" y="68" text-anchor="middle" class="font-base" font-weight="500" font-size="12px" fill="#ccfbf1">''' + escape_xml(subtitle) + '''</text>
  </g>
''')

    # STEP 1: USER UTTERANCE & SITUATIONAL CONTEXT
    bx = 50; by = 110; bw = 960; bh = 110
    step1_badge = "1. UJARAN BAHASA ALAMI &amp; KONTEKS SITUASIONAL" if is_id else "1. COLLOQUIAL UTTERANCE &amp; SITUATIONAL CONTEXT"
    step1_title = "Masukan Pengguna (Klien Browser / Perangkat Bergerak)" if is_id else "User Input (Mobile Client / Browser)"
    step1_query = '"Cari wisata pantai yang dekat dari saya, tiket maksimal 15 ribu dan buka sekarang."' if is_id else '"Find nearest beach from me, ticket max 15k and open now."'
    
    svg.append(f'''
  <!-- STEP 1 -->
  <g filter="url(#traceShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.8"/>
    <rect x="{bx + 16}" y="{by + 12}" width="280" height="20" rx="4" fill="#0284c7"/>
    <text x="{bx + 156}" y="{by + 26}" text-anchor="middle" class="font-base badge-text">{step1_badge}</text>
    <text x="{bx + 310}" y="{by + 27}" class="font-base card-title">{step1_title}</text>
    
    <!-- Speech bubble -->
    <rect x="{bx + 20}" y="{by + 42}" width="920" height="32" rx="6" fill="#ffffff" stroke="#93c5fd" stroke-width="1.2"/>
    <text x="{bx + 35}" y="{by + 63}" class="font-base" font-weight="600" font-size="13px" fill="#1e3a8a">{step1_query}</text>
    
    <!-- Badges context -->
    <rect x="{bx + 20}" y="{by + 82}" width="220" height="20" rx="4" fill="#e0f2fe"/>
    <text x="{bx + 30}" y="{by + 96}" class="font-base" font-weight="600" font-size="10.5px" fill="#0369a1">📍 GPS: -0.9471, 100.3541 (Padang)</text>
    
    <rect x="{bx + 250}" y="{by + 82}" width="190" height="20" rx="4" fill="#e0f2fe"/>
    <text x="{bx + 260}" y="{by + 96}" class="font-base" font-weight="600" font-size="10.5px" fill="#0369a1">🕒 Waktu: 14:30:00 WIB (Siang)</text>

    <rect x="{bx + 450}" y="{by + 82}" width="200" height="20" rx="4" fill="#e0f2fe"/>
    <text x="{bx + 460}" y="{by + 96}" class="font-base" font-weight="600" font-size="10.5px" fill="#0369a1">🌐 Sesi: Interaktif Leaflet.js</text>
  </g>
''')

    # Connector 1 -> 2
    c1_txt = "Ekstraksi Semantik LLM Sandbox (DeepSeek, temp: 0.0)" if is_id else "Semantic Extraction in LLM Sandbox (DeepSeek, temp: 0.0)"
    svg.append(f'''
  <line x1="{W/2}" y1="220" x2="{W/2}" y2="252" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowDown)"/>
  <rect x="{W/2 - 160}" y="226" width="320" height="20" rx="10" class="connector-bg"/>
  <text x="{W/2}" y="240" text-anchor="middle" class="font-base connector-text">{c1_txt}</text>
''')

    # STEP 2: CANONICAL SIR (CSIR DTO)
    bx = 50; by = 254; bw = 960; bh = 150
    step2_badge = "2. EKSTRAKSI CANONICAL SIR (CSIR DTO JSON)" if is_id else "2. CANONICAL SIR EXTRACTION (CSIR JSON DTO)"
    step2_title = "Representasi Maksud Terstruktur (Strictly-Typed DTO)" if is_id else "Strictly-Typed Spatial Intent Representation"
    
    svg.append(f'''
  <!-- STEP 2 -->
  <g filter="url(#traceShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#faf5ff" stroke="#e9d5ff" stroke-width="1.8"/>
    <rect x="{bx + 16}" y="{by + 12}" width="280" height="20" rx="4" fill="#7c3aed"/>
    <text x="{bx + 156}" y="{by + 26}" text-anchor="middle" class="font-base badge-text">{step2_badge}</text>
    <text x="{bx + 310}" y="{by + 27}" class="font-base card-title">{step2_title}</text>
    
    <!-- Code box -->
    <rect x="{bx + 20}" y="{by + 40}" width="920" height="98" rx="6" fill="url(#codeGrad)"/>
    <text x="{bx + 35}" y="{by + 60}" class="font-mono" font-size="11px" fill="#cbd5e1">&#123;</text>
    <text x="{bx + 55}" y="{by + 76}" class="font-mono" font-size="11px" fill="#38bdf8">"category": <tspan fill="#fef08a">"Pantai"</tspan>, <tspan fill="#38bdf8">"spatial_operator":</tspan> <tspan fill="#fef08a">"nearest"</tspan>, <tspan fill="#38bdf8">"reference_type":</tspan> <tspan fill="#fef08a">"gps"</tspan>, <tspan fill="#38bdf8">"user_lat":</tspan> <tspan fill="#f87171">-0.9471</tspan>, <tspan fill="#38bdf8">"user_lng":</tspan> <tspan fill="#f87171">100.3541</tspan>,</text>
    <text x="{bx + 55}" y="{by + 94}" class="font-mono" font-size="11px" fill="#38bdf8">"max_price": <tspan fill="#f87171">15000</tspan>, <tspan fill="#38bdf8">"open_now":</tspan> <tspan fill="#4ade80">true</tspan>, <tspan fill="#38bdf8">"sort":</tspan> <tspan fill="#fef08a">"terdekat"</tspan>, <tspan fill="#38bdf8">"isValid":</tspan> <tspan fill="#4ade80">true</tspan>, <tspan fill="#38bdf8">"executionPolicy":</tspan> <tspan fill="#fef08a">"execute_sql"</tspan></text>
    <text x="{bx + 35}" y="{by + 112}" class="font-mono" font-size="11px" fill="#cbd5e1">&#125;</text>
    <text x="{bx + 55}" y="{by + 128}" class="font-base" font-size="9.5px" fill="#94a3b8">• Terisolasi dari basis data | Output JSON murni tanpa celah injeksi SQL | No DB execution yet</text>
  </g>
''')

    # Connector 2 -> 3
    c2_txt = "Verifikasi 6-Dimensi SirValidator (Prinsip No Intent Alteration)" if is_id else "6-Dimensional SirValidator (No Intent Alteration Principle)"
    svg.append(f'''
  <line x1="{W/2}" y1="404" x2="{W/2}" y2="436" stroke="#7c3aed" stroke-width="2" marker-end="url(#arrowDown)"/>
  <rect x="{W/2 - 180}" y="410" width="360" height="20" rx="10" class="connector-bg"/>
  <text x="{W/2}" y="424" text-anchor="middle" class="font-base connector-text">{c2_txt}</text>
''')

    # STEP 3: SIR VALIDATOR 6-DIMENSI
    bx = 50; by = 438; bw = 960; bh = 116
    step3_badge = "3. VALIDATOR SIR 6-DIMENSI DETERMINISTIK" if is_id else "3. 6-DIMENSIONAL DETERMINISTIC SIR VALIDATOR"
    step3_title = "Evaluasi Invarian Keselamatan: 6 Dimensi Lolos 100%" if is_id else "Safety Invariants: All 6 Dimensions Passed (100%)"
    
    svg.append(f'''
  <!-- STEP 3 -->
  <g filter="url(#traceShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#fffbeb" stroke="#fde68a" stroke-width="1.8"/>
    <rect x="{bx + 16}" y="{by + 12}" width="280" height="20" rx="4" fill="#d97706"/>
    <text x="{bx + 156}" y="{by + 26}" text-anchor="middle" class="font-base badge-text">{step3_badge}</text>
    <text x="{bx + 310}" y="{by + 27}" class="font-base card-title">{step3_title}</text>
    
    <!-- 6 Check Pills in 2 rows of 3 -->
    <rect x="{bx + 20}" y="{by + 44}" width="290" height="28" class="check-pill"/>
    <text x="{bx + 35}" y="{by + 62}" class="font-base check-text">✓ D1: Skema &amp; Strict Typing Valid</text>
    
    <rect x="{bx + 335}" y="{by + 44}" width="290" height="28" class="check-pill"/>
    <text x="{bx + 350}" y="{by + 62}" class="font-base check-text">✓ D2: Domain Spasial WGS84 Valid</text>

    <rect x="{bx + 650}" y="{by + 44}" width="290" height="28" class="check-pill"/>
    <text x="{bx + 665}" y="{by + 62}" class="font-base check-text">✓ D3: Operator Sesuai Ontologi</text>

    <rect x="{bx + 20}" y="{by + 78}" width="290" height="28" class="check-pill"/>
    <text x="{bx + 35}" y="{by + 96}" class="font-base check-text">✓ D4: Batasan Harga Positif (≥ 0)</text>

    <rect x="{bx + 335}" y="{by + 78}" width="290" height="28" class="check-pill"/>
    <text x="{bx + 350}" y="{by + 96}" class="font-base check-text">✓ D5: Cakupan Wilayah Kota Padang</text>

    <rect x="{bx + 650}" y="{by + 78}" width="290" height="28" class="check-pill"/>
    <text x="{bx + 665}" y="{by + 96}" class="font-base check-text">✓ D6: Invarian Keamanan Lolos</text>
  </g>
''')

    # Connector 3 -> 4
    c3_txt = "Kompilasi ke SQL Terparameterisasi (MySQL 8.0)" if is_id else "Compilation to Parameterized SQL (MySQL 8.0)"
    svg.append(f'''
  <line x1="{W/2}" y1="554" x2="{W/2}" y2="586" stroke="#d97706" stroke-width="2" marker-end="url(#arrowDown)"/>
  <rect x="{W/2 - 160}" y="560" width="320" height="20" rx="10" class="connector-bg"/>
  <text x="{W/2}" y="574" text-anchor="middle" class="font-base connector-text">{c3_txt}</text>
''')

    # STEP 4: SPATIAL QUERY COMPILATION (MYSQL 8.0)
    bx = 50; by = 588; bw = 960; bh = 158
    step4_badge = "4. KOMPILASI KUERI SPASIAL SQL (DETERMINISTIK)" if is_id else "4. DETERMINISTIC SPATIAL SQL COMPILATION"
    step4_title = "Kueri Geodesik Terparameterisasi (Formula ST_Distance_Sphere)" if is_id else "Parameterized Geodesic Query (ST_Distance_Sphere)"

    svg.append(f'''
  <!-- STEP 4 -->
  <g filter="url(#traceShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1.8"/>
    <rect x="{bx + 16}" y="{by + 12}" width="280" height="20" rx="4" fill="#059669"/>
    <text x="{bx + 156}" y="{by + 26}" text-anchor="middle" class="font-base badge-text">{step4_badge}</text>
    <text x="{bx + 310}" y="{by + 27}" class="font-base card-title">{step4_title}</text>
    
    <!-- Code box -->
    <rect x="{bx + 20}" y="{by + 40}" width="920" height="106" rx="6" fill="url(#codeGrad)"/>
    <text x="{bx + 35}" y="{by + 60}" class="font-mono" font-size="11px" fill="#38bdf8"><tspan fill="#c084fc">SELECT</tspan> id, nama, alamat, harga_tiket, jam_buka, jam_tutup,</text>
    <text x="{bx + 85}" y="{by + 76}" class="font-mono" font-size="11px" fill="#4ade80">ROUND(ST_Distance_Sphere(POINT(lng, lat), POINT(100.3541, -0.9471)) / 1000.0, 2) <tspan fill="#c084fc">AS</tspan> jarak_km</text>
    <text x="{bx + 35}" y="{by + 92}" class="font-mono" font-size="11px" fill="#38bdf8"><tspan fill="#c084fc">FROM</tspan> wisata <tspan fill="#c084fc">JOIN</tspan> kategori <tspan fill="#c084fc">ON</tspan> wisata.kategori_id = kategori.id</text>
    <text x="{bx + 35}" y="{by + 108}" class="font-mono" font-size="11px" fill="#38bdf8"><tspan fill="#c084fc">WHERE</tspan> status_aktif = 1 <tspan fill="#c084fc">AND</tspan> kategori.nama = <tspan fill="#fef08a">'Pantai'</tspan> <tspan fill="#c084fc">AND</tspan> harga_tiket &lt;= 15000</text>
    <text x="{bx + 75}" y="{by + 124}" class="font-mono" font-size="11px" fill="#38bdf8"><tspan fill="#c084fc">AND</tspan> (<tspan fill="#fef08a">'14:30:00'</tspan> <tspan fill="#c084fc">BETWEEN</tspan> jam_buka <tspan fill="#c084fc">AND</tspan> jam_tutup) <tspan fill="#c084fc">ORDER BY</tspan> jarak_km <tspan fill="#c084fc">ASC LIMIT</tspan> 10;</text>
    <text x="{bx + 35}" y="{by + 140}" class="font-base" font-size="9.5px" fill="#94a3b8">• Formula Geodesik C++ Bawaan MySQL 8.0 | SPATIAL INDEX R-Tree pada kolom geom POINT SRID 4326</text>
  </g>
''')

    # Connector 4 -> 5
    c4_txt = "Eksekusi Basis Data Spasial (Latensi: 1,21 ms)" if is_id else "Spatial Database Execution (Latency: 1.21 ms)"
    svg.append(f'''
  <line x1="{W/2}" y1="746" x2="{W/2}" y2="778" stroke="#059669" stroke-width="2" marker-end="url(#arrowDown)"/>
  <rect x="{W/2 - 160}" y="752" width="320" height="20" rx="10" class="connector-bg"/>
  <text x="{W/2}" y="766" text-anchor="middle" class="font-base connector-text">{c4_txt}</text>
''')

    # STEP 5: FACTS SET F
    bx = 50; by = 780; bw = 960; bh = 170
    step5_badge = "5. HIMPUNAN TUPEL FAKTA TERVERIFIKASI F" if is_id else "5. VERIFIED SPATIAL FACT TUPLES SET F"
    step5_title = "Hasil Basis Data Relasional-Spasial (Single Source of Truth)" if is_id else "Relational-Spatial Result (Single Source of Truth)"

    svg.append(f'''
  <!-- STEP 5 -->
  <g filter="url(#traceShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#f0fdfa" stroke="#99f6e4" stroke-width="1.8"/>
    <rect x="{bx + 16}" y="{by + 12}" width="280" height="20" rx="4" fill="#0f766e"/>
    <text x="{bx + 156}" y="{by + 26}" text-anchor="middle" class="font-base badge-text">{step5_badge}</text>
    <text x="{bx + 310}" y="{by + 27}" class="font-base card-title">{step5_title}</text>
    
    <!-- Table Container -->
    <rect x="{bx + 20}" y="{by + 42}" width="920" height="116" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    
    <!-- Table Header -->
    <rect x="{bx + 20}" y="{by + 42}" width="920" height="28" rx="6" fill="#0f766e"/>
    <rect x="{bx + 20}" y="{by + 58}" width="920" height="12" fill="#0f766e"/>
    <text x="{bx + 35}" y="{by + 60}" class="font-base" font-weight="700" font-size="11px" fill="#ffffff">No</text>
    <text x="{bx + 80}" y="{by + 60}" class="font-base" font-weight="700" font-size="11px" fill="#ffffff">Nama Destinasi Wisata</text>
    <text x="{bx + 320}" y="{by + 60}" class="font-base" font-weight="700" font-size="11px" fill="#ffffff">Kategori</text>
    <text x="{bx + 440}" y="{by + 60}" class="font-base" font-weight="700" font-size="11px" fill="#ffffff">Jarak Geodesik (d)</text>
    <text x="{bx + 600}" y="{by + 60}" class="font-base" font-weight="700" font-size="11px" fill="#ffffff">Tarif Tiket</text>
    <text x="{bx + 720}" y="{by + 60}" class="font-base" font-weight="700" font-size="11px" fill="#ffffff">Jam Buka - Tutup</text>
    <text x="{bx + 850}" y="{by + 60}" class="font-base" font-weight="700" font-size="11px" fill="#ffffff">Status</text>

    <!-- Row 1 -->
    <text x="{bx + 35}" y="{by + 86}" class="font-base" font-weight="700" font-size="11px" fill="#0f172a">1</text>
    <text x="{bx + 80}" y="{by + 86}" class="font-base" font-weight="700" font-size="11px" fill="#0f766e">Pantai Padang (Taplau)</text>
    <text x="{bx + 320}" y="{by + 86}" class="font-base" font-size="11px" fill="#475569">Pantai</text>
    <text x="{bx + 440}" y="{by + 86}" class="font-base" font-weight="700" font-size="11px" fill="#0284c7">0,40 km</text>
    <text x="{bx + 600}" y="{by + 86}" class="font-base" font-weight="700" font-size="11px" fill="#16a34a">Rp0 (Gratis)</text>
    <text x="{bx + 720}" y="{by + 86}" class="font-base" font-size="11px" fill="#475569">06:00 – 22:00 WIB</text>
    <text x="{bx + 850}" y="{by + 86}" class="font-base" font-weight="700" font-size="10.5px" fill="#059669">✓ Sedang Buka</text>
    <line x1="{bx + 20}" y1="{by + 96}" x2="{bx + 940}" y2="{by + 96}" stroke="#f1f5f9"/>

    <!-- Row 2 -->
    <text x="{bx + 35}" y="{by + 114}" class="font-base" font-weight="700" font-size="11px" fill="#0f172a">2</text>
    <text x="{bx + 80}" y="{by + 114}" class="font-base" font-weight="700" font-size="11px" fill="#0f766e">Pantai Air Manis (Malin Kundang)</text>
    <text x="{bx + 320}" y="{by + 114}" class="font-base" font-size="11px" fill="#475569">Pantai</text>
    <text x="{bx + 440}" y="{by + 114}" class="font-base" font-weight="700" font-size="11px" fill="#0284c7">3,20 km</text>
    <text x="{bx + 600}" y="{by + 114}" class="font-base" font-weight="700" font-size="11px" fill="#0f172a">Rp10.000</text>
    <text x="{bx + 720}" y="{by + 114}" class="font-base" font-size="11px" fill="#475569">06:00 – 18:00 WIB</text>
    <text x="{bx + 850}" y="{by + 114}" class="font-base" font-weight="700" font-size="10.5px" fill="#059669">✓ Sedang Buka</text>
    <line x1="{bx + 20}" y1="{by + 124}" x2="{bx + 940}" y2="{by + 124}" stroke="#f1f5f9"/>

    <!-- Row 3 -->
    <text x="{bx + 35}" y="{by + 142}" class="font-base" font-weight="700" font-size="11px" fill="#0f172a">3</text>
    <text x="{bx + 80}" y="{by + 142}" class="font-base" font-weight="700" font-size="11px" fill="#0f766e">Pantai Pasir Jambak</text>
    <text x="{bx + 320}" y="{by + 142}" class="font-base" font-size="11px" fill="#475569">Pantai</text>
    <text x="{bx + 440}" y="{by + 142}" class="font-base" font-weight="700" font-size="11px" fill="#0284c7">3,46 km</text>
    <text x="{bx + 600}" y="{by + 142}" class="font-base" font-weight="700" font-size="11px" fill="#0f172a">Rp5.000</text>
    <text x="{bx + 720}" y="{by + 142}" class="font-base" font-size="11px" fill="#475569">07:00 – 18:30 WIB</text>
    <text x="{bx + 850}" y="{by + 142}" class="font-base" font-weight="700" font-size="10.5px" fill="#059669">✓ Sedang Buka</text>
  </g>
''')

    # Connector 5 -> 6
    c5_txt = "Grounding Firewall Algoritmik (∀e ∈ Entities, e ∈ F) + Mesin Rute OSRM" if is_id else "Algorithmic Grounding Firewall (∀e ∈ Entities, e ∈ F) + OSRM Routing"
    svg.append(f'''
  <line x1="{W/2}" y1="950" x2="{W/2}" y2="982" stroke="#0f766e" stroke-width="2" marker-end="url(#arrowDown)"/>
  <rect x="{W/2 - 210}" y="956" width="420" height="20" rx="10" class="connector-bg"/>
  <text x="{W/2}" y="970" text-anchor="middle" class="font-base connector-text">{c5_txt}</text>
''')

    # STEP 6: GROUNDED RESPONSE & DUAL-SYNCHRONIZED CARTOGRAPHY
    bx = 50; by = 984; bw = 960; bh = 220
    step6_badge = "6. RESPON BERNARASI TER-GROUNDING &amp; KARTOGRAFI DWITUNGGAL" if is_id else "6. GROUNDED NARRATIVE &amp; DUAL CARTOGRAPHY"
    step6_title = "Verifikasi Bebas Halusinasi &amp; Rendering Multimodal Sinkron" if is_id else "Hallucination-Free Verification &amp; Multimodal Rendering"

    svg.append(f'''
  <!-- STEP 6 -->
  <g filter="url(#traceShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#fff1f2" stroke="#fecdd3" stroke-width="1.8"/>
    <rect x="{bx + 16}" y="{by + 12}" width="320" height="20" rx="4" fill="#e11d48"/>
    <text x="{bx + 176}" y="{by + 26}" text-anchor="middle" class="font-base badge-text">{step6_badge}</text>
    <text x="{bx + 350}" y="{by + 27}" class="font-base card-title">{step6_title}</text>
    
    <!-- Grounding Verification Bar -->
    <rect x="{bx + 20}" y="{by + 40}" width="920" height="26" rx="5" fill="#f0fdf4" stroke="#86efac" stroke-width="1.2"/>
    <text x="{bx + 35}" y="{by + 57}" class="font-base" font-weight="700" font-size="11px" fill="#166534">🛡️ GROUNDING AUDIT PASSED:</text>
    <text x="{bx + 230}" y="{by + 57}" class="font-base" font-size="11px" fill="#14532d">Semua entitas {{Pantai Padang, Pantai Air Manis, Pantai Pasir Jambak}} terbukti ada pada F.</text>
    <text x="{bx + 760}" y="{by + 57}" class="font-base" font-weight="800" font-size="11px" fill="#047857">Grounding Fidelity: 100,00%</text>

    <!-- Grounded Narrative Box -->
    <rect x="{bx + 20}" y="{by + 74}" width="920" height="66" rx="6" fill="#ffffff" stroke="#f43f5e" stroke-width="1.2"/>
    <text x="{bx + 35}" y="{by + 94}" class="font-base" font-weight="700" font-size="11px" fill="#9f1239">💬 Balasan Percakapan AI Terverifikasi (Floating AI Chat Panel):</text>
    <text x="{bx + 35}" y="{by + 112}" class="font-base" font-style="italic" font-size="11px" fill="#334155">"Berikut 3 pantai terdekat yang buka saat ini dengan tiket &lt;= Rp15.000: (1) Pantai Padang (0,40 km, gratis, buka s.d. 22:00 WIB),</text>
    <text x="{bx + 35}" y="{by + 128}" class="font-base" font-style="italic" font-size="11px" fill="#334155">(2) Pantai Air Manis (3,20 km, Rp10.000, buka s.d. 18:00 WIB), dan (3) Pantai Pasir Jambak (3,46 km, Rp5.000, buka s.d. 18:30 WIB)."</text>

    <!-- Dual Sync Badges -->
    <rect x="{bx + 20}" y="{by + 148}" width="450" height="60" rx="6" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.2"/>
    <text x="{bx + 35}" y="{by + 168}" class="font-base" font-weight="700" font-size="11px" fill="#0369a1">🗺️ Kartografi Interaktif Leaflet.js:</text>
    <text x="{bx + 35}" y="{by + 185}" class="font-base" font-size="10.5px" fill="#334155">• Auto-pan viewport ke klaster pantai</text>
    <text x="{bx + 35}" y="{by + 199}" class="font-base" font-size="10.5px" fill="#334155">• Pin marker SVG tematik + popup kartu operasional</text>

    <rect x="{bx + 490}" y="{by + 148}" width="450" height="60" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.2"/>
    <text x="{bx + 505}" y="{by + 168}" class="font-base" font-weight="700" font-size="11px" fill="#1d4ed8">🚗 Navigasi Jaringan Jalan Raya OSRM:</text>
    <text x="{bx + 505}" y="{by + 185}" class="font-base" font-size="10.5px" fill="#334155">• Polyline rute jalan turn-by-turn terpendek</text>
    <text x="{bx + 505}" y="{by + 199}" class="font-base" font-size="10.5px" fill="#334155">• Estimasi durasi berkendara &amp; jarak rute aktual</text>
  </g>
''')

    # Summary footer banner
    foot_txt = "PEMBUKTIAN KERANGKA TIGA TINGKAT KEBENARAN: KEBENARAN SEMANTIK (CSIR) ➔ KEBENARAN SPASIAL (SQL) ➔ KEBENARAN GROUNDING (NARRATIVE)" if is_id else "THREE-TIER CORRECTNESS PROOF: SEMANTIC CORRECTNESS ➔ SPATIAL CORRECTNESS ➔ GROUNDING CORRECTNESS"
    svg.append(f'''
  <!-- Footer Banner -->
  <rect x="50" y="1224" width="960" height="42" rx="8" fill="#1e293b"/>
  <text x="{W/2}" y="1250" text-anchor="middle" class="font-base" font-weight="700" font-size="11px" fill="#f8fafc">{foot_txt}</text>
''')

    svg.append('</svg>')
    return '\n'.join(svg)

# Main Generation
print("Generating Concrete Execution Trace Diagrams...")

# 1. Indonesian (Gambar 4)
id_svg_p = os.path.join(IMG_DIR, "gambar4_alur_eksekusi_konkret.svg")
with open(id_svg_p, "w", encoding="utf-8") as f:
    f.write(make_trace_diagram_svg("id"))
print(f"Wrote: {id_svg_p}")

id_png_p = os.path.join(IMG_DIR, "gambar4_alur_eksekusi_konkret.png")
subprocess.run(["rsvg-convert", "-d", "300", "-p", "300", id_svg_p, "-o", id_png_p], check=True)
print(f"Generated 300-DPI: {id_png_p}")

# 2. English (Figure 4)
en_svg_p = os.path.join(IMG_DIR, "figure4_concrete_execution_trace.svg")
with open(en_svg_p, "w", encoding="utf-8") as f:
    f.write(make_trace_diagram_svg("en"))
print(f"Wrote: {en_svg_p}")

en_png_p = os.path.join(IMG_DIR, "figure4_concrete_execution_trace.png")
subprocess.run(["rsvg-convert", "-d", "300", "-p", "300", en_svg_p, "-o", en_png_p], check=True)
print(f"Generated 300-DPI: {en_png_p}")

print("Done generating Concrete Execution Trace diagrams!")

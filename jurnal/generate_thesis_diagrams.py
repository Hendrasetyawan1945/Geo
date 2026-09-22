#!/usr/bin/env python3
"""
generate_thesis_diagrams.py
Generates publication-quality SVG & 300-DPI PNG diagrams for Thesis Chapter 3:
- Gambar 3.4: Flowchart Sistem 5-Layer Terintegrasi (Alur Logika Eksekusi End-to-End)
- Gambar 3.5: Sequence Diagram Interaksi Percakapan Spasial Lengkap
"""

import os
import subprocess

IMG_DIR = "/var/www/html/Geo/jurnal/images"
os.makedirs(IMG_DIR, exist_ok=True)

def escape_xml(s):
    if not isinstance(s, str):
        return s
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def make_flowchart_5layer_svg():
    W = 1100
    H = 1580
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    svg.append('''
  <defs>
    <linearGradient id="fcHeader" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f766e"/>
      <stop offset="50%" stop-color="#0e7490"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
    <filter id="fcShadow" x="-3%" y="-4%" width="106%" height="112%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.09"/>
    </filter>
    <filter id="headerShadow" x="-2%" y="-5%" width="104%" height="118%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.14"/>
    </filter>
    <marker id="arrowDown" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 2 L 5 8 L 10 2 z" fill="#0284c7"/>
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 2 L 5 8 L 10 2 z" fill="#e11d48"/>
    </marker>
    <marker id="arrowAmber" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 2 L 5 8 L 10 2 z" fill="#d97706"/>
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 2 L 5 8 L 10 2 z" fill="#059669"/>
    </marker>
  </defs>

  <style>
    .font-base { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .node-title { font-weight: 700; font-size: 13.5px; fill: #0f172a; }
    .node-desc { font-weight: 450; font-size: 11px; fill: #334155; line-height: 1.4; }
    .badge-text { font-weight: 700; font-size: 9.5px; fill: #ffffff; letter-spacing: 0.5px; }
    .edge-label-bg { fill: #ffffff; stroke: #94a3b8; stroke-width: 1.2; rx: 9; }
    .edge-label-text { font-weight: 600; font-size: 10px; fill: #0369a1; }
    .edge-label-red { font-weight: 700; font-size: 10px; fill: #b91c1c; }
    .edge-label-amber { font-weight: 700; font-size: 10px; fill: #b45309; }
    .edge-label-green { font-weight: 700; font-size: 10px; fill: #047857; }
    .diamond-text { font-weight: 700; font-size: 11.5px; fill: #78350f; text-anchor: middle; }
    .diamond-sub { font-weight: 500; font-size: 10px; fill: #92400e; text-anchor: middle; }
  </style>

  <!-- Background Canvas -->
  <rect width="100%" height="100%" fill="#f8fafc" rx="14"/>
  <rect x="2" y="2" width="''' + str(W-4) + '''" height="''' + str(H-4) + '''" fill="none" stroke="#e2e8f0" stroke-width="2" rx="12"/>

  <!-- Top Header Banner -->
  <g filter="url(#headerShadow)">
    <rect x="25" y="20" width="''' + str(W-50) + '''" height="66" rx="10" fill="url(#fcHeader)"/>
    <text x="''' + str(W/2) + '''" y="46" text-anchor="middle" class="font-base" font-weight="800" font-size="16px" fill="#ffffff" letter-spacing="0.3px">FLOWCHART ALUR LOGIKA EKSEKUSI SISTEM 5-LAYER TERINTEGRASI</text>
    <text x="''' + str(W/2) + '''" y="68" text-anchor="middle" class="font-base" font-weight="500" font-size="12px" fill="#ccfbf1">Alur End-to-End: Dari Masukan Pengguna &amp; GPS, Validasi Invarian SIR, Kompilasi Spasial, hingga Grounding Validator</text>
  </g>
''')

    # STEP 1: USER INPUT (x=550)
    # Box center: (550, 115), w=540, h=62
    bx = 280; by = 112; bw = 540; bh = 62
    svg.append(f'''
  <!-- STEP 1: USER INPUT -->
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="#f0f9ff" stroke="#7dd3fc" stroke-width="2"/>
    <rect x="{bx + 14}" y="{by + 10}" width="95" height="18" rx="4" fill="#0284c7"/>
    <text x="{bx + 61}" y="{by + 23}" text-anchor="middle" class="font-base badge-text">USER INPUT</text>
    <text x="{bx + 120}" y="{by + 24}" class="font-base node-title">1. Pengguna Memasukkan Pesan Alami &amp; Lokasi GPS</text>
    <text x="{bx + 18}" y="{by + 46}" class="font-base node-desc">Pesan teks (cth: "pantai terdekat tiket dibawah 20rb") + Koordinat Klien (lat, lng) + Waktu Sirkadian</text>
  </g>
''')

    # Arrow 1 -> 2
    svg.append('''
  <line x1="550" y1="174" x2="550" y2="204" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowDown)"/>
''')

    # STEP 2: LAYER 2 LLM SEMANTIC PARSER
    bx = 260; by = 206; bw = 580; bh = 72
    svg.append(f'''
  <!-- STEP 2: LAYER 2 -->
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#faf5ff" stroke="#d8b4fe" stroke-width="1.8"/>
    <rect x="{bx + 14}" y="{by + 10}" width="165" height="18" rx="4" fill="#7c3aed"/>
    <text x="{bx + 96}" y="{by + 23}" text-anchor="middle" class="font-base badge-text">LAYER 2: COGNITIVE AIR-GAP</text>
    <text x="{bx + 190}" y="{by + 24}" class="font-base node-title">LLM Semantic Parser (DeepSeek API)</text>
    <text x="{bx + 18}" y="{by + 46}" class="font-base node-desc">• Sandbox JSON Mode (temperature: 0.0, isolasi total dari basis data &amp; SQL)</text>
    <text x="{bx + 18}" y="{by + 62}" class="font-base node-desc">• Ekstraksi slot semantik spasial terikat taksonomi: intent, kategori, operator, radius, max_price</text>
  </g>
''')

    # Arrow 2 -> 3 with Badge
    svg.append('''
  <line x1="550" y1="278" x2="550" y2="318" stroke="#7c3aed" stroke-width="2" marker-end="url(#arrowDown)"/>
  <rect x="440" y="286" width="220" height="20" rx="10" class="edge-label-bg"/>
  <text x="550" y="300" text-anchor="middle" class="font-base edge-label-text">Objek Raw SIR DTO (JSON)</text>
''')

    # STEP 3: LAYER 3 SIR VALIDATOR
    bx = 250; by = 320; bw = 600; bh = 74
    svg.append(f'''
  <!-- STEP 3: LAYER 3 -->
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#fffbeb" stroke="#fde68a" stroke-width="1.8"/>
    <rect x="{bx + 14}" y="{by + 10}" width="180" height="18" rx="4" fill="#d97706"/>
    <text x="{bx + 104}" y="{by + 23}" text-anchor="middle" class="font-base badge-text">LAYER 3: FIREWALL KENDALI</text>
    <text x="{bx + 204}" y="{by + 24}" class="font-base node-title">SirValidator (6 Dimensi Invarian)</text>
    <text x="{bx + 18}" y="{by + 46}" class="font-base node-desc">• Prinsip No Intent Alteration: Menolak asumsi sepihak atau mutasi diam-diam atas preferensi kueri</text>
    <text x="{bx + 18}" y="{by + 62}" class="font-base node-desc">• Evaluasi 6 Dimensi: Domain, Operator, Bounding Box, Range Batas Numerik, Status, &amp; Safety</text>
  </g>
''')

    # Arrow 3 -> Diamond 1
    svg.append('''
  <line x1="550" y1="394" x2="550" y2="424" stroke="#d97706" stroke-width="2" marker-end="url(#arrowAmber)"/>
''')

    # DIAMOND 1: HASIL VALIDASI INVARIAN SIR
    # Center (550, 470), rx=130, ry=44
    svg.append('''
  <!-- DECISION DIAMOND 1 -->
  <g filter="url(#fcShadow)">
    <polygon points="550,426 690,470 550,514 410,470" fill="#fef3c7" stroke="#d97706" stroke-width="2.2"/>
    <text x="550" y="465" class="font-base diamond-text">Hasil Validasi Invarian SIR?</text>
    <text x="550" y="482" class="font-base diamond-sub">Evaluasi Status &amp; Policy CSIR</text>
  </g>
''')

    # THREE BRANCHES FROM DIAMOND 1:
    # Branch 1 (Left): isOutOfScope == true
    svg.append('''
  <!-- Branch 1: Out of Scope -->
  <path d="M 410 470 H 170 V 534" fill="none" stroke="#e11d48" stroke-width="2" marker-end="url(#arrowRed)"/>
  <rect x="185" y="458" width="165" height="20" rx="9" fill="#fff1f2" stroke="#fecdd3" stroke-width="1.2"/>
  <text x="267" y="472" text-anchor="middle" class="font-base edge-label-red">isOutOfScope == true</text>
''')
    # Box 1A: Honest Rejection
    bx = 60; by = 536; bw = 220; bh = 76
    svg.append(f'''
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="#fff1f2" stroke="#fecdd3" stroke-width="1.6"/>
    <rect x="{bx + 10}" y="{by + 8}" width="105" height="17" rx="4" fill="#e11d48"/>
    <text x="{bx + 62}" y="{by + 20}" text-anchor="middle" class="font-base badge-text">HONEST REJECT</text>
    <text x="{bx + 10}" y="{by + 40}" class="font-base" font-weight="700" font-size="12px" fill="#9f1239">Penolakan Jujur</text>
    <text x="{bx + 10}" y="{by + 55}" class="font-base" font-size="10.5px" fill="#475569">• 0 Beban Basis Data (0 SQL)</text>
    <text x="{bx + 10}" y="{by + 69}" class="font-base" font-size="10.5px" fill="#475569">• Respons klarifikasi batas sistem</text>
  </g>
''')

    # Branch 2 (Right): isValid == false (Violation / Ambiguity)
    svg.append('''
  <!-- Branch 2: Invalid -->
  <path d="M 690 470 H 930 V 534" fill="none" stroke="#d97706" stroke-width="2" marker-end="url(#arrowAmber)"/>
  <rect x="745" y="458" width="160" height="20" rx="9" fill="#fffbeb" stroke="#fde68a" stroke-width="1.2"/>
  <text x="825" y="472" text-anchor="middle" class="font-base edge-label-amber">isValid == false</text>
''')
    # Box 2A: Clarify User
    bx = 820; by = 536; bw = 220; bh = 76
    svg.append(f'''
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="#fffbeb" stroke="#fde68a" stroke-width="1.6"/>
    <rect x="{bx + 10}" y="{by + 8}" width="95" height="17" rx="4" fill="#d97706"/>
    <text x="{bx + 57}" y="{by + 20}" text-anchor="middle" class="font-base badge-text">CLARIFY USER</text>
    <text x="{bx + 10}" y="{by + 40}" class="font-base" font-weight="700" font-size="12px" fill="#92400e">Minta Klarifikasi</text>
    <text x="{bx + 10}" y="{by + 55}" class="font-base" font-size="10.5px" fill="#475569">• Tanpa manipulasi parameter</text>
    <text x="{bx + 10}" y="{by + 69}" class="font-base" font-size="10.5px" fill="#475569">• Mengajukan opsi penegasan</text>
  </g>
''')

    # Branch 3 (Center Down): isValid == true -> Validated CSIR
    svg.append('''
  <!-- Branch 3: Valid -->
  <line x1="550" y1="514" x2="550" y2="548" stroke="#059669" stroke-width="2.2" marker-end="url(#arrowGreen)"/>
  <rect x="475" y="520" width="150" height="18" rx="9" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1.2"/>
  <text x="550" y="533" text-anchor="middle" class="font-base edge-label-green">isValid == true</text>
''')

    # STEP 3B: CANONICAL SIR (CSIR)
    bx = 360; by = 550; bw = 380; bh = 54
    svg.append(f'''
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="#f0fdf4" stroke="#86efac" stroke-width="1.8"/>
    <rect x="{bx + 12}" y="{by + 7}" width="125" height="17" rx="4" fill="#059669"/>
    <text x="{bx + 74}" y="{by + 19}" text-anchor="middle" class="font-base badge-text">CANONICAL SIR</text>
    <text x="{bx + 148}" y="{by + 20}" class="font-base" font-weight="700" font-size="12.5px" fill="#166534">CSIR Tervalidasi (Strict DTO)</text>
    <text x="{bx + 14}" y="{by + 40}" class="font-base node-desc">Parameter spasial &amp; operasional terkunci, siap dikompilasi ke SQL</text>
  </g>
''')

    # Arrow 3B -> 4
    svg.append('''
  <line x1="550" y1="604" x2="550" y2="636" stroke="#059669" stroke-width="2" marker-end="url(#arrowDown)"/>
''')

    # STEP 4: LAYER 4 SPATIAL QUERY COMPILER
    bx = 240; by = 638; bw = 620; bh = 76
    svg.append(f'''
  <!-- STEP 4: LAYER 4 COMPILER -->
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1.8"/>
    <rect x="{bx + 14}" y="{by + 10}" width="195" height="18" rx="4" fill="#059669"/>
    <text x="{bx + 111}" y="{by + 23}" text-anchor="middle" class="font-base badge-text">LAYER 4: COMPILER SPASIAL</text>
    <text x="{bx + 218}" y="{by + 24}" class="font-base node-title">Spatial Query Compiler (Deterministik)</text>
    <text x="{bx + 18}" y="{by + 46}" class="font-base node-desc">• Kompilasi CSIR ke SQL terparameterisasi dengan formula geodesik ST_Distance_Sphere</text>
    <text x="{bx + 18}" y="{by + 62}" class="font-base node-desc">• Penyusunan klausa filter: radius_km, kategori_id, max_price, status_operasional, jam_buka</text>
  </g>
''')

    # Arrow 4 -> 5 with Badge
    svg.append('''
  <line x1="550" y1="714" x2="550" y2="754" stroke="#059669" stroke-width="2" marker-end="url(#arrowDown)"/>
  <rect x="420" y="722" width="260" height="20" rx="10" class="edge-label-bg"/>
  <text x="550" y="736" text-anchor="middle" class="font-base edge-label-text">Parameterized SQL (SRID 4326 POINT)</text>
''')

    # STEP 5: MYSQL 8.0 SPATIAL ENGINE
    bx = 230; by = 756; bw = 640; bh = 76
    svg.append(f'''
  <!-- STEP 5: MYSQL ENGINE -->
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#f0fdfa" stroke="#99f6e4" stroke-width="1.8"/>
    <rect x="{bx + 14}" y="{by + 10}" width="180" height="18" rx="4" fill="#0f766e"/>
    <text x="{bx + 104}" y="{by + 23}" text-anchor="middle" class="font-base badge-text">DATA STORAGE &amp; ENGINE</text>
    <text x="{bx + 204}" y="{by + 24}" class="font-base node-title">Eksekusi MySQL 8.0 Spatial Engine</text>
    <text x="{bx + 18}" y="{by + 46}" class="font-base node-desc">• Evaluasi R-Tree SPATIAL INDEX pada kolom geom POINT (latensi rata-rata: 1,21 ms)</text>
    <text x="{bx + 18}" y="{by + 62}" class="font-base node-desc">• Menghasilkan Tupel Fakta Terverifikasi: F = {{t₁, t₂, ..., t_k}} (Single Source of Truth)</text>
  </g>
''')

    # Arrow 5 -> 6 with Badge
    svg.append('''
  <line x1="550" y1="832" x2="550" y2="872" stroke="#0f766e" stroke-width="2" marker-end="url(#arrowDown)"/>
  <rect x="430" y="840" width="240" height="20" rx="10" class="edge-label-bg"/>
  <text x="550" y="854" text-anchor="middle" class="font-base edge-label-text">Tupel Fakta Terverifikasi F</text>
''')

    # STEP 6: OSRM ROUTING + LAYER 5 LLM NLG (IN PARALLEL / SEQUENTIAL)
    # Side-by-side or stacked:
    # Let's stack OSRM Engine (sub-task) and LLM NLG
    bx = 250; by = 874; bw = 600; bh = 66
    svg.append(f'''
  <!-- STEP 6A: OSRM ROUTE -->
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.8"/>
    <rect x="{bx + 14}" y="{by + 10}" width="165" height="18" rx="4" fill="#0284c7"/>
    <text x="{bx + 96}" y="{by + 23}" text-anchor="middle" class="font-base badge-text">ROUTING ENGINE</text>
    <text x="{bx + 190}" y="{by + 24}" class="font-base node-title">OSRM Highway Network Engine</text>
    <text x="{bx + 18}" y="{by + 46}" class="font-base node-desc">• Komputasi rute jalan raya turn-by-turn dari posisi pengguna ke destinasi wisata</text>
    <text x="{bx + 18}" y="{by + 60}" class="font-base node-desc">• Menghasilkan Polyline GeoJSON, estimasi jarak jalan raya (km), &amp; durasi tempuh (menit)</text>
  </g>
''')

    # Arrow 6A -> 6B
    svg.append('''
  <line x1="550" y1="940" x2="550" y2="970" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowDown)"/>
''')

    # STEP 6B: LAYER 5 LLM GROUNDED GENERATOR
    bx = 240; by = 972; bw = 620; bh = 74
    svg.append(f'''
  <!-- STEP 6B: LAYER 5 NLG -->
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#fff1f2" stroke="#fecdd3" stroke-width="1.8"/>
    <rect x="{bx + 14}" y="{by + 10}" width="180" height="18" rx="4" fill="#e11d48"/>
    <text x="{bx + 104}" y="{by + 23}" text-anchor="middle" class="font-base badge-text">LAYER 5: GROUNDED NLG</text>
    <text x="{bx + 204}" y="{by + 24}" class="font-base node-title">LLM Grounded Generator (DeepSeek NLG)</text>
    <text x="{bx + 18}" y="{by + 46}" class="font-base node-desc">• Sintesis narasi percakapan alami terikat ketat pada himpunan tupel fakta F</text>
    <text x="{bx + 18}" y="{by + 62}" class="font-base node-desc">• Mengubah data tabular menjadi narasi komunikatif yang ramah dan kontekstual</text>
  </g>
''')

    # Arrow 6B -> 7 with Badge
    svg.append('''
  <line x1="550" y1="1046" x2="550" y2="1086" stroke="#e11d48" stroke-width="2" marker-end="url(#arrowDown)"/>
  <rect x="440" y="1054" width="220" height="20" rx="10" class="edge-label-bg"/>
  <text x="550" y="1068" text-anchor="middle" class="font-base edge-label-text">Draf Narasi Respons NLG</text>
''')

    # STEP 7: ALGORITHMIC GROUNDING VALIDATOR
    bx = 230; by = 1088; bw = 640; bh = 76
    svg.append(f'''
  <!-- STEP 7: GROUNDING VALIDATOR -->
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#fff1f2" stroke="#fda4af" stroke-width="1.8"/>
    <rect x="{bx + 14}" y="{by + 10}" width="195" height="18" rx="4" fill="#be123c"/>
    <text x="{bx + 111}" y="{by + 23}" text-anchor="middle" class="font-base badge-text">GROUNDING FIREWALL</text>
    <text x="{bx + 218}" y="{by + 24}" class="font-base node-title">Algorithmic Grounding Validator</text>
    <text x="{bx + 18}" y="{by + 46}" class="font-base node-desc">• Validasi Pasca-Generasi: Penegakan Kontrak Formal ∀e ∈ Entities(Narasi), e ∈ F</text>
    <text x="{bx + 18}" y="{by + 62}" class="font-base node-desc">• Deteksi halusinasi POI fiktif, fabrikasi jarak, atau inkonsistensi tarif &amp; jam operasional</text>
  </g>
''')

    # Arrow 7 -> Diamond 2
    svg.append('''
  <line x1="550" y1="1164" x2="550" y2="1194" stroke="#be123c" stroke-width="2" marker-end="url(#arrowRed)"/>
''')

    # DIAMOND 2: GROUNDING CHECK
    # Center (550, 1236), rx=130, ry=42
    svg.append('''
  <!-- DECISION DIAMOND 2 -->
  <g filter="url(#fcShadow)">
    <polygon points="550,1196 685,1238 550,1280 415,1238" fill="#ffe4e6" stroke="#be123c" stroke-width="2.2"/>
    <text x="550" y="1233" class="font-base" font-weight="700" font-size="11.5px" fill="#881337" text-anchor="middle">Semua Entitas Valid pada F?</text>
    <text x="550" y="1250" class="font-base" font-weight="500" font-size="10px" fill="#9f1239" text-anchor="middle">Garansi Entitas Faktual 100%</text>
  </g>
''')

    # TWO BRANCHES FROM DIAMOND 2:
    # Branch 2A (Right): Ada Entitas Fiktif / Halusinasi
    svg.append('''
  <!-- Branch False: Entitas Fiktif -->
  <path d="M 685 1238 H 890 V 1290" fill="none" stroke="#ea580c" stroke-width="2" marker-end="url(#arrowAmber)"/>
  <rect x="715" y="1226" width="150" height="20" rx="9" fill="#fff7ed" stroke="#fed7aa" stroke-width="1.2"/>
  <text x="790" y="1240" text-anchor="middle" class="font-base" font-weight="700" font-size="10px" fill="#c2410c">Ada Entitas Fiktif</text>
''')
    # Box Fallback Template
    bx = 770; by = 1292; bw = 240; bh = 64
    svg.append(f'''
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="#fff7ed" stroke="#fed7aa" stroke-width="1.6"/>
    <rect x="{bx + 10}" y="{by + 8}" width="130" height="17" rx="4" fill="#ea580c"/>
    <text x="{bx + 75}" y="{by + 20}" text-anchor="middle" class="font-base badge-text">FALLBACK TEMPLATE</text>
    <text x="{bx + 10}" y="{by + 40}" class="font-base" font-weight="700" font-size="11.5px" fill="#9a3412">Substitusi Template Deterministik</text>
    <text x="{bx + 10}" y="{by + 56}" class="font-base node-desc">Ganti narasi halusinatif dengan format fakta baku</text>
  </g>
''')

    # Branch 2B (Center Down): Semua Entitas Valid
    svg.append('''
  <!-- Branch True: Valid Grounding -->
  <line x1="550" y1="1280" x2="550" y2="1308" stroke="#059669" stroke-width="2.2" marker-end="url(#arrowGreen)"/>
  <rect x="465" y="1286" width="170" height="18" rx="9" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1.2"/>
  <text x="550" y="1299" text-anchor="middle" class="font-base edge-label-green">Semua Entitas Valid (Lolos)</text>
''')
    # Box Grounded OK
    bx = 400; by = 1310; bw = 300; bh = 46
    svg.append(f'''
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="#f0fdf4" stroke="#86efac" stroke-width="1.6"/>
    <text x="{bx + 150}" y="{by + 20}" text-anchor="middle" class="font-base" font-weight="700" font-size="12px" fill="#166534">Teks Narasi Lolos Uji Grounding</text>
    <text x="{bx + 150}" y="{by + 36}" text-anchor="middle" class="font-base node-desc">Entity Fabrication Rate: 0,00% Tergaransi</text>
  </g>
''')

    # Merge lines from both Grounding results to Dual-Payload Dispatcher
    svg.append('''
  <!-- Connectors into Dispatcher -->
  <line x1="550" y1="1356" x2="550" y2="1388" stroke="#0284c7" stroke-width="2" marker-end="url(#arrowDown)"/>
  <path d="M 890 1356 V 1374 H 550" fill="none" stroke="#ea580c" stroke-width="1.8"/>
''')

    # Routing from Honest Reject (left) and Clarify (right) down to Dispatcher
    svg.append('''
  <!-- Left Reject Route to Dispatcher -->
  <path d="M 170 612 V 1374 H 550" fill="none" stroke="#e11d48" stroke-width="1.5" stroke-dasharray="5,4"/>
  <!-- Right Clarify Route to Dispatcher -->
  <path d="M 930 612 V 1200" fill="none" stroke="#d97706" stroke-width="1.5" stroke-dasharray="5,4"/>
''')

    # STEP 8: DISPATCH DUAL-PAYLOAD JSON
    bx = 260; by = 1390; bw = 580; bh = 64
    svg.append(f'''
  <!-- STEP 8: DUAL PAYLOAD -->
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#eef2ff" stroke="#c7d2fe" stroke-width="1.8"/>
    <rect x="{bx + 14}" y="{by + 10}" width="165" height="18" rx="4" fill="#4f46e5"/>
    <text x="{bx + 96}" y="{by + 23}" text-anchor="middle" class="font-base badge-text">DUAL-PAYLOAD DISPATCH</text>
    <text x="{bx + 190}" y="{by + 24}" class="font-base node-title">Kirim Payload JSON Sinkron ke Web Client</text>
    <text x="{bx + 18}" y="{by + 46}" class="font-base node-desc">• Muatan Lengkap: {{ status: "success", text: NarasiTerverifikasi, wisata: POI[], route: GeoJSON }}</text>
  </g>
''')

    # Arrow 8 -> 9
    svg.append('''
  <line x1="550" y1="1454" x2="550" y2="1484" stroke="#4f46e5" stroke-width="2" marker-end="url(#arrowDown)"/>
''')

    # STEP 9: LAYER 1 CLIENT PRESENTATION / RENDERING
    bx = 230; by = 1486; bw = 640; bh = 70
    svg.append(f'''
  <!-- STEP 9: LAYER 1 PRESENTATION -->
  <g filter="url(#fcShadow)">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="#f0f9ff" stroke="#7dd3fc" stroke-width="2"/>
    <rect x="{bx + 14}" y="{by + 10}" width="180" height="18" rx="4" fill="#0284c7"/>
    <text x="{bx + 104}" y="{by + 23}" text-anchor="middle" class="font-base badge-text">LAYER 1: CLIENT RENDERING</text>
    <text x="{bx + 204}" y="{by + 24}" class="font-base node-title">Render Antarmuka Dwitunggal Sinkron</text>
    <text x="{bx + 18}" y="{by + 46}" class="font-base node-desc">• Peta Leaflet.js: Auto-pan ke centroid, marker SVG tematik, popup info, &amp; polyline rute jalan OSRM</text>
    <text x="{bx + 18}" y="{by + 60}" class="font-base node-desc">• Floating AI Chat: Narasi rekomendasi ter-grounding &amp; kartu interaktif destinasi wisata</text>
  </g>
''')

    svg.append('</svg>')
    return '\n'.join(svg)

def make_sequence_diagram_svg():
    W = 1140
    H = 920
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    svg.append('''
  <defs>
    <linearGradient id="seqHeader" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="50%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <filter id="seqShadow" x="-3%" y="-4%" width="106%" height="112%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.1"/>
    </filter>
    <marker id="seqArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#0284c7"/>
    </marker>
    <marker id="seqArrowDash" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#64748b"/>
    </marker>
    <marker id="seqArrowGreen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#059669"/>
    </marker>
    <marker id="seqArrowPurple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#7c3aed"/>
    </marker>
    <marker id="seqArrowRed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#e11d48"/>
    </marker>
  </defs>

  <style>
    .font-base { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .actor-box { rx: 8; fill: #ffffff; stroke: #cbd5e1; stroke-width: 1.5; }
    .actor-title { font-weight: 700; font-size: 11px; fill: #0f172a; text-anchor: middle; }
    .actor-sub { font-weight: 500; font-size: 9.5px; fill: #64748b; text-anchor: middle; }
    .msg-text { font-weight: 600; font-size: 10px; fill: #1e293b; }
    .msg-note { font-weight: 500; font-size: 9px; fill: #64748b; }
  </style>

  <!-- Canvas -->
  <rect width="100%" height="100%" fill="#f8fafc" rx="14"/>
  <rect x="2" y="2" width="''' + str(W-4) + '''" height="''' + str(H-4) + '''" fill="none" stroke="#e2e8f0" stroke-width="2" rx="12"/>

  <!-- Header -->
  <g filter="url(#seqShadow)">
    <rect x="25" y="20" width="''' + str(W-50) + '''" height="60" rx="10" fill="url(#seqHeader)"/>
    <text x="''' + str(W/2) + '''" y="45" text-anchor="middle" class="font-base" font-weight="800" font-size="15.5px" fill="#ffffff">SEQUENCE DIAGRAM INTERAKSI PERCAKAPAN SPASIAL END-TO-END</text>
    <text x="''' + str(W/2) + '''" y="65" text-anchor="middle" class="font-base" font-weight="500" font-size="11.5px" fill="#cbd5e1">Kronologi Pemanggilan Komponen: Dari Parsing Semantik, Validasi Invarian, Kompilasi Kueri, hingga Grounding</text>
  </g>
''')

    # Lifelines definition
    actors = [
        {"name": "Browser / User", "sub": "Leaflet & Chat", "x": 80, "color": "#0284c7"},
        {"name": "ChatController", "sub": "CodeIgniter 4", "x": 220, "color": "#0284c7"},
        {"name": "LlmService", "sub": "DeepSeek API", "x": 370, "color": "#7c3aed"},
        {"name": "SirValidator", "sub": "Invarian 6-Dim", "x": 520, "color": "#d97706"},
        {"name": "QueryCompiler", "sub": "SQL Generator", "x": 670, "color": "#059669"},
        {"name": "MySQL 8.0", "sub": "Spatial InnoDB", "x": 810, "color": "#0f766e"},
        {"name": "OSRM Engine", "sub": "Road Routing", "x": 940, "color": "#0369a1"},
        {"name": "GroundingVal", "sub": "Grounding Firewall", "x": 1050, "color": "#e11d48"},
    ]

    top_y = 100
    bot_y = 860

    # Draw Lifelines
    for act in actors:
        x = act["x"]
        act_name = escape_xml(act["name"])
        act_sub = escape_xml(act["sub"])
        svg.append(f'''
  <!-- Lifeline {act_name} -->
  <line x1="{x}" y1="{top_y + 45}" x2="{x}" y2="{bot_y}" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4"/>
  <g filter="url(#seqShadow)">
    <rect x="{x - 55}" y="{top_y}" width="110" height="42" rx="6" fill="#ffffff" stroke="{act["color"]}" stroke-width="1.8"/>
    <text x="{x}" y="{top_y + 18}" class="font-base actor-title">{act_name}</text>
    <text x="{x}" y="{top_y + 32}" class="font-base actor-sub">{act_sub}</text>
  </g>
''')

    # Sequence Messages
    # Format: (y, from_act, to_act, label, note, is_return, color, marker)
    messages = [
        (170, 0, 1, "1. POST /api/chat (text, lat, lng)", "Kirim kueri bahasa alami + koordinat GPS", False, "#0284c7", "seqArrow"),
        (215, 1, 2, "2. parseSIR(prompt, lat, lng)", "Isolasi sandbox JSON, temp: 0.0", False, "#7c3aed", "seqArrowPurple"),
        (260, 2, 1, "3. Raw SIR DTO (JSON)", "intent, category, radius, price", True, "#64748b", "seqArrowDash"),
        (305, 1, 3, "4. validate(rawSir)", "Uji 6 dimensi invarian No Intent Alteration", False, "#d97706", "seqArrow"),
        (350, 3, 1, "5. Canonical SIR (CSIR)", "Status: validated, Policy: execute_sql", True, "#64748b", "seqArrowDash"),
        (400, 1, 4, "6. compileAndExecute(csir, lat, lng)", "Kompilasi kueri geodesik ST_Distance_Sphere", False, "#059669", "seqArrowGreen"),
        (450, 4, 5, "7. SELECT ... ST_Distance_Sphere()", "Eksekusi SPATIAL INDEX R-Tree", False, "#0f766e", "seqArrow"),
        (500, 5, 4, "8. Rows Data Fakta SQL", "Hasil terurut jarak geodesik (1,21 ms)", True, "#64748b", "seqArrowDash"),
        (545, 4, 1, "9. Array Tupel Fakta Terverifikasi F", "Single Source of Truth", True, "#64748b", "seqArrowDash"),
        (595, 1, 6, "10. /route/v1/driving (user_coord, dest_coord)", "Kueri jaringan jalan raya turn-by-turn", False, "#0369a1", "seqArrow"),
        (640, 6, 1, "11. GeoJSON Polyline + Jarak & Durasi", "Geometri jalur jalan raya", True, "#64748b", "seqArrowDash"),
        (685, 1, 2, "12. generateGroundedNlg(fakta_F, query)", "Sintesis draf percakapan terikat fakta", False, "#7c3aed", "seqArrowPurple"),
        (730, 2, 1, "13. Draf Teks Respons NLG", "Narasi komunikatif", True, "#64748b", "seqArrowDash"),
        (775, 1, 7, "14. validateGrounding(drafTeks, fakta_F)", "Kontrak formal: Semua entitas ∈ F?", False, "#e11d48", "seqArrowRed"),
        (815, 7, 1, "15. GroundingResult (isGrounded: true)", "Entity Fabrication: 0,00% (Tanpa Halusinasi)", True, "#64748b", "seqArrowDash"),
        (855, 1, 0, "16. JSON Dual-Payload {text, wisata, route}", "Render sinkron peta Leaflet & panel chat AI", True, "#0284c7", "seqArrow"),
    ]

    for y, f_idx, t_idx, lbl_raw, note_raw, is_ret, col, mrk in messages:
        lbl = escape_xml(lbl_raw)
        note = escape_xml(note_raw)
        x1 = actors[f_idx]["x"]
        x2 = actors[t_idx]["x"]
        dash = ' stroke-dasharray="5,4"' if is_ret else ''
        mid_x = (x1 + x2) / 2
        
        # Offset label position slightly
        text_anchor = "middle"
        
        svg.append(f'''
  <!-- Message: {lbl_raw} -->
  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="1.6"{dash} marker-end="url(#{mrk})"/>
  <rect x="{mid_x - len(lbl_raw)*3.2 - 8}" y="{y - 18}" width="{len(lbl_raw)*6.4 + 16}" height="15" rx="3" fill="#ffffff" fill-opacity="0.9"/>
  <text x="{mid_x}" y="{y - 6}" text-anchor="{text_anchor}" class="font-base msg-text" fill="{col}">{lbl}</text>
  <text x="{mid_x}" y="{y + 12}" text-anchor="{text_anchor}" class="font-base msg-note">{note}</text>
''')

    svg.append('</svg>')
    return '\n'.join(svg)

# Main Execution
print("Generating Thesis Chapter 3 Diagrams...")

# 1. Flowchart 5-Layer (Gambar 3.4)
fc_svg_p = os.path.join(IMG_DIR, "gambar3_4_flowchart_sistem.svg")
with open(fc_svg_p, "w") as f:
    f.write(make_flowchart_5layer_svg())
print(f"Wrote: {fc_svg_p}")

fc_png_p = os.path.join(IMG_DIR, "gambar3_4_flowchart_sistem.png")
subprocess.run(["rsvg-convert", "-d", "300", "-p", "300", fc_svg_p, "-o", fc_png_p], check=True)
print(f"Generated 300-DPI: {fc_png_p}")

# 2. Sequence Diagram (Gambar 3.5)
seq_svg_p = os.path.join(IMG_DIR, "gambar3_5_sequence_diagram.svg")
with open(seq_svg_p, "w") as f:
    f.write(make_sequence_diagram_svg())
print(f"Wrote: {seq_svg_p}")

seq_png_p = os.path.join(IMG_DIR, "gambar3_5_sequence_diagram.png")
subprocess.run(["rsvg-convert", "-d", "300", "-p", "300", seq_svg_p, "-o", seq_png_p], check=True)
print(f"Generated 300-DPI: {seq_png_p}")

print("Done generating Chapter 3 diagrams!")

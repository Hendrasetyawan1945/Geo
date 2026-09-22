#!/usr/bin/env python3
"""
generate_diagrams.py
Menghasilkan diagram vektor SVG dan raster PNG 300-DPI berkualitas publikasi (Q2 IJG & Tesis):
1. Gambar 2: Kerangka Operasional Interaksi Spasial Eksploratori (ID & EN)
2. Gambar 1: Arsitektur Sistem 5-Layer Cognitive Air-Gap & Grounding Firewall (ID & EN)
3. Gambar 3: Skema Basis Data Relasional-Spasial MySQL 8.0 (ERD) (ID & EN)
"""

import os
import subprocess

IMG_DIR = "/var/www/html/Geo/jurnal/images"
os.makedirs(IMG_DIR, exist_ok=True)

def escape_xml(s):
    if not isinstance(s, str):
        return s
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def make_operational_framework_svg(lang="id"):
    is_id = (lang == "id")
    
    title = escape_xml("KERANGKA OPERASIONAL INTERAKSI SPASIAL EKSPLORATORI TERKONTROL SEMANTIK" if is_id else "OPERATIONAL FRAMEWORK: ITERATIVE COGNITIVE-CONTROL-EXECUTION LOOP")
    subtitle = escape_xml("Siklus Iteratif Kognitif-Kendali-Eksekusi (Evolusi Model Afnarius dkk., 2026)" if is_id else "Semantic-Controlled Exploratory Spatial Interaction (Evolving Afnarius et al., 2026)")
    
    stages = [
        {
            "num": "1",
            "title": escape_xml("1. Formulasi Intensi Kognitif Bahasa Alami & Konteks Situasional" if is_id else "1. Natural Language Cognitive Intent Formulation & Context"),
            "type": escape_xml("CLIENT / PRESENTATION"),
            "color_top": "#0284c7",
            "color_bg": "#f0f9ff",
            "color_border": "#bae6fd",
            "bullet1": escape_xml("• Wisatawan mengekspresikan preferensi majemuk melalui bahasa alami sehari-hari" if is_id else "• Tourists express compound preferences via natural conversational language"),
            "bullet2": escape_xml("• Resolusi konteks klien: koordinat GPS (lat, lng), waktu sirkadian, preferensi sesi" if is_id else "• Client context resolution: GPS coordinates (lat, lng), circadian time, session state"),
            "arrow": escape_xml("Kueri Bahasa Alami + Vektor Konteks Situasional" if is_id else "Natural Language Query + Situational Context Vector")
        },
        {
            "num": "2",
            "title": escape_xml("2. Cognitive Air-Gap: Interpretasi Semantik (Sandbox JSON LLM)" if is_id else "2. Cognitive Air-Gap: Semantic Interpretation (LLM JSON Sandbox)"),
            "type": escape_xml("COGNITIVE AI LAYER"),
            "color_top": "#7c3aed",
            "color_bg": "#faf5ff",
            "color_border": "#e9d5ff",
            "bullet1": escape_xml("• DeepSeek LLM (temperature: 0.0, response_format: JSON) terisolasi dari database" if is_id else "• DeepSeek LLM (temperature: 0.0, JSON mode) isolated from database access"),
            "bullet2": escape_xml("• Ekstraksi slot semantik dibatasi Ontologi Operator Spasial & Taksonomi Klaster" if is_id else "• Semantic slot extraction bounded by Spatial Operator Ontology & Taxonomy"),
            "bullet3": escape_xml("• Memancarkan DTO Canonical Spatial Intent Representation (CSIR) mentah" if is_id else "• Emits raw Canonical Spatial Intent Representation (CSIR) DTO"),
            "arrow": escape_xml("Objek CSIR Mentah (DTO Terstruktur JSON)" if is_id else "Raw CSIR Object (Structured JSON DTO)")
        },
        {
            "num": "3",
            "title": escape_xml("3. Firewall Kendali Deterministik & Invarian Kompilasi Spasial" if is_id else "3. Deterministic Control Firewall & Spatial Query Compilation"),
            "type": escape_xml("SEMANTIC CONTROL & BACKEND"),
            "color_top": "#d97706",
            "color_bg": "#fffbeb",
            "color_border": "#fde68a",
            "bullet1": escape_xml("• SIR Validator: 6-Dimensi Invarian menegakkan prinsip 'No Intent Alteration'" if is_id else "• SIR Validator: 6-Dimension Invariants enforce 'No Intent Alteration'"),
            "bullet2": escape_xml("• Evaluasi batas numerik, domain safety, penetapan: direct_execute | clarify | reject" if is_id else "• Evaluates bounds, domain safety; sets: direct_execute | clarify | reject"),
            "bullet3": escape_xml("• Spatial Query Compiler: Safety Invariant (!isValid ==> Pembatalan Eksekusi SQL)" if is_id else "• Spatial Query Compiler: Safety Invariant (!isValid ==> Zero DB Execution)"),
            "arrow": escape_xml("Pernyataan SQL Terparameterisasi Valid (ST_Distance_Sphere)" if is_id else "Validated Parameterized SQL Statement (ST_Distance_Sphere)")
        },
        {
            "num": "4",
            "title": escape_xml("4. Komputasi Spasial Geodesik Deterministik & Pengayaan Konteks" if is_id else "4. Deterministic Geodesic Spatial Computation & Contextualization"),
            "type": escape_xml("DATA STORAGE & ENGINE"),
            "color_top": "#059669",
            "color_bg": "#f0fdf4",
            "color_border": "#bbf7d0",
            "bullet1": escape_xml("• MySQL 8.0 InnoDB 3NF: wisata JOIN kategori (SPATIAL INDEX pada geom POINT)" if is_id else "• MySQL 8.0 InnoDB 3NF: wisata JOIN kategori (SPATIAL INDEX on geom POINT)"),
            "bullet2": escape_xml("• Kernel C++: ST_Distance_Sphere(POINT(lng, lat), POINT(u_lng, u_lat)) / 1000.0" if is_id else "• C++ Kernel: ST_Distance_Sphere(POINT(lng, lat), POINT(u_lng, u_lat)) / 1000.0"),
            "bullet3": escape_xml("• Filter multi-kriteria: open_now, max_price, status ==> Tupel Fakta Tervalidasi F" if is_id else "• Multi-criteria filter: open_now, max_price, status ==> Verified Fact Table F"),
            "arrow": escape_xml("Himpunan Tupel Fakta Terverifikasi F = {t1, t2, ..., tk}" if is_id else "Verified Fact Tuples Set F = {t1, t2, ..., tk}")
        },
        {
            "num": "5",
            "title": escape_xml("5. Validator Grounding Algoritmik Pasca-Generasi (Grounding Firewall)" if is_id else "5. Post-Generation Algorithmic Grounding Validator (Grounding Firewall)"),
            "type": escape_xml("GROUNDING VERIFICATION"),
            "color_top": "#e11d48",
            "color_bg": "#fff1f2",
            "color_border": "#fecdd3",
            "bullet1": escape_xml("• LLM mensintesis narasi percakapan terikat ketat pada Tabel Fakta F" if is_id else "• LLM synthesizes natural response strictly conditioned on Fact Table F"),
            "bullet2": escape_xml("• Kontrak Algoritmik Ketat: ∀e ∈ Entities(Response), e ∈ Entities(Facts_SQL)" if is_id else "• Strict Grounding Contract: ∀e ∈ Entities(Response), e ∈ Entities(Facts_SQL)"),
            "bullet3": escape_xml("• Garansi matematis: Entity Fabrication Rate = 0,00% (0 Pelanggaran Grounding)" if is_id else "• Mathematical guarantee: Entity Fabrication Rate = 0.00% (0 Grounding Violations)"),
            "arrow": escape_xml("Muatan Ganda Sinkron (Dual-Payload: GeoJSON + Narasi Ter-grounding)" if is_id else "Synchronous Dual-Payload (GeoJSON Features + Grounded Response)")
        },
        {
            "num": "6",
            "title": escape_xml("6. Rendering Multimodal Dwitunggal Sinkron (Interaksi Web GIS)" if is_id else "6. Synchronous Dual-Modal Rendering (Web GIS Client Interaction)"),
            "type": escape_xml("CLIENT PRESENTATION & ROUTING"),
            "color_top": "#0284c7",
            "color_bg": "#f0f9ff",
            "color_border": "#bae6fd",
            "bullet1": escape_xml("• Peta Interaktif Leaflet.js: Auto-pan, pin SVG tematik, popup info terverifikasi" if is_id else "• Interactive Leaflet.js Map: Auto-pan, thematic SVG pins, verified popups"),
            "bullet2": escape_xml("• Mesin Rute OSRM: Poliline navigasi jalan raya turn-by-turn & estimasi waktu" if is_id else "• OSRM Routing Engine: Turn-by-turn road network polyline & transit time"),
            "bullet3": escape_xml("• Panel Percakapan AI: Narasi rekomendasi informatif, akurat, dan ramah" if is_id else "• AI Conversation Drawer: Grounded, informative, and cohesive narrative"),
            "arrow": escape_xml("Status Spasial Tervisualisasi & Umpan Balik Kognitif Pengguna" if is_id else "Visualized Spatial State & User Cognitive Feedback")
        },
        {
            "num": "7",
            "title": escape_xml("7. Evaluasi Kognitif Pengguna & Lingkaran Percakapan Adaptif" if is_id else "7. User Cognitive Evaluation & Adaptive Conversational Refinement"),
            "type": escape_xml("USER EXPERIENCE & ADAPTIVE LOOP"),
            "color_top": "#4f46e5",
            "color_bg": "#eef2ff",
            "color_border": "#c7d2fe",
            "bullet1": escape_xml("• Wisatawan mengevaluasi sebaran spasial, waktu tempuh, tarif, dan kartu wisata" if is_id else "• Tourist evaluates spatial distribution, transit times, tariffs, and POI cards"),
            "bullet2": escape_xml("• Dialog multi-turn: CSIR(t+1) = Merge(CSIR(t), ΔCSIR(t+1)) memperbarui preferensi" if is_id else "• Multi-turn dialog: CSIR(t+1) = Merge(CSIR(t), ΔCSIR(t+1)) updates context"),
            "bullet3": escape_xml("• Menggantikan manipulasi slider manual (Afnarius dkk., 2026) dengan dialog adaptif" if is_id else "• Replaces manual slider tweaking (Afnarius et al., 2026) with adaptive dialog"),
            "arrow": ""
        }
    ]
    
    W = 1080
    card_w = 820
    card_x = 70
    card_h = 108
    gap_y = 52
    start_y = 115
    total_h = start_y + len(stages) * (card_h + gap_y) + 30
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {total_h}" width="{W}" height="{total_h}">')
    svg.append('''
  <defs>
    <linearGradient id="gradHeader" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f766e"/>
      <stop offset="50%" stop-color="#0e7490"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
    <filter id="shadow" x="-3%" y="-4%" width="106%" height="112%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <filter id="headerShadow" x="-2%" y="-5%" width="104%" height="118%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.15"/>
    </filter>
    <marker id="arrowDown" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 2 L 5 8 L 10 2 z" fill="#0284c7"/>
    </marker>
    <marker id="arrowLoop" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 2 1 L 8 5 L 2 9 z" fill="#4f46e5"/>
    </marker>
  </defs>

  <style>
    .font-base { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .stage-title { font-weight: 700; font-size: 14.5px; fill: #0f172a; }
    .stage-desc { font-weight: 450; font-size: 11.5px; fill: #334155; line-height: 1.4; }
    .badge-text { font-weight: 700; font-size: 9.5px; fill: #ffffff; letter-spacing: 0.5px; }
    .num-text { font-weight: 800; font-size: 16px; fill: #ffffff; }
    .arrow-badge-bg { fill: #ffffff; stroke: #94a3b8; stroke-width: 1.2; rx: 11; }
    .arrow-badge-text { font-weight: 600; font-size: 10.5px; fill: #0369a1; }
    .loop-badge-bg { fill: #eef2ff; stroke: #6366f1; stroke-width: 1.5; rx: 12; }
    .loop-badge-text { font-weight: 700; font-size: 11px; fill: #3730a3; }
  </style>

  <!-- Background Canvas -->
  <rect width="100%" height="100%" fill="#f8fafc" rx="14"/>
  <rect x="2" y="2" width="''' + str(W-4) + '''" height="''' + str(total_h-4) + '''" fill="none" stroke="#e2e8f0" stroke-width="2" rx="12"/>

  <!-- Top Header Banner -->
  <g filter="url(#headerShadow)">
    <rect x="25" y="22" width="''' + str(W-50) + '''" height="68" rx="10" fill="url(#gradHeader)"/>
    <text x="''' + str(W/2) + '''" y="50" text-anchor="middle" class="font-base" font-weight="800" font-size="16px" fill="#ffffff" letter-spacing="0.3px">''' + title + '''</text>
    <text x="''' + str(W/2) + '''" y="72" text-anchor="middle" class="font-base" font-weight="500" font-size="12.5px" fill="#ccfbf1">''' + subtitle + '''</text>
  </g>
''')

    # Draw stages
    for i, st in enumerate(stages):
        cur_y = start_y + i * (card_h + gap_y)
        
        # Card container with shadow
        svg.append(f'  <!-- STAGE {st["num"]} -->')
        svg.append(f'  <g filter="url(#shadow)">')
        svg.append(f'    <rect x="{card_x}" y="{cur_y}" width="{card_w}" height="{card_h}" rx="10" fill="{st["color_bg"]}" stroke="{st["color_border"]}" stroke-width="1.8"/>')
        
        # Number badge on the left
        num_cx = card_x + 36
        num_cy = cur_y + card_h / 2
        svg.append(f'    <circle cx="{num_cx}" cy="{num_cy}" r="22" fill="{st["color_top"]}"/>')
        svg.append(f'    <text x="{num_cx}" y="{num_cy + 6}" text-anchor="middle" class="font-base num-text">{st["num"]}</text>')
        
        # Type badge
        type_w = len(st["type"]) * 6.5 + 16
        type_x = card_x + 72
        type_y = cur_y + 14
        svg.append(f'    <rect x="{type_x}" y="{type_y}" width="{type_w}" height="18" rx="4" fill="{st["color_top"]}"/>')
        svg.append(f'    <text x="{type_x + type_w/2}" y="{type_y + 13}" text-anchor="middle" class="font-base badge-text">{st["type"]}</text>')
        
        # Stage title
        title_x = type_x + type_w + 12
        svg.append(f'    <text x="{title_x}" y="{type_y + 14}" class="font-base stage-title">{st["title"]}</text>')
        
        # Divider line
        svg.append(f'    <line x1="{card_x + 72}" y1="{cur_y + 40}" x2="{card_x + card_w - 20}" y2="{cur_y + 40}" stroke="{st["color_border"]}" stroke-width="1.2"/>')
        
        # Bullets
        bx = card_x + 75
        by1 = cur_y + 58
        by2 = cur_y + 76
        by3 = cur_y + 94
        svg.append(f'    <text x="{bx}" y="{by1}" class="font-base stage-desc">{st["bullet1"]}</text>')
        svg.append(f'    <text x="{bx}" y="{by2}" class="font-base stage-desc">{st["bullet2"]}</text>')
        if "bullet3" in st:
            svg.append(f'    <text x="{bx}" y="{by3}" class="font-base stage-desc">{st["bullet3"]}</text>')
        
        svg.append('  </g>')
        
        # Connector arrow to next stage
        if i < len(stages) - 1:
            arrow_x = card_x + card_w / 2 - 40
            arrow_y1 = cur_y + card_h + 3
            arrow_y2 = cur_y + card_h + gap_y - 6
            arrow_mid_y = (arrow_y1 + arrow_y2) / 2
            
            svg.append(f'  <!-- Connector {i+1} -> {i+2} -->')
            svg.append(f'  <line x1="{arrow_x}" y1="{arrow_y1}" x2="{arrow_x}" y2="{arrow_y2}" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arrowDown)"/>')
            
            # Badge over connector
            if st["arrow"]:
                label_txt = st["arrow"]
                txt_w = len(label_txt) * 6.5 + 24
                svg.append(f'  <rect x="{arrow_x - txt_w/2}" y="{arrow_mid_y - 12}" width="{txt_w}" height="22" rx="11" class="arrow-badge-bg"/>')
                svg.append(f'  <text x="{arrow_x}" y="{arrow_mid_y + 3}" text-anchor="middle" class="font-base arrow-badge-text">{label_txt}</text>')

    # -------------------------------------------------------------
    # FEEDBACK LOOP: FROM STAGE 7 BACK TO STAGE 1 / 2
    # -------------------------------------------------------------
    s7_y = start_y + 6 * (card_h + gap_y) + card_h / 2
    s1_y = start_y + 0 * (card_h + gap_y) + card_h / 2 + 10
    loop_x = card_x + card_w + 35
    
    svg.append('  <!-- ADAPTIVE FEEDBACK LOOP -->')
    svg.append(f'  <path d="M {card_x + card_w} {s7_y} H {loop_x} V {s1_y} H {card_x + card_w + 6}" fill="none" stroke="#4f46e5" stroke-width="2.8" stroke-dasharray="6,4" marker-end="url(#arrowLoop)"/>')
    
    # Loop Callout Box (Right Side)
    loop_mid_y = (s1_y + s7_y) / 2
    box_w = 140
    box_h = 160
    box_x = loop_x - box_w / 2
    box_y = loop_mid_y - box_h / 2
    
    svg.append(f'  <rect x="{box_x}" y="{box_y}" width="{box_w}" height="{box_h}" rx="10" class="loop-badge-bg"/>')
    
    loop_head = "LINGKARAN UMPAN BALIK" if is_id else "FEEDBACK LOOP"
    loop_sub1 = "Multi-Turn Dialog"
    loop_sub2 = "Penyempurnaan" if is_id else "Conversational"
    loop_sub3 = "Intensi Percakapan" if is_id else "Intent Refinement"
    loop_math = "CSIR(t+1) = Merge()"
    loop_foot = "Evolusi Slider WIMP" if is_id else "Evolving WIMP GUI"
    loop_foot2 = "(Afnarius dkk., 2026)" if is_id else "(Afnarius et al., 2026)"
    
    svg.append(f'  <text x="{loop_x}" y="{box_y + 24}" text-anchor="middle" class="font-base" font-weight="800" font-size="10.5px" fill="#312e81">{loop_head}</text>')
    svg.append(f'  <line x1="{box_x + 15}" y1="{box_y + 32}" x2="{box_x + box_w - 15}" y2="{box_y + 32}" stroke="#c7d2fe" stroke-width="1.2"/>')
    svg.append(f'  <text x="{loop_x}" y="{box_y + 50}" text-anchor="middle" class="font-base" font-weight="700" font-size="10.5px" fill="#4338ca">{loop_sub1}</text>')
    svg.append(f'  <text x="{loop_x}" y="{box_y + 68}" text-anchor="middle" class="font-base" font-weight="600" font-size="10px" fill="#475569">{loop_sub2}</text>')
    svg.append(f'  <text x="{loop_x}" y="{box_y + 84}" text-anchor="middle" class="font-base" font-weight="600" font-size="10px" fill="#475569">{loop_sub3}</text>')
    svg.append(f'  <rect x="{box_x + 10}" y="{box_y + 94}" width="{box_w - 20}" height="20" rx="4" fill="#4338ca"/>')
    svg.append(f'  <text x="{loop_x}" y="{box_y + 108}" text-anchor="middle" class="font-base" font-weight="700" font-size="9px" fill="#ffffff">{loop_math}</text>')
    svg.append(f'  <text x="{loop_x}" y="{box_y + 132}" text-anchor="middle" class="font-base" font-weight="500" font-size="9.5px" fill="#64748b">{loop_foot}</text>')
    svg.append(f'  <text x="{loop_x}" y="{box_y + 146}" text-anchor="middle" class="font-base" font-weight="500" font-size="9.5px" fill="#64748b">{loop_foot2}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)

def make_database_erd_svg(lang="id"):
    is_id = (lang == "id")
    title = escape_xml("SKEMA BASIS DATA RELASIONAL & SPASIAL (MySQL 8.0 / SRID 4326)" if is_id else "INTEGRATED RELATIONAL-SPATIAL DATABASE SCHEMA (MySQL 8.0 / SRID 4326)")
    subtitle = escape_xml("Model Data Objek Wisata, Kategori Tematik, & Metadata Operasional" if is_id else "Data Model of Tourism POIs, Thematic Categories, & Operational Constraints")
    
    W = 1000
    H = 680
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    svg.append('''
  <defs>
    <linearGradient id="erdHeader" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
    <linearGradient id="tblWisataHeader" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
    <linearGradient id="tblKatHeader" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d9488"/>
      <stop offset="100%" stop-color="#0f766e"/>
    </linearGradient>
    <filter id="erdShadow" x="-3%" y="-4%" width="106%" height="112%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.12"/>
    </filter>
  </defs>

  <style>
    .font-base { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .tbl-header { font-weight: 700; font-size: 14px; fill: #ffffff; }
    .tbl-sub { font-weight: 500; font-size: 10.5px; fill: #e2e8f0; }
    .col-pk { font-weight: 700; font-size: 11.5px; fill: #b91c1c; }
    .col-fk { font-weight: 700; font-size: 11.5px; fill: #0369a1; }
    .col-geo { font-weight: 700; font-size: 11.5px; fill: #047857; }
    .col-name { font-weight: 600; font-size: 11.5px; fill: #1e293b; }
    .col-type { font-family: "Courier New", monospace; font-size: 11px; fill: #64748b; }
  </style>

  <rect width="100%" height="100%" fill="#f8fafc" rx="14"/>
  <rect x="2" y="2" width="''' + str(W-4) + '''" height="''' + str(H-4) + '''" fill="none" stroke="#e2e8f0" stroke-width="2" rx="12"/>

  <!-- Header -->
  <g filter="url(#erdShadow)">
    <rect x="25" y="22" width="''' + str(W-50) + '''" height="60" rx="10" fill="url(#erdHeader)"/>
    <text x="''' + str(W/2) + '''" y="48" text-anchor="middle" class="font-base" font-weight="800" font-size="16px" fill="#ffffff">''' + title + '''</text>
    <text x="''' + str(W/2) + '''" y="68" text-anchor="middle" class="font-base" font-weight="500" font-size="12px" fill="#94a3b8">''' + subtitle + '''</text>
  </g>

  <!-- TABLE: kategori (Parent / Reference Table) -->
  <g filter="url(#erdShadow)">
    <rect x="50" y="115" width="340" height="230" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="50" y="115" width="340" height="42" rx="8" fill="url(#tblKatHeader)"/>
    <rect x="50" y="145" width="340" height="12" fill="url(#tblKatHeader)"/>
    <text x="70" y="136" class="font-base tbl-header">kategori</text>
    <text x="70" y="150" class="font-base tbl-sub">Tabel Dimensi / Taksonomi Wisata</text>

    <!-- Rows -->
    <line x1="50" y1="157" x2="390" y2="157" stroke="#e2e8f0"/>
    <text x="65" y="180" class="font-base col-pk">[PK] id</text> <text x="250" y="180" class="col-type">INT AUTO_INC</text>
    <line x1="50" y1="195" x2="390" y2="195" stroke="#f1f5f9"/>
    <text x="65" y="215" class="font-base col-name">nama_kategori</text> <text x="250" y="215" class="col-type">VARCHAR(100)</text>
    <line x1="50" y1="230" x2="390" y2="230" stroke="#f1f5f9"/>
    <text x="65" y="250" class="font-base col-name">slug</text> <text x="250" y="250" class="col-type">VARCHAR(100)</text>
    <line x1="50" y1="265" x2="390" y2="265" stroke="#f1f5f9"/>
    <text x="65" y="285" class="font-base col-name">deskripsi</text> <text x="250" y="285" class="col-type">TEXT</text>
    <line x1="50" y1="300" x2="390" y2="300" stroke="#f1f5f9"/>
    <text x="65" y="320" class="font-base col-name">icon_marker</text> <text x="250" y="320" class="col-type">VARCHAR(50)</text>
  </g>

  <!-- TABLE: wisata (Main Fact / Spatial Table) -->
  <g filter="url(#erdShadow)">
    <rect x="520" y="115" width="430" height="520" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="520" y="115" width="430" height="42" rx="8" fill="url(#tblWisataHeader)"/>
    <rect x="520" y="145" width="430" height="12" fill="url(#tblWisataHeader)"/>
    <text x="540" y="136" class="font-base tbl-header">wisata</text>
    <text x="540" y="150" class="font-base tbl-sub">Tabel Entitas Wisata Spasial (22 Curated POIs Kota Padang)</text>

    <!-- Rows -->
    <line x1="520" y1="157" x2="950" y2="157" stroke="#e2e8f0"/>
    <text x="535" y="180" class="font-base col-pk">[PK] id</text> <text x="780" y="180" class="col-type">INT AUTO_INC</text>
    <line x1="520" y1="195" x2="950" y2="195" stroke="#f1f5f9"/>
    <text x="535" y="215" class="font-base col-fk">[FK] kategori_id</text> <text x="780" y="215" class="col-type">INT (kategori.id)</text>
    <line x1="520" y1="230" x2="950" y2="230" stroke="#f1f5f9"/>
    <text x="535" y="250" class="font-base col-name">nama_wisata</text> <text x="780" y="250" class="col-type">VARCHAR(255)</text>
    <line x1="520" y1="265" x2="950" y2="265" stroke="#f1f5f9"/>
    <text x="535" y="285" class="font-base col-geo">[GEO] latitude</text> <text x="780" y="285" class="col-type">DECIMAL(10,8)</text>
    <line x1="520" y1="300" x2="950" y2="300" stroke="#f1f5f9"/>
    <text x="535" y="320" class="font-base col-geo">[GEO] longitude</text> <text x="780" y="320" class="col-type">DECIMAL(11,8)</text>
    <line x1="520" y1="335" x2="950" y2="335" stroke="#f1f5f9"/>
    <text x="535" y="355" class="font-base col-geo">[SPATIAL] geom</text> <text x="780" y="355" class="col-type">POINT SRID 4326</text>
    <line x1="520" y1="370" x2="950" y2="370" stroke="#f1f5f9"/>
    <text x="535" y="390" class="font-base col-name">harga_tiket</text> <text x="780" y="390" class="col-type">INT (Rupiah)</text>
    <line x1="520" y1="405" x2="950" y2="405" stroke="#f1f5f9"/>
    <text x="535" y="425" class="font-base col-name">jam_buka / jam_tutup</text> <text x="780" y="425" class="col-type">TIME</text>
    <line x1="520" y1="440" x2="950" y2="440" stroke="#f1f5f9"/>
    <text x="535" y="460" class="font-base col-name">hari_buka</text> <text x="780" y="460" class="col-type">VARCHAR(100)</text>
    <line x1="520" y1="475" x2="950" y2="475" stroke="#f1f5f9"/>
    <text x="535" y="495" class="font-base col-name">fasilitas</text> <text x="780" y="495" class="col-type">TEXT</text>
    <line x1="520" y1="510" x2="950" y2="510" stroke="#f1f5f9"/>
    <text x="535" y="530" class="font-base col-name">foto / gambar</text> <text x="780" y="530" class="col-type">VARCHAR(255)</text>
    <line x1="520" y1="545" x2="950" y2="545" stroke="#f1f5f9"/>
    <text x="535" y="565" class="font-base col-name">status_operasional</text> <text x="780" y="565" class="col-type">VARCHAR(50)</text>
    <line x1="520" y1="580" x2="950" y2="580" stroke="#f1f5f9"/>
    <text x="535" y="605" class="font-base col-name">deskripsi</text> <text x="780" y="605" class="col-type">LONGTEXT</text>
  </g>

  <!-- Relationship Connector Line (1 to Many) -->
  <path d="M 390 180 H 460 V 215 H 520" fill="none" stroke="#0284c7" stroke-width="2.5"/>
  <circle cx="390" cy="180" r="4" fill="#0284c7"/>
  <polygon points="520,215 510,210 510,220" fill="#0284c7"/>

  <!-- Relationship Pill Badge -->
  <rect x="420" y="185" width="60" height="24" rx="6" fill="#0284c7"/>
  <text x="450" y="201" text-anchor="middle" class="font-base" font-weight="700" font-size="11px" fill="#ffffff">1 : N</text>

  <!-- Spatial Index Callout Box -->
  <g filter="url(#erdShadow)">
    <rect x="50" y="380" width="340" height="150" rx="8" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
    <text x="70" y="410" class="font-base" font-weight="700" font-size="13px" fill="#166534">SPATIAL INDEX &amp; FUNGSI GEODETIK</text>
    <line x1="70" y1="420" x2="370" y2="420" stroke="#bbf7d0" stroke-width="1"/>
    <text x="70" y="445" class="font-base" font-weight="500" font-size="11px" fill="#14532d">• SPATIAL INDEX (geom) pada MySQL 8.0</text>
    <text x="70" y="468" class="font-base" font-weight="500" font-size="11px" fill="#14532d">• ST_Distance_Sphere(geom, POINT(u_lng, u_lat))</text>
    <text x="70" y="491" class="font-base" font-weight="500" font-size="11px" fill="#14532d">• Geodesik WGS84: Jarak Great-Circle Presisi Tinggi</text>
    <text x="70" y="514" class="font-base" font-weight="500" font-size="11px" fill="#14532d">• Filter Multikriteria: status, jam_buka, harga_tiket</text>
  </g>
</svg>''')
    return '\n'.join(svg)

def make_architecture_5layer_svg(lang="id"):
    is_id = (lang == "id")
    title = escape_xml("ARSITEKTUR SISTEM INFORMASI SPASIAL CERDAS 5-LAYER" if is_id else "5-LAYER ARCHITECTURE OF INTELLIGENT WEB GIS")
    subtitle = escape_xml("Dual-Process Cognitive Air-Gap & Deterministic Grounding Firewall (Kota Padang)" if is_id else "Dual-Process Cognitive Air-Gap & Deterministic Grounding Firewall (Padang City)")
    
    layers = [
        {
            "num": "L1",
            "name": escape_xml("CONVERSATIONAL INTERACTION LAYER (PRESENTATION / CLIENT)"),
            "sub": escape_xml("Antarmuka Dwitunggal Sinkron: Full-viewport Leaflet.js + Floating AI Chat Drawer" if is_id else "Synchronous Dual Interface: Full-viewport Leaflet.js + Floating AI Chat Drawer"),
            "tech": escape_xml("HTML5 Geolocation (GPS) | Leaflet.js OSM | OSRM Routing Engine | Responsive CSS"),
            "color": "#0284c7",
            "bg": "#f0f9ff",
            "border": "#bae6fd",
            "arrow": escape_xml("[A] Kueri Bahasa Alami + Konteks Situasional (GPS, Waktu Sirkadian)" if is_id else "[A] Natural Language Query + Situational Context (GPS, Circadian Time)")
        },
        {
            "num": "L2",
            "name": escape_xml("LLM SEMANTIC INTERPRETATION LAYER (COGNITIVE AIR-GAP)"),
            "sub": escape_xml("DeepSeek API (temperature: 0.0, response_format: JSON) Terisolasi dari Basis Data" if is_id else "DeepSeek API (temperature: 0.0, JSON mode) Isolated from Database Access"),
            "tech": escape_xml("Ekstraksi Slot Semantik Spasial | Ontologi Operator Spasial | Taksonomi Klaster Wisata"),
            "color": "#7c3aed",
            "bg": "#faf5ff",
            "border": "#e9d5ff",
            "arrow": escape_xml("[B] Objek CSIR Mentah (DTO Canonical Spatial Intent Representation)" if is_id else "[B] Raw CSIR Object (Canonical Spatial Intent Representation DTO)")
        },
        {
            "num": "L3",
            "name": escape_xml("SEMANTIC CONTROL & COMPILATION LAYER (BACKEND: CodeIgniter 4 / PHP 8.2)"),
            "sub": escape_xml("SIR Validator 6-Dimensi ('No Intent Alteration') & Spatial Query Compiler" if is_id else "6-Dimension SIR Validator ('No Intent Alteration') & Spatial Query Compiler"),
            "tech": escape_xml("Kebijakan: direct_execute | clarify_user | reject_out_of_scope | Safety Invariant (!isValid ==> 0 DB Load)"),
            "color": "#d97706",
            "bg": "#fffbeb",
            "border": "#fde68a",
            "arrow": escape_xml("[C] Kueri Spasial SQL Terparameterisasi dengan ST_Distance_Sphere" if is_id else "[C] Validated Parameterized Spatial SQL with ST_Distance_Sphere")
        },
        {
            "num": "L4",
            "name": escape_xml("DETERMINISTIC SPATIAL COMPUTATION LAYER (DATA STORAGE & ENGINE)"),
            "sub": escape_xml("MySQL 8.0 InnoDB (SRID 4326 POINT) | Komputasi Jarak Geodesik C++ Bawaan" if is_id else "MySQL 8.0 InnoDB (SRID 4326 POINT) | Built-in C++ Great-Circle Computation"),
            "tech": escape_xml("ST_Distance_Sphere(POINT, POINT) / 1000.0 | SPATIAL INDEX (geom) | Filter Relasional (open_now, harga)"),
            "color": "#059669",
            "bg": "#f0fdf4",
            "border": "#bbf7d0",
            "arrow": escape_xml("[D] Himpunan Tupel Fakta Tervalidasi F = {t1, t2, ..., tk}" if is_id else "[D] Verified Fact Tuples Set F = {t1, t2, ..., tk}")
        },
        {
            "num": "L5",
            "name": escape_xml("GROUNDED RESPONSE & VERIFICATION LAYER (GROUNDING FIREWALL)"),
            "sub": escape_xml("Algorithmic Grounding Validator: Kontrak Ketat ∀e ∈ Entities(Response), e ∈ F" if is_id else "Algorithmic Grounding Validator: Strict Contract ∀e ∈ Entities(Response), e ∈ F"),
            "tech": escape_xml("Substitusi Otomatis Token Halusinasi dengan DTO Faktual | Dual-Payload Dispatcher (GeoJSON + Text)"),
            "color": "#e11d48",
            "bg": "#fff1f2",
            "border": "#fecdd3",
            "arrow": escape_xml("[E] Penanda Peta Sinkron, Rute Jalan Raya, & Narasi Ter-grounding" if is_id else "[E] Synchronized Map Pins, Highway Route, & Grounded Response")
        }
    ]
    
    W = 1040
    card_w = 940
    card_x = 50
    card_h = 88
    gap_y = 44
    start_y = 108
    total_h = start_y + len(layers) * (card_h + gap_y) + 30
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {total_h}" width="{W}" height="{total_h}">')
    svg.append('''
  <defs>
    <linearGradient id="archHeader" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f766e"/>
      <stop offset="50%" stop-color="#0369a1"/>
      <stop offset="100%" stop-color="#1e40af"/>
    </linearGradient>
    <filter id="archShadow" x="-2%" y="-4%" width="104%" height="112%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.09"/>
    </filter>
    <marker id="archArrow" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 2 L 5 8 L 10 2 z" fill="#0284c7"/>
    </marker>
  </defs>

  <style>
    .font-base { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .layer-title { font-weight: 700; font-size: 13.5px; fill: #0f172a; }
    .layer-sub { font-weight: 500; font-size: 11.5px; fill: #334155; }
    .layer-tech { font-family: "Courier New", monospace; font-size: 10.5px; fill: #475569; }
    .arrow-text { font-weight: 600; font-size: 10.5px; fill: #0369a1; }
  </style>

  <rect width="100%" height="100%" fill="#f8fafc" rx="14"/>
  <rect x="2" y="2" width="''' + str(W-4) + '''" height="''' + str(total_h-4) + '''" fill="none" stroke="#e2e8f0" stroke-width="2" rx="12"/>

  <!-- Banner -->
  <g filter="url(#archShadow)">
    <rect x="25" y="22" width="''' + str(W-50) + '''" height="64" rx="10" fill="url(#archHeader)"/>
    <text x="''' + str(W/2) + '''" y="48" text-anchor="middle" class="font-base" font-weight="800" font-size="16px" fill="#ffffff">''' + title + '''</text>
    <text x="''' + str(W/2) + '''" y="68" text-anchor="middle" class="font-base" font-weight="500" font-size="12px" fill="#ccfbf1">''' + subtitle + '''</text>
  </g>
''')

    for i, ly in enumerate(layers):
        cur_y = start_y + i * (card_h + gap_y)
        
        svg.append(f'  <!-- {ly["num"]} -->')
        svg.append(f'  <g filter="url(#archShadow)">')
        svg.append(f'    <rect x="{card_x}" y="{cur_y}" width="{card_w}" height="{card_h}" rx="8" fill="{ly["bg"]}" stroke="{ly["border"]}" stroke-width="1.6"/>')
        
        # Num pill
        svg.append(f'    <rect x="{card_x + 16}" y="{cur_y + 14}" width="38" height="24" rx="6" fill="{ly["color"]}"/>')
        svg.append(f'    <text x="{card_x + 35}" y="{cur_y + 30}" text-anchor="middle" class="font-base" font-weight="800" font-size="12.5px" fill="#ffffff">{ly["num"]}</text>')
        
        # Name
        svg.append(f'    <text x="{card_x + 64}" y="{cur_y + 30}" class="font-base layer-title">{ly["name"]}</text>')
        # Sub
        svg.append(f'    <text x="{card_x + 64}" y="{cur_y + 52}" class="font-base layer-sub">{ly["sub"]}</text>')
        # Tech
        svg.append(f'    <text x="{card_x + 64}" y="{cur_y + 72}" class="font-base layer-tech">{ly["tech"]}</text>')
        svg.append(f'  </g>')
        
        if i < len(layers) - 1:
            arr_x = card_x + card_w / 2
            arr_y1 = cur_y + card_h + 2
            arr_y2 = cur_y + card_h + gap_y - 6
            mid_y = (arr_y1 + arr_y2) / 2
            
            svg.append(f'  <line x1="{arr_x}" y1="{arr_y1}" x2="{arr_x}" y2="{arr_y2}" stroke="#0284c7" stroke-width="2" marker-end="url(#archArrow)"/>')
            
            lbl = ly["arrow"]
            lbl_w = len(lbl) * 6.5 + 24
            svg.append(f'  <rect x="{arr_x - lbl_w/2}" y="{mid_y - 11}" width="{lbl_w}" height="20" rx="10" fill="#ffffff" stroke="#94a3b8" stroke-width="1.2"/>')
            svg.append(f'  <text x="{arr_x}" y="{mid_y + 3}" text-anchor="middle" class="font-base arrow-text">{lbl}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)

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

# Main generation
print("Generating diagrams...")

# 1. Operational Framework (Gambar 2 / Figure 2)
with open(os.path.join(IMG_DIR, "gambar2_kerangka_operasional.svg"), "w") as f:
    f.write(make_operational_framework_svg("id"))
with open(os.path.join(IMG_DIR, "figure2_operational_framework.svg"), "w") as f:
    f.write(make_operational_framework_svg("en"))

# 2. Database ERD (Gambar 3 / Figure 3)
with open(os.path.join(IMG_DIR, "gambar3_skema_basisdata.svg"), "w") as f:
    f.write(make_database_erd_svg("id"))
with open(os.path.join(IMG_DIR, "figure3_database_schema.svg"), "w") as f:
    f.write(make_database_erd_svg("en"))

# 3. 5-Layer Architecture (Gambar 1 / Figure 1)
with open(os.path.join(IMG_DIR, "gambar1_arsitektur_sistem.svg"), "w") as f:
    f.write(make_architecture_5layer_svg("id"))
with open(os.path.join(IMG_DIR, "figure1_system_architecture.svg"), "w") as f:
    f.write(make_architecture_5layer_svg("en"))

# 4. Concrete Execution Trace (Gambar 4 / Figure 4)
with open(os.path.join(IMG_DIR, "gambar4_alur_eksekusi_konkret.svg"), "w") as f:
    f.write(make_trace_diagram_svg("id"))
with open(os.path.join(IMG_DIR, "figure4_concrete_execution_trace.svg"), "w") as f:
    f.write(make_trace_diagram_svg("en"))

# Convert all SVGs to high-resolution PNGs via rsvg-convert (300 DPI)
svg_files = [
    "gambar1_arsitektur_sistem.svg",
    "figure1_system_architecture.svg",
    "gambar2_kerangka_operasional.svg",
    "figure2_operational_framework.svg",
    "gambar3_skema_basisdata.svg",
    "figure3_database_schema.svg",
    "gambar4_alur_eksekusi_konkret.svg",
    "figure4_concrete_execution_trace.svg",
]

for s in svg_files:
    svg_p = os.path.join(IMG_DIR, s)
    png_p = os.path.join(IMG_DIR, s.replace(".svg", ".png"))
    cmd = ["rsvg-convert", "-d", "300", "-p", "300", svg_p, "-o", png_p]
    subprocess.run(cmd, check=True)
    print(f"Generated: {png_p}")

# Sequential Renumbering Copies: 4 -> 5, 5 -> 6, 6 -> 7
import shutil
shutil.copyfile(os.path.join(IMG_DIR, "gambar4_antarmuka_webgis.png"), os.path.join(IMG_DIR, "gambar5_antarmuka_webgis.png"))
shutil.copyfile(os.path.join(IMG_DIR, "gambar5_rute_navigasi.png"), os.path.join(IMG_DIR, "gambar6_rute_navigasi.png"))
shutil.copyfile(os.path.join(IMG_DIR, "gambar6_evaluasi_halusinasi.png"), os.path.join(IMG_DIR, "gambar7_evaluasi_halusinasi.png"))

shutil.copyfile(os.path.join(IMG_DIR, "figure4_webgis_interface.png"), os.path.join(IMG_DIR, "figure5_webgis_interface.png"))
shutil.copyfile(os.path.join(IMG_DIR, "figure5_routing_navigation.png"), os.path.join(IMG_DIR, "figure6_routing_navigation.png"))
shutil.copyfile(os.path.join(IMG_DIR, "figure6_hallucination_evaluation.png"), os.path.join(IMG_DIR, "figure7_hallucination_evaluation.png"))

# Copy to brain artifact directory
brain_dir = "/home/ubuntu/.gemini/antigravity-ide/brain/586c50a5-1bb9-4da7-a0c5-ba09f79594bf"
for f in ["gambar4_alur_eksekusi_konkret.png", "figure4_concrete_execution_trace.png"]:
    shutil.copyfile(os.path.join(IMG_DIR, f), os.path.join(brain_dir, f))

print("All diagrams successfully generated and synchronized!")


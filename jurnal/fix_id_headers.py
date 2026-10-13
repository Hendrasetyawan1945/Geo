#!/usr/bin/env python3
"""
fix_id_headers.py
Normalizes all subsection and sub-subsection headers in DRAFT_JURNAL_ILMIAH_INDONESIA.md.
"""

import os
import re

JURNAL_DIR = "/var/www/html/Geo/jurnal"
FILE_PATH = os.path.join(JURNAL_DIR, "DRAFT_JURNAL_ILMIAH_INDONESIA.md")

with open(FILE_PATH, "r", encoding="utf-8") as f:
    text = f.read()

replacements = [
    # Section 3
    ("### 2.1.1 Kerangka Tiga Tingkat Kebenaran (The Tripartite Correctness Framework)", "#### 3.1.1 Kerangka Tiga Tingkat Kebenaran (The Tripartite Correctness Framework)"),
    ("### 2.3.1 Model Pelacakan Status Percakapan Bertingkat (Multi-Turn Conversational State Tracking Model)", "#### 3.2.1 Model Pelacakan Status Percakapan Bertingkat (Multi-Turn Conversational State Tracking Model)"),
    ("### 2.3.2 Asal-Usul Data (Data Provenance) dan Pemisahan Tanggung Jawab Komputasi", "#### 3.2.2 Asal-Usul Data (Data Provenance) dan Pemisahan Tanggung Jawab Komputasi"),
    ("### 2.3.3 Taksonomi Lima Operasi Kontrol Semantik", "#### 3.2.3 Taksonomi Lima Operasi Kontrol Semantik"),
    ("### 2.4.1 Tabel Kontrak Formal Ontologi Operator Spasial", "#### 3.5.1 Tabel Kontrak Formal Ontologi Operator Spasial"),
    ("### 2.4.2 Pipa Formal Resolusi Entitas Deterministik (Deterministic Entity Resolution)", "#### 3.3.1 Pipa Formal Resolusi Entitas Deterministik (Deterministic Entity Resolution)"),
    ("#### 3.7.1 Formalisasi Matematis Grounding Fidelity", "#### 3.6.1 Formalisasi Matematis Grounding Fidelity"),
    ("#### 3.7.2 Verifikasi Algoritmik Pasca-Generasi (Algorithmic Grounding Validator)", "#### 3.6.2 Verifikasi Algoritmik Pasca-Generasi (Algorithmic Grounding Validator)"),
    
    # Section 4
    ("### 3.1.1 Kerangka Operasional Interaksi Spasial Eksploratori Terkontrol Semantik", "#### 4.2.1 Kerangka Operasional Interaksi Spasial Eksploratori Terkontrol Semantik"),
    ("### 3.1.2 Model Konseptual Basis Data Spasial Relasional (Normalisasi 3NF vs. Partisi Kategori DTExplorer)", "#### 4.2.2 Model Konseptual Basis Data Spasial Relasional (Normalisasi 3NF vs. Partisi Kategori DTExplorer)"),
    
    # Section 6
    ("#### 4.2.1 Evaluasi Kebenaran Predikat Spasial (Pure Spatial: 100,00%, Overall Compliance: 100,00%)", "#### 6.1.1 Evaluasi Kebenaran Predikat Spasial (Pure Spatial: 100,00%, Overall Compliance: 100,00%)"),
    ("#### 4.2.2 Evaluasi Diagnostik GroundingValidator dan Batasan Lingkup Skema Tertutup", "#### 6.1.2 Evaluasi Diagnostik GroundingValidator dan Batasan Lingkup Skema Tertutup"),
    ("#### 4.2.3 Jejak Sumber Data dan Batasan Ilmiah Dataset 22 Objek Wisata (Data Provenance)", "#### 6.1.3 Batasan Ilmiah Dataset 22 Objek Wisata pada Evaluasi Empiris"),
    ("#### 4.5.1 Pembuktian Manfaat Ilmiah Arsitektur: Jawaban terhadap Empat Pertanyaan Kritis", "#### 6.3.1 Pembuktian Manfaat Ilmiah Arsitektur terhadap Empat Pertanyaan Kritis"),
    ("#### 4.5.2 Evaluasi Keamanan Kompiler SQL Deterministik (Security Evaluation)", "#### 6.6.1 Evaluasi Keamanan Kompiler SQL Deterministik (Security Evaluation)"),
    ("#### 4.5.3 Evaluasi Eksperimental Pelacakan Status Percakapan Multi-Turn (Multi-Turn State Tracking)", "#### 6.3.2 Evaluasi Eksperimental Pelacakan Status Percakapan Multi-Turn (Multi-Turn State Tracking)")
]

for old, new in replacements:
    if old in text:
        text = text.replace(old, new)
        print(f"[✓] Replaced: {old[:40]} -> {new[:40]}")
    else:
        print(f"[!] Not found: {old[:40]}")

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("[✓] All headers successfully normalized.")

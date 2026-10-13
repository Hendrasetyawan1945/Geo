#!/usr/bin/env python3
"""
build_restructured_indonesia.py
Restructures DRAFT_JURNAL_ILMIAH_INDONESIA.md into the 9-section structure requested by the reviewer:
1. Introduction
2. Related Work
3. Methodology
4. System Implementation
5. Experimental Design
6. Results
7. Discussion
8. Threats to Validity and Limitations
9. Conclusion
"""

import os
import re

JURNAL_DIR = "/var/www/html/Geo/jurnal"
SRC_PATH = os.path.join(JURNAL_DIR, "DRAFT_JURNAL_ILMIAH_INDONESIA.md")

with open(SRC_PATH, "r", encoding="utf-8") as f:
    src = f.read()

# Helper to slice text between two regex headers
def get_between(start_pat, end_pat, text=src):
    m_start = re.search(start_pat, text, re.M)
    if not m_start:
        raise ValueError(f"Pattern start not found: {start_pat}")
    start_pos = m_start.end()
    if end_pat:
        m_end = re.search(end_pat, text[start_pos:], re.M)
        if not m_end:
            raise ValueError(f"Pattern end not found: {end_pat}")
        return text[start_pos:start_pos + m_end.start()].strip()
    else:
        return text[start_pos:].strip()

# 1. Header, Abstract
header_and_abstract = text_header = src[:src.find("## 1. PENDAHULUAN")].strip()

# Update abstract to ensure strongest results are prominently highlighted and bounded
header_and_abstract = header_and_abstract.replace(
    "92,50%** (37/40) dengan keselarasan amplob eksekusi pasca-kebijakan **90,00%** (36/40), rata-rata akurasi tingkat atribut (*field-level*) **99,25% (398/401)**",
    "87,50%** (35/40) dengan keselarasan amplob eksekusi pasca-kebijakan **90,00%** (36/40), rata-rata akurasi tingkat atribut (*field-level*) **98,62% (748/758)**"
)
header_and_abstract = header_and_abstract.replace(
    "92.50%** (37/40) (**90.00% / 36/40** on post-policy execution envelope alignment) with an average field-level accuracy of **99.25% (398/401)**",
    "87.50%** (35/40) (**90.00% / 36/40** on post-policy execution envelope alignment) with an average field-level accuracy of **98.62% (748/758)**"
)

# Extract sections
sec1_raw = get_between(r"^## 1\. PENDAHULUAN\s*", r"^## 2\. LANDASAN TEORETIS")
sec2_raw = get_between(r"^## 2\. LANDASAN TEORETIS.*\s*", r"^## 3\. METODOLOGI DAN ARSITEKTUR")
sec3_raw = get_between(r"^## 3\. METODOLOGI DAN ARSITEKTUR.*\s*", r"^## 4\. HASIL EVALUASI DAN PEMBAHASAN")
sec4_raw = get_between(r"^## 4\. HASIL EVALUASI DAN PEMBAHASAN\s*", r"^## 5\. KESIMPULAN DAN SARAN")
sec5_raw = get_between(r"^## 5\. KESIMPULAN DAN SARAN\s*", r"^## DAFTAR PUSTAKA")
references_and_appendix = src[src.find("## DAFTAR PUSTAKA"):].strip()

print("[✓] Raw text successfully sliced into sections.")

#!/usr/bin/env python3
with open('/var/www/html/Geo/jurnal/DRAFT_JURNAL_IJG_ENGLISH.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for idx, l in enumerate(lines):
    if l.startswith('#'):
        print(f"L{idx+1:04d}: {l.strip()}")

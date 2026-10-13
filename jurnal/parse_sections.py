#!/usr/bin/env python3
import re

with open('/var/www/html/Geo/jurnal/DRAFT_JURNAL_ILMIAH_INDONESIA.md', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for idx, line in enumerate(lines):
    if line.startswith('#'):
        print(f"L{idx+1:04d}: {line}")

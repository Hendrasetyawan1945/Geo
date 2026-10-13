#!/usr/bin/env python3
import os
import re

JURNAL_DIR = "/var/www/html/Geo/jurnal"
SRC_FILE = os.path.join(JURNAL_DIR, "DRAFT_JURNAL_ILMIAH_INDONESIA.md")

with open(SRC_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Verify that file has been read
print(f"Read source file: {len(text)} chars")

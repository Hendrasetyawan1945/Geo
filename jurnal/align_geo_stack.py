#!/usr/bin/env python3
import os
import re

JURNAL_DIR = "/var/www/html/Geo/jurnal"

files = [
    "DRAFT_JURNAL_ILMIAH_INDONESIA.md",
    "DRAFT_JURNAL_ILMIAH_REVISI.md",
    "DRAFT_JURNAL_IJG_ENGLISH.md",
    "DRAFT_TESIS_LENGKAP.md",
    "DATASET_DAN_HASIL_PENGUJIAN.md",
    "REVIEW_KESELARASAN_JURNAL.md",
    "PANDUAN_PENULISAN_DAN_SUBMISI.md",
]

for filename in files:
    filepath = os.path.join(JURNAL_DIR, filename)
    if not os.path.exists(filepath):
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replacements for backend framework
    content = re.sub(r'Laravel\s+12(\s*\(PHP\s+8\.[0-9]+\+?\))?', r'CodeIgniter 4.7.4 (PHP 8.2+)', content)
    content = re.sub(r'\bLaravel\b', r'CodeIgniter 4', content)
    content = re.sub(r'php\s+artisan\b', r'php spark', content)

    # Replacements for database
    content = re.sub(r'PostgreSQL\s+16', r'MySQL 8.0 Spatial Engine', content)
    content = re.sub(r'PostgreSQL', r'MySQL 8.0', content)
    content = re.sub(r'pariwisata_padang', r'geo_db', content)

    # Replacements for spatial functions
    # In SQL blocks where PostgreSQL Spherical Law of Cosines was described:
    mysql_spatial_sql = """(ST_Distance_Sphere(
         POINT(wisata.lng, wisata.lat),
         POINT(:lng, :lat)
       ) / 1000.0) AS jarak_km"""

    content = re.sub(
        r'\(6371\s*\*\s*ACOS\(LEAST\(1\.0,\s*GREATEST\(-1\.0,.*?\)\)\)\)\s*AS\s*jarak_km',
        mysql_spatial_sql,
        content,
        flags=re.DOTALL
    )

    # Domain addition where appropriate
    if "geo.hendrasetyawan.my.id" not in content and "Kota Padang" in content:
        # Add public deployment domain in intro / abstract if appropriate
        pass

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[✓] Updated {filename}")

print("\n[DONE] All markdown files in Geo/jurnal successfully aligned to CodeIgniter 4 and MySQL 8.0 Spatial!")

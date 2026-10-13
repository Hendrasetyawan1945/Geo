# Panduan Reproduksibilitas Eksperimen Empiris (Reproducibility Guide)

Panduan ini mendokumentasikan prosedur formal untuk mereproduksi seluruh hasil eksperimen, benchmark, pengujian integrasi database, dan evaluasi 4-lapis sistem rekomendasi spasial cerdas Kota Padang.

---

## 1. Lingkungan Sistem & Prasyarat (System Environment)

- **Sistem Operasi**: Linux Ubuntu 24.04 LTS (x86_64)
- **Runtime**: PHP 8.2.33 CLI (ekstensi: `mysqli`, `pdo_mysql`, `mbstring`, `curl`, `json`)
- **Basis Data**: MySQL 8.0.46 (geo_db, 22 POI acuan, mesin spasial `ST_Distance_Sphere`)
- **Framework**: CodeIgniter 4.7.4
- **Pengujian Unit**: PHPUnit 10.5.64

---

## 2. Struktur Artefak Reproduksibilitas

```
benchmark/
├── dataset_40.json                       # 40 Skenario Terstandarisasi (19 Field CSIR Kanonikal)
├── DATASET_PROVENANCE_22_POI.md          # Provenans 22 POI Ground-Truth Kota Padang
├── run_all.sh                            # Skrip Master Runner Otomatis Seluruh Benchmark
├── proposed/
│   ├── evaluator.php                     # Runner Evaluasi Sistem Usulan (Dual Control Boundaries)
│   ├── results_replay.json               # Hasil Evaluasi Mode Standar Replay / Mock
│   ├── raw_evaluations_replay.json       # Log Mentah 120 Evaluasi Replay
│   ├── results_live.json                 # Hasil Evaluasi Mode LIVE LLM
│   ├── raw_evaluations_live.json         # Log Mentah 120 Evaluasi LIVE
│   └── latency_stage_breakdown.json      # Rincian Latensi 5 Tahap Pipeline
├── baseline_text2sql/
│   ├── runner.php                        # Runner Baseline 1 (Direct Text-to-SQL)
│   ├── prompt.txt                        # DDL Schema Prompt
│   ├── results_replay.json               # Hasil Eksekusi Replay SQL pada MySQL 8.0
│   └── raw_evaluations_replay.json       # Log Mentah 120 Evaluasi
├── baseline_unconstrained/
│   ├── runner.php                        # Runner Baseline 2 (Unconstrained Free-form LLM)
│   ├── prompt.txt                        # Zero-Shot Tourist Guide Prompt
│   ├── results_replay.json               # Hasil Evaluasi Bebas Replay
│   └── raw_evaluations_replay.json       # Log Mentah 120 Evaluasi
└── reproducibility/
    ├── ENVIRONMENT_METADATA.json         # Spesifikasi Lengkap Perangkat & DBMS
    ├── DEPENDENCY_LOCK_SNAPSHOT.json     # Versi Terkunci Paket Composer & Alat
    ├── REPRODUCIBILITY_GUIDE.md          # Panduan Ini
    └── SHA256SUMS.txt                    # Checksum Kriptografis Berkas Eksperimen
```

---

## 3. Perintah Eksekusi Pengujian & Benchmark

### A. Menjalankan Rangkaian Pengujian PHPUnit (Unit & Database Integration)
```bash
cd /var/www/html/Geo
vendor/bin/phpunit
```
Target capaian: **45 tests, 172 assertions, 100% PASS**.
Mencakup pengujian integrasi database MySQL (`SpatialDatabaseIntegrationTest`) dan verifikasi grounding klaim (`GroundingValidatorTest`).

### B. Menjalankan Evaluasi Sistem Usulan (Proposed Architecture)
- **Mode Standard Deterministic Replay (Evaluasi Cepat & CI/CD)**:
  ```bash
  cd /var/www/html/Geo
  php benchmark/proposed/evaluator.php
  ```
  Menghasilkan: `benchmark/proposed/results_replay.json` dan `benchmark/proposed/raw_evaluations_replay.json`.

- **Mode LIVE LLM (Menggunakan DeepSeek API)**:
  ```bash
  cd /var/www/html/Geo
  php benchmark/proposed/evaluator.php --live
  ```
  Menghasilkan: `benchmark/proposed/results_live.json` dan `benchmark/proposed/raw_evaluations_live.json`.

### C. Menjalankan Baseline 1: Direct Text-to-SQL
```bash
cd /var/www/html/Geo
php benchmark/baseline_text2sql/runner.php
```
Mengeksekusi SQL secara nyata terhadap MySQL 8.0 `geo_db` dan mencatat syntax error, koordinat terbalik, halusinasi skema, dan latensi.

### D. Menjalankan Baseline 2: Unconstrained LLM
```bash
cd /var/www/html/Geo
php benchmark/baseline_unconstrained/runner.php
```
Memverifikasi respons bebas LLM terhadap 22 POI acuan Padang dan menghitung rasio fabrikasi entitas fiktif serta yurisdiksi luar kota.

### E. Menjalankan Master Runner Seluruh Benchmark
```bash
cd /var/www/html/Geo
bash benchmark/run_all.sh
```

---

## 4. Verifikasi Integritas Data (Checksum Verification)

Untuk memverifikasi bahwa berkas dataset, prompt, dan kode evaluasi belum mengalami modifikasi:
```bash
cd /var/www/html/Geo/benchmark/reproducibility
sha256sum -c SHA256SUMS.txt
```
Semua berkas wajib berstatus `OK`.

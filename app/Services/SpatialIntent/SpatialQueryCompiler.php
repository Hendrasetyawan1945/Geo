<?php

declare(strict_types=1);

namespace App\Services\SpatialIntent;

/**
 * Deterministic Spatial Query Compiler (MySQL 8.0 Engine)
 *
 * Menerjemahkan Canonical Spatial Intent Representation (CSIR) yang telah tervalidasi
 * menjadi SQL terparameterisasi dengan formula spasial MySQL 8.0 (ST_Distance_Sphere).
 *
 * Prinsip Rekayasa:
 * 1. LLM dilarang keras menyusun atau memodifikasi sintaks SQL.
 * 2. Eksekusi SQL 100% menggunakan parameter binding (?) untuk mencegah SQL Injection.
 * 3. Safety Invariant: Jika SIR tidak valid (!isValid) atau out-of-scope,
 *    compiler secara deterministik menolak kompilasi dan mengembalikan query kosong.
 */
class SpatialQueryCompiler
{
    /**
     * Kompilasi objek SpatialIntent menjadi query SQL terparameterisasi.
     *
     * @param SpatialIntent $sir
     * @param int $limit
     * @return array{sql: string, params: array<int, mixed>, isExecutable: bool}
     */
    public function compile(SpatialIntent $sir, int $limit = 10): array
    {
        // Safety Invariant: Jangan pernah mengeksekusi SIR yang tidak lolos validasi!
        if (!$sir->isValid || $sir->isOutOfScope) {
            return [
                'sql'          => '',
                'params'       => [],
                'isExecutable' => false,
            ];
        }

        $params = [];
        $hasCoords = ($sir->latitude !== null && $sir->longitude !== null);

        // Basis SELECT
        $selectFields = [
            'wisata.id',
            'wisata.nama',
            'wisata.deskripsi',
            'wisata.alamat',
            'wisata.telepon',
            'wisata.lat',
            'wisata.lng',
            'wisata.harga_tiket',
            'wisata.jam_buka',
            'wisata.jam_tutup',
            'wisata.rating',
            'wisata.foto',
            'wisata.status_operasional',
            'wisata.catatan_status',
            'kategori.nama AS kategori',
        ];

        // Komputasi Jarak Spasial (MySQL 8.0 ST_Distance_Sphere)
        if ($hasCoords) {
            $selectFields[] = 'ROUND(ST_Distance_Sphere(POINT(wisata.lng, wisata.lat), POINT(?, ?)) / 1000.0, 2) AS jarak_km';
            $params[] = $sir->longitude;
            $params[] = $sir->latitude;
        } else {
            $selectFields[] = 'NULL AS jarak_km';
        }

        $sql = 'SELECT ' . implode(', ', $selectFields) . ' '
             . 'FROM wisata '
             . 'JOIN kategori ON wisata.kategori_id = kategori.id '
             . 'WHERE wisata.status_aktif = 1 ';

        // 1. Filter Kategori
        if ($sir->category !== null) {
            $sql .= 'AND kategori.nama = ? ';
            $params[] = $sir->category;
        }

        // 2. Filter Nama Target (Entity Lookup / Exact / Partial)
        if ($sir->targetName !== null) {
            $sql .= 'AND (wisata.nama LIKE ? OR wisata.deskripsi LIKE ?) ';
            $params[] = '%' . $sir->targetName . '%';
            $params[] = '%' . $sir->targetName . '%';
        }

        // 3. Filter Kata Kunci
        if ($sir->keyword !== null) {
            $sql .= 'AND (wisata.nama LIKE ? OR wisata.deskripsi LIKE ?) ';
            $params[] = '%' . $sir->keyword . '%';
            $params[] = '%' . $sir->keyword . '%';
        }

        // 4. Filter Wilayah Administratif
        if ($sir->adminArea !== null) {
            $sql .= 'AND wisata.alamat LIKE ? ';
            $params[] = '%' . $sir->adminArea . '%';
        }

        // 5. Filter Tiket Gratis
        if ($sir->isFree) {
            $sql .= 'AND wisata.harga_tiket = 0 ';
        } elseif ($sir->maxPrice !== null) {
            $sql .= 'AND wisata.harga_tiket <= ? ';
            $params[] = $sir->maxPrice;
        }

        // 6. Filter Jam Operasional
        if ($sir->open24h) {
            $sql .= "AND (wisata.jam_buka = '00:00:00' AND wisata.jam_tutup >= '23:59:00') ";
        } elseif ($sir->openNow) {
            // Predikat temporal: jam sekarang berada di antara jam buka dan tutup
            $currentTime = date('H:i:s');
            $sql .= "AND (
                (wisata.jam_buka <= wisata.jam_tutup AND ? BETWEEN wisata.jam_buka AND wisata.jam_tutup)
                OR
                (wisata.jam_buka > wisata.jam_tutup AND (? >= wisata.jam_buka OR ? <= wisata.jam_tutup))
            ) ";
            $params[] = $currentTime;
            $params[] = $currentTime;
            $params[] = $currentTime;
        }

        // 7. Filter Radius Spasial
        if ($sir->spatialOperator === 'within_radius' && $hasCoords && $sir->radius !== null) {
            $sql .= 'AND (ST_Distance_Sphere(POINT(wisata.lng, wisata.lat), POINT(?, ?)) / 1000.0) <= ? ';
            $params[] = $sir->longitude;
            $params[] = $sir->latitude;
            $params[] = $sir->radius;
        }

        // 8. Klausul Pengurutan (ORDER BY)
        if ($hasCoords && ($sir->spatialOperator === 'nearest' || $sir->sort === 'terdekat')) {
            $sql .= 'ORDER BY ST_Distance_Sphere(POINT(wisata.lng, wisata.lat), POINT(?, ?)) ASC ';
            $params[] = $sir->longitude;
            $params[] = $sir->latitude;
        } elseif ($sir->sort === 'termurah') {
            $sql .= 'ORDER BY wisata.harga_tiket ASC ';
        } elseif ($sir->sort === 'termahal') {
            $sql .= 'ORDER BY wisata.harga_tiket DESC ';
        } elseif ($sir->sort === 'terbaik') {
            $sql .= 'ORDER BY wisata.rating DESC ';
        } elseif ($hasCoords) {
            $sql .= 'ORDER BY ST_Distance_Sphere(POINT(wisata.lng, wisata.lat), POINT(?, ?)) ASC ';
            $params[] = $sir->longitude;
            $params[] = $sir->latitude;
        } else {
            $sql .= 'ORDER BY wisata.rating DESC ';
        }

        // 9. LIMIT
        $sql .= 'LIMIT ?;';
        $params[] = $limit;

        return [
            'sql'          => $sql,
            'params'       => $params,
            'isExecutable' => true,
        ];
    }
}

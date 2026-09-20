<?php

namespace App\Models;

use CodeIgniter\Model;

class WisataModel extends Model
{
    protected $table            = 'wisata';
    protected $primaryKey       = 'id';
    protected $useAutoIncrement = true;
    protected $returnType       = 'array';
    protected $useSoftDeletes   = false;
    protected $allowedFields    = [
        'kategori_id', 'nama', 'deskripsi', 'alamat', 'telepon',
        'lat', 'lng', 'harga_tiket', 'jam_buka', 'jam_tutup',
        'rating', 'foto', 'status_aktif', 'status_operasional', 'catatan_status'
    ];
    protected $useTimestamps    = true;
    protected $createdField     = 'created_at';
    protected $updatedField     = 'updated_at';

    /**
     * Ambil data wisata dengan join ke tabel kategori.
     */
    public function getAllWithKategori(bool $onlyActive = true): array
    {
        $builder = $this->db->table('wisata')
            ->select('wisata.*, kategori.nama AS kategori_nama')
            ->join('kategori', 'kategori.id = wisata.kategori_id', 'left');

        if ($onlyActive) {
            $builder->where('wisata.status_aktif', 1);
        }

        return $builder->orderBy('wisata.rating', 'DESC')->get()->getResultArray();
    }

    /**
     * Eksekusi SQL terparameterisasi yang dikompilasi secara deterministik oleh SpatialQueryCompiler.
     *
     * @param string $sql
     * @param array $params
     * @return array
     */
    public function executeCompiledSpatialQuery(string $sql, array $params): array
    {
        $query = $this->db->query($sql, $params);
        return $query->getResultArray();
    }
}

<?php

declare(strict_types=1);

namespace App\Controllers;

use App\Models\KategoriModel;
use App\Models\WisataModel;
use CodeIgniter\Controller;

class WebGisController extends Controller
{
    public function index()
    {
        $kategoriModel = new KategoriModel();
        $wisataModel = new WisataModel();

        $data = [
            'title'      => 'Web GIS Pariwisata Kota Padang — Sistem Informasi Spasial Cerdas',
            'kategori'   => $kategoriModel->findAll(),
            'wisataList' => $wisataModel->getAllWithKategori(true),
        ];

        return view('webgis', $data);
    }
}

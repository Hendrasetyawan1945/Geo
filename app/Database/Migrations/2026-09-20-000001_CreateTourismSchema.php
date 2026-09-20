<?php

namespace App\Database\Migrations;

use CodeIgniter\Database\Migration;

class CreateTourismSchema extends Migration
{
    public function up()
    {
        // 1. Tabel Kategori
        $this->forge->addField([
            'id' => [
                'type'           => 'BIGINT',
                'unsigned'       => true,
                'auto_increment' => true,
            ],
            'nama' => [
                'type'       => 'VARCHAR',
                'constraint' => 50,
                'unique'     => true,
            ],
            'created_at' => [
                'type' => 'DATETIME',
                'null' => true,
            ],
            'updated_at' => [
                'type' => 'DATETIME',
                'null' => true,
            ],
        ]);
        $this->forge->addKey('id', true);
        $this->forge->createTable('kategori', true);

        // 2. Tabel Wisata
        $this->forge->addField([
            'id' => [
                'type'           => 'BIGINT',
                'unsigned'       => true,
                'auto_increment' => true,
            ],
            'kategori_id' => [
                'type'     => 'BIGINT',
                'unsigned' => true,
            ],
            'nama' => [
                'type'       => 'VARCHAR',
                'constraint' => 100,
            ],
            'deskripsi' => [
                'type' => 'TEXT',
                'null' => true,
            ],
            'alamat' => [
                'type'       => 'VARCHAR',
                'constraint' => 255,
                'null'       => true,
            ],
            'telepon' => [
                'type'       => 'VARCHAR',
                'constraint' => 30,
                'null'       => true,
            ],
            'lat' => [
                'type'       => 'DECIMAL',
                'constraint' => '10,7',
            ],
            'lng' => [
                'type'       => 'DECIMAL',
                'constraint' => '10,7',
            ],
            'harga_tiket' => [
                'type'       => 'DECIMAL',
                'constraint' => '12,0',
                'default'    => 0,
            ],
            'jam_buka' => [
                'type' => 'TIME',
                'null' => true,
            ],
            'jam_tutup' => [
                'type' => 'TIME',
                'null' => true,
            ],
            'rating' => [
                'type'       => 'DECIMAL',
                'constraint' => '2,1',
                'default'    => 0.0,
            ],
            'foto' => [
                'type' => 'LONGTEXT',
                'null' => true,
            ],
            'status_aktif' => [
                'type'    => 'BOOLEAN',
                'default' => true,
            ],
            'status_operasional' => [
                'type'       => 'VARCHAR',
                'constraint' => 30,
                'default'    => 'normal',
            ],
            'catatan_status' => [
                'type' => 'TEXT',
                'null' => true,
            ],
            'created_at' => [
                'type' => 'DATETIME',
                'null' => true,
            ],
            'updated_at' => [
                'type' => 'DATETIME',
                'null' => true,
            ],
        ]);
        $this->forge->addKey('id', true);
        $this->forge->addKey('kategori_id');
        $this->forge->addKey('status_aktif');
        $this->forge->addKey(['lat', 'lng']);
        $this->forge->addForeignKey('kategori_id', 'kategori', 'id', 'RESTRICT', 'CASCADE');
        $this->forge->createTable('wisata', true);

        // 3. Tabel Users (Admin)
        $this->forge->addField([
            'id' => [
                'type'           => 'BIGINT',
                'unsigned'       => true,
                'auto_increment' => true,
            ],
            'name' => [
                'type'       => 'VARCHAR',
                'constraint' => 255,
            ],
            'email' => [
                'type'       => 'VARCHAR',
                'constraint' => 255,
                'unique'     => true,
            ],
            'password' => [
                'type'       => 'VARCHAR',
                'constraint' => 255,
            ],
            'role' => [
                'type'       => 'VARCHAR',
                'constraint' => 20,
                'default'    => 'user',
            ],
            'remember_token' => [
                'type'       => 'VARCHAR',
                'constraint' => 100,
                'null'       => true,
            ],
            'created_at' => [
                'type' => 'DATETIME',
                'null' => true,
            ],
            'updated_at' => [
                'type' => 'DATETIME',
                'null' => true,
            ],
        ]);
        $this->forge->addKey('id', true);
        $this->forge->createTable('users', true);

        // 4. Tabel Chat Sessions
        $this->forge->addField([
            'id' => [
                'type'           => 'BIGINT',
                'unsigned'       => true,
                'auto_increment' => true,
            ],
            'session_token' => [
                'type'       => 'VARCHAR',
                'constraint' => 64,
                'unique'     => true,
            ],
            'lat' => [
                'type'       => 'DECIMAL',
                'constraint' => '10,7',
                'null'       => true,
            ],
            'lng' => [
                'type'       => 'DECIMAL',
                'constraint' => '10,7',
                'null'       => true,
            ],
            'created_at' => [
                'type' => 'DATETIME',
                'null' => true,
            ],
            'updated_at' => [
                'type' => 'DATETIME',
                'null' => true,
            ],
        ]);
        $this->forge->addKey('id', true);
        $this->forge->createTable('chat_sessions', true);

        // 5. Tabel Chat Messages (dengan intent_json untuk audit SIR & evaluasi jurnal)
        $this->forge->addField([
            'id' => [
                'type'           => 'BIGINT',
                'unsigned'       => true,
                'auto_increment' => true,
            ],
            'session_id' => [
                'type'     => 'BIGINT',
                'unsigned' => true,
            ],
            'role' => [
                'type'       => 'ENUM',
                'constraint' => ['user', 'assistant'],
            ],
            'pesan' => [
                'type' => 'TEXT',
            ],
            'intent_json' => [
                'type' => 'JSON',
                'null' => true,
            ],
            'created_at' => [
                'type' => 'DATETIME',
                'null' => true,
            ],
            'updated_at' => [
                'type' => 'DATETIME',
                'null' => true,
            ],
        ]);
        $this->forge->addKey('id', true);
        $this->forge->addKey('session_id');
        $this->forge->addForeignKey('session_id', 'chat_sessions', 'id', 'CASCADE', 'CASCADE');
        $this->forge->createTable('chat_messages', true);
    }

    public function down()
    {
        $this->forge->dropTable('chat_messages', true);
        $this->forge->dropTable('chat_sessions', true);
        $this->forge->dropTable('users', true);
        $this->forge->dropTable('wisata', true);
        $this->forge->dropTable('kategori', true);
    }
}

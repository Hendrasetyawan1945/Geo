<?php

namespace App\Models;

use CodeIgniter\Model;

class ChatMessageModel extends Model
{
    protected $table            = 'chat_messages';
    protected $primaryKey       = 'id';
    protected $useAutoIncrement = true;
    protected $returnType       = 'array';
    protected $allowedFields    = ['session_id', 'role', 'pesan', 'intent_json'];
    protected $useTimestamps    = true;
    protected $createdField     = 'created_at';
    protected $updatedField     = 'updated_at';

    public function getHistory(int $sessionId, int $limit = 20): array
    {
        return $this->where('session_id', $sessionId)
            ->orderBy('id', 'ASC')
            ->limit($limit)
            ->findAll();
    }
}

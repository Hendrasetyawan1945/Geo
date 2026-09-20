<?php

namespace App\Models;

use CodeIgniter\Model;

class ChatSessionModel extends Model
{
    protected $table            = 'chat_sessions';
    protected $primaryKey       = 'id';
    protected $useAutoIncrement = true;
    protected $returnType       = 'array';
    protected $allowedFields    = ['session_token', 'lat', 'lng'];
    protected $useTimestamps    = true;
    protected $createdField     = 'created_at';
    protected $updatedField     = 'updated_at';

    public function getOrCreateSession(string $token, ?float $lat = null, ?float $lng = null): array
    {
        $session = $this->where('session_token', $token)->first();
        if ($session) {
            if ($lat !== null && $lng !== null) {
                $this->update($session['id'], [
                    'lat' => $lat,
                    'lng' => $lng,
                    'updated_at' => date('Y-m-d H:i:s'),
                ]);
                $session['lat'] = $lat;
                $session['lng'] = $lng;
            }
            return $session;
        }

        $id = $this->insert([
            'session_token' => $token,
            'lat'           => $lat,
            'lng'           => $lng,
            'created_at'    => date('Y-m-d H:i:s'),
            'updated_at'    => date('Y-m-d H:i:s'),
        ]);

        return $this->find($id);
    }
}

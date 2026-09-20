<?php

declare(strict_types=1);

namespace App\Controllers;

use App\Models\ChatMessageModel;
use App\Models\ChatSessionModel;
use App\Models\WisataModel;
use App\Services\LlmService;
use App\Services\SpatialIntent\GroundedFactBuilder;
use App\Services\SpatialIntent\SpatialPolicyHandler;
use App\Services\SpatialIntent\SpatialQueryCompiler;
use CodeIgniter\RESTful\ResourceController;

class ChatController extends ResourceController
{
    protected $format = 'json';

    protected LlmService $llmService;
    protected SpatialPolicyHandler $policyHandler;
    protected SpatialQueryCompiler $compiler;
    protected GroundedFactBuilder $factBuilder;
    protected WisataModel $wisataModel;
    protected ChatSessionModel $sessionModel;
    protected ChatMessageModel $messageModel;

    public function __construct()
    {
        $this->llmService = new LlmService();
        $this->policyHandler = new SpatialPolicyHandler();
        $this->compiler = new SpatialQueryCompiler();
        $this->factBuilder = new GroundedFactBuilder();
        $this->wisataModel = new WisataModel();
        $this->sessionModel = new ChatSessionModel();
        $this->messageModel = new ChatMessageModel();
    }

    public function setMockMode(bool $mock): void
    {
        $this->llmService->mockMode = $mock;
    }

    /**
     * POST /api/chat
     * Endpoint utama pemrosesan kueri percakapan spasial dwitunggal.
     */
    public function send()
    {
        $json = $this->request->getJSON(true) ?? $this->request->getPost();
        $message = trim((string) ($json['message'] ?? ''));
        $token = trim((string) ($json['session_token'] ?? ''));

        if ($message === '') {
            return $this->fail('Pesan pengguna tidak boleh kosong.', 400);
        }

        $lat = isset($json['latitude']) && is_numeric($json['latitude']) 
            ? (float) $json['latitude'] 
            : (isset($json['lat']) && is_numeric($json['lat']) ? (float) $json['lat'] : null);
        $lng = isset($json['longitude']) && is_numeric($json['longitude']) 
            ? (float) $json['longitude'] 
            : (isset($json['lng']) && is_numeric($json['lng']) ? (float) $json['lng'] : null);

        if ($token === '') {
            $token = bin2hex(random_bytes(16));
        }

        // 1. Sesi & Riwayat
        $session = $this->sessionModel->getOrCreateSession($token, $lat, $lng);
        $userLat = $lat ?? ($session['lat'] !== null ? (float) $session['lat'] : null);
        $userLng = $lng ?? ($session['lng'] !== null ? (float) $session['lng'] : null);

        $history = $this->messageModel->getHistory((int) $session['id'], 6);

        // Simpan pesan user
        $this->messageModel->insert([
            'session_id'  => $session['id'],
            'role'        => 'user',
            'pesan'       => $message,
            'intent_json' => null,
            'created_at'  => date('Y-m-d H:i:s'),
            'updated_at'  => date('Y-m-d H:i:s'),
        ]);

        // 2. Proses Inti Pipeline 5-Lapis
        $result = $this->processCore($message, $userLat, $userLng, $history);
        $sir = $result['sir'];
        $replyText = $result['replyText'];
        $places = $result['places'];

        // Simpan pesan balasan asisten beserta CSIR metadata untuk audit riset
        $this->messageModel->insert([
            'session_id'  => $session['id'],
            'role'        => 'assistant',
            'pesan'       => $replyText,
            'intent_json' => json_encode($sir->toCanonicalArray(), JSON_UNESCAPED_UNICODE),
            'created_at'  => date('Y-m-d H:i:s'),
            'updated_at'  => date('Y-m-d H:i:s'),
        ]);

        return $this->respond([
            'success'          => true,
            'session_token'    => $token,
            'response'         => $replyText,
            'sir'              => $sir->toCanonicalArray(),
            'places'           => $places,
            'user_location'    => ($userLat !== null && $userLng !== null) ? ['lat' => $userLat, 'lng' => $userLng] : null,
            'fallback_applied' => $sir->fallbackApplied,
            'fallback_notice'  => $sir->fallbackNotice,
            'timings'          => $result['timings'],
        ]);
    }

    /**
     * Memproses pesan melalui seluruh 5-lapis arsitektur (digunakan oleh controller dan riset evaluasi).
     */
    public function processCore(string $message, ?float $userLat = null, ?float $userLng = null, array $history = []): array
    {
        $t0 = microtime(true);

        // 1. Ekstraksi SIR
        $t1 = microtime(true);
        $sir = $this->llmService->extractSir($message, $history);
        $intentTimeMs = (microtime(true) - $t1) * 1000.0;

        if ($userLat !== null && $userLng !== null) {
            if ($sir->latitude === null || $sir->longitude === null) {
                $sir->latitude = $userLat;
                $sir->longitude = $userLng;
                if ($sir->referenceType === 'unknown') {
                    $sir->referenceType = 'gps';
                }
            }
        }

        // 2. Kebijakan Spasial & Batas Wilayah Padang
        $sir = $this->policyHandler->applyPolicy($sir);

        $replyText = '';
        $places = [];
        $sqlTimeMs = 0.0;
        $nlgTimeMs = 0.0;

        // 3. Evaluasi Execution Policy
        if ($sir->executionPolicy === 'reject_out_of_scope') {
            $replyText = sprintf(
                'Maaf, permintaan mengenai "%s" berada di luar lingkup domain pariwisata Kota Padang. Layanan ini khusus menyediakan informasi objek wisata resmi (pantai, pulau, alam, museum, sejarah, kuliner) di Kota Padang.',
                $sir->keyword ?? $message
            );
        } elseif ($sir->executionPolicy === 'clarify_user') {
            $errorList = implode("\n- ", $sir->validationErrors);
            $replyText = "Mohon maaf, permintaan Anda belum dapat kami proses karena kendala berikut:\n- {$errorList}\n\nSilakan sesuaikan kembali kriteria pencarian Anda.";
        } else {
            // 4. Kompilasi SQL Deterministik untuk MySQL 8.0
            $compiled = $this->compiler->compile($sir, 10);

            if ($compiled['isExecutable']) {
                $tSql0 = microtime(true);
                $rows = $this->wisataModel->executeCompiledSpatialQuery($compiled['sql'], $compiled['params']);
                $sqlTimeMs = (microtime(true) - $tSql0) * 1000.0;

                $facts = $this->factBuilder->buildFactList($rows);

                // 5. Grounded NLG Synthesis & Algorithmic Grounding Validation
                $tNlg0 = microtime(true);
                $replyText = $this->llmService->generateGroundedResponse($message, $facts, $sir);
                $nlgTimeMs = (microtime(true) - $tNlg0) * 1000.0;
                $places = $rows;
            } else {
                $replyText = 'Maaf, kueri spasial tidak dapat dieksekusi secara aman.';
            }
        }

        $totalTimeMs = (microtime(true) - $t0) * 1000.0;

        return [
            'replyText' => $replyText,
            'sir'       => $sir,
            'places'    => $places,
            'timings'   => [
                'intent_ms' => $intentTimeMs,
                'sql_ms'    => $sqlTimeMs,
                'nlg_ms'    => $nlgTimeMs,
                'total_ms'  => $totalTimeMs,
            ],
        ];
    }

    /**
     * GET /api/places
     * Endpoint data seluruh objek wisata untuk inisialisasi peta Leaflet.
     */
    public function places()
    {
        $places = $this->wisataModel->getAllWithKategori(true);
        return $this->respond([
            'success' => true,
            'data'    => $places,
        ]);
    }
}

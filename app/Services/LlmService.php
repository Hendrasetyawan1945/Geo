<?php

declare(strict_types=1);

namespace App\Services;

use App\Services\SpatialIntent\GroundingValidator;
use App\Services\SpatialIntent\GroundedFactBuilder;
use App\Services\SpatialIntent\SirValidator;
use App\Services\SpatialIntent\SpatialIntent;

/**
 * LLM Service
 *
 * Mengelola interaksi kognitif pemrosesan bahasa alami (NLP) dengan LLM:
 * 1. Semantic Intent Parsing: Natural Language -> Raw SIR
 * 2. Grounded NLG: SQL Facts + Strict Grounding Contract -> Verifiable Natural Language Text
 * 3. Algorithmic Verification: Output divalidasi oleh GroundingValidator sebelum dikirim ke pengguna.
 */
class LlmService
{
    protected string $apiUrl = '';
    protected string $apiKey = '';
    protected string $model = 'deepseek-chat';

    protected SirValidator $sirValidator;
    protected GroundingValidator $groundingValidator;
    protected GroundedFactBuilder $factBuilder;
    public bool $mockMode = false;

    public function __construct(
        ?SirValidator $sirValidator = null,
        ?GroundingValidator $groundingValidator = null,
        ?GroundedFactBuilder $factBuilder = null
    ) {
        $this->apiUrl = (string) (env('LLM_API_URL') ?: getenv('LLM_API_URL') ?: ($_ENV['LLM_API_URL'] ?? 'http://127.0.0.1:20128/v1/chat/completions'));
        $this->apiKey = (string) (env('LLM_API_KEY') ?: getenv('LLM_API_KEY') ?: ($_ENV['LLM_API_KEY'] ?? 'sk-6b3ac6ef8e3b70c9-qmmygk-f971dec1'));
        $this->model = (string) (env('LLM_MODEL') ?: getenv('LLM_MODEL') ?: ($_ENV['LLM_MODEL'] ?? 'jurnal/deepseek-v4-flash'));

        $this->sirValidator = $sirValidator ?? new SirValidator();
        $this->groundingValidator = $groundingValidator ?? new GroundingValidator();
        $this->factBuilder = $factBuilder ?? new GroundedFactBuilder();
    }

    /**
     * Ekstraksi teks bahasa alami pengguna menjadi Spatial Intent Representation (SIR).
     *
     * @param string $userMessage
     * @param array<int, array<string, string>> $history
     * @return SpatialIntent
     */
    public function extractSir(string $userMessage, array $history = []): SpatialIntent
    {
        $rawSirData = null;

        // Jika API Key tersedia dan bukan mode mock, coba panggil LLM secara live
        if (!$this->mockMode && !empty($this->apiKey)) {
            $rawSirData = $this->callLlmForSir($userMessage, $history);
        }

        // Jika API key tidak ada atau panggilan API gagal/timeout, gunakan rule-based semantic parser
        if (!is_array($rawSirData) || empty($rawSirData)) {
            $rawSirData = $this->heuristicSemanticParse($userMessage);
        }

        // Buat objek Raw SIR
        $rawSir = SpatialIntent::fromArray($rawSirData, $userMessage);

        // Validasi melalui SIR Validator 6-Dimensi (No Intent Alteration)
        $validation = $this->sirValidator->validate($rawSir);

        return $validation['sir'];
    }

    /**
     * Rangkai narasi rekomendasi akhir (Grounded NLG) dari fakta basis data.
     *
     * @param string $userMessage
     * @param array<int, array<string, mixed>> $facts
     * @param SpatialIntent $sir
     * @return string
     */
    public function generateGroundedResponse(string $userMessage, array $facts, SpatialIntent $sir): string
    {
        // Jika data fakta kosong
        if (empty($facts)) {
            return $this->factBuilder->buildDeterministicFallbackResponse($facts, $sir);
        }

        // Jika API key tersedia dan bukan mode mock, coba rangkai via LLM dengan Strict Grounding Contract
        if (!$this->mockMode && !empty($this->apiKey)) {
            $llmText = $this->callLlmForGroundedNlg($userMessage, $facts, $sir);

            if (!empty($llmText)) {
                // Verifikasi kepatuhan grounding secara algoritmik
                $validation = $this->groundingValidator->validate($llmText, $facts);

                if ($validation['isGrounded']) {
                    return $llmText;
                }
            }
        }

        // Fallback deterministik berbasis fakta SQL (Zero Hallucination Guarantee)
        return $this->factBuilder->buildDeterministicFallbackResponse($facts, $sir);
    }

    /**
     * Panggilan LLM untuk ekstraksi SIR.
     */
    protected function callLlmForSir(string $userMessage, array $history): ?array
    {
        $systemPrompt = <<<PROMPT
You are a spatial intent parser for a tourism Web GIS in Padang City, Indonesia.
Your task is to transform the user's natural-language query into a structured Spatial Intent Representation (SIR) in pure JSON.

RULES:
1. Return JSON ONLY. No markdown, no explanation, no other text.
2. Do not generate SQL.
3. Do not answer the user's question or provide recommendations.
4. Allowed Categories: "Pantai" | "Pulau" | "Alam" | "Museum" | "Sejarah" | "Kuliner" | null
5. Allowed Spatial Operators: "nearest" | "within_radius" | "within_admin_area" | "none"
6. Preserve spatial constraints exactly as expressed by user.
7. If user requests impossible things for Padang (e.g. ski, snow, casino), set is_out_of_scope: true.

SCHEMA:
{
  "intent": "spatial_recommendation" | "entity_lookup" | "general_inquiry",
  "entity": "tourism_object",
  "category": "Pantai" | "Pulau" | "Alam" | "Museum" | "Sejarah" | "Kuliner" | null,
  "target_name": string or null,
  "keyword": string or null,
  "spatial_operator": "nearest" | "within_radius" | "within_admin_area" | "none",
  "reference_type": "gps" | "city_center" | "poi" | "unknown",
  "radius": float or null,
  "distance_unit": "km",
  "admin_area": string or null,
  "is_free": boolean,
  "max_price": integer or null,
  "open_now": boolean,
  "open_24h": boolean,
  "sort": "termurah" | "termahal" | "terdekat" | "terbaik" | null,
  "is_out_of_scope": boolean
}
PROMPT;

        $messages = [
            ['role' => 'system', 'content' => $systemPrompt],
            ['role' => 'user', 'content' => $userMessage],
        ];

        $payload = [
            'model'           => $this->model,
            'messages'        => $messages,
            'temperature'     => 0.0,
            'max_tokens'      => 400,
            'response_format' => ['type' => 'json_object'],
        ];

        $res = $this->sendHttpRequest($payload);
        if ($res && isset($res['choices'][0]['message']['content'])) {
            $raw = trim($res['choices'][0]['message']['content']);
            $raw = preg_replace('/^```json\s*|\s*```$/i', '', $raw);
            $parsed = json_decode($raw, true);
            if (is_array($parsed)) {
                return $parsed;
            }
        }

        return null;
    }

    /**
     * Panggilan LLM untuk Grounded NLG dengan Grounding Contract ketat.
     */
    protected function callLlmForGroundedNlg(string $userMessage, array $facts, SpatialIntent $sir): ?string
    {
        $factsJson = json_encode($facts, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        $notice = $sir->fallbackApplied ? ("CATATAN: " . $sir->fallbackNotice) : "";

        $systemPrompt = <<<PROMPT
Kamu adalah asisten cerdas Web GIS Pariwisata Kota Padang.
Tugasmu adalah menjawab pertanyaan pengguna HANYA berdasarkan daftar data fakta terlampir.

KONTRAK GROUNDING KETAT (STRICT GROUNDING CONTRACT):
1. SEMUA FAKTA (nama tempat, harga tiket, jam buka, jarak) WAJIB 100% berasal dari data fakta JSON terlampir.
2. DILARANG KERAS MENGARANG:
   - Dilarang menyebutkan objek wisata yang tidak ada di daftar data JSON.
   - Dilarang mengarang harga tiket atau jam operasional.
   - Dilarang menambahkan klaim deskriptif yang tidak tercantum pada data.
3. Sebutkan nama objek wisata dengan cetak tebal (**Nama Objek**).
4. Gunakan bahasa Indonesia yang santun, informatif, dan ringkas.
$notice
PROMPT;

        $userContent = "Pertanyaan pengguna: {$userMessage}\n\nData Fakta Resmi Basis Data:\n{$factsJson}";

        $payload = [
            'model'       => $this->model,
            'messages'    => [
                ['role' => 'system', 'content' => $systemPrompt],
                ['role' => 'user', 'content' => $userContent],
            ],
            'temperature' => 0.0,
            'max_tokens'  => 600,
        ];

        $res = $this->sendHttpRequest($payload);
        if ($res && isset($res['choices'][0]['message']['content'])) {
            return trim($res['choices'][0]['message']['content']);
        }

        return null;
    }

    /**
     * Rule-based Semantic Parser deterministik sebagai fallback handal jika LLM API offline.
     */
    protected function heuristicSemanticParse(string $query): array
    {
        $lower = strtolower($query);
        $data = [
            'intent'           => 'spatial_recommendation',
            'entity'           => 'tourism_object',
            'category'         => null,
            'target_name'      => null,
            'keyword'          => null,
            'spatial_operator' => 'none',
            'reference_type'   => 'unknown',
            'radius'           => null,
            'distance_unit'    => 'km',
            'admin_area'       => null,
            'is_free'          => false,
            'max_price'        => null,
            'open_now'         => false,
            'open_24h'         => false,
            'sort'             => null,
            'is_out_of_scope'  => false,
        ];

        // 0. Deteksi Out-of-Scope Kueri
        foreach (SirValidator::OUT_OF_SCOPE_KEYWORDS as $outKeyword) {
            if (str_contains($lower, $outKeyword)) {
                $data['is_out_of_scope'] = true;
                return $data;
            }
        }

        // 1. Deteksi Kategori
        if (preg_match('/pantai|laut|pesisir|pasir/i', $lower)) {
            $data['category'] = 'Pantai';
        } elseif (preg_match('/pulau|snorkeling|diving/i', $lower)) {
            $data['category'] = 'Pulau';
        } elseif (preg_match('/air terjun|bukit|hutan|tahura|alam|tracking|lubuk/i', $lower)) {
            $data['category'] = 'Alam';
        } elseif (preg_match('/museum|adityawarman|sejarah/i', $lower)) {
            $data['category'] = 'Museum';
        } elseif (preg_match('/jembatan|siti nurbaya|ganting|monumen|tugu/i', $lower)) {
            $data['category'] = 'Sejarah';
        } elseif (preg_match('/kuliner|makan|soto|rendang|restoran|warung|mie/i', $lower)) {
            $data['category'] = 'Kuliner';
        }

        // 2. Deteksi Operator Spasial & Radius
        if (preg_match('/radius\s*(\d+(\.\d+)?)\s*km/i', $lower, $m)) {
            $data['spatial_operator'] = 'within_radius';
            $data['radius'] = (float) $m[1];
        } elseif (preg_match('/dalam\s*(\d+(\.\d+)?)\s*km/i', $lower, $m)) {
            $data['spatial_operator'] = 'within_radius';
            $data['radius'] = (float) $m[1];
        } elseif (preg_match('/terdekat|paling dekat|dekat/i', $lower)) {
            $data['spatial_operator'] = 'nearest';
            $data['sort'] = 'terdekat';
        }

        // 3. Deteksi Wilayah Administratif
        if (preg_match('/padang selatan|padang barat|padang utara|padang timur|bungus|kuranji|lubuk kilangan|koto tangah|nanggalo/i', $lower, $m)) {
            $data['admin_area'] = ucwords($m[0]);
            if ($data['spatial_operator'] === 'none') {
                $data['spatial_operator'] = 'within_admin_area';
            }
        }

        // 4. Deteksi Harga & Tiket
        if (preg_match('/gratis|tanpa bayar|free/i', $lower)) {
            $data['is_free'] = true;
        } elseif (preg_match('/(?:di bawah|maksimal|budget|kurang dari|harga)\s*(?:rp\.?\s*)?(\d+)(?:\s*(?:rb|ribu|k))?/i', $lower, $m)) {
            $nominal = (int) $m[1];
            if (isset($m[2]) || str_contains($lower, 'ribu') || str_contains($lower, 'rb') || str_contains($lower, 'k')) {
                if ($nominal < 1000) {
                    $nominal *= 1000;
                }
            }
            $data['max_price'] = $nominal;
        }

        // 5. Deteksi Jam Operasional
        if (preg_match('/buka sekarang|sedang buka|saat ini buka/i', $lower)) {
            $data['open_now'] = true;
        }
        if (preg_match('/24 jam/i', $lower)) {
            $data['open_24h'] = true;
        }

        // 6. Deteksi Pengurutan
        if (preg_match('/termurah|paling murah/i', $lower)) {
            $data['sort'] = 'termurah';
        } elseif (preg_match('/terbaik|rating tertinggi/i', $lower)) {
            $data['sort'] = 'terbaik';
        }

        // 7. Deteksi Target POI Tertentu
        $knownPois = [
            'Pantai Air Manis', 'Pantai Padang', 'Pantai Nirwana', 'Pantai Carolina', 'Pantai Pasir Jambak',
            'Pulau Sikuai', 'Pulau Setan Lokang', 'Pulau Pisang Gantung', 'Lubuk Hitam', 'Bukit Nobita',
            'Bukit Lampu', 'Taman Hutan Raya Bung Hatta', 'Museum Adityawarman', 'Museum Situs Rumah Bersejarah',
            'Rumah Gadang Pallindo', 'Jembatan Siti Nurbaya', 'Masjid Raya Ganting', 'Tugu Adipura',
            'Rumah Makan Sederhana', 'Warung Soto Padang', 'Pondok Mie Kocok Bandung', 'Pasar Raya Padang'
        ];
        foreach ($knownPois as $poi) {
            if (str_contains($lower, strtolower($poi))) {
                $data['target_name'] = $poi;
                $data['intent'] = 'entity_lookup';
                break;
            }
        }

        return $data;
    }

    /**
     * Kirim HTTP Request ke API LLM via cURL.
     */
    protected function sendHttpRequest(array $payload): ?array
    {
        $ch = curl_init($this->apiUrl);
        if (!$ch) {
            return null;
        }

        $headers = [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $this->apiKey,
        ];

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_TIMEOUT, 15);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

        $response = curl_exec($ch);
        $err = curl_error($ch);
        curl_close($ch);

        if ($err || !$response) {
            return null;
        }

        // Bersihkan stream marker seperti "data: [DONE]" yang kerap disisipkan oleh proxy model lokal
        $cleanResponse = preg_replace('/data:\s*\[DONE\].*$/s', '', trim($response));
        $decoded = json_decode($cleanResponse, true);
        if (is_array($decoded)) {
            return $decoded;
        }

        if (preg_match('/\{[\s\S]*\}/', $response, $matches)) {
            $extracted = json_decode($matches[0], true);
            if (is_array($extracted)) {
                return $extracted;
            }
        }

        return null;
    }
}

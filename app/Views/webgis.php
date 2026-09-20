<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= esc($title) ?></title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
    <style>
        :root {
            --bg-main: #090d16;
            --bg-panel: rgba(15, 23, 42, 0.88);
            --bg-card: rgba(30, 41, 59, 0.7);
            --border: rgba(148, 163, 184, 0.15);
            --border-hover: rgba(148, 163, 184, 0.3);
            --primary: #06b6d4;
            --primary-glow: rgba(6, 182, 212, 0.35);
            --accent: #3b82f6;
            --emerald: #10b981;
            --amber: #f59e0b;
            --rose: #f43f5e;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --radius-lg: 18px;
            --radius-md: 12px;
            --radius-sm: 8px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: var(--bg-main);
            color: var(--text-main);
        }

        /* App Layout */
        .app-container {
            display: flex;
            width: 100vw;
            height: 100vh;
            position: relative;
        }

        /* Top Navigation Header */
        .top-navbar {
            position: absolute;
            top: 16px;
            left: 20px;
            right: 480px;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 18px;
            background: var(--bg-panel);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
        }

        .brand-section {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-logo {
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, #06b6d4, #3b82f6);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 0 16px var(--primary-glow);
        }

        .brand-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.15rem;
            letter-spacing: -0.02em;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .badge-system {
            font-size: 0.68rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 20px;
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .badge-system::before {
            content: '';
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 0 8px #10b981;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }

        /* Category Filter Chips */
        .category-filters {
            display: flex;
            gap: 6px;
            overflow-x: auto;
            max-width: 520px;
            padding: 2px 0;
            scrollbar-width: none;
        }

        .category-filters::-webkit-scrollbar {
            display: none;
        }

        .cat-chip {
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 500;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .cat-chip:hover, .cat-chip.active {
            background: var(--primary);
            color: #04131d;
            font-weight: 600;
            border-color: var(--primary);
            box-shadow: 0 0 12px var(--primary-glow);
        }

        /* Map Section */
        #map {
            flex: 1;
            height: 100%;
            width: 100%;
            z-index: 1;
            background: #0b1120;
        }

        /* Floating Map Buttons */
        .map-floating-controls {
            position: absolute;
            left: 20px;
            bottom: 30px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .btn-float {
            width: 44px;
            height: 44px;
            border-radius: var(--radius-md);
            background: var(--bg-panel);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            color: var(--text-main);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            cursor: pointer;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
            transition: all 0.2s ease;
        }

        .btn-float:hover {
            border-color: var(--primary);
            color: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px var(--primary-glow);
        }

        /* Chat Panel (Right Sidebar) */
        .chat-panel {
            width: 460px;
            height: 100%;
            background: var(--bg-panel);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-left: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            z-index: 1001;
            position: relative;
            box-shadow: -10px 0 35px rgba(0, 0, 0, 0.5);
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .chat-header {
            padding: 18px 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(15, 23, 42, 0.6);
        }

        .chat-header-info h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .chat-header-info p {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 2px;
        }

        .gps-status-pill {
            font-size: 0.72rem;
            padding: 5px 10px;
            border-radius: 20px;
            background: rgba(56, 189, 248, 0.1);
            border: 1px solid rgba(56, 189, 248, 0.25);
            color: #38bdf8;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }

        .gps-status-pill:hover {
            background: rgba(56, 189, 248, 0.2);
            border-color: #38bdf8;
        }

        /* Quick Suggestions Chips */
        .quick-suggestions {
            padding: 10px 16px;
            display: flex;
            gap: 6px;
            overflow-x: auto;
            border-bottom: 1px solid rgba(148, 163, 184, 0.08);
            background: rgba(10, 15, 29, 0.4);
            scrollbar-width: none;
        }

        .quick-suggestions::-webkit-scrollbar {
            display: none;
        }

        .suggest-chip {
            padding: 5px 12px;
            border-radius: 16px;
            font-size: 0.72rem;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border);
            color: var(--text-muted);
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s ease;
        }

        .suggest-chip:hover {
            background: rgba(6, 182, 212, 0.15);
            color: var(--primary);
            border-color: var(--primary);
        }

        /* Message Stream */
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 18px;
            scroll-behavior: smooth;
        }

        .chat-messages::-webkit-scrollbar {
            width: 6px;
        }

        .chat-messages::-webkit-scrollbar-thumb {
            background: rgba(148, 163, 184, 0.2);
            border-radius: 3px;
        }

        .message-bubble {
            display: flex;
            flex-direction: column;
            max-width: 90%;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message-bubble.user {
            align-self: flex-end;
        }

        .message-bubble.user .bubble-body {
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: #ffffff;
            border-radius: 16px 16px 4px 16px;
            padding: 12px 16px;
            font-size: 0.88rem;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
        }

        .message-bubble.assistant {
            align-self: flex-start;
            max-width: 95%;
        }

        .message-bubble.assistant .bubble-body {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px 16px 16px 4px;
            padding: 14px 18px;
            font-size: 0.88rem;
            line-height: 1.55;
            color: #e2e8f0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }

        .bubble-meta {
            font-size: 0.68rem;
            color: var(--text-muted);
            margin-top: 4px;
            padding: 0 4px;
        }

        /* CSIR Inspector Accordion */
        .csir-inspector {
            margin-top: 10px;
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: var(--radius-sm);
            background: rgba(8, 14, 26, 0.7);
            font-size: 0.75rem;
            overflow: hidden;
        }

        .csir-toggle {
            padding: 7px 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            color: #38bdf8;
            font-weight: 600;
            user-select: none;
            background: rgba(56, 189, 248, 0.06);
        }

        .csir-content {
            display: none;
            padding: 10px 12px;
            background: #050b14;
            color: #94a3b8;
            font-family: monospace;
            font-size: 0.72rem;
            max-height: 220px;
            overflow-y: auto;
            border-top: 1px solid rgba(56, 189, 248, 0.15);
            white-space: pre-wrap;
            word-break: break-all;
        }

        /* Place Cards in Bot Message */
        .place-cards-carousel {
            display: flex;
            gap: 10px;
            margin-top: 12px;
            overflow-x: auto;
            padding-bottom: 6px;
            scrollbar-width: thin;
        }

        .place-mini-card {
            min-width: 210px;
            max-width: 210px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: all 0.2s ease;
        }

        .place-mini-card:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 6px 18px var(--primary-glow);
        }

        .place-mini-img {
            width: 100%;
            height: 90px;
            object-fit: cover;
            background: #0f172a;
        }

        .place-mini-content {
            padding: 10px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            flex: 1;
        }

        .place-mini-title {
            font-weight: 700;
            font-size: 0.82rem;
            color: #f1f5f9;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .place-mini-badge {
            font-size: 0.65rem;
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(6, 182, 212, 0.15);
            color: #22d3ee;
            display: inline-block;
            align-self: flex-start;
        }

        .place-mini-details {
            font-size: 0.7rem;
            color: var(--text-muted);
            margin-top: 4px;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .place-mini-actions {
            display: flex;
            gap: 6px;
            margin-top: 8px;
        }

        .btn-mini {
            flex: 1;
            padding: 5px 0;
            border-radius: 6px;
            font-size: 0.68rem;
            font-weight: 600;
            border: none;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s;
        }

        .btn-mini-view {
            background: rgba(255, 255, 255, 0.08);
            color: #f8fafc;
            border: 1px solid var(--border);
        }

        .btn-mini-view:hover {
            background: var(--primary);
            color: #04131d;
        }

        .btn-mini-route {
            background: rgba(59, 130, 246, 0.2);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.35);
        }

        .btn-mini-route:hover {
            background: #2563eb;
            color: #ffffff;
        }

        /* Chat Input Section */
        .chat-input-area {
            padding: 16px 20px;
            border-top: 1px solid var(--border);
            background: rgba(15, 23, 42, 0.7);
        }

        .chat-input-box {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(2, 6, 23, 0.8);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 6px 10px;
            transition: all 0.2s ease;
        }

        .chat-input-box:focus-within {
            border-color: var(--primary);
            box-shadow: 0 0 16px var(--primary-glow);
        }

        .chat-input-box input {
            flex: 1;
            background: transparent;
            border: none;
            color: #fff;
            padding: 8px 10px;
            font-size: 0.88rem;
            outline: none;
        }

        .chat-input-box input::placeholder {
            color: rgba(148, 163, 184, 0.5);
        }

        .btn-send {
            width: 38px;
            height: 38px;
            border-radius: 12px;
            background: linear-gradient(135deg, #06b6d4, #2563eb);
            border: none;
            color: #fff;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px var(--primary-glow);
        }

        .btn-send:hover {
            transform: scale(1.05);
        }

        .btn-send:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        /* Typing indicator */
        .typing-indicator {
            display: none;
            align-items: center;
            gap: 4px;
            padding: 8px 14px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            width: fit-content;
        }

        .typing-dot {
            width: 6px;
            height: 6px;
            background: var(--primary);
            border-radius: 50%;
            animation: bounce 1.2s infinite ease-in-out;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes bounce {
            0%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-6px); }
        }

        /* Leaflet Marker Styling */
        .custom-poi-marker {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            border: 2px solid #ffffff;
            font-size: 17px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .custom-poi-marker:hover, .custom-poi-marker.highlighted {
            transform: scale(1.25);
            box-shadow: 0 0 20px var(--primary-glow);
            border-color: #06b6d4;
            z-index: 1000 !important;
        }

        /* Marker colors per category */
        .marker-pantai { background: linear-gradient(135deg, #0284c7, #0369a1); }
        .marker-pulau { background: linear-gradient(135deg, #0891b2, #0e7490); }
        .marker-alam { background: linear-gradient(135deg, #059669, #047857); }
        .marker-museum { background: linear-gradient(135deg, #b45309, #92400e); }
        .marker-sejarah { background: linear-gradient(135deg, #6366f1, #4f46e5); }
        .marker-kuliner { background: linear-gradient(135deg, #e11d48, #be123c); }

        .leaflet-popup-content-wrapper {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: 14px;
            color: #f8fafc;
            padding: 4px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }

        .leaflet-popup-tip {
            background: rgba(15, 23, 42, 0.95);
        }

        /* Route overlay box */
        .route-info-badge {
            position: absolute;
            left: 20px;
            top: 90px;
            z-index: 1000;
            background: var(--bg-panel);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 10px 16px;
            font-size: 0.8rem;
            display: none;
            align-items: center;
            gap: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }

        @media (max-width: 1024px) {
            .top-navbar {
                right: 20px;
            }
            .chat-panel {
                position: absolute;
                right: 0;
                top: 0;
                bottom: 0;
                transform: translateX(100%);
            }
            .chat-panel.open {
                transform: translateX(0);
            }
            .chat-toggle-btn {
                display: flex !important;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Top Navbar Overlay -->
        <header class="top-navbar">
            <div class="brand-section">
                <div class="brand-logo">🗺️</div>
                <div>
                    <div class="brand-title">GeoPadang AI</div>
                    <span class="badge-system">MySQL 8.0 Spatial • SIR Layer</span>
                </div>
            </div>

            <!-- Categories Filter -->
            <div class="category-filters">
                <button class="cat-chip active" data-category="Semua">Semua (22)</button>
                <?php foreach ($kategori as $k): ?>
                    <button class="cat-chip" data-category="<?= esc($k['nama']) ?>"><?= esc($k['nama']) ?></button>
                <?php endforeach; ?>
            </div>

            <div style="display: flex; gap: 8px; align-items: center;">
                <button id="btn-detect-gps" class="gps-status-pill">
                    <span id="gps-dot" style="width:7px; height:7px; border-radius:50%; background:#94a3b8;"></span>
                    <span id="gps-text">Deteksi GPS</span>
                </button>
            </div>
        </header>

        <!-- Route Info Floating Badge -->
        <div id="route-info" class="route-info-badge">
            <span style="font-size: 1.2rem;">🚗</span>
            <div>
                <strong id="route-dest-name">Menghitung rute...</strong>
                <div id="route-stats" style="color: var(--text-muted); font-size: 0.72rem;"></div>
            </div>
            <button onclick="clearRoute()" style="background:transparent; border:none; color:#f43f5e; cursor:pointer; font-size:16px;">✕</button>
        </div>

        <!-- Floating Map Buttons -->
        <div class="map-floating-controls">
            <button class="btn-float" onclick="resetToCenter()" title="Pusat Kota Padang">🏛️</button>
            <button class="btn-float" onclick="locateUser()" title="Posisiku">📍</button>
        </div>

        <!-- Fullscreen Leaflet Map -->
        <main id="map"></main>

        <!-- Dual-Panel Chat Drawer -->
        <aside class="chat-panel" id="chat-panel">
            <div class="chat-header">
                <div class="chat-header-info">
                    <h2>💬 Asisten Spasial Cerdas</h2>
                    <p>Natural Language → CSIR → MySQL 8.0 Spatial</p>
                </div>
                <div class="badge-system" style="background: rgba(6, 182, 212, 0.1); border-color: rgba(6, 182, 212, 0.25); color: #22d3ee;">
                    Deterministic
                </div>
            </div>

            <!-- Quick Suggestion Chips -->
            <div class="quick-suggestions">
                <button class="suggest-chip" onclick="askPreset('Carikan pantai terdekat dari lokasi saya')">🌊 Pantai terdekat</button>
                <button class="suggest-chip" onclick="askPreset('Tempat kuliner khas Padang yang legendaris')">🍛 Kuliner Padang</button>
                <button class="suggest-chip" onclick="askPreset('Wisata alam gratis buka sekarang')">🏞️ Wisata gratis</button>
                <button class="suggest-chip" onclick="askPreset('Museum dengan tiket di bawah 10 ribu')">🏛️ Museum murah</button>
                <button class="suggest-chip" onclick="askPreset('Cari tempat ski salju di Padang')">⚠️ Uji Out-of-Scope</button>
            </div>

            <!-- Messages Stream -->
            <div class="chat-messages" id="chat-messages">
                <!-- Welcome Bot Message -->
                <div class="message-bubble assistant">
                    <div class="bubble-body">
                        Halo! Saya asisten cerdas <strong>Web GIS Pariwisata Kota Padang</strong> yang diperkuat oleh <em>Structured Semantic Control Layer</em>.<br><br>
                        Anda dapat menanyakan rekomendasi wisata menggunakan bahasa alami, misalnya:<br>
                        • <em>"Pantai terdekat dalam radius 10 km"</em><br>
                        • <em>"Tempat makan soto atau rendang buka 24 jam"</em><br>
                        • <em>"Wisata sejarah di Padang Barat tiket gratis"</em>
                    </div>
                    <div class="bubble-meta">Sistem • Faktual Terverifikasi</div>
                </div>
            </div>

            <!-- Typing Indicator -->
            <div id="typing-indicator" class="typing-indicator" style="margin: 0 20px 10px;">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <span style="font-size: 0.72rem; color: var(--text-muted); margin-left: 6px;">Mengekstrak SIR & kueri spasial...</span>
            </div>

            <!-- Chat Input Form -->
            <div class="chat-input-area">
                <form id="chat-form" class="chat-input-box" onsubmit="handleSend(event)">
                    <input type="text" id="chat-input" placeholder="Ketik permintaan wisata Anda di sini..." autocomplete="off">
                    <button type="submit" id="btn-submit" class="btn-send">➤</button>
                </form>
            </div>
        </aside>
    </div>

    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <script>
        // Inisialisasi Data & Titik Pusat Padang
        const PADANG_CENTER = [-0.9471, 100.4174];
        let map;
        let markersLayer;
        let routeLayer;
        let userMarker;
        let userCoords = null;
        let sessionToken = localStorage.getItem('geo_session_token') || '';

        // Master Data POI dari Server
        const allPlaces = <?= json_encode($wisataList, JSON_UNESCAPED_UNICODE) ?>;

        document.addEventListener('DOMContentLoaded', () => {
            initMap();
            plotPlaces(allPlaces);
            setupCategoryFilters();
            autoDetectGps();
        });

        function initMap() {
            map = L.map('map', {
                center: PADANG_CENTER,
                zoom: 13,
                zoomControl: false
            });

            // Modern Dark/Clean Map Tile OpenStreetMap
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19
            }).addTo(map);

            L.control.zoom({ position: 'bottomleft' }).addTo(map);

            markersLayer = L.layerGroup().addTo(map);
            routeLayer = L.layerGroup().addTo(map);
        }

        function getMarkerCategoryClass(kategori) {
            const k = (kategori || '').toLowerCase();
            if (k.includes('pantai')) return 'marker-pantai';
            if (k.includes('pulau')) return 'marker-pulau';
            if (k.includes('alam')) return 'marker-alam';
            if (k.includes('museum')) return 'marker-museum';
            if (k.includes('sejarah')) return 'marker-sejarah';
            if (k.includes('kuliner')) return 'marker-kuliner';
            return 'marker-alam';
        }

        function getCategoryIcon(kategori) {
            const k = (kategori || '').toLowerCase();
            if (k.includes('pantai')) return '🏖️';
            if (k.includes('pulau')) return '🏝️';
            if (k.includes('alam')) return '🌿';
            if (k.includes('museum')) return '🏛️';
            if (k.includes('sejarah')) return '🏰';
            if (k.includes('kuliner')) return '🍲';
            return '📍';
        }

        function plotPlaces(places) {
            markersLayer.clearLayers();

            places.forEach(p => {
                const lat = parseFloat(p.lat);
                const lng = parseFloat(p.lng);
                const catClass = getMarkerCategoryClass(p.kategori_nama || p.kategori);
                const iconEmoji = getCategoryIcon(p.kategori_nama || p.kategori);

                const icon = L.divIcon({
                    className: 'custom-div-icon',
                    html: `<div class="custom-poi-marker ${catClass}" data-id="${p.id}">${iconEmoji}</div>`,
                    iconSize: [36, 36],
                    iconAnchor: [18, 18],
                    popupAnchor: [0, -18]
                });

                const tiket = p.harga_tiket == 0 ? 'Gratis' : 'Rp' + parseInt(p.harga_tiket).toLocaleString('id-ID');
                const jam = (p.jam_buka && p.jam_tutup) ? (p.jam_buka.substring(0, 5) + ' - ' + p.jam_tutup.substring(0, 5) + ' WIB') : 'Buka 24 Jam';

                const popupHtml = `
                    <div style="min-width: 220px; font-family: 'Inter', sans-serif;">
                        <img src="${p.foto}" style="width: 100%; height: 90px; object-fit: cover; border-radius: 8px; margin-bottom: 8px;">
                        <span style="font-size: 0.65rem; padding: 2px 6px; border-radius: 4px; background: rgba(6,182,212,0.2); color:#22d3ee; font-weight:600;">
                            ${p.kategori_nama || p.kategori || 'Wisata'}
                        </span>
                        <h4 style="font-size: 0.95rem; font-weight: 700; margin: 4px 0 6px;">${p.nama}</h4>
                        <p style="font-size: 0.75rem; color: #94a3b8; line-height: 1.4; margin-bottom: 8px;">${p.deskripsi || ''}</p>
                        <div style="font-size: 0.72rem; color: #cbd5e1; display:flex; flex-direction:column; gap:2px; margin-bottom: 10px;">
                            <div>🎫 <strong>Tiket:</strong> ${tiket}</div>
                            <div>⏰ <strong>Jam:</strong> ${jam}</div>
                            <div>📍 <strong>Alamat:</strong> ${p.alamat || '-'}</div>
                        </div>
                        <div style="display: flex; gap: 6px;">
                            <button onclick="askAboutPlace('${p.nama}')" style="flex:1; padding: 6px; font-size: 0.72rem; background: var(--primary); color: #04131d; font-weight:600; border:none; border-radius:6px; cursor:pointer;">
                                Tanya AI
                            </button>
                            <button onclick="calculateRoute(${lat}, ${lng}, '${p.nama}')" style="flex:1; padding: 6px; font-size: 0.72rem; background: rgba(59,130,246,0.3); color: #93c5fd; font-weight:600; border:1px solid #3b82f6; border-radius:6px; cursor:pointer;">
                                Rute OSRM
                            </button>
                        </div>
                    </div>
                `;

                const marker = L.marker([lat, lng], { icon: icon }).bindPopup(popupHtml);
                marker.poiId = p.id;
                markersLayer.addLayer(marker);
            });
        }

        function setupCategoryFilters() {
            document.querySelectorAll('.cat-chip').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.cat-chip').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');

                    const selected = btn.getAttribute('data-category');
                    if (selected === 'Semua') {
                        plotPlaces(allPlaces);
                        resetToCenter();
                    } else {
                        const filtered = allPlaces.filter(p => (p.kategori_nama || p.kategori) === selected);
                        plotPlaces(filtered);
                        if (filtered.length > 0) {
                            const group = L.featureGroup(markersLayer.getLayers());
                            map.fitBounds(group.getBounds().pad(0.2));
                        }
                    }
                });
            });
        }

        function resetToCenter() {
            map.flyTo(PADANG_CENTER, 13, { duration: 1.2 });
        }

        function autoDetectGps() {
            const gpsDot = document.getElementById('gps-dot');
            const gpsText = document.getElementById('gps-text');

            if ('geolocation' in navigator) {
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        userCoords = { lat: pos.coords.latitude, lng: pos.coords.longitude };
                        gpsDot.style.background = '#10b981';
                        gpsDot.style.boxShadow = '0 0 8px #10b981';
                        gpsText.textContent = `${userCoords.lat.toFixed(3)}, ${userCoords.lng.toFixed(3)}`;
                        updateUserMarker();
                    },
                    (err) => {
                        console.log('GPS error/permission denied, fallback to default center:', err.message);
                        gpsDot.style.background = '#f59e0b';
                        gpsText.textContent = 'GPS Standby';
                    },
                    { enableHighAccuracy: true, timeout: 5000 }
                );
            }
        }

        function locateUser() {
            if (userCoords) {
                map.flyTo([userCoords.lat, userCoords.lng], 15, { duration: 1 });
            } else {
                autoDetectGps();
            }
        }

        function updateUserMarker() {
            if (!userCoords) return;
            if (userMarker) {
                userMarker.setLatLng([userCoords.lat, userCoords.lng]);
            } else {
                const userIcon = L.divIcon({
                    className: 'custom-user-icon',
                    html: '<div style="width:18px;height:18px;border-radius:50%;background:#38bdf8;border:3px solid #ffffff;box-shadow:0 0 14px #38bdf8;"></div>',
                    iconSize: [18, 18],
                    iconAnchor: [9, 9]
                });
                userMarker = L.marker([userCoords.lat, userCoords.lng], { icon: userIcon }).addTo(map).bindPopup('📍 Posisi Anda');
            }
        }

        // Hitung Rute Menggunakan OSRM
        async function calculateRoute(destLat, destLng, destName) {
            const originLat = userCoords ? userCoords.lat : PADANG_CENTER[0];
            const originLng = userCoords ? userCoords.lng : PADANG_CENTER[1];

            const routeBadge = document.getElementById('route-info');
            const routeName = document.getElementById('route-dest-name');
            const routeStats = document.getElementById('route-stats');

            routeName.textContent = `Menghubungkan ke ${destName}...`;
            routeStats.textContent = 'Mengambil polyline OSRM...';
            routeBadge.style.display = 'flex';

            const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${originLng},${originLat};${destLng},${destLat}?overview=full&geometries=geojson`;

            try {
                const res = await fetch(osrmUrl);
                const data = await res.json();

                if (data.routes && data.routes.length > 0) {
                    const route = data.routes[0];
                    const distanceKm = (route.distance / 1000).toFixed(1);
                    const durationMins = Math.round(route.duration / 60);

                    routeLayer.clearLayers();

                    const polyline = L.geoJSON(route.geometry, {
                        style: {
                            color: '#38bdf8',
                            weight: 5,
                            opacity: 0.9,
                            dashArray: '1, 6',
                            lineCap: 'round'
                        }
                    }).addTo(routeLayer);

                    map.fitBounds(polyline.getBounds().pad(0.2));

                    routeName.textContent = destName;
                    routeStats.textContent = `Jarak Rute: ${distanceKm} km • Estimasi Tempuh: ~${durationMins} menit`;
                } else {
                    routeStats.textContent = 'Jalur rute OSRM tidak ditemukan.';
                }
            } catch (e) {
                console.error('OSRM route error:', e);
                routeStats.textContent = 'Gagal memuat rute dari peladen OSRM.';
            }
        }

        function clearRoute() {
            routeLayer.clearLayers();
            document.getElementById('route-info').style.display = 'none';
        }

        // Chat Interaction Functions
        function askPreset(text) {
            document.getElementById('chat-input').value = text;
            handleSend(new Event('submit'));
        }

        function askAboutPlace(name) {
            document.getElementById('chat-input').value = `Informasi lengkap mengenai ${name}`;
            handleSend(new Event('submit'));
        }

        async function handleSend(e) {
            e.preventDefault();
            const input = document.getElementById('chat-input');
            const text = input.value.trim();
            if (!text) return;

            input.value = '';
            appendUserMessage(text);

            const submitBtn = document.getElementById('btn-submit');
            submitBtn.disabled = true;
            document.getElementById('typing-indicator').style.display = 'flex';

            const payload = {
                message: text,
                session_token: sessionToken,
                latitude: userCoords ? userCoords.lat : null,
                longitude: userCoords ? userCoords.lng : null
            };

            try {
                const chatApiUrl = window.location.pathname.replace(/\/$/, '') + '/api/chat';
                const res = await fetch(chatApiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                if (data.session_token) {
                    sessionToken = data.session_token;
                    localStorage.setItem('geo_session_token', sessionToken);
                }

                appendAssistantMessage(data);

                // Update marker & sorot peta jika ada places
                if (data.places && data.places.length > 0) {
                    plotPlaces(data.places);
                    const group = L.featureGroup(markersLayer.getLayers());
                    map.fitBounds(group.getBounds().pad(0.3));
                }
            } catch (err) {
                console.error('Chat error:', err);
                appendAssistantMessage({
                    response: 'Terjadi kendala jaringan saat menghubungi layanan asisten spasial.'
                });
            } finally {
                submitBtn.disabled = false;
                document.getElementById('typing-indicator').style.display = 'none';
            }
        }

        function appendUserMessage(text) {
            const container = document.getElementById('chat-messages');
            const el = document.createElement('div');
            el.className = 'message-bubble user';
            el.innerHTML = `
                <div class="bubble-body">${escapeHtml(text)}</div>
                <div class="bubble-meta">Anda • ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
            `;
            container.appendChild(el);
            container.scrollTop = container.scrollHeight;
        }

        function appendAssistantMessage(data) {
            const container = document.getElementById('chat-messages');
            const el = document.createElement('div');
            el.className = 'message-bubble assistant';

            // Format markdown text sederhana (bold, list, bullet)
            let formattedText = escapeHtml(data.response || '')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/\n/g, '<br>');

            // Place mini cards jika ada destinasi
            let placesHtml = '';
            if (data.places && data.places.length > 0) {
                placesHtml = '<div class="place-cards-carousel">';
                data.places.forEach(p => {
                    const tiket = p.harga_tiket == 0 ? 'Gratis' : 'Rp' + parseInt(p.harga_tiket).toLocaleString('id-ID');
                    const jarak = p.jarak_km ? `${parseFloat(p.jarak_km).toFixed(1)} km` : '';
                    placesHtml += `
                        <div class="place-mini-card">
                            <img src="${p.foto}" class="place-mini-img">
                            <div class="place-mini-content">
                                <span class="place-mini-badge">${p.kategori || 'Wisata'}</span>
                                <div class="place-mini-title">${escapeHtml(p.nama)}</div>
                                <div class="place-mini-details">
                                    <span>🎫 ${tiket}</span>
                                    ${jarak ? `<span>📍 ${jarak}</span>` : ''}
                                </div>
                                <div class="place-mini-actions">
                                    <button class="btn-mini btn-mini-view" onclick="focusOnPoi(${p.id}, ${p.lat}, ${p.lng})">Peta</button>
                                    <button class="btn-mini btn-mini-route" onclick="calculateRoute(${p.lat}, ${p.lng}, '${escapeHtml(p.nama)}')">Rute</button>
                                </div>
                            </div>
                        </div>
                    `;
                });
                placesHtml += '</div>';
            }

            // CSIR Inspector Accordion untuk audit riset
            let csirHtml = '';
            if (data.sir) {
                const sirJson = JSON.stringify(data.sir, null, 2);
                csirHtml = `
                    <div class="csir-inspector">
                        <div class="csir-toggle" onclick="toggleCsir(this)">
                            <span>🔬 CSIR Inspector [${data.sir.control_metadata.validation_status}]</span>
                            <span>▾</span>
                        </div>
                        <div class="csir-content">${escapeHtml(sirJson)}</div>
                    </div>
                `;
            }

            el.innerHTML = `
                <div class="bubble-body">
                    ${formattedText}
                    ${placesHtml}
                    ${csirHtml}
                </div>
                <div class="bubble-meta">Asisten Spasial • MySQL 8.0 • ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
            `;

            container.appendChild(el);
            container.scrollTop = container.scrollHeight;
        }

        function focusOnPoi(id, lat, lng) {
            map.flyTo([lat, lng], 16, { duration: 1 });
            markersLayer.eachLayer(layer => {
                if (layer.poiId == id) {
                    layer.openPopup();
                }
            });
        }

        function toggleCsir(headerEl) {
            const content = headerEl.nextElementSibling;
            if (content.style.display === 'block') {
                content.style.display = 'none';
                headerEl.querySelector('span:last-child').textContent = '▾';
            } else {
                content.style.display = 'block';
                headerEl.querySelector('span:last-child').textContent = '▴';
            }
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Auto-run query from URL param (useful for research evaluations & screenshots)
        window.addEventListener('DOMContentLoaded', () => {
            const params = new URLSearchParams(window.location.search);
            const q = params.get('q');
            if (q) {
                setTimeout(async () => {
                    const input = document.getElementById('chat-input');
                    if (input) {
                        input.value = q;
                        await handleSend(new Event('submit'));
                        if (params.get('route')) {
                            setTimeout(() => {
                                calculateRoute(-0.958742, 100.354128, 'Pantai Padang');
                            }, 1200);
                        }
                        if (params.get('open_csir')) {
                            setTimeout(() => {
                                document.querySelectorAll('.csir-toggle').forEach(el => el.click());
                            }, 1500);
                        }
                    }
                }, 800);
            }
        });
    </script>
</body>
</html>

<?php

use CodeIgniter\Router\RouteCollection;

/** @var RouteCollection $routes */
$routes->match(['get', 'head'], '/', 'WebGisController::index');

// API Endpoints
$routes->post('api/chat', 'ChatController::send');
$routes->match(['get', 'head'], 'api/places', 'ChatController::places');

<?php

// routes/api.php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ChatController;
use App\Http\Controllers\ImageProcessorController;

Route::middleware([\App\Http\Middleware\CorsMiddleware::class])->group(function () {
    Route::post('/chat', [ChatController::class, 'chat']);
    Route::post('/process-image', [ImageProcessorController::class, 'processImage']);
});


<?php

// routes/api.php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use App\Http\Controllers\ChatController;
use Illuminate\Support\Facades\Route;

Route::post('/chat', [ChatController::class, 'chat']);
Route::post('/process-image', function(Request $request) {
    $response = Http::attach(
        'file', $request->file('image')->get(),
        $request->file('image')->getClientOriginalName()
    )->post('http://127.0.0.1:8001/process-image');

    return response()->json($response->json());
});


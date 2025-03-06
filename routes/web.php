<?php
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ChatController;
use App\Http\Controllers\ImageProcessorController;

Route::get('/', function () {
return view('welcome');});

Route::post('/chat', [ChatController::class, 'chat']);
Route::post('/process-image', [ChatController::class, 'imageProcessor']);
Route::post('/imageprocess', [ImageProcessorController::class, 'processImage']);
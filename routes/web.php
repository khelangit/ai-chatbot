<?php
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ChatController;

Route::get('/', function () {
return view('welcome');});

Route::post('/chat', [ChatController::class, 'chat']);
Route::post('/process-image', [ChatController::class, 'imageProcessor']);
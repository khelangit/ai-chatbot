<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class ImageProcessorController extends Controller
{
    public function processImage(Request $request)
    {
        // The controller validates 'image' parameter
        $request->validate([
            'file' => 'required|image|mimes:jpeg,png,jpg,gif|max:2048',
        ]);

        // But attaches the file as 'file' to the FastAPI request
        $response = Http::timeout(90)
            ->attach(
                'file',
                file_get_contents($request->file('file')->getRealPath()),
                $request->file('file')->getClientOriginalName()
            )
            ->post('http://127.0.0.1:8001/process_image/');

        if ($response->failed()) {
        Log::error("FastAPI Error: " . $response->body());
            return response()->json(['error' => 'FastAPI Error: ' . $response->body()], 500);
        }

        return response()->json($response->json());
    }
}

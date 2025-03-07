<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class ImageProcessorController extends Controller
{
    public function processImage(Request $request)
    {
        $request->validate([
            'image' => 'required|image|mimes:jpeg,png,jpg,gif|max:2048',
        ]);

        try {
            $response = Http::timeout(300) // Increase timeout to 300 seconds
                ->attach(
                    'file',
                    file_get_contents($request->file('image')->getRealPath()),
                    $request->file('image')->getClientOriginalName()
                )
                ->post('http://127.0.0.1:8001/process_image/');

            if ($response->failed()) {
            Log::error("FastAPI Error: " . $response->body());
                return response()->json(['error' => 'FastAPI Error: ' . $response->body()], 500);
            }

            return response()->json($response->json());
        } catch (\Exception $e) {
            Log::error("Image Processing Exception: " . $e->getMessage());
            return response()->json(['error' => 'Error processing image: ' . $e->getMessage()], 500);
        }
    }
}

<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class ChatController extends Controller
{
    public function chat(Request $request)
    {
        $query = $request->input('prompt');

        try {
            $response = Http::timeout(300)->post('http://127.0.0.1:11434/api/generate', [
                'model' => 'mistral',
                'prompt' => $query,
                'stream' => false
            ]);

            if ($response->successful()) {
                return response()->json(['reply' => $response->json()['response']]);
            } else {
                return response()->json(['error' => 'AI Model did not respond properly.'], 500);
            }
        } catch (\Exception $e) {
            Log::error('Chat API Error: ' . $e->getMessage());
            return response()->json(['error' => 'Error connecting to AI model: ' . $e->getMessage()], 500);
        }
    }

    public function processImage(Request $request)
    {
        try {
            // Validate image file
            $request->validate([
                'image' => 'required|image|mimes:jpeg,png,jpg,gif|max:2048',
            ]);

            // Make a POST request with the image file
            $response = Http::attach(
                'file', 
                file_get_contents($request->file('image')->path()), 
                $request->file('image')->getClientOriginalName()
            )->post('http://127.0.0.1:8001/process-image');

            // Check response
            if ($response->successful()) {
                return response()->json($response->json());
            } else {
                return response()->json(['error' => 'Image processing failed.'], 500);
            }
        } catch (\Exception $e) {
            Log::error('Image Processing Error: ' . $e->getMessage());
            return response()->json(['error' => 'Error processing image: ' . $e->getMessage()], 500);
        }
    }
}
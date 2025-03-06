<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ImageProcessController extends Controller
{
    public function processImage(Request $request)
    {
        $request->validate([
            'image' => 'required|image|mimes:jpeg,png,jpg|max:2048',
        ]);

        $response = Http::attach(
            'file', 
            file_get_contents($request->file('image')->getRealPath()), 
            $request->file('image')->getClientOriginalName()
        )->post('http://127.0.0.1:8001/process_image/');

        return response()->json($response->json());
    }
}

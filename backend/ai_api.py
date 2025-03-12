from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import torch
from diffusers import StableDiffusionPipeline
import cv2
from paddleocr import PaddleOCR
import numpy as np
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
import uvicorn
import asyncio
import os
import time
import traceback
import multiprocessing 
import base64
from io import BytesIO
from PIL import Image

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create output directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize models
ocr = PaddleOCR(use_angle_cls=True, lang='en')

try:
    # Load SAM Model
    sam_checkpoint = "sam_vit_b.pth"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    sam = sam_model_registry["vit_b"](checkpoint=sam_checkpoint).to(device)
    mask_generator = SamAutomaticMaskGenerator(sam)

    # Load Stable Diffusion Model
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32).to(device)
except Exception as e:
    print(f"Error loading models: {e}")

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    start_time = time.time()
    temp_files = []
    
    try:
        # Read Image
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Empty file received")
            
        # Convert bytes to image
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # Save original image
        original_path = os.path.join(UPLOAD_DIR, f"original_{int(time.time())}.png")
        cv2.imwrite(original_path, image)
        temp_files.append(original_path)

        # OCR Text Extraction
        ocr_result = ocr.ocr(image)
        extracted_text = [word_info[1][0] for line in ocr_result for word_info in line]

        # Generate Image
        prompt = f"A structured HTML layout based on: {' '.join(extracted_text[:100])}"
        output_image = pipe(prompt, height=512, width=512).images[0]
        
        # Convert output image to base64
        output_base64 = image_to_base64(output_image)

        return JSONResponse({
            "extracted_text": extracted_text,
            "output_image": f"data:image/png;base64,{output_base64}"
        })

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup temporary files
        elapsed_time = time.time() - start_time
        print(f"Processing took {elapsed_time:.2f} seconds")
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"Error cleaning up {temp_file}: {e}")

@app.get("/")
def read_root():
    return {"message": "API is running!"}

if __name__ == "__main__":
    multiprocessing.set_start_method("fork", force=True)
    uvicorn.run("ai_api:app", host="127.0.0.1", port=8001, reload=True, timeout_keep_alive=600)

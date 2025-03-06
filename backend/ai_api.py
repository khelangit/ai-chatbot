from fastapi import FastAPI, UploadFile, File
import torch
from diffusers import StableDiffusionPipeline
import cv2
from paddleocr import PaddleOCR
import numpy as np
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
import uvicorn

app = FastAPI()

# Load PaddleOCR Model
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Load SAM Model
sam_checkpoint = "sam_vit_b.pth"
device = "cuda" if torch.cuda.is_available() else "cpu"
sam = sam_model_registry["vit_b"](checkpoint=sam_checkpoint).to(device)
mask_generator = SamAutomaticMaskGenerator(sam)

# Load Stable Diffusion Model
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32).to("cpu")

@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    # Read Image
    image_bytes = await file.read()
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # OCR Text Extraction
    ocr_result = ocr.ocr(image)
    extracted_text = [word_info[1][0] for line in ocr_result for word_info in line]

    # Image Segmentation (SAM)
    masks = mask_generator.generate(image)

    # Generate Image (Stable Diffusion)
    prompt = "A structured HTML layout based on the extracted content"
    output_image = pipe(prompt, height=512, width=512).images[0]

    # Save & Return Result
    output_image_path = "output.png"
    output_image.save(output_image_path)
    
    return {
        "extracted_text": extracted_text,
        "output_image": output_image_path
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

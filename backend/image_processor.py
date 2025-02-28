import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers.utils import load_image
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore # Use StreamingResponse for in-memory file bytes
import io
from PIL import Image

app = FastAPI()  # FastAPI instance

class ImageProcessor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Use float16 for GPU, float32 for CPU
        self.dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        self.controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/sd-controlnet-canny",
            torch_dtype=self.dtype
        )
        self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            controlnet=self.controlnet,
            torch_dtype=self.dtype
        )
        self.pipe.to(self.device)

    def process_image(self, image_path, prompt, negative_prompt=""):
        # Load and preprocess the image
        image = load_image(image_path)
        image = np.array(image)
        
        # Apply Canny edge detection
        low_threshold = 100
        high_threshold = 200
        image = cv2.Canny(image, low_threshold, high_threshold)
        image = image[:, :, None]
        image = np.concatenate([image, image, image], axis=2)
        canny_image = torch.from_numpy(image).float() / 255.0

        # Generate image
        output = self.pipe(
            prompt,
            negative_prompt=negative_prompt,
            image=canny_image,
            num_inference_steps=20
        ).images[0]
        
        return output

# Create a global instance of ImageProcessor
processor = ImageProcessor()

@app.post("/process-image/")
async def process_image_endpoint(
    file: UploadFile = File(...),
    prompt: str = "A beautiful mountain landscape, high quality, detailed",
    negative_prompt: str = "blur, low quality"
):
    # Save uploaded file temporarily
    temp_path = "temp_input.jpg"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Process the image
    result = processor.process_image(temp_path, prompt, negative_prompt)
    
    # Convert PIL image to bytes and return a StreamingResponse instead of FileResponse
    img_byte_arr = io.BytesIO()
    result.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return StreamingResponse(img_byte_arr, media_type="image/png")

# Run example when executed as a script
if __name__ == "__main__":
    processor = ImageProcessor()
    
    # Example usage
    result = processor.process_image(
        "input.jpg",
        "A beautiful mountain landscape, high quality, detailed",
        "blur, low quality"
    )
    result.save("output.jpg")
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
from ai_api import ImageProcessor

app = FastAPI()
processor = ImageProcessor()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/process-image/")
async def process_image(image: UploadFile = File(...)):
    print("Saving image to")
    image_path = f"{UPLOAD_FOLDER}/{image.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    try:
        result = processor.process_image(image_path)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

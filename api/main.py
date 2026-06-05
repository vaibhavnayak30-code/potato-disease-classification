import os
from io import BytesIO

import numpy as np
import tensorflow as tf
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

app = FastAPI()

cors_origins = os.getenv("CORS_ORIGINS", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if cors_origins == "*" else cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "saved_models", "1", "1.keras")

MODEL = tf.keras.models.load_model(MODEL_PATH)

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]


def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data)).convert("RGB")
    image = image.resize((256, 256))
    return np.array(image)


@app.get("/")
async def root():
    return {"message": "Potato Disease API Running"}


@app.post("/prediction")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    return {
        "predicted_class": predicted_class,
        "confidence": float(confidence),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
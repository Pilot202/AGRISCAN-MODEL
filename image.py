import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from tensorflow.keras.models import model_from_jsonA
from tensorflow.keras.preprocessing import image
import numpy as np

# Initialize router
router = APIRouter()

# Load the trained model (ensure paths are correct)
MODEL_ARCHITECTURE_PATH = "models/agroscanmodel1_architecture"
MODEL_WEIGHTS_PATH = "models/agroscanmodel1_weights.weights.h5"

with open(MODEL_ARCHITECTURE_PATH, "r") as file:
    model = model_from_json(file.read())
model.load_weights(MODEL_WEIGHTS_PATH)

# Disease classification mapping (12 classes)
DISEASE_CLASSES = [
    "Blight", "Rust", "Gray Leaf Spot", "Northern Leaf Blight", 
    "Common Rust", "Leaf Spot", "Smut", "Downy Mildew",
    "Healthy", "Anthracnose", "Maize Streak Virus", "Ear Rot"
]

# Function to preprocess image
def preprocess_image(image_path: str):
    img = image.load_img(image_path, target_size=(224, 224))  # Adjust size as needed
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize pixel values
    return img_array

# Endpoint to handle image upload and prediction
@router.post("/predict")
async def predict_disease(image_file: UploadFile = File(...), current_user: dict = Depends()):
    """
    Handle uploaded images, run prediction, and return disease details.
    """
    if image_file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG or PNG images are supported.")

    # Save uploaded file temporarily
    file_location = f"temp/{image_file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await image_file.read())

    # Preprocess the image
    try:
        img_array = preprocess_image(file_location)
    except Exception as e:
        os.remove(file_location)
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

    # Predict using the model
    try:
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        disease_name = DISEASE_CLASSES[predicted_class]

        # Read additional details (causes, symptoms, and cure) from a text file
        disease_details_file = f"disease_info/{disease_name.lower().replace(' ', '_')}.txt"
        if os.path.exists(disease_details_file):
            with open(disease_details_file, "r") as file:
                details = file.read()
        else:
            details = "Details not available for this disease."

        # Return prediction and details
        return JSONResponse(content=jsonable_encoder({
            "disease": disease_name,
            "details": details
        }))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    finally:
        os.remove(file_location)  # Clean up temporary file

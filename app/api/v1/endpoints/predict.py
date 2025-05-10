import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.ml.predict import predict_dinosaur
from app.ml.train import get_train_generator
from typing import Dict, Any

router = APIRouter()

@router.post("/predict/", response_model=Dict[str, Any])
async def predict_image(image: UploadFile = File(...)):
    """
    Endpoint to predict dinosaur species from an image.
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail="File must be an image"
        )
    
    # Create temporary directory for image processing
    temp_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "data", "temp")
    os.makedirs(temp_dir, exist_ok=True)
    img_path = os.path.join(temp_dir, "temp_image.jpg")
    
    try:
        # Save uploaded image
        with open(img_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        
        # Get prediction
        result = predict_dinosaur(img_path, get_train_generator().class_indices)
        
        # Handle prediction errors
        if "error" in result:
            raise HTTPException(
                status_code=500 if result["error"] != "Model not available" else 503,
                detail=result["message"]
            )
        
        return result
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    
    finally:
        # Cleanup temporary file
        if os.path.exists(img_path):
            os.remove(img_path) 
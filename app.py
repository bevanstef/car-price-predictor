"""
app.py - FastAPI Inference Backend

Clean Architecture:
- Domain / Presentation: Pydantic schemas validating input and output
- Service Layer: In-memory sklearn prediction pipeline loaded via lifespan
- API Layer: POST /predict endpoint
"""

from contextlib import asynccontextmanager
from typing import Literal
import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Global reference for the loaded sklearn pipeline
# Note: Named 'prediction_pipeline' to avoid collision with request field 'model'
prediction_pipeline = None
MODEL_PATH = "model.joblib"


class CarFeatures(BaseModel):
    brand: str = Field(..., example="Toyota")
    model: str = Field(..., example="Aqua")
    year: int = Field(..., ge=2005, le=2025, example=2018)
    mileage_km: float = Field(..., ge=0, example=45000.0)
    fuel: Literal["Petrol", "Diesel", "Hybrid", "Electric"] = Field(..., example="Hybrid")
    transmission: Literal["Manual", "Automatic"] = Field(..., example="Automatic")
    engine_cc: int = Field(..., example=1500)


class PredictionResponse(BaseModel):
    price_lkr: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the trained machine learning pipeline once at application startup."""
    global prediction_pipeline
    if os.path.exists(MODEL_PATH):
        prediction_pipeline = joblib.load(MODEL_PATH)
        print(f"[OK] Loaded ML pipeline from {MODEL_PATH}")
    else:
        print(f"[WARNING] {MODEL_PATH} not found. Run train.py first!")
    yield


app = FastAPI(
    title="Sri Lanka Used Car Price Predictor API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def health_check():
    return {"status": "ok", "model_loaded": prediction_pipeline is not None}


@app.post("/predict", response_model=PredictionResponse)
def predict_price(car: CarFeatures):
    """Validate request, transform into dataframe, and execute prediction."""
    if prediction_pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded. Please train the model and generate model.joblib first.",
        )

    # Convert Pydantic model to a 1-row DataFrame matching the training schema
    input_data = pd.DataFrame([car.model_dump()])
    predicted_price = float(prediction_pipeline.predict(input_data)[0])

    return PredictionResponse(price_lkr=round(predicted_price, -3))

from fastapi import APIRouter
from app.schemas.schema import HouseFeatures
from app.services.ml_service import predict_price

router = APIRouter()

@router.post("/predict")
def predict(features: HouseFeatures):
    return {
        "predicted_price": predict_price(features)
    }
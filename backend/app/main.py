from fastapi import FastAPI
from app.api.routes import predict, health, location_router, feature_routes, quality_router, utilities_router, price_trends_router, map_router

app = FastAPI(title="House Price Prediction API")

app.include_router(predict.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(price_trends_router.router, prefix="/api")
app.include_router(location_router.router, prefix="/api")
app.include_router(feature_routes.router, prefix="/api")
app.include_router(quality_router.router, prefix="/api")
app.include_router(utilities_router.router, prefix="/api")
app.include_router(map_router.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend Running"}
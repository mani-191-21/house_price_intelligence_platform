from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

DATA_PATH = os.path.join(BASE_DIR, "data", "house_prices1.csv")

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"CSV file not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    return df

@router.get("/features/building-types")
def building_types():
    df = load_data()
    data = df["Building Type"].value_counts().reset_index()
    data.columns = ["Type", "Count"]
    return data.to_dict(orient="records")

@router.get("/features/house-styles")
def house_styles():
    df = load_data()
    data = df["House Style"].value_counts().reset_index()
    data.columns = ["Style", "Count"]
    return data.to_dict(orient="records")

@router.get("/features/foundations")
def foundations():
    df = load_data()
    data = df["Foundation Type"].value_counts().reset_index()
    data.columns = ["Foundation", "Count"]
    return data.to_dict(orient="records")

@router.get("/features/living-area-impact")
def living_area_impact():
    df = load_data()
    return df[["Above Ground Living Area", "House Sale Price", "Overall Material Quality", "Total Basement Area"]]\
        .dropna().to_dict(orient="records")

@router.get("/features/floor-impact")
def floor_impact():
    df = load_data()
    df["Total Floors"] = df["First Floor Area"] + df["Second Floor Area"]
    return df[["Total Floors", "House Sale Price"]].dropna().to_dict(orient="records")

@router.get("/features/bedrooms")
def bedroom_impact():
    df = load_data()
    data = df.groupby("Bedrooms Above Ground")["House Sale Price"].mean().reset_index()
    return data.to_dict(orient="records")

@router.get("/features/bathrooms")
def bathroom_impact():
    df = load_data()
    data = df.groupby("Full Bathrooms")["House Sale Price"].mean().reset_index()
    return data.to_dict(orient="records")

@router.get("/features/garage")
def garage_impact():
    df = load_data()
    data = df.groupby("Garage Capacity Cars")["House Sale Price"].mean().reset_index()
    return data.to_dict(orient="records")

@router.get("/features/outdoor")
def outdoor_features():
    df = load_data()
    return df[["Wood Deck Area", "Open Porch Area", "House Sale Price"]].dropna().to_dict(orient="records")

@router.get("/features/pool")
def pool_quality():
    df = load_data()
    pool = df[df["Pool Area"] > 0].groupby("Pool Quality")["House Sale Price"].mean().reset_index()
    return pool.to_dict(orient="records")
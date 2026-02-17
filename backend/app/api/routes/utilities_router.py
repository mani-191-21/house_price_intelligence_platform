from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()

# ============================
# PATH SETUP
# ============================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        )
    )
)

DATA_PATH = os.path.join(BASE_DIR, "data", "house_prices1.csv")


# ============================
# LOAD CSV
# ============================

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"CSV not found: {DATA_PATH}")
    return pd.read_csv(DATA_PATH)


# ============================
# CENTRAL AIR
# ============================

@router.get("/utilities/central-air")
def central_air():
    df = load_data()
    data = df.groupby("Central Air Conditioning")["House Sale Price"].mean().reset_index()
    return data.to_dict(orient="records")


# ============================
# HEATING QUALITY
# ============================

@router.get("/utilities/heating-quality")
def heating_quality():
    df = load_data()
    data = df.groupby("Heating Quality")["House Sale Price"].mean().reset_index()
    return data.sort_values("House Sale Price", ascending=False).to_dict(orient="records")


# ============================
# ELECTRICAL SYSTEM
# ============================

@router.get("/utilities/electrical")
def electrical():
    df = load_data()
    data = df.groupby("Electrical System")["House Sale Price"].mean().reset_index()
    return data.sort_values("House Sale Price", ascending=False).to_dict(orient="records")


# ============================
# GARAGE YEAR VS PRICE
# ============================

@router.get("/utilities/garage-age")
def garage_age():
    df = load_data()

    gdf = df.dropna(subset=["Garage Construction Year"])

    return gdf[["Garage Construction Year", "House Sale Price", "Garage Capacity Cars"]].to_dict(orient="records")


# ============================
# UTILITIES SUMMARY
# ============================

@router.get("/utilities/summary")
def utilities_summary():
    df = load_data()

    cols = ["Heating Quality", "Electrical System", "Central Air Conditioning", "Driveway Paving"]

    summary = {}

    for col in cols:
        summary[col] = df[col].value_counts().to_dict()

    return summary
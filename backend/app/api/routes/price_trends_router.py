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

    # ── Aggressive column name cleaning ─────────────────────────────
    # 1. Strip whitespace
    df.columns = df.columns.str.strip()
    
    # 2. Convert to title case (Yearbuilt → YearBuilt)
    df.columns = df.columns.str.title()
    
    # Debug: show what we actually have (comment out in production)
    print("Loaded columns:", df.columns.tolist())
    year_cols = [c for c in df.columns if "year" in c.lower()]
    print("Year-related columns:", year_cols)
    
    return df


@router.get("/price-trends/yearly")
def yearly_price_trends():
    df = load_data()
    
    year_col = "Construction Year"
    if year_col not in df.columns:
        year_candidates = [c for c in df.columns if "year" in c.lower() and "built" in c.lower()]
        if year_candidates:
            year_col = year_candidates[0]
            print(f"Using fallback year column: {year_col}")
        else:
            return {"error": "No year built column found in dataset"}
    
    yearly = (
        df.groupby(year_col)["House Sale Price"]
        .mean()
        .reset_index()
        .rename(columns={year_col: "Construction Year", "House Sale Price": "House Sale Price"})
    )
    
    return yearly.to_dict(orient="records")


@router.get("/price-trends/seasonal")
def seasonal_patterns():
    df = load_data()
    seasonal = (
        df.groupby("Month Sold")["House Sale Price"]
        .mean()
        .reset_index()
        .rename(columns={"Month Sold": "Month Sold", "House Sale Price": "House Sale Price"})
    )
    return seasonal.to_dict(orient="records")


@router.get("/price-trends/distribution")
def price_distribution():
    df = load_data()
    stats = df["House Sale Price"].describe()
    result = [
        {"Metric": k, "Value": float(v)}
        for k, v in stats.items()
    ]
    return result


@router.get("/price-trends/segments")
def market_segments():
    df = load_data()
    segments = (
        df.groupby("Overall Material Quality")["House Sale Price"]
        .mean()
        .reset_index()
        .rename(columns={"Overall Material Quality": "Overall Material Quality", "House Sale Price": "House Sale Price"})
    )
    return segments.to_dict(orient="records")
from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()

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

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"CSV file not found: {DATA_PATH}")

    return pd.read_csv(DATA_PATH)


@router.get("/location/neighborhood")
def neighborhood_comparison():

    df = load_data()

    if df.empty:
        return {"error": "Dataset empty"}

    # =============================
    # 1. Neighborhood Comparison
    # =============================

    neighborhood_stats = df.groupby("Neighborhood Name").agg(
        AvgPrice=("House Sale Price", "mean"),
        MedianPrice=("House Sale Price", "median"),
        TotalSales=("House Sale Price", "count")
    ).reset_index().sort_values(by="AvgPrice", ascending=False)

    # =============================
    # 2. Zoning Impact
    # =============================

    zoning_impact = df.groupby("Zoning Classification").agg(
        AvgPrice=("House Sale Price", "mean"),
        MedianPrice=("House Sale Price", "median"),
        TotalSales=("House Sale Price", "count")
    ).reset_index().sort_values(by="AvgPrice", ascending=False)

    # =============================
    # 3. Lot Frontage vs Price
    # =============================

    lot_frontage = df[["Lot Frontage Length", "House Sale Price"]].dropna()

    # =============================
    # 4. Lot Area Impact
    # =============================

    lot_area = df.groupby(
        pd.cut(
            df["Lot Area Square Feet"],
            bins=[0, 5000, 10000, 20000, 50000, df["Lot Area Square Feet"].max()]
        )
    ).agg(
        AvgPrice=("House Sale Price", "mean"),
        Count=("House Sale Price", "count")
    ).reset_index()

    lot_area["Lot Area Range"] = lot_area["Lot Area Square Feet"].astype(str)

    # =============================
    # 5. Alley Access
    # =============================

    alley_analysis = df.groupby("Alley Access").agg(
        AvgPrice=("House Sale Price", "mean"),
        Count=("House Sale Price", "count")
    ).reset_index()

    alley_analysis["Alley Access"] = alley_analysis["Alley Access"].fillna("No Alley")

    # =============================
    # 6. Paved Drive Premium
    # =============================

    paved_drive = df.groupby("Driveway Paving").agg(
        AvgPrice=("House Sale Price", "mean"),
        MedianPrice=("House Sale Price", "median"),
        Count=("House Sale Price", "count")
    ).reset_index()

    # =============================
    # API RESPONSE
    # =============================

    return {
        "neighborhood_comparison": neighborhood_stats.to_dict(orient="records"),
        "zoning_impact": zoning_impact.to_dict(orient="records"),
        "lot_frontage_vs_price": lot_frontage.to_dict(orient="records"),
        "lot_area_impact": lot_area[["Lot Area Range", "AvgPrice", "Count"]].to_dict(orient="records"),
        "alley_access_analysis": alley_analysis.to_dict(orient="records"),
        "paved_drive_premium": paved_drive.to_dict(orient="records")
    }

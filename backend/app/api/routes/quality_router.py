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
        raise FileNotFoundError(f"CSV file not found: {DATA_PATH}")

    return pd.read_csv(DATA_PATH)


# ============================
# OVERALL QUALITY
# ============================

@router.get("/quality/overall")
def overall_quality():
    df = load_data()
    data = df.groupby("Overall Material Quality")["House Sale Price"].mean().reset_index()
    return data.to_dict(orient="records")


# ============================
# OVERALL CONDITION
# ============================

@router.get("/quality/condition")
def overall_condition():
    df = load_data()
    data = df["Overall Condition Rating"].value_counts().reset_index()
    data.columns = ["Overall Condition Rating", "Count"]
    return data.to_dict(orient="records")


# ============================
# EXTERIOR QUALITY
# ============================

@router.get("/quality/exterior")
def exterior_quality():
    df = load_data()
    data = df.groupby("Exterior Quality")["House Sale Price"].mean().reset_index()
    data.columns = ["Category", "House Sale Price"]
    return data.to_dict(orient="records")


# ============================
# KITCHEN QUALITY
# ============================

@router.get("/quality/kitchen")
def kitchen_quality():
    df = load_data()
    data = df.groupby("Kitchen Quality")["House Sale Price"].mean().reset_index()
    data.columns = ["Category", "House Sale Price"]
    return data.to_dict(orient="records")


# ============================
# BASEMENT QUALITY
# ============================

@router.get("/quality/basement")
def basement_quality():
    df = load_data()
    data = df.groupby("Basement Height Quality")["House Sale Price"].mean().reset_index()
    data.columns = ["Category", "House Sale Price"]
    return data.to_dict(orient="records")


# ============================
# FIREPLACE QUALITY
# ============================

@router.get("/quality/fireplace")
def fireplace_quality():
    df = load_data()

    if "Fireplace Quality" not in df.columns:
        return []

    data = df.groupby("Fireplace Quality")["House Sale Price"].mean().reset_index()
    data.columns = ["Category", "House Sale Price"]
    return data.to_dict(orient="records")


# ============================
# MASONRY VENEER
# ============================

@router.get("/quality/masonry")
def masonry_quality():
    df = load_data()
    data = df.groupby("Masonry Veneer Type")["House Sale Price"].mean().reset_index()
    return data.to_dict(orient="records")


# ============================
# EXTERIOR CONDITION
# ============================

@router.get("/quality/exterior-condition")
def exterior_condition():
    df = load_data()
    data = df.groupby("Exterior Condition")["House Sale Price"].mean().reset_index()
    return data.to_dict(orient="records")

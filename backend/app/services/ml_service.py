import joblib
import os
import pandas as pd
import numpy as np

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "house_price_full_pipeline.pkl"
)

loaded_object = joblib.load(MODEL_PATH)

model = loaded_object["model"]
scaler = loaded_object["scaler"]
label_encoders = loaded_object.get("label_encoders", {})  # Get label encoders if they exist


def predict_price(features):
    # Create DataFrame
    df = pd.DataFrame([{
        "MSSubClass": features.MSSubClass,
        "MSZoning": features.MSZoning,
        "LotFrontage": features.LotFrontage,
        "LotArea": features.LotArea,
        "Street": features.Street,
        "Alley": features.Alley,
        "LotShape": features.LotShape,
        "LandContour": features.LandContour,
        "Utilities": features.Utilities,
        "LotConfig": features.LotConfig,
        "LandSlope": features.LandSlope,
        "Neighborhood": features.Neighborhood,
        "Condition1": features.Condition1,
        "Condition2": features.Condition2,
        "BldgType": features.BldgType,
        "HouseStyle": features.HouseStyle,
        "OverallQual": features.OverallQual,
        "OverallCond": features.OverallCond,
        "YearBuilt": features.YearBuilt,
        "YearRemodAdd": features.YearRemodAdd,
        "RoofStyle": features.RoofStyle,
        "RoofMatl": features.RoofMatl,
        "Exterior1st": features.Exterior1st,
        "Exterior2nd": features.Exterior2nd,
        "MasVnrType": features.MasVnrType,
        "MasVnrArea": features.MasVnrArea,
        "ExterQual": features.ExterQual,
        "ExterCond": features.ExterCond,
        "Foundation": features.Foundation,
        "BsmtQual": features.BsmtQual,
        "BsmtCond": features.BsmtCond,
        "BsmtExposure": features.BsmtExposure,
        "BsmtFinType1": features.BsmtFinType1,
        "BsmtFinSF1": features.BsmtFinSF1,
        "BsmtFinType2": features.BsmtFinType2,
        "BsmtFinSF2": features.BsmtFinSF2,
        "BsmtUnfSF": features.BsmtUnfSF,
        "TotalBsmtSF": features.TotalBsmtSF,
        "Heating": features.Heating,
        "HeatingQC": features.HeatingQC,
        "CentralAir": features.CentralAir,
        "Electrical": features.Electrical,
        "1stFlrSF": features.FirstFlrSF,
        "2ndFlrSF": features.SecondFlrSF,
        "LowQualFinSF": features.LowQualFinSF,
        "GrLivArea": features.GrLivArea,
        "BsmtFullBath": features.BsmtFullBath,
        "BsmtHalfBath": features.BsmtHalfBath,
        "FullBath": features.FullBath,
        "HalfBath": features.HalfBath,
        "BedroomAbvGr": features.BedroomAbvGr,
        "KitchenAbvGr": features.KitchenAbvGr,
        "KitchenQual": features.KitchenQual,
        "TotRmsAbvGrd": features.TotRmsAbvGrd,
        "Functional": features.Functional,
        "Fireplaces": features.Fireplaces,
        "FireplaceQu": features.FireplaceQu,
        "GarageType": features.GarageType,
        "GarageYrBlt": features.GarageYrBlt,
        "GarageFinish": features.GarageFinish,
        "GarageCars": features.GarageCars,
        "GarageArea": features.GarageArea,
        "GarageQual": features.GarageQual,
        "GarageCond": features.GarageCond,
        "PavedDrive": features.PavedDrive,
        "WoodDeckSF": features.WoodDeckSF,
        "OpenPorchSF": features.OpenPorchSF,
        "EnclosedPorch": features.EnclosedPorch,
        "3SsnPorch": features.ThreeSsnPorch,
        "ScreenPorch": features.ScreenPorch,
        "PoolArea": features.PoolArea,
        "PoolQC": features.PoolQC,
        "Fence": features.Fence,
        "MiscFeature": features.MiscFeature,
        "MiscVal": features.MiscVal,
        "MoSold": features.MoSold,
        "YrSold": features.YrSold,
        "SaleType": features.SaleType,
        "SaleCondition": features.SaleCondition
    }])

    # STEP 1: Apply label encoding to categorical columns
    if label_encoders:
        for column, encoder in label_encoders.items():
            if column in df.columns:
                try:
                    # Handle unknown categories by using a default value or the first class
                    if df[column].iloc[0] in encoder.classes_:
                        df[column] = encoder.transform(df[column])
                    else:
                        # If value not seen during training, use the most common class (0)
                        df[column] = 0
                except Exception as e:
                    print(f"Warning: Could not encode {column}: {e}")
                    df[column] = 0

    # STEP 2: Apply scaling
    # Get the exact feature names and order the scaler expects
    try:
        expected_features = scaler.feature_names_in_
        
        # Reorder DataFrame to match scaler's expected order
        df_ordered = df[expected_features]
        
        # Scale the data
        df_scaled = scaler.transform(df_ordered)
        
        # Convert back to DataFrame
        df_final = pd.DataFrame(df_scaled, columns=expected_features)
        
    except AttributeError:
        # If scaler doesn't have feature_names_in_, just scale as is
        df_scaled = scaler.transform(df)
        df_final = pd.DataFrame(df_scaled, columns=df.columns)

    # STEP 3: Predict
    prediction = model.predict(df_final)

    return float(prediction[0])
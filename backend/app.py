
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request


# ---------------------------------------------------------
# Initialize the Flask application
# ---------------------------------------------------------
superkart_api = Flask(__name__)


# ---------------------------------------------------------
# Load the serialized model pipeline
# ---------------------------------------------------------
# This creates a reliable path relative to app.py,
# regardless of the folder from which the application is run.
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "random_forest_sales_forecast.joblib"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Serialized model was not found at: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)


# ---------------------------------------------------------
# Define the features expected by the trained model
# ---------------------------------------------------------
REQUIRED_FEATURES = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category",
]


# ---------------------------------------------------------
# Home endpoint
# ---------------------------------------------------------
@superkart_api.get("/")
def home():
    return jsonify(
        {
            "message": "Welcome to the SuperKart Sales Forecast API.",
            "status": "running",
            "prediction_endpoint": "/v1/predict",
        }
    )


# ---------------------------------------------------------
# Health-check endpoint
# ---------------------------------------------------------
@superkart_api.get("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "model_loaded": True,
        }
    )


# ---------------------------------------------------------
# Sales prediction endpoint
# ---------------------------------------------------------
@superkart_api.post("/v1/predict")
def predict_sales():
    try:
        # Read the JSON request body
        data = request.get_json(silent=True)

        if data is None:
            return jsonify(
                {
                    "error": "Request body must contain valid JSON."
                }
            ), 400

        # Check for missing input features
        missing_features = [
            feature
            for feature in REQUIRED_FEATURES
            if feature not in data
        ]

        if missing_features:
            return jsonify(
                {
                    "error": "Required features are missing.",
                    "missing_features": missing_features,
                }
            ), 400

        # Build the input sample using the same feature names
        # that were used during model training.
        sample = {
            "Product_Weight": float(data["Product_Weight"]),
            "Product_Sugar_Content": str(
                data["Product_Sugar_Content"]
            ),
            "Product_Allocated_Area": float(
                data["Product_Allocated_Area"]
            ),
            "Product_MRP": float(data["Product_MRP"]),
            "Store_Size": str(data["Store_Size"]),
            "Store_Location_City_Type": str(
                data["Store_Location_City_Type"]
            ),
            "Store_Type": str(data["Store_Type"]),
            "Product_Id_char": str(data["Product_Id_char"]),
            "Store_Age_Years": int(data["Store_Age_Years"]),
            "Product_Type_Category": str(
                data["Product_Type_Category"]
            ),
        }

        # Convert the sample into a one-row DataFrame
        input_data = pd.DataFrame(
            [sample],
            columns=REQUIRED_FEATURES,
        )

        # The saved pipeline automatically performs:
        # 1. One-hot encoding
        # 2. Numerical-feature passthrough
        # 3. Random Forest prediction
        prediction = float(model.predict(input_data)[0])

        return jsonify(
            {
                "predicted_sales": round(prediction, 2)
            }
        ), 200

    except (TypeError, ValueError) as error:
        return jsonify(
            {
                "error": "One or more input values have an invalid data type.",
                "details": str(error),
            }
        ), 400

    except Exception as error:
        return jsonify(
            {
                "error": "An unexpected prediction error occurred.",
                "details": str(error),
            }
        ), 500


# ---------------------------------------------------------
# Start the Flask development server
# ---------------------------------------------------------
if __name__ == "__main__":
    superkart_api.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )

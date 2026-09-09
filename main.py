from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel

import joblib
import cv2
import numpy as np

from fashion_recommendation import generate_fashion_recommendations

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

from models import BodyMeasurementResult


app = FastAPI(
    title="AI Body Measurement & Fashion Recommendation API",
    description="AI-based body measurement and fashion recommendation system",
    version="1.0.0"
)


# ============================================================
# LOAD MODEL
# ============================================================

MODEL_PATH = "body_measurement_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Body measurement model loaded successfully!")
    print("✅ Model expects:", model.n_features_in_, "features")
except Exception as e:
    print("❌ Error loading model:", e)
    model = None


# ============================================================
# TEMPORARY USER STORAGE
# ============================================================

users_db = {}


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# ============================================================
# REGISTER
# ============================================================

@app.post("/register")
def register(user: UserRegister):

    if user.username in users_db:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(user.password)

    users_db[user.username] = hashed_password

    return {
        "status": "success",
        "message": "User registered successfully"
    }


# ============================================================
# LOGIN
# ============================================================

@app.post("/login")
def login(user: UserLogin):

    if user.username not in users_db:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    stored_password = users_db[user.username]

    if not verify_password(user.password, stored_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "status": "success",
        "access_token": access_token,
        "token_type": "bearer"
    }


# ============================================================
# FEATURE EXTRACTION
# ============================================================

def extract_features(image_bytes):

    image_array = np.frombuffer(image_bytes, np.uint8)

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_GRAYSCALE
    )

    if image is None:
        raise ValueError("Unable to read image")

    # Threshold
    _, binary = cv2.threshold(
        image,
        127,
        255,
        cv2.THRESH_BINARY
    )

    points = cv2.findNonZero(binary)

    if points is None:
        raise ValueError("No body/silhouette detected in image")

    x, y, width, height = cv2.boundingRect(points)

    silhouette_area = cv2.countNonZero(binary)

    if height == 0:
        raise ValueError("Invalid body height detected")

    area_height_ratio = silhouette_area / height

    width_height_ratio = width / height

    # --------------------------------------------------------
    # Width extraction at different body positions
    # --------------------------------------------------------

    relative_positions = [
        0.20,
        0.35,
        0.50,
        0.65,
        0.78
    ]

    widths = []

    for position in relative_positions:

        row = int(y + height * position)

        if row >= binary.shape[0]:
            row = binary.shape[0] - 1

        row_pixels = np.where(
            binary[row] > 0
        )[0]

        if len(row_pixels) > 0:
            row_width = row_pixels.max() - row_pixels.min() + 1
        else:
            row_width = width

        widths.append(row_width)

    shoulder_width_px = widths[0]
    chest_width_px = widths[1]
    waist_width_px = widths[2]
    hip_width_px = widths[3]
    thigh_width_px = widths[4]

    # Ratios
    shoulder_body_ratio = shoulder_width_px / height
    chest_body_ratio = chest_width_px / height
    waist_body_ratio = waist_width_px / height

    # --------------------------------------------------------
    # EXACT 11 FEATURES EXPECTED BY MODEL
    # --------------------------------------------------------

    features = np.array([
        height,
        silhouette_area,
        area_height_ratio,
        shoulder_width_px,
        chest_width_px,
        waist_width_px,
        hip_width_px,
        thigh_width_px,
        shoulder_body_ratio,
        chest_body_ratio,
        waist_body_ratio
    ]).reshape(1, -1)

    return features


# ============================================================
# MEASUREMENT NAMES
# ============================================================

measurement_names = [
    "ankle",
    "arm-length",
    "bicep",
    "calf",
    "chest",
    "forearm",
    "height",
    "hip",
    "leg-length",
    "shoulder-breadth",
    "shoulder-to-crotch",
    "thigh",
    "waist",
    "wrist"
]


# ============================================================
# PREDICT MEASUREMENTS
# ============================================================

@app.post("/predict-measurements")
def predict_measurements(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Measurement model is not loaded"
        )

    try:

        image_bytes = file.file.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Empty image file"
            )

        features = extract_features(image_bytes)

        prediction = model.predict(features)

        prediction = prediction[0]

        measurements = {
            name: round(float(value), 2)
            for name, value in zip(
                measurement_names,
                prediction
            )
        }

        result = BodyMeasurementResult(
            filename=file.filename,
            measurements=measurements
        )

        return {
            "status": "success",
            "filename": result.filename,
            "user": current_user,
            "features_used": int(features.shape[1]),
            "measurements": result.measurements
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )


# ============================================================
# FASHION RECOMMENDATIONS
# ============================================================

@app.post("/fashion-recommendations")
def fashion_recommendations(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Measurement model is not loaded"
        )

    try:

        image_bytes = file.file.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Empty image file"
            )

        features = extract_features(image_bytes)

        prediction = model.predict(features)

        prediction = prediction[0]

        measurements = {
            name: round(float(value), 2)
            for name, value in zip(
                measurement_names,
                prediction
            )
        }

        result = BodyMeasurementResult(
            filename=file.filename,
            measurements=measurements
        )

        recommendations = generate_fashion_recommendations(
            result.measurements
        )

        return {
            "status": "success",
            "filename": result.filename,
            "user": current_user,
            "measurements": result.measurements,
            "fashion_recommendations": recommendations
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation error: {str(e)}"
        )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "AI Body Measurement & Fashion Recommendation API",
        "status": "running"
    }
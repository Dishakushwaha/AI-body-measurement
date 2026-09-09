from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import joblib
import cv2
import numpy as np

from fashion_recommendation import generate_fashion_recommendations
from models import BodyMeasurementResult
from pydantic import BaseModel

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)


# ==============================
# FASTAPI APP
# ==============================

app = FastAPI(
    title="AI Body Measurement & Fashion API",
    description="AI-powered API for body measurement estimation and fashion recommendations",
    version="1.0.0"
)


# ==============================
# TEMPORARY USER STORAGE
# ==============================

users_db = {}


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# ==============================
# REGISTER
# ==============================

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


# ==============================
# LOGIN
# ==============================

@app.post("/login")
def login(user: UserLogin):

    if user.username not in users_db:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    stored_password = users_db[user.username]

    if not verify_password(
        user.password,
        stored_password
    ):
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


# ==============================
# LOAD MODEL
# ==============================

MODEL_PATH = "body_measurement_model.pkl"

try:

    model = joblib.load(MODEL_PATH)

    print("Body measurement model loaded successfully!")
    print(
        "Model expects:",
        model.n_features_in_,
        "features"
    )

except Exception as e:

    model = None

    print(
        "Model loading failed:",
        e
    )


# ==============================
# MEASUREMENT NAMES
# ==============================

MEASUREMENT_NAMES = [
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


# ==============================
# ROOT ENDPOINT
# ==============================

@app.get("/")
def home():

    return {
        "message": "AI Body Measurement & Fashion API is running!",
        "status": "success",
        "docs": "/docs"
    }


# ==============================
# IMAGE FEATURE EXTRACTION
# ==============================

def extract_image_features(image_bytes):

    image_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_GRAYSCALE
    )

    if image is None:

        raise ValueError(
            "Unable to read image"
        )

    _, binary = cv2.threshold(
        image,
        127,
        255,
        cv2.THRESH_BINARY
    )

    points = cv2.findNonZero(binary)

    if points is None:

        raise ValueError(
            "No body/silhouette detected in image"
        )

    x, y, width, height = cv2.boundingRect(
        points
    )

    if height == 0:

        raise ValueError(
            "Invalid body height detected"
        )

    silhouette_area = cv2.countNonZero(
        binary
    )

    def get_width_at_height(relative_position):

        row = int(
            y + height * relative_position
        )

        if row >= binary.shape[0]:

            return 0.0

        row_pixels = np.where(
            binary[row] > 0
        )[0]

        if len(row_pixels) == 0:

            return 0.0

        return float(
            row_pixels[-1]
            - row_pixels[0]
            + 1
        )

    shoulder_width = get_width_at_height(0.20)

    chest_width = get_width_at_height(0.35)

    waist_width = get_width_at_height(0.50)

    hip_width = get_width_at_height(0.65)

    thigh_width = get_width_at_height(0.78)


    # ==============================
    # FALLBACK VALUES
    # ==============================

    if shoulder_width == 0:
        shoulder_width = float(width)

    if chest_width == 0:
        chest_width = float(width)

    if waist_width == 0:
        waist_width = float(width)

    if hip_width == 0:
        hip_width = float(width)

    if thigh_width == 0:
        thigh_width = float(width)


    # ==============================
    # RATIOS
    # ==============================

    area_height_ratio = (
        silhouette_area / height
    )

    shoulder_body_ratio = (
        shoulder_width / height
    )

    chest_body_ratio = (
        chest_width / height
    )

    waist_body_ratio = (
        waist_width / height
    )


    # ==============================
    # EXACT 11 FEATURES
    # ==============================

    features = np.array(
        [[
            height,
            silhouette_area,
            area_height_ratio,
            shoulder_width,
            chest_width,
            waist_width,
            hip_width,
            thigh_width,
            shoulder_body_ratio,
            chest_body_ratio,
            waist_body_ratio
        ]],
        dtype=np.float32
    )

    print("\n================================")
    print("IMAGE FEATURES")
    print("================================")

    print(
        "body_height_px:",
        height
    )

    print(
        "silhouette_area_px:",
        silhouette_area
    )

    print(
        "area_height_ratio:",
        area_height_ratio
    )

    print(
        "shoulder_width_px:",
        shoulder_width
    )

    print(
        "chest_width_px:",
        chest_width
    )

    print(
        "waist_width_px:",
        waist_width
    )

    print(
        "hip_width_px:",
        hip_width
    )

    print(
        "thigh_width_px:",
        thigh_width
    )

    print(
        "shoulder_body_ratio:",
        shoulder_body_ratio
    )

    print(
        "chest_body_ratio:",
        chest_body_ratio
    )

    print(
        "waist_body_ratio:",
        waist_body_ratio
    )

    print(
        "Feature shape:",
        features.shape
    )

    print("================================\n")

    return features


# ==============================
# PREDICT BODY MEASUREMENTS
# ==============================

@app.post("/predict-measurements")
async def predict_measurements(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):

    if model is None:

        raise HTTPException(
            status_code=500,
            detail="Measurement model is not loaded"
        )

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/jpg"
    ]

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG or PNG image"
        )

    try:

        image_bytes = await file.read()

        if not image_bytes:

            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty"
            )

        features = extract_image_features(
            image_bytes
        )

        if features.shape[1] != model.n_features_in_:

            raise ValueError(
                f"Feature mismatch: API generated "
                f"{features.shape[1]} features, "
                f"but model expects "
                f"{model.n_features_in_} features."
            )

        predictions = model.predict(
            features
        )[0]

        measurements = {}

        for name, value in zip(
            MEASUREMENT_NAMES,
            predictions
        ):

            measurements[name] = round(
                float(value),
                2
            )

        result = BodyMeasurementResult(
            filename=file.filename,
            measurements=measurements
        )

        return {
            "status": "success",
            "filename": result.filename,
            "user": current_user,
            "features_used": int(
                features.shape[1]
            ),
            "measurements": result.measurements
        }

    except HTTPException:

        raise

    except Exception as e:

        print(
            "Prediction error:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==============================
# FASHION RECOMMENDATIONS
# ==============================

@app.post("/fashion-recommendations")
async def fashion_recommendations(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):

    if model is None:

        raise HTTPException(
            status_code=500,
            detail="Measurement model is not loaded"
        )

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/jpg"
    ]

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG or PNG image"
        )

    try:

        image_bytes = await file.read()

        if not image_bytes:

            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty"
            )

        features = extract_image_features(
            image_bytes
        )

        if features.shape[1] != model.n_features_in_:

            raise ValueError(
                f"Feature mismatch: API generated "
                f"{features.shape[1]} features, "
                f"but model expects "
                f"{model.n_features_in_} features."
            )

        predictions = model.predict(
            features
        )[0]

        measurements = {}

        for name, value in zip(
            MEASUREMENT_NAMES,
            predictions
        ):

            measurements[name] = round(
                float(value),
                2
            )

        result = BodyMeasurementResult(
            filename=file.filename,
            measurements=measurements
        )

        recommendations = (
            generate_fashion_recommendations(
                result.measurements
            )
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

        print(
            "Fashion recommendation error:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
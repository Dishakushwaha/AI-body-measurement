import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# ==========================================
# LOAD DATASETS
# ==========================================

train = pd.read_csv("train_features.csv")
val = pd.read_csv("validation_features.csv")
test = pd.read_csv("test_features.csv")

# ==========================================
# SELECT USEFUL IMAGE FEATURES
# ==========================================

features = [
    "body_height_px",
    "silhouette_area_px",
    "area_height_ratio",
    "shoulder_width_px",
    "chest_width_px",
    "waist_width_px",
    "hip_width_px",
    "thigh_width_px",
    "shoulder_body_ratio",
    "chest_body_ratio",
    "waist_body_ratio"
]

# ==========================================
# BODY MEASUREMENT TARGETS
# ==========================================

targets = [
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

# ==========================================
# INPUT / OUTPUT
# ==========================================

X_train = train[features]
y_train = train[targets]

X_val = val[features]
y_val = val[targets]

X_test = test[features]
y_test = test[targets]

# ==========================================
# IMPROVED RANDOM FOREST
# ==========================================

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    min_samples_split=3,
    min_samples_leaf=1,
    max_features="sqrt",
    random_state=42,
    n_jobs=-1
)

multi_model = MultiOutputRegressor(model)

# ==========================================
# TRAIN
# ==========================================

print("Training improved model...")

multi_model.fit(X_train, y_train)

# ==========================================
# VALIDATION PREDICTION
# ==========================================

val_pred = multi_model.predict(X_val)

# ==========================================
# TEST PREDICTION
# ==========================================

test_pred = multi_model.predict(X_test)

# ==========================================
# VALIDATION RESULTS
# ==========================================

print("\n===== IMPROVED VALIDATION RESULTS =====")

val_mae = mean_absolute_error(y_val, val_pred)

val_rmse = np.sqrt(
    mean_squared_error(y_val, val_pred)
)

val_r2 = r2_score(
    y_val,
    val_pred,
    multioutput="uniform_average"
)

print("MAE :", round(val_mae, 4))
print("RMSE:", round(val_rmse, 4))
print("R2  :", round(val_r2, 4))

# ==========================================
# TEST RESULTS
# ==========================================

print("\n===== IMPROVED TEST RESULTS =====")

test_mae = mean_absolute_error(y_test, test_pred)

test_rmse = np.sqrt(
    mean_squared_error(y_test, test_pred)
)

test_r2 = r2_score(
    y_test,
    test_pred,
    multioutput="uniform_average"
)

print("MAE :", round(test_mae, 4))
print("RMSE:", round(test_rmse, 4))
print("R2  :", round(test_r2, 4))

# ==========================================
# INDIVIDUAL MEASUREMENT R2
# ==========================================

print("\n===== INDIVIDUAL MEASUREMENT R2 =====")

for i, target in enumerate(targets):

    score = r2_score(
        y_test.iloc[:, i],
        test_pred[:, i]
    )

    print(f"{target}: {score:.4f}")

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    multi_model,
    "body_measurement_model.pkl"
)

print("\nModel saved as: body_measurement_model.pkl")

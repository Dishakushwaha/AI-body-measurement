import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# ==========================================
# LOAD TRAINING DATA
# ==========================================

train = pd.read_csv("train_features.csv")

# ==========================================
# IMAGE-DERIVED FEATURES
# ==========================================

features = [
    "body_width_px",
    "body_height_px",
    "silhouette_area_px",
    "width_height_ratio",
    "area_height_ratio",
    "shoulder_width_px",
    "chest_width_px",
    "waist_width_px",
    "hip_width_px",
    "thigh_width_px",
    "shoulder_body_ratio",
    "chest_body_ratio",
    "waist_body_ratio",
    "hip_body_ratio"
]

# ==========================================
# 14 BODY MEASUREMENT TARGETS
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

X = train[features]

# ==========================================
# CHECK FEATURE IMPORTANCE
# ==========================================

print("\n==========================================")
print(" FEATURE IMPORTANCE - ALL 14 MEASUREMENTS")
print("==========================================")

for target in targets:

    print("\n------------------------------------------")
    print(f" Target: {target}")
    print("------------------------------------------")

    y = train[target]

    # Random Forest
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    # Feature importance
    importance = pd.DataFrame({
        "Feature": features,
        "Importance": model.feature_importances_
    })

    # Sort highest to lowest
    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    print(importance.to_string(index=False))

# ==========================================
# COMPLETE
# ==========================================

print("\n==========================================")
print(" FEATURE IMPORTANCE CHECK COMPLETE")
print("==========================================")

import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ==========================================
# LOAD CURRENT MODEL
# ==========================================

model = joblib.load("body_measurement_model.pkl")

# ==========================================
# LOAD TEST DATA
# ==========================================

test = pd.read_csv("test_features.csv")

# ==========================================
# FEATURES
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
# TARGETS
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
# PREPARE TEST DATA
# ==========================================

X_test = test[features]
y_test = test[targets]

# ==========================================
# PREDICTIONS
# ==========================================

predictions = model.predict(X_test)

# ==========================================
# ERROR ANALYSIS TABLE
# ==========================================

results = []

for i, target in enumerate(targets):

    actual = y_test.iloc[:, i].values
    predicted = predictions[:, i]

    mae = mean_absolute_error(actual, predicted)

    rmse = np.sqrt(
        mean_squared_error(actual, predicted)
    )

    r2 = r2_score(actual, predicted)

    mean_error = np.mean(predicted - actual)

    mean_abs_error = np.mean(
        np.abs(predicted - actual)
    )

    results.append({
        "Measurement": target,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "Mean Error": mean_error,
        "Mean Absolute Error": mean_abs_error
    })

results_df = pd.DataFrame(results)

# ==========================================
# SORT BY MAE
# ==========================================

results_df = results_df.sort_values(
    by="MAE",
    ascending=False
)

# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n==========================================")
print("        ERROR ANALYSIS RESULTS")
print("==========================================\n")

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)

# ==========================================
# ACTUAL VS PREDICTED VALUES
# ==========================================

print("\n\n==========================================")
print("       ACTUAL VS PREDICTED VALUES")
print("==========================================\n")

for i, target in enumerate(targets):

    print(f"\n--- {target} ---")

    actual = y_test.iloc[:, i].values
    predicted = predictions[:, i]

    for j in range(len(actual)):

        error = predicted[j] - actual[j]

        print(
            f"Actual: {actual[j]:.2f} | "
            f"Predicted: {predicted[j]:.2f} | "
            f"Error: {error:.2f}"
        )

# ==========================================
# WORST MEASUREMENTS
# ==========================================

print("\n\n==========================================")
print("       WORST PERFORMING MEASUREMENTS")
print("==========================================\n")

worst = results_df.head(5)

for _, row in worst.iterrows():

    print(
        f"{row['Measurement']} -> "
        f"MAE: {row['MAE']:.4f}, "
        f"RMSE: {row['RMSE']:.4f}, "
        f"R2: {row['R2']:.4f}"
    )

# ==========================================
# BEST MEASUREMENTS
# ==========================================

print("\n\n==========================================")
print("       BEST PERFORMING MEASUREMENTS")
print("==========================================\n")

best = results_df.sort_values(
    by="R2",
    ascending=False
).head(5)

for _, row in best.iterrows():

    print(
        f"{row['Measurement']} -> "
        f"MAE: {row['MAE']:.4f}, "
        f"RMSE: {row['RMSE']:.4f}, "
        f"R2: {row['R2']:.4f}"
    )

# ==========================================
# SAVE ERROR ANALYSIS
# ==========================================

results_df.to_csv(
    "error_analysis_results.csv",
    index=False
)

print("\n\nError analysis saved as:")
print("error_analysis_results.csv")

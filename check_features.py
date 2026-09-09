import pandas as pd

df = pd.read_csv("bodym_image_features.csv")

print("===== FEATURE DATASET CHECK =====")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())

print("\n===== FEATURE SUMMARY =====")
print(df[
    [
        "body_width_px",
        "body_height_px",
        "silhouette_area_px",
        "width_height_ratio",
        "area_height_ratio"
    ]
].describe())

print("\n===== SUBJECTS =====")
print("Unique subjects:", df["subject_id"].nunique())

print("\n===== CHECK COMPLETE =====")
import pandas as pd

# Load the BodyM CSV files
measurements = pd.read_csv("measurements.csv")
photo_map = pd.read_csv("subject_to_photo_map.csv")

# Merge photos with body measurements using subject_id
dataset = photo_map.merge(
    measurements,
    on="subject_id",
    how="inner"
)

# Create the local path for each mask image
dataset["image_path"] = (
    "train/mask/" + dataset["photo_id"].astype(str) + ".png"
)

# Reorder columns
columns = [
    "subject_id",
    "photo_id",
    "image_path",
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
    "wrist",
]

dataset = dataset[columns]

# Save the final dataset
dataset.to_csv("bodym_dataset.csv", index=False)

# Display basic information
print("Dataset created successfully!")
print("Rows:", len(dataset))
print("Columns:", len(dataset.columns))
print("\nFirst 5 rows:")
print(dataset.head())
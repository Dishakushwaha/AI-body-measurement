import pandas as pd
import cv2

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv("bodym_dataset_cleaned.csv")

# Use first 100 images
df = df[df["image_path"].notna()].head(100).copy()

features = []

# ==========================================
# FEATURE EXTRACTION
# ==========================================

for index, row in df.iterrows():

    image_path = row["image_path"]

    # Read silhouette image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Image not found:", image_path)
        continue

    # Binary silhouette
    _, binary = cv2.threshold(
        image, 127, 255, cv2.THRESH_BINARY
    )

    points = cv2.findNonZero(binary)

    if points is None:
        print("No silhouette found:", image_path)
        continue

    # Get body pixel coordinates
    points = points.reshape(-1, 2)

    xs = points[:, 0]
    ys = points[:, 1]

    # ==========================================
    # BODY BOUNDING BOX
    # ==========================================

    x_min = xs.min()
    x_max = xs.max()
    y_min = ys.min()
    y_max = ys.max()

    body_width = x_max - x_min
    body_height = y_max - y_min

    # ==========================================
    # BASIC FEATURES
    # ==========================================

    area = cv2.countNonZero(binary)

    width_height_ratio = (
        body_width / body_height
        if body_height != 0 else 0
    )

    area_height_ratio = (
        area / body_height
        if body_height != 0 else 0
    )

    # ==========================================
    # BODY REGION WIDTHS
    # ==========================================

    def get_region_width(y_start, y_end):

        region = binary[y_start:y_end, :]

        region_points = cv2.findNonZero(region)

        if region_points is None:
            return 0

        region_points = region_points.reshape(-1, 2)

        return (
            region_points[:, 0].max()
            - region_points[:, 0].min()
        )

    # Divide body vertically into regions
    height = body_height

    shoulder_y1 = int(y_min + height * 0.15)
    shoulder_y2 = int(y_min + height * 0.25)

    chest_y1 = int(y_min + height * 0.25)
    chest_y2 = int(y_min + height * 0.40)

    waist_y1 = int(y_min + height * 0.40)
    waist_y2 = int(y_min + height * 0.55)

    hip_y1 = int(y_min + height * 0.55)
    hip_y2 = int(y_min + height * 0.70)

    thigh_y1 = int(y_min + height * 0.70)
    thigh_y2 = int(y_min + height * 0.82)

    shoulder_width = get_region_width(
        shoulder_y1, shoulder_y2
    )

    chest_width = get_region_width(
        chest_y1, chest_y2
    )

    waist_width = get_region_width(
        waist_y1, waist_y2
    )

    hip_width = get_region_width(
        hip_y1, hip_y2
    )

    thigh_width = get_region_width(
        thigh_y1, thigh_y2
    )

    # ==========================================
    # ADD FEATURES
    # ==========================================

    features.append({

        "subject_id": row["subject_id"],
        "photo_id": row["photo_id"],
        "image_path": image_path,

        # Image features
        "body_width_px": body_width,
        "body_height_px": body_height,
        "silhouette_area_px": area,
        "width_height_ratio": width_height_ratio,
        "area_height_ratio": area_height_ratio,

        # Region features
        "shoulder_width_px": shoulder_width,
        "chest_width_px": chest_width,
        "waist_width_px": waist_width,
        "hip_width_px": hip_width,
        "thigh_width_px": thigh_width,

        # Ratios
        "shoulder_body_ratio": (
            shoulder_width / body_width
            if body_width != 0 else 0
        ),

        "chest_body_ratio": (
            chest_width / body_width
            if body_width != 0 else 0
        ),

        "waist_body_ratio": (
            waist_width / body_width
            if body_width != 0 else 0
        ),

        "hip_body_ratio": (
            hip_width / body_width
            if body_width != 0 else 0
        ),

        # Actual measurements
        "ankle": row["ankle"],
        "arm-length": row["arm-length"],
        "bicep": row["bicep"],
        "calf": row["calf"],
        "chest": row["chest"],
        "forearm": row["forearm"],
        "height": row["height"],
        "hip": row["hip"],
        "leg-length": row["leg-length"],
        "shoulder-breadth": row["shoulder-breadth"],
        "shoulder-to-crotch": row["shoulder-to-crotch"],
        "thigh": row["thigh"],
        "waist": row["waist"],
        "wrist": row["wrist"]
    })


# ==========================================
# CREATE FEATURE DATASET
# ==========================================

features_df = pd.DataFrame(features)

features_df.to_csv(
    "bodym_image_features.csv",
    index=False
)

print("\n===== IMPROVED FEATURE EXTRACTION COMPLETE =====")
print("Images processed:", len(features_df))
print("Rows:", len(features_df))
print("Columns:", len(features_df.columns))

print("\nFeature columns:")
print(features_df.columns.tolist())
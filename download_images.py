import pandas as pd
import os
import subprocess

# ==========================================
# SETTINGS
# ==========================================

CSV_FILE = "bodym_dataset_cleaned.csv"
BUCKET = "amazon-bodym"

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(CSV_FILE)

print("Dataset loaded!")
print("Total rows:", len(df))

# Get unique image paths
image_paths = df["image_path"].dropna().unique()[:200]

print("Unique images:", len(image_paths))

# ==========================================
# DOWNLOAD IMAGES
# ==========================================

downloaded = 0
skipped = 0
failed = 0

for i, image_path in enumerate(image_paths, start=1):

    # Local path
    local_path = image_path.replace("/", os.sep)

    # Create folder if needed
    folder = os.path.dirname(local_path)

    if folder:
        os.makedirs(folder, exist_ok=True)

    # Skip if already downloaded
    if os.path.exists(local_path):
        skipped += 1
        print(f"[{i}/{len(image_paths)}] Already exists: {local_path}")
        continue

    # AWS S3 path
    s3_path = f"s3://{BUCKET}/{image_path}"

    print(f"[{i}/{len(image_paths)}] Downloading: {image_path}")

    result = subprocess.run(
        [
            "aws",
            "s3",
            "cp",
            "--no-sign-request",
            s3_path,
            local_path
        ],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        downloaded += 1
    else:
        failed += 1
        print("FAILED:", image_path)
        print(result.stderr)

# ==========================================
# SUMMARY
# ==========================================

print("\n===== DOWNLOAD SUMMARY =====")
print("Total unique images:", len(image_paths))
print("Downloaded:", downloaded)
print("Already existed:", skipped)
print("Failed:", failed)
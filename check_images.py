import pandas as pd
import os

# Load dataset
df = pd.read_csv("bodym_dataset_cleaned.csv")

# Check first 10 image paths
print("===== IMAGE PATH CHECK =====")

for path in df["image_path"].head(10):
    exists = os.path.exists(path)
    print(f"{path} -> {exists}")
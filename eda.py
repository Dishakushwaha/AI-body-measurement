import pandas as pd

# Load cleaned BodyM dataset
df = pd.read_csv("bodym_dataset_cleaned.csv")

print("\n===== DATASET SHAPE =====")
print(df.shape)

print("\n===== COLUMNS =====")
print(df.columns.tolist())

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())

print("\n===== STATISTICAL SUMMARY =====")
print(df.describe())

import matplotlib.pyplot as plt
import seaborn as sns

# ===== HEIGHT DISTRIBUTION =====
plt.figure(figsize=(8, 5))
sns.histplot(df["height"], bins=30, kde=True)
plt.title("Height Distribution")
plt.xlabel("Height (cm)")
plt.ylabel("Number of Subjects")
plt.show()


# ===== CHEST DISTRIBUTION =====
plt.figure(figsize=(8, 5))
sns.histplot(df["chest"], bins=30, kde=True)
plt.title("Chest Measurement Distribution")
plt.xlabel("Chest (cm)")
plt.ylabel("Number of Subjects")
plt.show()
 

# ===== WAIST DISTRIBUTION =====
plt.figure(figsize=(8, 5))
sns.histplot(df["waist"], bins=30, kde=True)
plt.title("Waist Measurement Distribution")
plt.xlabel("Waist (cm)")
plt.ylabel("Number of Subjects")
plt.show()


# ===== CORRELATION HEATMAP =====
measurement_columns = [
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

plt.figure(figsize=(14, 10))
sns.heatmap(
    df[measurement_columns].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Body Measurement Correlation Heatmap")
plt.tight_layout()
plt.show()
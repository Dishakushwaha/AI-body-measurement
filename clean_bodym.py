import pandas as pd

# Load prepared dataset
df = pd.read_csv("bodym_dataset.csv")

print("Original shape:", df.shape)

# -------------------------------
# 1. Remove completely empty rows
# -------------------------------
df = df.dropna(how="all")

# -------------------------------
# 2. Remove duplicate rows
# -------------------------------
duplicates = df.duplicated().sum()
print("Duplicate rows found:", duplicates)

df = df.drop_duplicates()

# -------------------------------
# 3. Check missing values
# -------------------------------
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# -------------------------------
# 4. Convert measurement columns to numeric
# -------------------------------
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
    

for column in measurement_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

# -------------------------------
# 5. Remove rows with missing
#    target measurements
# -------------------------------
existing_measurements = [
    col for col in measurement_columns
    if col in df.columns
]

df = df.dropna(subset=existing_measurements)

# -------------------------------
# 6. Reset index
# -------------------------------
df = df.reset_index(drop=True)

# -------------------------------
# 7. Save cleaned dataset
# -------------------------------
df.to_csv("bodym_dataset_cleaned.csv", index=False)

print("\nCleaning completed!")
print("Cleaned shape:", df.shape)

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nCleaned dataset saved as:")
print("bodym_dataset_cleaned.csv")
# -------------------------------
# 9. Round measurements
# -------------------------------
df[measurement_columns] = df[measurement_columns].round(2)

# -------------------------------
# 10. Save final transformed dataset
# -------------------------------
df.to_csv("bodym_dataset_final.csv", index=False)

print("\nFinal transformed dataset saved as:")
print("bodym_dataset_final.csv")

print("Final shape:", df.shape)
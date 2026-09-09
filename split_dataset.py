import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

# Load feature dataset
df = pd.read_csv("bodym_image_features.csv")

# First split: 80% training, 20% temporary
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_idx, temp_idx = next(
    splitter.split(df, groups=df["subject_id"])
)

train_df = df.iloc[train_idx]
temp_df = df.iloc[temp_idx]

# Second split: temporary data into validation and test
splitter2 = GroupShuffleSplit(
    n_splits=1,
    test_size=0.50,
    random_state=42
)

val_idx, test_idx = next(
    splitter2.split(temp_df, groups=temp_df["subject_id"])
)

val_df = temp_df.iloc[val_idx]
test_df = temp_df.iloc[test_idx]

# Save datasets
train_df.to_csv("train_features.csv", index=False)
val_df.to_csv("validation_features.csv", index=False)
test_df.to_csv("test_features.csv", index=False)

print("===== DATASET SPLIT COMPLETE =====")

print("Training rows:", len(train_df))
print("Validation rows:", len(val_df))
print("Testing rows:", len(test_df))

print("\nUnique subjects:")
print("Training:", train_df["subject_id"].nunique())
print("Validation:", val_df["subject_id"].nunique())
print("Testing:", test_df["subject_id"].nunique())

print("\nSubject overlap check:")
print(
    "Train ∩ Validation:",
    len(set(train_df["subject_id"]) & set(val_df["subject_id"]))
)

print(
    "Train ∩ Test:",
    len(set(train_df["subject_id"]) & set(test_df["subject_id"]))
)

print(
    "Validation ∩ Test:",
    len(set(val_df["subject_id"]) & set(test_df["subject_id"]))
)
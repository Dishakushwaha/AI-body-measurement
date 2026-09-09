import pandas as pd

# ==========================================
# LOAD TEST DATA
# ==========================================

test = pd.read_csv("test_features.csv")

print("\n==========================================")
print("          TEST SUBJECT CHECK")
print("==========================================")

# ==========================================
# BASIC INFORMATION
# ==========================================

print("\nTotal test rows:", len(test))

print("Total unique subjects:", test["subject_id"].nunique())

print("Total unique images:", test["photo_id"].nunique())

# ==========================================
# SUBJECT IMAGE COUNTS
# ==========================================

print("\n==========================================")
print("       IMAGES PER SUBJECT")
print("==========================================\n")

subject_counts = test.groupby("subject_id")["photo_id"].nunique()

print(subject_counts)

# ==========================================
# CHECK FOR SUBJECT DUPLICATES
# ==========================================

print("\n==========================================")
print("       SUBJECT DUPLICATE CHECK")
print("==========================================\n")

duplicates = subject_counts[subject_counts > 1]

if len(duplicates) == 0:
    print("No subject has multiple test images.")
else:
    print("Subjects with multiple test images:")
    print(duplicates)

# ==========================================
# TEST SUBJECT DETAILS
# ==========================================

print("\n==========================================")
print("          TEST SUBJECT DETAILS")
print("==========================================\n")

columns_to_show = [
    "subject_id",
    "photo_id",
    "image_path",
    "height",
    "chest",
    "waist",
    "hip",
    "shoulder-breadth",
    "leg-length"
]

available_columns = [
    col for col in columns_to_show
    if col in test.columns
]

print(
    test[available_columns].to_string(index=False)
)

# ==========================================
# CHECK DUPLICATE ROWS
# ==========================================

print("\n==========================================")
print("          DUPLICATE ROW CHECK")
print("==========================================\n")

print(
    "Duplicate rows:",
    test.duplicated().sum()
)

# ==========================================
# CHECK SAME SUBJECT IN TEST
# ==========================================

print("\n==========================================")
print("       SUBJECT LIST IN TEST SET")
print("==========================================\n")

for subject in test["subject_id"].unique():
    print(subject)

# ==========================================
# FINISHED
# ==========================================

print("\n==========================================")
print("             CHECK COMPLETE")
print("==========================================")

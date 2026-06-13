import pandas as pd
from sklearn.model_selection import train_test_split
import os

# =====================================
# LOAD DATASET
# =====================================

print("\nLoading Dataset...\n")

df = pd.read_csv("data/phishing_email.csv")

print("Dataset Shape:", df.shape)
print(df.head())

# =====================================
# BASIC CLEANING
# =====================================

df = df.dropna()

df["text_combined"] = df["text_combined"].astype(str)

print("\nAfter Cleaning:", df.shape)

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    df["text_combined"],
    df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

# =====================================
# SAVE SPLITS
# =====================================

os.makedirs("data/processed", exist_ok=True)

pd.DataFrame({
    "text": X_train,
    "label": y_train
}).to_csv("data/processed/train.csv", index=False)

pd.DataFrame({
    "text": X_test,
    "label": y_test
}).to_csv("data/processed/test.csv", index=False)

print("\nFiles Saved Successfully")

print("Train Size:", len(X_train))
print("Test Size:", len(X_test))
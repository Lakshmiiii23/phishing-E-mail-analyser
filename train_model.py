import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report
)

# =====================================
# LOAD DATA
# =====================================

train_df = pd.read_csv("data/processed/train.csv")
test_df = pd.read_csv("data/processed/test.csv")

# =====================================
# TF-IDF
# =====================================

vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words="english"
)

X_train = vectorizer.fit_transform(train_df["text"])

X_test = vectorizer.transform(test_df["text"])

# =====================================
# MODEL
# =====================================

model = LogisticRegression(
    max_iter=1000
)

model.fit(X_train, train_df["label"])

# =====================================
# EVALUATION
# =====================================

preds = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(test_df["label"], preds))

print("\nClassification Report:")
print(
    classification_report(
        test_df["label"],
        preds
    )
)

# =====================================
# SAVE
# =====================================

joblib.dump(
    model,
    "models/phishing_model.pkl"
)

joblib.dump(
    vectorizer,
    "models/vectorizer.pkl"
)

print("\nModel Saved")
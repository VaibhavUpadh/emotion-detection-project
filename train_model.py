import pandas as pd
import re
import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv(
    "dataset/train.txt",
    sep=";",
    names=["text", "emotion"]
)

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# -------------------------
# Clean Text
# -------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

df["clean_text"] = df["text"].apply(clean_text)

# -------------------------
# TF-IDF
# -------------------------
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(df["clean_text"])

y = df["emotion"]

# -------------------------
# Split Data
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -------------------------
# Train Model
# -------------------------
model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

# -------------------------
# Evaluate Model
# -------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -------------------------
# Save Model
# -------------------------
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\nModel saved successfully!")
print("Vectorizer saved successfully!")
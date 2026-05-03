import pandas as pd
import pickle
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# -----------------------------
# Load dataset
# -----------------------------
DATA_PATH = "dataset/resumes.csv"

if not os.path.exists(DATA_PATH):
    print("❌ Dataset not found:", DATA_PATH)
    exit()

data = pd.read_csv(DATA_PATH)

# -----------------------------
# Data Cleaning
# -----------------------------
data = data.dropna(subset=["Resume", "Category"])

X = data["Resume"]
y = data["Category"]

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Vectorization
# -----------------------------
vectorizer = TfidfVectorizer(stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -----------------------------
# Model Training
# -----------------------------
model = LinearSVC()
model.fit(X_train_vec, y_train)

# -----------------------------
# Evaluation
# -----------------------------
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")

# -----------------------------
# Save Model
# -----------------------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model and vectorizer saved successfully")

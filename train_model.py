import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# Load dataset
data = pd.read_csv("dataset/resumes.csv")

X = data["Resume"]
y = data["Category"]

# Convert text to numbers
vectorizer = TfidfVectorizer(stop_words="english")
X_vec = vectorizer.fit_transform(X)

# Train model
model = LinearSVC()
model.fit(X_vec, y)

# Save files
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("DONE")

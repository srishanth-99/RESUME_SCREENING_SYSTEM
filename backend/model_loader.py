import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_role(text):
    data = vectorizer.transform([text])
    return model.predict(data)[0]

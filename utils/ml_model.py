from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()

def compute_similarity(resume_text, job_text):

    docs = [resume_text, job_text]
    tfidf = vectorizer.fit_transform(docs)

    score = cosine_similarity(tfidf[0], tfidf[1])[0][0]

    return round(score * 100, 2)

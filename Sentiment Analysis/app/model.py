import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from typing import Tuple
from app.preprocessing import TextPreprocessor

class SentimentModel:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression()

    def train(self, texts: list, labels: list) -> None:
        processed_texts = [self.preprocessor.clean_text(text) for text in texts]
        X = self.vectorizer.fit_transform(processed_texts)
        print(X)
        self.model.fit(X, labels)

    def predict(self, text: str) -> Tuple[str, float]:
        processed_text = self.preprocessor.clean_text(text)
        X = self.vectorizer.transform([processed_text])
        prediction = self.model.predict(X)[0]
        confidence = max(self.model.predict_proba(X)[0])
        return prediction, confidence

    def save(self, path: str) -> None:
        joblib.dump((self.vectorizer, self.model), path)

    def load(self, path: str) -> None:
        self.vectorizer, self.model = joblib.load(path)

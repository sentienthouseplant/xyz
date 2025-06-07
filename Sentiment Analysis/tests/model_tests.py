import pytest
from app.model import SentimentModel
from app.preprocessing import TextPreprocessor

def test_preprocessing():
    preprocessor = TextPreprocessor()
    text = "Hello, --World!!!"
    processed = preprocessor.clean_text(text)
    assert processed == "hello world"

def test_model_prediction():
    model = SentimentModel()
    # Test with dummy data
    texts = ["great very cool product", "absolutely massively terrible service"]
    labels = ["positive", "negative"]
    model.train(texts, labels)

    prediction, confidence = model.predict("amazing product")
    assert isinstance(prediction, str)
    assert isinstance(confidence, float)
    assert 0 <= confidence <= 1

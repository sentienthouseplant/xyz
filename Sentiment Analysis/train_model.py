# train_model.py
import pandas as pd
from app.model import SentimentModel

def train_and_save_model():

    df = pd.read_csv('train.csv', header=None, names=['label', 'text'])

    print(df.head())

    # Convert numeric labels to text labels
    label_map = {
        1: 'negative',
        2: 'positive'
    }
    df['label'] = df['label'].map(label_map)

    model = SentimentModel()

    model.train(
        texts=df['text'].tolist(),
        labels=df['label'].tolist()
        # Now contains 'positive' and 'negative'
    )

    # Save the model
    model.save("models/sentiment_model.pkl")

    # Optional: Test the model
    test_text = "This is amazing!"
    prediction, confidence = model.predict(test_text)
    print(f"Test prediction: {prediction}")
    print(f"Confidence: {confidence:.2f}")

if __name__ == "__main__":
    train_and_save_model()

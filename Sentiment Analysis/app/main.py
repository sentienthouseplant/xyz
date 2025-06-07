from fastapi import FastAPI, HTTPException
from .schemas import TextInput, SentimentResponse
from .model import SentimentModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sentiment Analysis API")
model = SentimentModel()

@app.on_event("startup")
async def startup_event():
    try:
        model.load("models/sentiment_model.pkl")
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise RuntimeError("Failed to load model")

@app.post("/predict", response_model=SentimentResponse)
async def predict_sentiment(input_data: TextInput):
    try:
        sentiment, confidence = model.predict(input_data.text)
        return SentimentResponse(
            text=input_data.text,
            sentiment=sentiment,
            confidence=float(confidence)
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

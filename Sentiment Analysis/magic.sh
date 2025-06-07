#!/bin/bash
set -e

# Check if model exists, if not, train it
if [ ! -f "models/sentiment_model.pkl" ]; then
    echo "Model not found. Training new model..."
    python train_model.py
fi

# Start the API server
uvicorn app.main:app --host 0.0.0.0 --port 8000

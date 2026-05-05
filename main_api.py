from fastapi import FastAPI
from model_logic import predict_for_location_zone
import pandas as pd

app = FastAPI()

@app.get("/")
def home():
    return {"message": "EcoTrack Waste Prediction API is running!"}

@app.get("/predict/")
def predict(start_date: str, location: str, zone: str):
    results = predict_for_location_zone(start_date, location, zone)
    if results.empty:
        return {"message": "No predictions found for this input."}
    return results.to_dict(orient="records")

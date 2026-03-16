from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["lecridusoir"]

@app.get("/")
def home():
    return {"status": "Le Cri du Soir API running"}

@app.post("/prayers")
def create_prayer(prayer: dict):
    db.prayers.insert_one(prayer)
    return {"message": "Prayer added"}




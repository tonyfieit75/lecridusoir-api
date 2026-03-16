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

@app.get("/prayers")
def get_prayers():
    prayers = list(db.prayers.find({}, {"_id": 0}))
    return prayers




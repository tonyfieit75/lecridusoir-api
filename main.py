from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27017")
db = client["lecridusoir"]

@app.get("/")
def home():
    return {"status": "Le Cri du Soir API running"}

@app.get("/prayers")
def get_prayers():
    prayers = list(db.prayers.find({}, {"_id": 0}))
    return prayers

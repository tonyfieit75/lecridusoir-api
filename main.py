from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(title="Le Cri du Soir API")

# -----------------------------
# CORS (required for Flutter Web)
# -----------------------------

origins = [
    "https://app.lecridusoir.com",
    "http://localhost:3000",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# MongoDB Connection
# -----------------------------

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

db = client["lecridusoir"]

prayer_collection = db["prayers"]

# -----------------------------
# Prayer Model
# -----------------------------

class Prayer(BaseModel):
    name: str
    phone: str
    message: str

# -----------------------------
# Root API
# -----------------------------

@app.get("/")
def home():
    return {"status": "Le Cri du Soir API running"}

# -----------------------------
# Create Prayer Request
# -----------------------------

@app.post("/prayers")
def create_prayer(prayer: Prayer):

    prayer_data = prayer.dict()

    prayer_data["count"] = 0

    prayer_data["date"] = datetime.now().strftime("%Y-%m-%d")

    prayer_collection.insert_one(prayer_data)

    return {"message": "Prayer added"}

# -----------------------------
# Get Prayer Wall
# -----------------------------

@app.get("/prayers")
def get_prayers():

    prayers = list(
        prayer_collection.find({}, {"_id": 0})
    )

    return prayers

# -----------------------------
# Pray for Someone
# -----------------------------

@app.post("/pray/{name}")
def pray_for_request(name: str):

    prayer_collection.update_one(
        {"name": name},
        {"$inc": {"count": 1}}
    )

    return {"message": "Prayer count updated"}



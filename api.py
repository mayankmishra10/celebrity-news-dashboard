from fastapi import FastAPI
import json
from collections import Counter

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_data():
    with open("data/final.json") as f:
        return json.load(f)

@app.get("/")
def home():
    return {"message": "API running 🚀"}

# 👉 Get all data
@app.get("/data")
def get_data():
    return load_data()

# 👉 Get trending celebrities
@app.get("/trending")
def get_trending():
    data = load_data()
    counts = Counter([d["celebrity"] for d in data])
    return counts.most_common(5)

# 👉 Filter by celebrity
@app.get("/celebrity/{name}")
def get_by_celebrity(name: str):
    data = load_data()
    return [d for d in data if name.lower() in d["celebrity"].lower()]
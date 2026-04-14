from fastapi import FastAPI, HTTPException
import json
from collections import Counter
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler('logs/app.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_data():
    try:
        with open("data/processed/final.json") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise HTTPException(status_code=500, detail="Failed to load data.")

@app.get("/")
def home():
    logger.info("Home endpoint called.")
    return {"message": "API running 🚀"}

# 👉 Get all data
@app.get("/data")
def get_data():
    logger.info("/data endpoint called.")
    return load_data()

# 👉 Get trending celebrities
@app.get("/trending")
def get_trending():
    logger.info("/trending endpoint called.")
    data = load_data()
    counts = Counter([d["celebrity"] for d in data])
    return counts.most_common(5)

# 👉 Filter by celebrity
@app.get("/celebrity/{name}")
def get_by_celebrity(name: str):
    logger.info(f"/celebrity/{name} endpoint called.")
    data = load_data()
    return [d for d in data if name.lower() in d["celebrity"].lower()]
import json
import os
import asyncio
import logging
from crawler.crawl import run_crawler
from processing.clean import clean_data
from processing.deduplicate import remove_duplicates
from processing.processor import process_batch
from utils.config import URLS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler('logs/app.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

os.makedirs("data", exist_ok=True)

async def main():
    logger.info("🚀 Starting pipeline...")
    try:
        # STEP 1: Crawl
        raw_data = await run_crawler(URLS)
        logger.info(f"📰 Crawled Articles: {len(raw_data)}")
        with open("data/raw/raw.json", "w") as f:
            json.dump(raw_data, f, indent=2)
        logger.info("💾 Raw data saved → raw.json")
        # STEP 2: Clean
        cleaned = clean_data(raw_data)
        logger.info(f"🧹 After Cleaning: {len(cleaned)}")
        # STEP 3: Deduplicate
        unique = remove_duplicates(cleaned)
        logger.info(f"🔁 After Deduplication: {len(unique)}")
        # STEP 4: NLP Processing
        texts = [item["content"] for item in unique]
        final_output = process_batch(texts)
        # Save final
        with open("data/processed/final.json", "w") as f:
            json.dump(final_output, f, indent=2)
        logger.info("💾 Final data saved → final.json")
        logger.info("🎯 Pipeline completed successfully!")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
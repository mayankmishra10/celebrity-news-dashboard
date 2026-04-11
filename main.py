import json
import os
import asyncio
from crawl import run_crawler
from clean import clean_data
from deduplicate import remove_duplicates
from processor import process_batch
from config import URLS

os.makedirs("data", exist_ok=True)

async def main():

    print("🚀 Starting pipeline...\n")

    # STEP 1: Crawl
    raw_data = await run_crawler(URLS)

    print(f"📰 Crawled Articles: {len(raw_data)}")


    with open("data/raw.json", "w") as f:
        json.dump(raw_data, f, indent=2)

    print("\n💾 Raw data saved → raw.json")

    # STEP 2: Clean
    cleaned = clean_data(raw_data)
    print(f"\n🧹 After Cleaning: {len(cleaned)}")

    # STEP 3: Deduplicate
    unique = remove_duplicates(cleaned)
    print(f"🔁 After Deduplication: {len(unique)}")

    # STEP 4: NLP Processing
    texts = [item["content"] for item in unique]
    final_output = process_batch(texts)

  



    # Save final
    with open("data/final.json", "w") as f:
        json.dump(final_output, f, indent=2)

    print("\n💾 Final data saved → final.json")

    print("\n🎯 Pipeline completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
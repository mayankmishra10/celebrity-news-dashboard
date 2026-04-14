import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler('logs/app.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def clean_data(data):
    cleaned = []
    for idx, item in enumerate(data):
        try:
            if item["title"] and item["content"]:
                cleaned.append({
                    "title": item["title"].strip(),
                    "content": item["content"].strip()
                })
            else:
                logger.warning(f"Skipping item at index {idx} due to missing title/content.")
        except Exception as e:
            logger.error(f"Error cleaning item at index {idx}: {e}")
    logger.info(f"Cleaned {len(cleaned)} items out of {len(data)}.")
    return cleaned
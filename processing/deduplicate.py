import hashlib
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler('logs/app.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def remove_duplicates(data):
    seen = set()
    unique = []
    for idx, item in enumerate(data):
        try:
            key = (item["title"] + item["content"]).encode("utf-8")
            h = hashlib.md5(key).hexdigest()
            if h not in seen:
                seen.add(h)
                unique.append(item)
            else:
                logger.info(f"Duplicate found at index {idx}, skipping.")
        except Exception as e:
            logger.error(f"Error deduplicating item at index {idx}: {e}")
    logger.info(f"Removed duplicates. {len(unique)} unique items out of {len(data)}.")
    return unique
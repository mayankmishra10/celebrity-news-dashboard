import spacy
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler('logs/app.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

nlp = spacy.load("en_core_web_sm")

def get_full_phrase(token):
    return " ".join([t.text for t in token.subtree])

def extract_relation(doc):
    results = []

    for sent in doc.sents:
        person = None
        obj = None

        for token in sent:
            if token.dep_ in ("nsubj", "nsubjpass") and token.ent_type_ == "PERSON":
                person = get_full_phrase(token)

            if token.dep_ in ("dobj", "pobj", "attr"):
                obj = get_full_phrase(token)

        if person and obj:
            results.append({
                "celebrity": person,
                "reason": obj
            })

    return results


def process_batch(texts):
    final = []
    logger.info(f"Processing {len(texts)} texts with spaCy NER/Dependency parser...")
    try:
        docs = nlp.pipe(texts, batch_size=20)

        for doc in docs:
            try:
                final.extend(extract_relation(doc))
            except Exception as e:
                logger.error(f"Error extracting relations from doc: {e}")
    except Exception as e:
        logger.error(f"spaCy batch processing failed: {e}")
    logger.info(f"Finished processing. Extracted {len(final)} relations.")

    return final
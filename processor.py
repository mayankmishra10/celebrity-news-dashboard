import spacy

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

    docs = nlp.pipe(texts, batch_size=20)

    for doc in docs:
        final.extend(extract_relation(doc))

    return final
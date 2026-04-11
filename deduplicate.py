import hashlib

def remove_duplicates(data):
    seen = set()
    unique = []

    for item in data:
        key = (item["title"] + item["content"]).encode("utf-8")
        h = hashlib.md5(key).hexdigest()

        if h not in seen:
            seen.add(h)
            unique.append(item)

    return unique
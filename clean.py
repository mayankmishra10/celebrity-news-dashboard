def clean_data(data):
    cleaned = []

    for item in data:
        if item["title"] and item["content"]:
            cleaned.append({
                "title": item["title"].strip(),
                "content": item["content"].strip()
            })

    return cleaned
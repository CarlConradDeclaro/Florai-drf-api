
def is_recommendation_query(question:str) -> bool:
    keywords = [
        "which plant", "what plants", "plants that", "recommend", "suggest", "best plant for",
        "good for", "grow in", "live in", "survive", "need", "thrives in", "type of plant",
        "can i grow", "ideal for", "i want a plant", "looking for", "would be good",
        "what kind of plant", "what would grow", "any plant that", "plants suitable for",
        "suitable for", "appropriate for", "good choice for", "i need a plant",
        "what should i plant", "great for", "works well in", "perfect for", "plant for",
        "fit for", "plants compatible with", "plant options for", "choices for","provide"
    ]
    question = question.lower()

    return any(kw in question for kw in keywords)

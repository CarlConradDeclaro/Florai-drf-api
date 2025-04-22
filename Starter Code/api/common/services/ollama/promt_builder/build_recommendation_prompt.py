
def recommendation_prompt(prompt,top_plants):
    plant_lines = "\n".join([f"{i+1}. **{p['common_name']}** – {p['description']}" for i, p in enumerate(top_plants)])
    context = "\n".join([f"{p['common_name']}: {p['description']}: {p['url']}" for p in top_plants])

    return f"""

    You are a professional plant expert AI assistant. A user askedL "{prompt}"

    Start are with a friendly and informative introduction

    Here are the top relevant plants based on the user's interest:
    {plant_lines}

    Relevant Context:
    {context}

    Respond in this format:
    Introduction
    
    I want you to display the Context in json format 
    display the common_name and description and the url



    Closing summary

    """
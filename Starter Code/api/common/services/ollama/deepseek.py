
import requests
from api.models import Plant
from api.serializers import PlantSerializer
from api.common.services.embeddings import semantic_search
from api.common.utils.recommendation_query import is_recommendation_query
from api.common.services.ollama.promt_builder.build_recommendation_prompt import recommendation_prompt
from api.common.services.ollama.promt_builder.build_general_prompt import general_prompt
from api.common.services.ollama.streamer.stream_openrouter import openrouter_response
from api.common.services.ollama.streamer.stream_local import local_response

# openRouter Ai model
def stream_openRouter_deepseek2(prompt: str, model="deepseek/deepseek-chat-v3-0324:free"):

    is_recommend = is_recommendation_query(prompt)
    plants = Plant.objects.all()
    serializer = PlantSerializer(plants, many=True)
    plant_data = serializer.data

    if is_recommend:
        plant_descriptions = [p['description'] for p in plant_data]
        relevant_plants_indices, _ = semantic_search(prompt, plant_descriptions, top_k=5)
        top_plants = [plant_data[i] for i in relevant_plants_indices]
        full_prompt = recommendation_prompt(prompt,top_plants)
    else:
        full_prompt =  general_prompt(prompt)

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",  # Replace with your frontend URL if needed
        "X-Title": "PlantQuest"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": full_prompt}],
        "stream": True
    }
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        stream=True
    )
    return  openrouter_response(response)

# this is for local ai models
def stream_ollama_deepseek(prompt: str, model="deepseek-r1:8b"):
    
    full_prompt = general_prompt(prompt)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": full_prompt,
            "stream": True
        },
        stream=True
    )
    return local_response(response)
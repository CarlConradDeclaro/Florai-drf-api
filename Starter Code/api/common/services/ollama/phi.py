import requests
from api.models import Plant
from api.serializers import PlantSerializer
from api.common.services.embeddings import semantic_search
from api.common.utils.recommendation_query import is_recommendation_query
from api.common.services.ollama.promt_builder.build_recommendation_prompt import recommendation_prompt
from api.common.services.ollama.promt_builder.build_general_prompt import general_prompt
from api.common.services.ollama.streamer.stream_local import local_response

def stream_ollama_phi(prompt: str, model="phi"):

    is_recommend = is_recommendation_query(prompt)
    plants = Plant.objects.all()
    serializer = PlantSerializer(plants, many=True)
    plant_data = serializer.data

    if is_recommend:
        plant_descriptions = [p['description'] for p in plant_data]
        relevant_plants_indices, _ = semantic_search(prompt, plant_descriptions, top_k=3)
        top_plants = [plant_data[i] for i in relevant_plants_indices]
        full_prompt = recommendation_prompt(prompt,top_plants)
    else:
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
  
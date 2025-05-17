
import requests
import re
from api.models import Plant
from api.serializers import PlantSerializer
from api.common.services.embeddings import semantic_search
from api.common.utils.recommendation_query import is_recommendation_query
from api.common.services.ollama.promt_builder.build_recommendation_prompt import recommendation_prompt,recommendation_prompt_for_json,predicted_image_response_details
from api.common.services.ollama.promt_builder.build_general_prompt import general_prompt
from api.common.services.ollama.streamer.stream_openrouter import openrouter_response
from api.common.services.ollama.streamer.stream_local import local_response
from api.common.utils.text_formater import strip_surrounding_stars
from django.db.models.expressions import result
 
# free apikey might expired soon haha
API_KEY = "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" 

def image_classification_response(prompt:str,model="deepseek/deepseek-chat-v3-0324:free"):

    full_prompt = predicted_image_response_details(prompt)
 
    headers ={
        "Authorization": "Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",  # Replace with your frontend URL if needed
        "X-Title": "PlantQuest"
    }

    payload = {
        "model":model,
        "messages": [{"role": "user", "content": full_prompt}],
        "stream":False
    }

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return {"error": f"OpenRouter returned {response.status_code}", "details": response.text}

def get_openRouter_deepseek_responsetoJSON(prompt: str, conversation ,model="deepseek/deepseek-chat-v3-0324:free"):
    is_recommend = is_recommendation_query(prompt)
    print(f"Is recommendation query: {is_recommend}")
   


    plants = Plant.objects.all()
    serializer = PlantSerializer(plants, many=True)
    plant_data = serializer.data
    relevant_plants_indices = []

    if is_recommend:
        try:
            plant_descriptions = [p['description'] for p in plant_data]
            relevant_plants_indices, _ = semantic_search(prompt, plant_descriptions, top_k=5)

            if hasattr(relevant_plants_indices, 'tolist'):
                relevant_plants_indices = relevant_plants_indices.tolist()
            if not isinstance(relevant_plants_indices, list):
                relevant_plants_indices = list(relevant_plants_indices)

            top_plants = [plant_data[i] for i in relevant_plants_indices]
            full_prompt = recommendation_prompt_for_json(prompt, top_plants,conversation)

        except Exception as e:
            print(f"Error in recommendation processing: {str(e)}")
            full_prompt = general_prompt(prompt,conversation)
            relevant_plants_indices = []
    else:
        full_prompt = general_prompt(prompt,conversation)

    headers = {
        "Authorization": "Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "PlantQuest"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": full_prompt}],
        "stream": False
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        response_data = response.json()
        ai_response = response_data['choices'][0]['message']['content']

        # Initialize introduction and summary
        introduction = ""
        summary = ""

        if is_recommend and ai_response:
            intro_match = re.search(r"(?i)INTRODUCTION:.*?(?=SUMMARY:|$)", ai_response, re.DOTALL)
            summary_match = re.search(r"(?i)SUMMARY:.*", ai_response, re.DOTALL)

            if intro_match:
                intro_text = intro_match.group().split("INTRODUCTION:")[-1].strip()
                intro_lines = [line.strip() for line in intro_text.split('\n') if line.strip()]
                introduction = " ".join([line for line in intro_lines if not re.match(r"^\d+\.\s", line)])
                introduction = strip_surrounding_stars(introduction)

            if summary_match:
                summary = summary_match.group().split("SUMMARY:")[-1].strip()
                summary = strip_surrounding_stars(summary)

            result = {
                "introduction": introduction,
                "relevant_plants": [plant_data[i] for i in relevant_plants_indices] if relevant_plants_indices else [],
                "summary": summary,

            }
        else:
            result = {
                "introduction": ai_response,
                "relevant_plants" :[],
                "summary": ""
            }
        return result

    except requests.exceptions.RequestException as e:
        print(f"API request error: {str(e)}")
        return {
            "error": f"API request failed: {str(e)}",
            "details": str(e)
        }
    except Exception as e:
        print(f"General error: {str(e)}")
        return {
            "error": f"Error processing request: {str(e)}",
            "details": str(e)
        }

# openRouter Ai model
def stream_openRouter_deepseek(prompt: str,conversation, model="deepseek/deepseek-chat-v3-0324:free"):

    is_recommend = is_recommendation_query(prompt)
    print(f"Is recommendation query: {is_recommend}")
    plants = Plant.objects.all()
    serializer = PlantSerializer(plants, many=True)
    plant_data = serializer.data

    if is_recommend:
        plant_descriptions = [p['description'] for p in plant_data]
        relevant_plants_indices, _ = semantic_search(prompt, plant_descriptions, top_k=5)
        top_plants = [plant_data[i] for i in relevant_plants_indices]
        full_prompt = recommendation_prompt(prompt,top_plants,conversation)
    else:
        full_prompt =  general_prompt(prompt,conversation)

    headers = {
        "Authorization": "Bearer {API_KEY}",
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



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
# 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
#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
#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

#wanda
#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


def image_classification_response(prompt:str,model="deepseek/deepseek-chat-v3-0324:free"):

    full_prompt = predicted_image_response_details(prompt)
#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
#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
# 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

    headers ={
        "Authorization": "Bearer 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",
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

def get_openRouter_deepseek2_json(prompt: str, conversation ,model="deepseek/deepseek-chat-v3-0324:free"):
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
        "Authorization": "Bearer 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",
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
def stream_openRouter_deepseek2(prompt: str,conversation, model="deepseek/deepseek-chat-v3-0324:free"):

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
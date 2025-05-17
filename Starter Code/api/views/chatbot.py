from rest_framework.decorators import api_view
from django.http import StreamingHttpResponse
from api.common.services.ollama.deepseek import  stream_openRouter_deepseek,get_openRouter_deepseek_responsetoJSON
from rest_framework.response import Response


@api_view(["POST"])
def chatbot_flor(request):
    data  = request.data
    conversation  = data.get("conversation",[])
    user_prompt = data.get("new_message","")
    json_response = get_openRouter_deepseek_responsetoJSON(user_prompt,conversation)
    return Response(json_response)

 
@api_view(["POST"])
def chatbot_flor2(request):
    data = request.data
    user_prompt = data.get("new_message", "")
    conversation = data.get("conversation", [])
    stream = stream_openRouter_deepseek(user_prompt,conversation)

    return StreamingHttpResponse(
        stream,
        content_type="text/plain"
    )


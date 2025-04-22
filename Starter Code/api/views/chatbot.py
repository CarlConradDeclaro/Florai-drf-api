from rest_framework.decorators import api_view, permission_classes
from api.common.services.ollama.mistral import stream_ollama_mistral
from django.http import StreamingHttpResponse
from api.common.services.ollama.phi import stream_ollama_phi
from api.common.services.ollama.deepseek import stream_ollama_deepseek, stream_openRouter_deepseek2


@api_view(["GET"])
def mistral(request):
    user_prompt = request.GET.get("q", "")

    stream = stream_ollama_mistral(user_prompt)

    return StreamingHttpResponse(
        stream,
        content_type="text/plain"
    )

@api_view(["GET"])
def phi(request):
    user_prompt = request.GET.get("q", "")

    stream = stream_ollama_phi(user_prompt)

    return StreamingHttpResponse(
        stream,
        content_type="text/plain"
    )

@api_view(["GET"])
def deepseek(request):
    user_prompt = request.GET.get("q", "")

    stream = stream_ollama_deepseek(user_prompt)

    return StreamingHttpResponse(
        stream,
        content_type="text/plain"
    )

@api_view(["GET"])
def deepseek2(request):
    user_prompt = request.GET.get("q", "")

    stream = stream_openRouter_deepseek2(user_prompt)

    return StreamingHttpResponse(
        stream,
        content_type="text/plain"
    )
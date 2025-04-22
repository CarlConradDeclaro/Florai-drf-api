import json

def openrouter_response(response):
    for line in response.iter_lines():
        if line:
            try:
                decoded = line.decode("utf-8")
                if decoded.startswith("data: "):
                    content = decoded[6:]
                    if content != "[DONE]":
                        data = json.loads(content)
                        delta =data["choices"][0].get("delta",{})
                        yield delta.get("content","")
            except Exception as e:
                yield f"\n[Stream Error : {str(e)}]\n"
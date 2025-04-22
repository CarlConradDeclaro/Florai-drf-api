import json

def local_response(response):
    for line in response:
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    yield data["response"]
            except Exception as e:
                yield f"\n[Error : {str(e)}]\n"
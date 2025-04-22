# utils/convex.py
import requests
import json

def fetch_convex_data():
    url = "https://effervescent-tapir-13.convex.site/hello"  # ← fetch all the plants
    response = requests.get(url)

    print("Raw Response Text:", response.text)

    if response.status_code == 200:
        try:
            return response.json()  
        except ValueError:
            return json.loads(response.text)  
    else:
        raise Exception("Failed to fetch data from Convex. Status code: {}".format(response.status_code))

import requests

API_KEY = open("AIzaSyC3dH8x-HlX01S2ygbpgjQWLBhaIaTb794").read()
SEARCH_ENGINE_ID = open("81bcf0b9be0314be5").read()

search_query = "Gatos"

url = 'https://www.googleapis.com/customsearch/v1'
params = {
    'q': search_query,
    'key': API_KEY,
    'cx': SEARCH_ENGINE_ID
}

response = requests.get(url, params=params)
results = response.json()
print(results)
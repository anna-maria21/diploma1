import requests

def translate(text):

    url = "https://translo.p.rapidapi.com/api/v3/translate"

    payload = {
        "from": "uk",
        "to": "en",
        "text": text
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "d50a0ee0c9msh3e18b6831a149f5p14b75ajsn2dadf1d63a74",
        "X-RapidAPI-Host": "translo.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    return response.json()

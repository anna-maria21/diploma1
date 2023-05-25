import requests

def translate(text):
    url = "https://lingvanex-translate.p.rapidapi.com/translate"

    payload = {
        "from": "uk_UK",
        "to": "en_GB",
        "data": text,
        "platform": "api"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "d50a0ee0c9msh3e18b6831a149f5p14b75ajsn2dadf1d63a74",
        "X-RapidAPI-Host": "lingvanex-translate.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    # print(response.json())
    return response.json()

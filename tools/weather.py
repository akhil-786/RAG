import requests

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return f"The weather in {city} is {response.text}"

        return f"Weather API returned {response.status_code}"

    except Exception as e:
        return f"Weather tool failed: {str(e)}"
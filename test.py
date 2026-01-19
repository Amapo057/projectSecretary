import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=34.9505&longitude=127.4878&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_probability_max&timezone=Asia%2FTokyo&past_days=1&forecast_days=1"

try:
    # params 없이 URL만 넣어도 됩니다
    response = requests.get(url)
    data = response.json()
    print(data)
except:
    pass
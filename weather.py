import requests


def get_todayWeather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=34.947&longitude=127.534&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FTokyo&past_days=1&forecast_days=1"
    try:
        # timeout으로 대기시간 제한
        response = requests.get(url, timeout=5)
        # 404, 500등 오류 답변 받을시 오류 발생
        response.raise_for_status()
        return response.json()
    except:
        # 오류발생시 None리턴
        return None
    

if __name__ == "__main__":
    data = get_todayWeather()
    print(data)
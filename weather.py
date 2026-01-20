import requests

# 데이터 받기
def getWeather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=34.9505&longitude=127.4878&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_min,precipitation_probability_max,precipitation_sum&timezone=Asia%2FTokyo&past_days=1&forecast_days=1"
    try:
        # timeout으로 대기시간 제한
        response = requests.get(url, timeout=5)
        # 404, 500등 오류 답변 받을시 오류 발생
        response.raise_for_status()
        return parsingWeather(response.json())
    except:
        # 오류발생시 None리턴
        return None

# 데이터에서 원하는 파트만 파싱
def parsingWeather(weatherData):
    weatherSummary = {}
    weatherSummary['weather_code'] = weatherData['daily']['weather_code']
    weatherSummary['temperature_2m_max'] = weatherData['daily']['temperature_2m_max']
    weatherSummary['temperature_2m_min'] = weatherData['daily']['temperature_2m_min']
    weatherSummary['apparent_temperature_min'] = weatherData['daily']['apparent_temperature_min']
    if weatherData['daily']['precipitation_probability_max'][1] >= 20:
        weatherSummary['precipitation_probability_max'] = weatherData['daily']['precipitation_probability_max']
        if weatherData['daily']['precipitation_probability_max'][1] >= 50:
            weatherSummary['precipitation_sum'] = weatherData['daily']['precipitation_sum']
    # print(weatherSummary)
    return(weatherSummary)

if __name__ == "__main__":
    data = getWeather()
    print(data)

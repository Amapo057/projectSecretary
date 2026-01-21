import llm
import termux_api
import weather


# 파일 경로 설정
MNN_BUILD_PATH = "/data/data/com.termux/files/home/MNN/build"
MNN_DEMO = "./llm_demo"
MODEL_CONFIG = "/data/data/com.termux/files/home/MNN/model/config.json"

# 실행시 나오는 문자열을 보고 정지 여부 판단
WAIT_PROMPT = "User: " 

# 날씨 코드 딕셔너리
weather_code_map = {
    # 1. 맑음 & 구름 (0~3)
    0: "맑고 화창한 날씨",
    1: "대체로 맑은 날씨",
    2: "구름이 조금 낀 날씨",
    3: "흐린 날씨",
    # 2. 안개 (45, 48)
    45: "안개가 낀 날씨",
    48: "짙은 안개가 낀 날씨",
    # 3. 이슬비 (51~55)
    51: "가벼운 이슬비",
    53: "이슬비",
    55: "강한 이슬비",
    # 4. 비 (61~65)
    61: "약한 비",
    63: "비",
    65: "강한 비",
    # 5. 어는 비 (66, 67) - 겨울철 주의
    66: "살얼음이 끼는 비",
    67: "강한 살얼음 비",
    # 6. 눈 (71~77)
    71: "약한 눈",
    73: "눈",
    75: "강한 눈",
    77: "싸락눈",
    # 7. 소나기 (80~82)
    80: "약한 소나기",
    81: "소나기",
    82: "강한 소나기",
    # 8. 눈 소나기 (85, 86)
    85: "약한 눈 소나기",
    86: "강한 눈 소나기",
    # 9. 뇌우/악천후 (95~99)
    95: "천둥번개",
    96: "우박을 동반한 천둥번개",
    99: "강한 우박과 천둥번개"
}

def main():
    # 날씨 받아오기
    today_weather = weather.getWeather()
    weather_repoert = (
        f"오늘 날씨는 {weather_code_map[today_weather['weather_code'][1]]}입니다. "
        f"어제 체감 기온은 {today_weather['apparent_temperature_min'][0]}입니다. "
        f"오늘 최저기온은 {today_weather['temperature_2m_min'][1]}, 최고기온은 {today_weather['temperature_2m_max'][1]}, 체감기온은 {today_weather['apparent_temperature_min'][1]}입니다.")

    print(weather_repoert)
if __name__ == '__main__':
    main()
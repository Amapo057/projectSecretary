import llm
import termux_api
import weather


# 파일 경로 설정
MNN_BUILD_PATH = "/data/data/com.termux/files/home/MNN/build"
MNN_DEMO = "./llm_demo"
MODEL_CONFIG = "/data/data/com.termux/files/home/MNN/model/config.json"

# 실행시 나오는 문자열을 보고 정지 여부 판단
WAIT_PROMPT = "User: " 
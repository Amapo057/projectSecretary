import subprocess
import time
import os
import threading
import queue

# 파일 경로 설정
MNN_BUILD_PATH = "/data/data/com.termux/files/home/MNN/build"
MNN_DEMO = "./llm_demo"
MODEL_CONFIG = "/data/data/com.termux/files/home/MNN/model/config.json"

# 실행시 나오는 문자열을 보고 정지 여부 판단
WAIT_PROMPT = "User: " 

class LocalLLM:
    # 인자는 각 경로, 데모, 설정파일
    def __init__(self, cwd, exe, config):
        # llm_demo보고 프로그램 시작
        self.process = subprocess.Popen(
            # llm_demo, config.json 파일 넣기
            [exe, config],
            # 경로 잡음
            cwd=cwd,
            # 각각 입력, 출력, 에러 연결
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # 비트가 아닌 문자열로 대화
            text=True,
            bufsize=0  # 버퍼링 끄기 (실시간 입출력 위해 필수)
        )

        # 데이터 저장용 큐 생성
        self.output_queue = queue.Queue()
        # 작동여부 판단 변수
        self.running = True

        # 출력을 실시간으로 읽어오는 스레드 시작
        self.reader_thread = threading.Thread(target=self._read_output)
        self.reader_thread.daemon = True
        self.reader_thread.start()

        # 초기 로딩 대기 (모델 로드 완료 메시지까지 기다림)
        # print("loading...")
        self.wait_for_ready()

    # MNN의 출력을 한글자씩 받아들임
    # 스레드로 사용
    def _read_output(self):
        while self.running:
            # char로 먼저 읽어오고, 문자열이면 큐에 삽입
            char = self.process.stdout.read(1)
            if not char:
                break
            self.output_queue.put(char)

    # 입력 대기 프롬프트인 User: 가 나올 때 까지 대기
    def wait_for_ready(self):
        # 문자열 생성용 버퍼
        buffer = ""
        while True:
            # 문자열 저장용 큐가 비지 않았을 때
            if not self.output_queue.empty():
                char = self.output_queue.get()
                buffer += char
                # print(char, end="", flush=True)

                # 받은 문자열에 User:가 있는지 확인
                if buffer.endswith(WAIT_PROMPT):
                    return

            # 큐가 비었을 시 대기
            else:
                time.sleep(0.01)

    # 채팅 입력
    def chat(self, user_input):
        # 1. 입력 전송
        self.process.stdin.write(user_input + "\n")
        self.process.stdin.flush()

        # 2. 답변 수신
        response_text = ""
        buffer = ""
        start_time = time.time()

        # 문자열 끝부분 확인해 끝났다면 실제 답변과 분리
        while True:
            if not self.output_queue.empty():
                char = self.output_queue.get()
                buffer += char

                # 프롬프트가 나오면 답변이 끝난 것임
                if buffer.endswith(WAIT_PROMPT):
                    # 프롬프트 문자열을 제외한 부분이 실제 답변
                    response_text = buffer[:-len(WAIT_PROMPT)].strip()
                    break
            else:
                # 타임아웃 또는 대기
                time.sleep(0.01)
        # 답변이 저장된 response_text 반환
        return response_text


    # 프로그램 종료
    def close(self):
        # 작동 여부 변수 거짓
        self.running = False
        # 프로세스 종료
        self.process.terminate()

        # print("LLM 프로세스가 완전히 종료되었습니다.")

def main():

    # LLM 초기화

    llm = LocalLLM(cwd=MNN_BUILD_PATH, exe=MNN_DEMO, config=MODEL_CONFIG)

    

    try:

        while True:

            # 1. 음성 인식 (STT)

            # user_text = stt()

            

            # if not user_text:

                # print("입력이 감지되지 않았습니다. 다시 시도합니다.")

                # continue

                

            # if user_text.lower() in ["종료", "exit", "stop"]:

                # break



            # print(f"인식된 명령: {user_text}")



            # 2. LLM 추론 (Qwen3)

            # MNN이 C++ 바이너리라 프롬프트 템플릿을 직접 씌워야 할 수도 있음 (모델에 따라 다름)

            # Qwen은 보통 채팅 포맷이 필요 없거나 MNN 데모가 알아서 처리함.

            answer = llm.chat("좋은아침! 아침식사 메뉴 추천해줄 수 있어? 3줄 이내로 설명해줘")



            # 3. 음성 출력 (TTS)

            # 답변에서 불필요한 시스템 메시지가 있다면 여기서 .replace() 등으로 제거

            tts(answer)
            llm.close()
            break


    except KeyboardInterrupt:

        print("\n종료합니다.")

    finally:

        llm.close()



if __name__ == "__main__":

    main()



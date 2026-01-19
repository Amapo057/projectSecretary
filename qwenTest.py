import subprocess

import time

import os

import threading

import queue



# ==========================================

# 설정 (경로를 본인 환경에 맞게 수정하세요)

# ==========================================

MNN_BUILD_PATH = "/data/data/com.termux/files/home/MNN/build" # 예시 경로

MNN_DEMO_EXE = "./llm_demo" # 또는 ./cli_demo (실제 파일명 확인 필요)

MODEL_CONFIG = "/data/data/com.termux/files/home/MNN/model/config.json" # 모델 설정 파일 경로



# MNN CLI가 사용자 입력을 기다릴 때 띄우는 프롬프트 문자열 (매우 중요)

# 실행해보고 "> " 인지 "User: " 인지 확인 후 수정해야 합니다.

WAIT_PROMPT = "User: " 



class LocalLLM:

    def __init__(self, cwd, exe, config):

        self.process = subprocess.Popen(

            [exe, config],

            cwd=cwd,

            stdin=subprocess.PIPE,

            stdout=subprocess.PIPE,

            stderr=subprocess.PIPE,

            text=True,

            bufsize=0  # 버퍼링 끄기 (실시간 입출력 위해 필수)

        )

        self.output_queue = queue.Queue()

        self.running = True

        

        # 출력을 실시간으로 읽어오는 스레드 시작

        self.reader_thread = threading.Thread(target=self._read_output)

        self.reader_thread.daemon = True

        self.reader_thread.start()

        

        # 초기 로딩 대기 (모델 로드 완료 메시지까지 기다림)

        print("모델 로딩 중...")

        self.wait_for_ready()

        print("모델 로드 완료!")



    def _read_output(self):

        """서브프로세스의 출력을 한 글자씩 읽어서 큐에 담음"""

        while self.running:

            char = self.process.stdout.read(1)

            if not char:

                break

            self.output_queue.put(char)



    def wait_for_ready(self):

        """입력 대기 프롬프트가 나올 때까지 출력을 소모"""

        buffer = ""

        while True:

            if not self.output_queue.empty():

                char = self.output_queue.get()

                buffer += char

                print(char, end="", flush=True) # 디버깅용 출력

                

                # 프롬프트 감지 시 루프 종료

                if buffer.endswith(WAIT_PROMPT):

                    return

            else:

                time.sleep(0.01)



    def chat(self, user_input):

        """명령을 보내고 답변을 받아옴"""

        # 1. 입력 전송

        self.process.stdin.write(user_input + "\n")

        self.process.stdin.flush()

        

        # 2. 답변 수신

        response_text = ""

        buffer = ""

        start_time = time.time()

        

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

                

        return response_text



    def close(self):

        self.running = False
        self.process.terminate()

         # 1단계: 프로그램 내부의 종료 명령어 전송 (가장 깔끔함)

        # MNN 데모가 특정 종료 키워드를 지원한다면 사용하는 게 좋습니다.

        # 보통 모르기 때문에 빈 줄을 보내서 입력 대기를 풀거나 exit를 시도합니다.

        # try:

            # if self.process.poll() is None:  # 프로세스가 아직 살아있다면

                # self.process.stdin.write("\n")  # 입력 대기 상태 깨우기

                # self.process.stdin.flush()

        # except (BrokenPipeError, OSError):

            # pass

        print("LLM 프로세스가 완전히 종료되었습니다.")



# ==========================================

# Termux API 함수들

# ==========================================

def stt():

    """Termux 마이크 입력"""

    print("\n[듣는 중...]")

    # termux-speech-to-text 명령 실행 및 결과 캡처

    try:

        result = subprocess.check_output(["termux-speech-to-text"], text=True)

        return result.strip()

    except subprocess.CalledProcessError:

        return ""



def tts(text):

    """Termux 스피커 출력"""

    print(f"\n[말하는 중]: {text}")

    subprocess.run(["termux-tts-speak", text])



# ==========================================

# 메인 실행 루프

# ==========================================

def main():

    # LLM 초기화

    llm = LocalLLM(cwd=MNN_BUILD_PATH, exe=MNN_DEMO_EXE, config=MODEL_CONFIG)

    

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



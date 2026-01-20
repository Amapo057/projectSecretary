import subprocess

def stt():
    try:

        result = subprocess.check_output(["termux-speech-to-text"], text=True)

        return result.strip()

    except subprocess.CalledProcessError:

        return ""



def tts(text):

    """Termux 스피커 출력"""

    print(f"\n[말하는 중]: {text}")

    subprocess.run(["termux-tts-speak", text])


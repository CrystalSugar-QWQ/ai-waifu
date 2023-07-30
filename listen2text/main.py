import listen2text
import threading, queue

wav_file = "./input.wav"


# 实时监听,为保证实时监听采用异步执行
def linten(audio_data):
    print("[开始监听]")
    while True:
        audio = listen2text.audio_listen(THRESHOLD = 600.0)
        audio_data.put(audio)


# 语音转文字,可能有延迟所以采用异步执行
def audio2text(audio_data, text_data):
    while True:
        audio = audio_data.get()
        listen2text.audio2wav(wav_file, audio)
        text = listen2text.wav2text_google(wav_file)
        # text = listen2text.wave2text_baidu(wav_file)
        print("[said]:", text)
        if text is not None:
            text_data.put(text)


# 合并等待调用
def listen_to_text(text_data):
    audio_data = queue.Queue()
    audio2wav_thread = threading.Thread(target=audio2text, args=(audio_data, text_data))
    audio2wav_thread.start()

    linten(audio_data)

    audio2wav_thread.join()
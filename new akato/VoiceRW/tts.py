import keyboard
import pyaudio
import wave
import numpy as np
import urllib.parse
import speech_recognition as sr
import requests, json
import io
import time


# 读出翻译结果(此处只针对voicevox生成的语音，"output.wav"是文件路径，要改改这个)
def read_wav():
    chunk = 1024

    try:
        with wave.open("output.wav", 'rb')as wav_file:
            audio = pyaudio.PyAudio()

            stream = audio.open(format=audio.get_format_from_width(wav_file.getsampwidth()),
                                channels=wav_file.getnchannels(),
                                rate=wav_file.getframerate(),
                                output=True)
            data = wav_file.readframes(chunk)
            while data:
                stream.write(data)
                data = wav_file.readframes(chunk)
            stream.stop_stream()
            stream.close()
            audio.terminate()
    except Exception:
        print("error wav")


# 录音功能(录音时间过短进入openai的语音转文字会报错，请一定注意)
def record_audio():
    pressdown_num = 0
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "input.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    print("Recording...")
    while keyboard.is_pressed('RIGHT_SHIFT'):
        data = stream.read(CHUNK)
        frames.append(data)
        pressdown_num = pressdown_num + 1
    print("Stopped recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    if pressdown_num >= 5:         # 粗糙的处理手段
        return 1
    else:
        print("杂鱼杂鱼，好短好短(录音时间过短,按右shift重新录制)")
        return 0


# (改语音可以看"speaker.json"及"voicevox")
# tts:输入
# voice:音色
def voicevox_tts(tts, voice):
    voicevox_url = 'http://localhost:50021'
    params_encoded = urllib.parse.urlencode({'text': tts, 'speaker': voice})
    request = requests.post(f'{voicevox_url}/audio_query?{params_encoded}')
    params_encoded = urllib.parse.urlencode({'speaker': voice, 'enable_interrogative_upspeak': True})
    request = requests.post(f'{voicevox_url}/synthesis?{params_encoded}', json=request.json())

    with open("output.wav", "wb") as outfile:
        outfile.write(request.content)


# 使用谷歌的语音转文字
def audio_listen_google():
    # 创建Recognizer对象
    r = sr.Recognizer()

    # 打开麦克风进行录音
    with sr.Microphone() as source:
        print("[等待语音输入]")
        try:
            # 从麦克风获取音频数据
            audio = r.listen(source)
            print("[语音输入完成]")
            # 进行实时语音识别
            # text = r.recognize_google(audio, language='zh-CN')
            # 输出识别结果
            # print("[question]:" + text)
            return audio
        except sr.UnknownValueError:
            print("[无法识别输入的语音]")
        except sr.RequestError as e:
            print("[请求出错]:" + str(e))


# THRESHOLD 设置音量阈值,默认值800.0,根据实际情况调整
def audio_listen(THRESHOLD = 800.0):
    audio = pyaudio.PyAudio()

    # 设置音频参数
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    SILENCE_THRESHOLD = 15     # 设置沉默阈值，根据实际情况调整

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []  # 存储录制的音频帧

    is_speaking = False  # 是否在说话
    silent_count = 0  # 沉默计数
    speaking_flag = False   #录入标志位 不重要

    while True:
        # 读取音频数据
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.short)
        max_dB = np.max(audio_data)
        # print(max_dB)
        if max_dB > THRESHOLD:
            is_speaking = True
            silent_count = 0
        elif is_speaking is True:
            silent_count += 1

        if is_speaking is True:
            frames.append(data)
            if speaking_flag is False:
                print("[录入中……]")
                speaking_flag = True

        if silent_count >= SILENCE_THRESHOLD:
            break
    print("[语音录入完成]")
    # 将音频保存为WAV文件
    '''with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))'''
    return frames


class Voicevox:
    def __init__(self,host="127.0.0.1",port=50021):
        self.host = host
        self.port = port

    def speak(self,text=None,speaker=None): # VOICEVOX:ナースロボ＿タイプＴ

        params = (
            ("text", text),
            ("speaker", speaker)  # 音声の種類をInt型で指定
        )

        init_q = requests.post(
            f"http://{self.host}:{self.port}/audio_query",
            params=params
        )

        res = requests.post(
            f"http://{self.host}:{self.port}/synthesis",
            headers={"Content-Type": "application/json"},
            params=params,
            data=json.dumps(init_q.json())
        )

        # メモリ上で展開
        audio = io.BytesIO(res.content)

        with wave.open(audio,'rb') as f:
            # 以下再生用処理
            p = pyaudio.PyAudio()

            def _callback(in_data, frame_count, time_info, status):
                data = f.readframes(frame_count)
                return (data, pyaudio.paContinue)

            stream = p.open(format=p.get_format_from_width(width=f.getsampwidth()),
                            channels=f.getnchannels(),
                            rate=f.getframerate(),
                            output=True,
                            stream_callback=_callback)

            # Voice再生
            stream.start_stream()
            while stream.is_active():
                time.sleep(0.1)

            stream.stop_stream()
            stream.close()
            p.terminate()


if __name__ == '__main__':
    audio_listen()

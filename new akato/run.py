import sys
import subtitle
import random
import open_ai.akato_ai
import Translate.MyTranslation
import VoiceRW.tts
import vts.vtube
import multiprocessing
import blivedm.sample
import asyncio
from VoiceRW.tts import Voicevox
import speech_recognition as sr
import pyaudio, wave
from aip import AipSpeech

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

owner_name = "sugar"
audio_input = "input.wav"


# 异步处理问题并输出
def ask_out(question, message_data, question2, tts_data):
    while True:
        # 从问题队列获取问题
        text = question.get()

        # 想ai提问，获取回答
        message = open_ai.akato_ai.ask_ai(owner_name, text)
        print("[Akato]:", message)

        # voicevox的输入翻译
        # tts = Translate.MyTranslation.translate_GPT3(message, "Japanese")
        tts = Translate.MyTranslation.translate_google(message, "JA")
        print("[翻译器][日语]:", tts)

        question2.put(text)
        message_data.put(message)
        tts_data.put(tts)


# 语音阅读+动作触发
def voice_out(question, action_data, message_data, tts_data):
    vv = Voicevox()
    while True:
        # 从问题队列获取问题
        text = question.get()
        message = message_data.get()
        tts = tts_data.get()

        try:
            # 生成语音文件
            #VoiceRW.tts.voicevox_tts(tts, 46)

            # 生成字幕文本
            subtitle.generate_subtitle(text, message)

            # 阅读语音
            #VoiceRW.tts.read_wav()

            # 生成+阅读语音
            vv.speak(text = tts, speaker = 46)
        except Exception:
            print("[VoiceVox ERROR]")
        finally:
            # 概率性触发动作
            sp = random.randint(1,100)
            if sp > 0 and sp <= 2:
                action_data.value = 4
            elif sp > 2 and sp <= 10:
                action_data.value = 3
            elif sp > 10 and sp <= 40:
                action_data.value = 1
            elif sp > 40 and sp <= 100:
                action_data.value = 2

            # 清空字幕文本
            with open("output.txt", "w") as f:
                f.truncate(0)
            with open("chat.txt", "w") as f:
                f.truncate(0)


def vtube_sport(shared_data):
    vts.vtube.vtube_worker(shared_data)


def BliveDM(question):
    asyncio.run(blivedm.sample.main(question))


# 语音(wav)翻译——谷歌
def wave_to_text_google(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language='zh-CN')
        return text
    except sr.UnknownValueError:
        print("[无法识别输入的语音]")
    except sr.RequestError as e:
        print("[请求出错]:" + str(e))


# 语音(wav)翻译——百度
def wave_to_text_baidu(file):
    # 设置 APPID、API Key 和 Secret Key 申请地址https://console.bce.baidu.com/ai/#/ai/speech/overview/index
    APP_ID = '36050058'
    API_KEY = 'xdENMcNpGiQmeNPEDlPuF46Y'
    SECRET_KEY = 'W5Aw2BrM78XEatjwNXiC3h4itEHlwTjM'
    # 初始化 AipSpeech 对象
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 读取音频文件
    with open(file, 'rb') as fp:
        audio = fp.read()

    # 识别音频文件
    res = client.asr(audio, 'wav', 16000, {
        'dev_pid': 1536,
    })
    if res['err_no'] == 0:
        return res['result'][0]
    else:
        print("[ERROR baidu:]",res['err_no'])


# question是我的提问队列，不用可以改掉
def wave_to_text(question, audio_data):
    # 设置音频参数
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    WAVE_OUTPUT_FILENAME = "input.wav"  # 保存路径自己改吧，摆烂了

    while True:
        frames = audio_data.get()

        # 将音频保存为WAV文件
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        # OPENAI翻译
        # open_ai.akato_ai.transcribe_audio(WAVE_OUTPUT_FILENAME)
        # 谷歌翻译
        # wave_to_text_google(WAVE_OUTPUT_FILENAME)
        # 百度翻译
        text = wave_to_text_baidu(WAVE_OUTPUT_FILENAME)
        
        try:
            # 输出识别结果
            print("[question]:" + text)
            
            # 在这里输出结果
            question.put(text)
        except Exception:
            pass


def listen_wave():
    audio = VoiceRW.tts.audio_listen()
    return audio


if __name__ == '__main__':
    # 创建队列
    question = multiprocessing.Queue(maxsize=0)
    question2 = multiprocessing.Queue(maxsize=0)
    message = multiprocessing.Queue(maxsize=0)
    tts_data = multiprocessing.Queue(maxsize=0)
    audio_data = multiprocessing.Queue(maxsize=0)
    action_data = multiprocessing.Value('i', 0)

    # 创建进程并启动 ps:别问我为什么只开进程，懒的
    p1 = multiprocessing.Process(target=ask_out, args=(question, message, question2, tts_data))
    # p1.start()
    p2 = multiprocessing.Process(target=vtube_sport, args=(action_data,))
    # p2.start()
    p3 = multiprocessing.Process(target=BliveDM, args=(question, ))
    p3.start()
    p4 = multiprocessing.Process(target=voice_out, args=(question2, action_data, message, tts_data))
    # p4.start()
    p5 = multiprocessing.Process(target=wave_to_text, args=(question, audio_data))
    # p5.start()
    
    print("[开始监听]")
    while True:
        q = listen_wave()
        # 向问题队列放入问题
        audio_data.put(q)

    # 主进程等待子进程结束
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()

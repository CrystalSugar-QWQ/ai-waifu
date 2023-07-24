import multiprocessing
import asyncio
import speech_recognition as sr
import pyaudio, wave
import utils
import blivedm.sample
import open_ai.akato_ai
import vts_sports.vtube

owner_name = "sugar"


def listen_wave():
    audio = utils.audio_listen()
    return audio


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


# question是我的提问队列，不用可以改掉
def wave_to_text(question, audio_data):
    # 设置音频参数
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    WAVE_OUTPUT_FILENAME = "./input.wav"  # 保存路径自己改吧，摆烂了

    while True:
        frames = audio_data.get()

        # 将音频保存为WAV文件
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        # 谷歌翻译
        text = wave_to_text_google(WAVE_OUTPUT_FILENAME)
        
        try:
            # 输出识别结果
            print("[question]:" + text)
            
            # 在这里输出结果
            question.put(text)
        except Exception:
            pass


def BliveDM(question):
    asyncio.run(blivedm.sample.main(question))


# 异步处理问题并输出
def ask_out(question, message_data, message_question):
    while True:
        # 从问题队列获取问题
        text = question.get()

        # 想ai提问，获取回答
        message = open_ai.akato_ai.ask_ai(owner_name, text)
        print("[Akato]:", message)

        message_question.put(text)
        message_data.put(message)


if __name__ == '__main__':
    # 创建队列
    audio_data = multiprocessing.Queue(maxsize=0)
    question = multiprocessing.Queue(maxsize=0)
    message = multiprocessing.Queue(maxsize=0)
    message_question = multiprocessing.Queue(maxsize=0)
    
    p1 = multiprocessing.Process(target=wave_to_text, args=(question, audio_data))
    p1.start()
    p2 = multiprocessing.Process(target=BliveDM, args=(question, ))
    p2.start()
    p3 = multiprocessing.Process(target=ask_out, args=(question, message, message_question))
    p3.start()
    p4 = multiprocessing.Process(target=vts_sports.vtube.main, args=(message, message_question))
    p4.start()

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

import asyncio, websockets
from snownlp import SnowNLP
import threading, queue, multiprocessing
import vts_sports.Vts as Vts
import vts_sports.VoiceVox as VoiceVox
import json
import random
import time

# 全局变量
emotion_data = 0
is_speak = 0


# 情绪处理，输出表情偏移量、表情动画
async def emotion_sport(websocket):
    expression = ""
    emotion_file = "neutral"
    if emotion_data >= 0.6:  # active状态
        Brows_shifting = 0.55 + ((emotion_data - 0.6)/4)
        MouthSmile_shifting = 0.6 + ((emotion_data - 0.6)/2)
        await Vts.vtube_hotkeys(websocket, "脸红")
        expression = "脸红"
        emotion_file = "active"
    elif 0.4 < emotion_data < 0.6:    # neutral状态
        Brows_shifting = 0.55
        MouthSmile_shifting = 0.6
    elif emotion_data <= 0.4:    # negative状态
        Brows_shifting = 0.5 - ((0.4 - emotion_data)/4)
        MouthSmile_shifting = 0.5 - ((0.4 - emotion_data)/2)
        emotion_file = "negative"
        if emotion_data <= 0.2:
            await Vts.vtube_hotkeys(websocket, "脸黑")
            expression = "脸黑"
    return Brows_shifting, MouthSmile_shifting, expression, emotion_file


# time单位1秒, is_speak停止标志位
async def wait_sport(websocket, time = 0):
    while True:
        parameter_values = await Vts.waiting_model(time)
        await Vts.vtube_control(websocket, parameter_values)
        await asyncio.sleep(0.02)
        if time == 4:
            return parameter_values
        if is_speak == 1:
            return parameter_values
        time += 0.02
        time = round(time, 2)


async def vtube_run():
    # 连接上服务器,并初始化
    try:
        websocket = await websockets.connect('ws://127.0.0.1:8001')
        await Vts.init(websocket)
        print("[VTS 初始化完成]")
    except Exception:
        print("[VTS 无法连接]")
        return

    while True:
        if is_speak == 1:
            Brows_shifting, MouthSmile_shifting, expression, emotion_file= await emotion_sport(websocket)
            # 随机数范围就是你有多少范围写多少
            sport_num = random.randint(1,1)
            file = f"./vts_sports/sport/{emotion_file}/sport{sport_num}.json"
            with open(file, "r") as config_file:     # 读文件
                data = json.load(config_file)
        
            parameter_values = await Vts.value_homing(websocket, parameter_values, time_end = 0.2, 
                                                      FaceAngleX_end = data[0][0]["value"], FaceAngleY_end = data[0][1]["value"], FaceAngleZ_end = data[0][2]["value"], 
                                                      EyeRightX_end = data[0][3]["value"], EyeRightY_end = data[0][4]["value"], EyeOpen_end = data[0][5]["value"], 
                                                      Brows_end = Brows_shifting, MouthSmile_end = MouthSmile_shifting)
            while True:
                if is_speak == 0:
                    parameter_values = await Vts.value_homing(websocket, parameter_values, time_end = 0.4)
                    await Vts.expression_close(websocket, expression)
                    break
                elif is_speak == 2:
                    parameter_values = await Vts.value_homing(websocket, parameter_values, time_end = 0.3)
                    await Vts.sport_wink1(websocket, parameter_values)
                    await Vts.expression_close(websocket, expression)
                    break
                time = 0 
                for i in range(len(data)):
                    if is_speak != 1:
                        break
                    Brows = Vts.sine_wave(time,amplitude=0.025, shifting=Brows_shifting)
                    MouthSmile = Vts.sine_wave(time, amplitude=0.08, shifting=MouthSmile_shifting)
                    parameter_values = data[i]
                    parameter_values.append({"id": "Brows", "value": Brows})
                    parameter_values.append({"id": "MouthSmile", "value": MouthSmile})
                    await Vts.vtube_control(websocket, parameter_values)
                    await asyncio.sleep(0.02)
                    time += 0.02
                    time = round(time, 2)
        else:
            parameter_values = await wait_sport(websocket)


def vtube_worker():
    asyncio.run(vtube_run())


# 翻译线程，输入文本，翻译为日文，提供给VOICEVOX
def translate_JA(text_data, tts_data):
    while True:
        text = text_data.get()
        # print("[输入文本]:", text)
        text_ja = VoiceVox.translateGoogle(text, "JA")
        print("[翻译器][日语]:", text_ja)
        tts_data.put(text_ja)


# 语音输出线程， 输入日文
def VoiceOut_with_Emotion(text_data, tts_data, question_data):
    global emotion_data, is_speak
    VV = VoiceVox.Voicevox()
    subtitle1_file = "./output.txt"
    subtitle2_file = "./input.txt"
    while True:
        tts = tts_data.get()
        text = text_data.get()
        question = question_data.get()

        try:
            # 生成字幕
            VoiceVox.generate_subtitle(text, subtitle1_file)
            VoiceVox.generate_subtitle(question, subtitle2_file)

            # 语音生成，speaker请看speaker.josn
            audio = VV.speak_1(text = tts, speaker = 46)

            # 等待语音生成完成，再启动情绪分析动作选择
            emotion = SnowNLP(text)
            # print(f"[语句'{text}'的情绪值]:", emotion.sentiments)
            emotion_data = emotion.sentiments

            # 语音阅读
            is_speak = 1
            VV.speak_2(audio)
        except Exception:
            print("[VoiceVox ERROR]")
        finally:
            if random.randint(1,100) <= (emotion_data*100) and emotion_data > 0.5:
                # 语音生成，speaker请看speaker.josn
                audio = VV.speak_1(text = "ウィンク", speaker = 46)
                is_speak = 2
                time.sleep(0.3)
                # 语音阅读
                VV.speak_2(audio)
            else:
                is_speak = 0
            VoiceVox.clear_subtitle(subtitle1_file)  # 清空字幕
            VoiceVox.clear_subtitle(subtitle2_file)  # 清空字幕


def main(text_data, message_question):
    # 创建各自处理队列
    text_1 = queue.Queue()
    text_2 = queue.Queue()
    tts_data = queue.Queue()
    question_data = queue.Queue()
    # 创建各自线程
    thread1 = threading.Thread(target=vtube_worker, )
    thread1.start()
    thread2 = threading.Thread(target=translate_JA, args=(text_2, tts_data))
    thread2.start()
    thread3 = threading.Thread(target=VoiceOut_with_Emotion, args=(text_1, tts_data, question_data))
    thread3.start()

    # 主线程负责处理数据并下发
    while True:
        text = text_data.get()
        text_1.put(text)
        text_2.put(text)
        question_text = message_question.get()
        question_data.put(question_text)

    thread1.join()
    thread2.join()
    thread3.join()

if __name__ == '__main__':
    text = multiprocessing.Queue(maxsize=0)
    VTUBE = multiprocessing.Process(target=main, args=(text, ))
    VTUBE.start()

    while True:
        q = input("[请输入语句]:\n")
        text.put(q)

    VTUBE.join()

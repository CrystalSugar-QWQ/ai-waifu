import time
import json
import random
import asyncio, websockets
import threading, queue
from snownlp import SnowNLP

import vtube
import voice_tts


# 全局变量
emotion_data = 0
is_speak = 0
lock = threading.Lock()


# 语音输出线程。 由于voicevox的特殊性，输入需要中日两种文本,这里交给翻译线程负责
def VoiceOut_with_Emotion(question_data, message_data, tts_data):
    global emotion_data, is_speak
    VV = voice_tts.Voicevox()
    question_file = "./input.txt"
    answer_file = "./output.txt"
    answer = ""
    while True:
        question = question_data.get()
        voice_tts.generate_subtitle(question, question_file)
        while True:
            tts = tts_data.get()
            message = message_data.get()
            if tts == "[end]" and message == "[end]":
                answer = ""

                lock.acquire()
                is_speak = 0
                lock.release()

                voice_tts.clear_subtitle(question_file)     # 清空问题字幕
                voice_tts.clear_subtitle(answer_file)       # 清空回答字幕
                break
            elif message == "wink。":
                # 生成字幕,增加字幕
                answer += message
                answer += "\n"
                voice_tts.generate_subtitle(answer, answer_file)
                # 拿日语发音拼的wink
                audio = VV.make_voice(text = "ウィンク", speaker = 46)

                lock.acquire()
                is_speak = 2
                lock.release()

                time.sleep(0.4)
                # 语音阅读
                VV.read_voice(audio)
            else:
                # 生成字幕,增加字幕
                answer += message
                answer += "\n"
                voice_tts.generate_subtitle(answer, answer_file)
                # 生成语音
                audio = VV.make_voice(text = tts, speaker = 46)

                # 等待语音生成完成，再启动情绪分析动作选择
                emotion = SnowNLP(message)
                lock.acquire()
                emotion_data = emotion.sentiments
                # 语音阅读
                is_speak = 1
                lock.release()

                VV.read_voice(audio)


# 翻译和数据整理
def translate_JA(message_data, tts_data, message_res):
    while True:
        message = message_data.get()
        if message == "[end]":
            message_res.put("[end]")
            tts_data.put("[end]")
        else:
            tts = voice_tts.translateGoogle(message, "JA")
            message_res.put(message)
            tts_data.put(tts)


# 情绪处理，输出表情偏移量、表情动画
async def emotion_sport(websocket):
    global emotion_data
    expression = ""
    emotion_file = "neutral"

    lock.acquire()
    emotion = emotion_data
    lock.release()

    if emotion >= 0.6:  # active状态
        Brows_shifting = 0.55 + ((emotion - 0.6)/4)
        MouthSmile_shifting = 0.6 + ((emotion - 0.6)/2)
        await vtube.vtube_hotkeys(websocket, "脸红")
        expression = "脸红"
        emotion_file = "active"
    elif 0.4 < emotion < 0.6:    # neutral状态
        Brows_shifting = 0.55
        MouthSmile_shifting = 0.6
    elif emotion <= 0.4:    # negative状态
        Brows_shifting = 0.5 - ((0.4 - emotion)/4)
        MouthSmile_shifting = 0.5 - ((0.4 - emotion)/2)
        emotion_file = "negative"
        if emotion <= 0.2:
            await vtube.vtube_hotkeys(websocket, "脸黑")
            expression = "脸黑"
    return Brows_shifting, MouthSmile_shifting, expression, emotion_file


# time单位1秒, is_speak停止标志位
async def wait_sport(websocket, time = 0):
    global is_speak
    while True:
        parameter_values = await vtube.waiting_model(time)
        await vtube.vtube_control(websocket, parameter_values)
        await asyncio.sleep(0.02)
        if time == 4:
            return parameter_values
        lock.acquire()
        speak_flag = is_speak
        lock.release()
        if speak_flag == 1:
            return parameter_values
        time += 0.02
        time = round(time, 2)


async def vtube_run():
    # 连接上服务器,并初始化
    try:
        websocket = await websockets.connect('ws://127.0.0.1:8001')
        await vtube.init(websocket)
        print("[VTS 初始化完成]")
    except Exception:
        print("[VTS 无法连接]")
        return

    while True:
        lock.acquire()
        speak_flag = is_speak
        lock.release()
        if speak_flag == 1:
            Brows_shifting, MouthSmile_shifting, expression, emotion_file= await emotion_sport(websocket)
            # ---------------------------在这里写动作选择--------------------------- #
            # sport_num = random.randint(1,1)
            # file = f"./sport/{emotion_file}/sport{sport_num}.json"
            file = f"./sport/{emotion_file}/sport1.json"    # 默认同一套动作
            # ---------------------------------end--------------------------------- #
            with open(file, "r") as config_file:     # 读文件
                data = json.load(config_file)
        
            parameter_values = await vtube.value_homing(websocket, parameter_values, time_end = 0.3, 
                                                      FaceAngleX_end = data[0][0]["value"], FaceAngleY_end = data[0][1]["value"], FaceAngleZ_end = data[0][2]["value"], 
                                                      EyeRightX_end = data[0][3]["value"], EyeRightY_end = data[0][4]["value"], EyeOpen_end = data[0][5]["value"], 
                                                      Brows_end = Brows_shifting, MouthSmile_end = MouthSmile_shifting)
            while True:
                lock.acquire()
                speak_flag = is_speak
                lock.release()
                if speak_flag == 0:
                    parameter_values = await vtube.value_homing(websocket, parameter_values, time_end = 0.6)
                    await vtube.expression_close(websocket, expression)
                    break
                elif speak_flag == 2:
                    parameter_values = await vtube.value_homing(websocket, parameter_values, time_end = 0.4)
                    await vtube.sport_wink1(websocket, parameter_values)
                    await vtube.expression_close(websocket, expression)
                    break
                time = 0 
                for i in range(len(data)):
                    Brows = vtube.sine_wave(time,amplitude=0.025, shifting=Brows_shifting)
                    MouthSmile = vtube.sine_wave(time, amplitude=0.02, shifting=MouthSmile_shifting)
                    parameter_values = data[i]
                    parameter_values.append({"id": "Brows", "value": Brows})
                    parameter_values.append({"id": "MouthSmile", "value": MouthSmile})
                    await vtube.vtube_control(websocket, parameter_values)
                    await asyncio.sleep(0.02)
                    time += 0.02
                    time = round(time, 2)
                    lock.acquire()
                    speak_flag = is_speak
                    lock.release()
                    if speak_flag != 1 and parameter_values[5]["value"] > 0.45:
                        break
        else:
            parameter_values = await wait_sport(websocket)


def vtube_worker():
    asyncio.run(vtube_run())


def main(question_data, message_data):
    tts_data = queue.Queue()        # 经过翻译处理，给voicevox准备的tts数据
    message_res = queue.Queue()     # 给生成字幕准备的数据
    # tts数据翻译
    translate_thread = threading.Thread(target=translate_JA, args=(message_data, tts_data, message_res))
    translate_thread.start()

    # 语音阅读，通过全局变量告知状态
    voice_thread = threading.Thread(target=VoiceOut_with_Emotion, args=(question_data, message_res, tts_data))
    voice_thread.start()

    # 动作输出
    VtsSport_thread = threading.Thread(target=vtube_worker, )
    VtsSport_thread.start()

    translate_thread.join()
    voice_thread.join()
    VtsSport_thread.join()

import pyaudio
import numpy as np


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
    return frames
import threading, queue
import time

import listen2text
import blivedm
import chatgpt, chatglm
import vtube, voice_tts

if __name__ == '__main__':
    question_data = queue.Queue()   # 问题输入队列，主要采集来源麦克风监听和弹幕
    question_re = queue.Queue()     # 问题输出队列，字幕输出用
    message_data = queue.Queue()    # 回答队列，传输给tts

    # 麦克风监听功能
    listen_thread = threading.Thread(target=listen2text.listen_to_text, args=(question_data, ))
    # listen_thread.start()

    # b站弹幕监听功能
    blivedm_thread = threading.Thread(target=blivedm.run, args=(question_data, ))
    blivedm_thread.start()

    # 语言模型功能,目前只支持gpt、glm。因为要对默认模型做人设,所以不是随便什么都能轻松接入
    # LLM_thread = threading.Thread(target=chatgpt.gpt, args=(question_data, message_data, question_re))       # 效果绝佳,烧钱速度绝佳
    LLM_thread = threading.Thread(target=chatglm.glm2, args=(question_data, message_data, question_re))    # 低智不推荐,省钱推荐,设定一定要非常清晰
    LLM_thread.start()

    # 语音动作同步输出,改tts进去改
    tts_thread = threading.Thread(target=vtube.main, args=(question_re, message_data))
    tts_thread.start()

    while True:
        time.sleep(10)

    listen_thread.join()
    blivedm_thread.join()
    LLM_thread.join()
    tts_thread.join()

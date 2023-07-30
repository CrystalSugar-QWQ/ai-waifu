import speech_recognition as sr
from aip import AipSpeech
from config import wav2text_baidu_APP_ID, wav2text_baidu_API_KEY, wav2text_baidu_SECRET_KEY


# 语音(wav)翻译——谷歌
def wav2text_google(file):
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
def wave2text_baidu(file):
    # 设置 APPID、API Key 和 Secret Key 申请地址https://console.bce.baidu.com/ai/#/ai/speech/overview/index
    # 初始化 AipSpeech 对象
    client = AipSpeech(wav2text_baidu_APP_ID, wav2text_baidu_API_KEY, wav2text_baidu_SECRET_KEY)

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
import urllib.parse, urllib.request
import hashlib
import random
import json

from pygtrans import Translate

from aip import AipSpeech
import speech_recognition as sr


appid = '20230707001737106'
secretKey = 'gXBBiujfAu7wGV57d7Um'
url_baidu = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
 

def translateBaidu(text, f='zh', t='jp'):
    salt = random.randint(32768, 65536)
    sign = appid + text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = url_baidu + '?appid=' + appid + '&q=' + urllib.parse.quote(text) + '&from=' + f + '&to=' + t + \
            '&salt=' + str(salt) + '&sign=' + sign
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    data = json.loads(content)
    result = str(data['trans_result'][0]['dst'])
    print(result)


def translateGoogle(text, target_language):
    client = Translate()
    tt = client.translate(text, target = target_language)
    print(tt.translatedText)
    return tt.translatedText


def audio_to_text_google():
    # 创建语音识别器实例
    recognizer = sr.Recognizer()

    # 定义 WAV 文件路径
    wav_file = "test.wav"

    # 使用语音识别器识别 WAV 文件
    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)  # 将音频文件转换为音频数据

        try:
            text = recognizer.recognize_google(audio, language='zh-CN')  # 使用 Google 语音识别进行识别
            print("识别结果：", text)
        except sr.UnknownValueError:
            print("无法识别语音")
        except sr.RequestError:
            print("请求语音识别服务出错")


def audio_to_text_baidu():
    # 语音翻译——百度
    # 设置 APPID、API Key 和 Secret Key
    APP_ID = '36050058'
    API_KEY = 'xdENMcNpGiQmeNPEDlPuF46Y'
    SECRET_KEY = 'W5Aw2BrM78XEatjwNXiC3h4itEHlwTjM'
    # 初始化 AipSpeech 对象
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 读取音频文件
    with open("test.wav", 'rb') as fp:
        audio = fp.read()

    # 识别音频文件
    res = client.asr(audio, 'wav', 16000, {
        'dev_pid': 1536,
    })
    if res['err_no'] == 0:
        print("识别结果：", res['result'][0])

audio_to_text_baidu()
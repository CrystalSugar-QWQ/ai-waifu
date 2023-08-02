import json
import random
import hashlib
import urllib.parse, urllib.request
from pygtrans import Translate

from config import translate_baidu_appid, translate_secretKey, translate_url_baidu
 

def translateBaidu(text, f='zh', t='jp'):
    salt = random.randint(32768, 65536)
    sign = translate_baidu_appid + text + str(salt) + translate_secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = translate_url_baidu + '?appid=' + translate_baidu_appid + '&q=' + urllib.parse.quote(text) + '&from=' + f + '&to=' + t + \
            '&salt=' + str(salt) + '&sign=' + sign
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    data = json.loads(content)
    result = str(data['trans_result'][0]['dst'])
    # print(result)
    print("[baidu][JA]:", result)
    return result


def translateGoogle(text, target_language):
    client = Translate()
    tt = client.translate(text, target = target_language)
    print("[google][JA]:", tt.translatedText)
    return tt.translatedText
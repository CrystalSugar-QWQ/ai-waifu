import urllib.parse, urllib.request
import hashlib
import random
import json

from pygtrans import Translate

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

translateGoogle("午饭", "JA")

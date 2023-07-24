import requests
import json
from snownlp import SnowNLP

API_KEY = "V2jIRvkwBqlBOGi6wlZfNiDA"
SECRET_KEY = "G1rY4vGSjGL0EXre68XIDwj5YFooOfTq"
    

def get_access_token():
    """
    使用 AK,SK 生成鉴权签名(Access Token)
    :return: access_token,或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


# 无场景: default, 闲聊对话: talk, 任务对话: task, 客服对话: customer_service
def text_analysis(text, scene = "talk"):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/emotion?charset=UTF-8&access_token=" + get_access_token()
    
    payload = json.dumps({
        "text": text,
        "scene": scene     
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    data = json.loads(response.text)
    
    print("[没什么用的id]:", data['log_id'], "\n[文本]:", data['text'], "\n[情绪倾向概率]:", data['items'][0]['prob'], "\n[情绪倾向]:", data['items'][0]['label'])
    if data['items'][0]['label'] != "neutral":
        # 情绪二级分类标签；
        # 客服模型正向（thankful感谢、happy愉快）、客服模型负向（complaining抱怨、angry愤怒）；
        # 闲聊模型正向（like喜爱、happy愉快）、闲聊模型负向（angry愤怒、disgusting厌恶、fearful恐惧、sad悲伤）
        print("[情绪概率]:", data['items'][0]['subitems'][0]['prob'], "\n[情绪]:", data['items'][0]['subitems'][0]['label'], "\n[建议回复]:", data['items'][0]['replies'][0])
        return data['items'][0]['subitems'][0]['label']
    return "neutral"


API_URL = "https://api-inference.modelscope.cn/api-inference/v1/models/damo/nlp_structbert_sentiment-classification_chinese-base"
# 请用自己的SDK令牌替换{YOUR_MODELSCOPE_SDK_TOKEN}（包括大括号）
headers = {"Authorization": f"Bearer 2c3f7cc1-7bed-4384-b6e5-512ed8ba8f72"}
def query(text):
    payload = {"input": text}
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

if __name__ == '__main__':
    output = query("我要杀了你？不，我要剁碎你！")
    print("[情绪]:", output['Data']['labels'][0], output['Data']['scores'][0])
    print("[情绪]:", output['Data']['labels'][1], output['Data']['scores'][1])
    
    text = '早'
    emotion = SnowNLP(text)
    print(emotion.sentiments) # 0.976923 positive

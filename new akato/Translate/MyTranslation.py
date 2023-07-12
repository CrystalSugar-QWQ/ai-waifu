import googletrans          # google翻译
import openai
from config import api_key
from pygtrans import Translate

# 翻译核心程序
def translate_text(text, target_language):
    try:
        translator = googletrans.Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception:
        print("error translate")
        return "error has ranslate"


# 翻译(报错重新执行，最多重复3次翻译)
def translate_google2(text, target_language):
    try_num = 1
    recivetest = translate_text(text, target_language)
    while recivetest == "error has ranslate":
        print("try again")
        recivetest = translate_text(text, target_language)
        try_num = try_num+1
        if try_num >= 5:
            if target_language == "JA":     # 保险起见这里不做二次翻译怕影响后续语音功能
                recivetest = "申し訳ありませんが、はっきりと聞いていませんでした"
            else:
                recivetest = translate_text("对不起没有听清楚", target_language)
            break
    return recivetest


def translate_google(text, target_language):
    client = Translate()
    tt = client.translate(text, target = target_language)
    # print(tt.translatedText)
    return tt.translatedText


def translate_GPT3(source_text, target_language):
    openai.api_key = api_key  # 你的 OpenAI API 密钥

    response = openai.Completion.create(
        engine='text-davinci-003',  # 可以选择适合的引擎
        prompt=f"Translate the following English text to {target_language}: \"{source_text}\"",
        max_tokens=200,
        temperature=0.7,
        n=1,
        stop=None
    )

    translation = response.choices[0].text.strip()
    return translation


if __name__ == '__main__':
    # 示例使用：将英文翻译为法文
    source_text = "早上好"
    target_language = "日文"

    translation = translate_GPT3(source_text, target_language)
    print(translation)
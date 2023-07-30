from snownlp import SnowNLP
import random
import re

import chatgpt


# 分句
def clause(text, message_data):
    # 使用正则表达式提取句子，并保留中文标点符号作为分隔符
    sentences = re.split(r'([！？。!?.~])', text)

    # 去除分隔符为空的元素
    sentences = [sentence for sentence in sentences if sentence.strip()]

    # 将相邻的分隔符和句子合并
    merged_sentences = [sentences[i] + sentences[i+1] for i in range(0, len(sentences), 2)]

    # 打印分句结果
    for i, sentence in enumerate(merged_sentences):
        message_data.put(sentence)


def gpt(question_data, message_data, question_re):
    while True:
        question = question_data.get()
        question_re.put(question)
        message = chatgpt.chatgpt_answer("红糖", question)
        clause(message, message_data)
        emotion = SnowNLP(message)
        if random.randint(1, 100) <= ((emotion.sentiments*100)-20) and emotion.sentiments > 0.5:
            message_data.put("wink。")
        message_data.put("[end]")   # 告知回答结束
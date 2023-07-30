from snownlp import SnowNLP
import random

import chatglm


def glm2(question_data, message_data, question_re):
    while True:
        question = question_data.get()
        question_re.put(question)
        message = chatglm.chatglm2_answer(question, message_data)
        emotion = SnowNLP(message)
        if random.randint(1, 100) <= ((emotion.sentiments*100)-20) and emotion.sentiments > 0.5:
            message_data.put("wink。")
        message_data.put("[end]")   # 告知回答结束
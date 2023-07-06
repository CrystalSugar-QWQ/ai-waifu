import openai
import json
import sys
import open_ai.promptMaker as promptMaker
from config import api_key

# to help the CLI write unicode characters to the terminal
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

conversation = []
history = {"history": conversation}
total_characters = 0

openai.api_key = api_key


# function to get an answer from OpenAI
def openai_answer():
    global total_characters, conversation

    total_characters = sum(len(d['content']) for d in conversation)

    while total_characters > 4000:
        try:
            # print(total_characters)
            # print(len(conversation))
            conversation.pop(2)
            total_characters = sum(len(d['content']) for d in conversation)
        except Exception as e:
            print("Error removing old messages: {0}".format(e))

    with open("open_ai/conversation.json", "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)

    prompt = promptMaker.getPrompt()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=prompt,
        max_tokens=200,
        temperature=1,
        top_p=0.9
    )
    message = response['choices'][0]['message']['content']
    conversation.append({'role': 'assistant', 'content': message})

    # translate_text(message)
    return message


# 使用openai进行文字提取(记得去填你的api)
def transcribe_audio(file):
    audio_file = open(file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    chat_now = transcript.text
    return chat_now


def ask_ai(name, text):
    global conversation
    # 将问题发送给openai(这段copy的出了问题请自行解决)
    result = name + " said " + text
    conversation.append({'role': 'user', 'content': result})
    message = openai_answer()
    return message

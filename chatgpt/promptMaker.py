import json
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

outputNum = 20  # 限制回答长度
identity_file = "./identity.txt"     # 人物设定地址
conversation_file = "./conversation.json"    # 历史文件地址


def getIdentity(identityPath):
    with open(identityPath, "r", encoding="utf-8") as f:
        identityContext = f.read()
    return {"role": "user", "content": identityContext}


def getPrompt():
    total_len = 0
    prompt = []
    prompt.append(getIdentity(identity_file))
    prompt.append({"role": "system", "content": f"Below is conversation history.\n"})

    with open(conversation_file, "r") as f:
        data = json.load(f)
    history = data["history"]
    for message in history[:-1]:
        prompt.append(message)

    prompt.append(
        {
            "role": "system",
            "content": f"Here is the latest conversation.\n*Make sure your response is within {outputNum} characters!\n",
        }
    )

    prompt.append(history[-1])

    total_len = sum(len(d['content']) for d in prompt)

    while total_len > 4000:
        try:
            # print(total_len)
            # print(len(prompt))
            prompt.pop(2)
            total_len = sum(len(d['content']) for d in prompt)
        except Exception:
            print("Error: Prompt too long!")

    # total_characters = sum(len(d['content']) for d in prompt)
    # print(f"Total characters: {total_characters}")

    return prompt


if __name__ == "__main__":
    prompt = getPrompt()
    print(prompt)
    print(len(prompt))

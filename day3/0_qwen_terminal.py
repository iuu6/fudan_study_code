import json

from openai import OpenAI

base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
api_key = 'sk-'  # 填自己的API_KEY
client = OpenAI(base_url=base_url, api_key=api_key)

model = 'qwen-max'
messages = [
    {'role': 'system', 'content': '你是一个能力很强的AI'},
]

while True:
    user_input = input('\n\nUser\n> ')
    if user_input.strip().lower() == 'exit':
        break
    messages.append(
        {'role': 'user', 'content': user_input}
    )

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    print('\nAssistant')
    result = ''
    for chunk in stream:
        text = chunk.choices[0].delta.content
        if text is not None:
            result += text
            print(text, end='')
    messages.append(
        {'role': 'assistant', 'content': result}
    )



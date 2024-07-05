from openai import OpenAI
import gradio as gr

base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
api_key = 'sk-'  # 填自己的API_KEY
client = OpenAI(base_url=base_url, api_key=api_key)
model = 'qwen-max'


def predict(message, history):
    print('\n\nUser:')
    print(message)
    messages = []
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": message})

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    print('\nAssistant:')
    result = ''
    for chunk in stream:
        text = chunk.choices[0].delta.content
        if text is not None:
            result += text
            print(text, end='')
            yield result


gr.ChatInterface(predict).launch()

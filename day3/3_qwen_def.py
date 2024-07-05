from openai import OpenAI
import os

# 封装成一个单次提问用的函数 输入问题 返回结果 过程中会打印模型的实时返回信息
def qwen(prompt):
    base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    api_key = 'sk-'  # 填自己的API_KEY
    client = OpenAI(base_url=base_url, api_key=api_key)

    model = 'qwen-max'
    messages = [
        {'role': 'system', 'content': '你是一个能力很强的AI助手'},
        {'role': 'user', 'content': prompt}
    ]
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
    return result


if __name__ == '__main__':
    result = qwen('该用户未做出评价！提取一下这条商品评论的感情倾向，是【褒义/贬义/无法确定】？')

    if '褒义' in result:
        print('千问说褒义')
    elif '贬义' in result:
        print('千问说贬义')
    else:
        print('千问说不知道')

    article = open('文章A.txt','r',encoding='utf-8').read()
    result = qwen(f'给这个小说起个名字，先思考，最后把名字放在书名号中：\n\n{article}')
    title = result.split('《')[1].split('》')[0]
    print('\n\n大模型返回标题是：',title)
    os.rename('文章A.txt',title+'.txt')
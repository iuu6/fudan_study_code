# encoding:utf-8
from aip import AipSpeech

'''
语音合成(TTS)
平台链接 https://ai.baidu.com/tech/speech/tts_online
'''

client = AipSpeech('xxx', 'xxx', 'xxx') # 在这里填入Key

result = client.synthesis('上海今天气温36℃', 'zh', 1)

if not isinstance(result, dict):
    open('audio.mp3', 'wb').write(result)
    print('合成完成')
else:
    print('合成失败')
    print(result)

from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '123'
API_KEY = 'xxx'
SECRET_KEY = 'xxx'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

data = open('audio.m4a','rb').read()
result = client.asr(data,'m4a',16000)
print(result)

text = ''.join(result['result'])
print('识别结果：',text)
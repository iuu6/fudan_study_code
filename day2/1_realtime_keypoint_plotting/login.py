# encoding:utf-8
import requests


def login(apiKey, secretKey):
    url = 'https://aip.baidubce.com/oauth/2.0/token'  # 接口的HTTP地址
    url += f'?grant_type=client_credentials&client_id={apiKey}&client_secret={secretKey}'  # 在地址后面携带账号密码参数信息
    headers = {  # HTTP请求的头部信息
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data='')  # 执行HTTP POST请求
    result = response.json()  # 将结果转为字典格式并存入result
    # print(result)  # 打印返回结果
    if 'access_token' in result:  # 根据返回信息判断是否登录成功 如果成功则会含有access_token
        token = result['access_token']  # 从字典中拿到所需的access_token信息
        print('登录成功:', token)
        return token
    else:
        print('登录失败')
        return ''


if __name__ == '__main__':
    login('', '')  # 程序入口 执行登录

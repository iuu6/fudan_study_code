# -*- coding:utf8 -*-
import time
import cv2
import base64
import requests
import json
from threading import Thread


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


access_token = login('xxx', 'xxx') # 在这里填入Key
if not access_token:
    exit(0)


request_url = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect'  # 车辆检测的接口地址
request_url += '?access_token=' + access_token  # 在地址后携带登录凭证信息

f = open('a.jpg', 'rb')  # 读取本地文件 地址填写图片路径(若与python程序在同一文件夹下可以直接写文件名) rb表示只读模式且以字节形式读取
img = base64.b64encode(f.read())  # 将图片字节信息转为base64格式的文本信息
data = {'image': img}  # 根据接口要求格式 组成字典
headers = {'Content-Type': 'application/x-www-form-urlencoded'}  # HTTP请求的头部信息
response = requests.post(request_url, data=data, headers=headers)  # 执行HTTP POST请求

if not response:
    print('网络连接错误')
    exit()

result = response.json()  # 将请求结果转为字典格式并存储在变量
print(json.dumps(result, indent=4))  # 转换为更清晰带缩进格式的文本并打印

if 'vehicle_num' not in result:  # 判断是否成功识别
    print('接口请求失败')
    exit()
if result['vehicle_num'] == 0:  # 判断图片中是否有人
    print('图片中未检测到车')
    exit()

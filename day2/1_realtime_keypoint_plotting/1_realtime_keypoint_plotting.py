# -*- coding:utf8 -*-
import time
import cv2
import base64
import requests
from threading import Thread

from login import login


access_token = login('xxx', 'xxx') # 在这里填入Key
if not access_token:
    exit(0)


def draw_person(image, result):
    ss = 0.4  # 显示点的置信度阈值
    lines = [  # 编写需要绘制的连线列表
        'left_ear,left_eye,nose,right_eye,right_ear',
        'left_wrist,left_elbow,left_shoulder,neck,right_shoulder,right_elbow,right_wrist',
        'nose,neck',
        'left_hip,right_hip',
        'left_shoulder,left_hip,left_knee,left_ankle',
        'right_shoulder,right_hip,right_knee,right_ankle',
    ]
    if result is None:
        return image
    if 'person_info' not in result:
        return image
    for info in result['person_info']:  # 循环绘制每一个人
        bp = info['body_parts']
        for l in lines:
            ks = l.split(',')
            for i in range(len(ks) - 1):
                v1, v2 = bp[ks[i]], bp[ks[i + 1]]
                c1, c2 = (int(v1['x']), int(v1['y'])), (int(v2['x']), int(v2['y']))
                if v1['score'] > ss and v2['score'] > ss:  # 当两个点都存在时绘制中间的连线
                    cv2.line(image, c1, c2, (255, 120, 120), 3)  # 绘制中间连线
        for k in bp:  # 循环绘制每一个点
            v = bp[k]
            if v['score'] > ss:
                c = (int(v['x']), int(v['y']))
                cv2.circle(image, c, 5, (120, 255, 120), -1)  # 绘制一个点
    return image


result = None


def update(frame):
    global result
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_base64 = str(base64.b64encode(img_encoded))[2:-1]

    request_url = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis'  # 人体关键点的接口地址
    request_url += '?access_token=' + access_token  # 在地址后携带登录凭证信息
    data = {'image': img_base64}  # 根据接口要求格式 组成字典
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}  # HTTP请求的头部信息
    response = requests.post(request_url, data=data, headers=headers)  # 执行HTTP POST请求

    if not response:
        print('网络连接错误')
        return

    result = response.json()  # 将请求结果转为字典格式并存储在变量
    # print(json.dumps(result, indent=4))  # 转换为更清晰带缩进格式的文本并打印

    if 'person_num' not in result:  # 判断是否成功识别
        print('接口请求失败')
        result = None
        return

    print('检测成功 人数:', result['person_num'])


cap = cv2.VideoCapture(0)
t = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        print('画面读取失败')
        exit(0)

    if time.time() - t > 0.51:
        Thread(target=update, args=(frame,)).start()
        t = time.time()

    if result is not None:
        draw_person(frame, result)
    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


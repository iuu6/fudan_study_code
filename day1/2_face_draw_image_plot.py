# encoding:utf-8
import time

import requests
import base64
import json
import cv2

access_token = '24.' # 在这里填入1中获取的token
request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis"
request_url += "?access_token=" + access_token

f = open('618cebc2cecb9483.jpg', 'rb')  # r rb w wb a 修改成图片位置
img = base64.b64encode(f.read())
params = {"image": img}
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)

result = response.json()
print(json.dumps(result, indent=4))

body_parts = result['person_info'][0]['body_parts']

if not result ['person_info']:
    print('Request error.')
    exit()
if result['person_num']==0:
    print('No human in image.')
    exit()


# 绘制结果到图像上
def draw_person(image, json):
    ss = 0.4  # 显示点的置信度阈值
    lines = [  # 需要绘制的连线列表
        'left_ear,left_eye,nose,right_eye,right_ear',
        'left_wrist,left_elbow,left_shoulder,neck,right_shoulder,right_elbow,right_wrist',
        'nose,neck',
        'left_hip,right_hip',
        'left_shoulder,left_hip,left_knee,left_ankle',
        'right_shoulder,right_hip,right_knee,right_ankle',
    ]
    for info in json['person_info']:  # 循环绘制每一个人
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

# 调用opencv画图
image = cv2.imread('618cebc2cecb9483.jpg') # 要修改成图片位置
image_plot = draw_person(image, result)
cv2.imwrite('image_plot.png', image_plot)
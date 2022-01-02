import requests
import qrcode
import cv2
from threading import Thread
import time
import os

import settings


def show():
    # 显示二维码
    img = cv2.imread("./logginQrcode.png")
    cv2.imshow("QRCODE", img)
    cv2.waitKey()
    time.sleep(180)
    cv2.destroyAllWindows()

def ifLogin():
    if not os.path.exists("sessdata.log"):
        open("sessdata.log", "w", encoding="utf8")
        return

    with open("sessdata.log", "r+", encoding="utf8") as f:
        line_list = f.readlines()
        for line in line_list:
            if time.time() - int(line.split(",")[0].split(".")[0]) <= 20 * 60:
                return line.split(",")[1]
            else:
                line_list.pop(0)

def verify(key):
    SESSDATA = None
    print("若已经确认,",end="")
    os.system("pause")
    url = "http://passport.bilibili.com/qrcode/getLoginInfo"
    os.system(f'curl {url} -d "oauthKey={key}" -c cookie.txt')
    with open("cookie.txt", "r", encoding="utf8") as f:
        f.read()
    time.sleep(5)

    
def loggin():
    # 验证是否登录
    # data = ifLogin()
    # if data:
    #     settings.HEADERS["cookie"] = data
    #     return

    # 获取登录url
    url = "http://passport.bilibili.com/qrcode/getLoginUrl"
    resp = requests.get(url=url, headers=settings.HEADERS)
    loggin_url = resp.json()["data"]["url"]
    key = resp.json()["data"]["oauthKey"]

    # 制作二维码
    img = qrcode.make(loggin_url)
    type(img)
    img.save("logginQrcode.png")

    # 开一个线程显示二维码
    t = Thread(target=show)
    t.start()
    
    # 验证登录
    verify(key)


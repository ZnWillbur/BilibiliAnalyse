import requests
import qrcode
import cv2
from threading import Thread
import time

import settings


def show():
    # 显示二维码
    img = cv2.imread("./logginQrcode.png")
    cv2.imshow("QRCODE", img)
    cv2.waitKey()
    time.sleep(180)
    cv2.destroyAllWindows()

def loggin():
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
    SESSDATA = None
    while True:
        url = "http://passport.bilibili.com/qrcode/getLoginInfo"
        resp = requests.post(url=url, headers=settings.HEADERS, params={"oauthKey": key})
        if not isinstance(resp.json()["data"], int):
            print(resp.json())
            SESSDATA = resp.json()["data"]["url"].rsplit("&")[-3].rsplit("=")[-1]
            settings.HEADERS["cookie": str(SESSDATA)]
            break
        time.sleep(3)


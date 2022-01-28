import winreg  # 和注册表交互
import re  # 正则模块
import requests
import settings
from lxml import etree
import os
from zipfile import ZipFile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json


version_re = re.compile(r'^[1-9]\d*\.\d*.\d*')  # 匹配前3位版本号的正则表达式

def getChromeVersion():
    try:
        # 从注册表中获得版本号
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
        _v, type = winreg.QueryValueEx(key, 'version')
        return version_re.findall(_v)[0]  # 返回前3位版本号
    except WindowsError as e:
        print('check Chrome failed:{}'.format(e))
    
def getChromeEngine(version):
    url = "https://npm.taobao.org/mirrors/chromedriver/"
    resp = requests.get(url, headers=settings.HEADERS)
    html = etree.HTML(resp.text)
    a_list = html.xpath("//pre/a/text()")
    for a in a_list:
        if a.rsplit(".", 1)[0] == version:
            url = url + a + "chromedriver_win32.zip"
            resp = requests.get(url, headers=settings.HEADERS)
            file_path = os.path.join(settings.DownloadDefaultPath, "chromedriver_win32.zip")
            with open(file_path, "wb") as f:
                f.write(resp.content)
            zip_file = ZipFile(file_path)
            zip_list = zip_file.namelist() # 得到压缩包里所有文件
            for f in zip_list:
                zip_file.extract(f, file_path.rsplit(".", 1)[0])
            zip_file.close()
            os.remove(file_path)
            break

def openChrome():
    file_path = os.path.join(settings.DownloadDefaultPath, "chromedriver_win32", "chromedriver.exe")
    # 解决版本警告
    s = Service(file_path)
    chrome = webdriver.Chrome(service=s)
    chrome.get("https://passport.bilibili.com/login")
    while True:
        jsoncookies = chrome.get_cookies()
        textcookies = json.dumps(jsoncookies)
        if "SESSDATA" in textcookies:
            f_cookie = ""
            for cookie in jsoncookies:
                f_cookie += (cookie["name"] + "=" + cookie["value"] + "; ")
            return f_cookie

def loggin():
    # 获得chrome的版本号
    version = getChromeVersion()
    # 下载chrome对应版本的引擎
    getChromeEngine(version)
    # 打开登录界面并获取登录cookie
    f_cookie = openChrome()
    # 添加cookie到请求头
    settings.HEADERS["cookie"] = f_cookie
    # 询问是否记录登录状态
    if input("是否记录登录状态?(1.是;0.否)"):
        with open("_cookie.txt", 'w', encoding="utf8") as f:
            f.write(f_cookie)
import os
import VideoDownload
import settings
from loggin import loggin

def start():
    if input("请问是否需要登录?(1.登录;回车.不登录/使用上次登录)"):
        loggin()
    else:
        file = os.path.join(settings.DownloadDefaultPath, "_cookie.txt")
        if os.path.exists(file):
            with open(file, "r", encoding="utf8") as f:
                cookie = f.read()
                if cookie:
                    settings.HEADERS["cookie"] = cookie
    os.system("cls")
    print("""
    欢迎使用Bilibili网站分析器
    该软件由ZnWillbur提供!

    分析器有如下功能:
    1.下载视频

    注意事项:
    1.不可以使用系统代理
    """)
    flag = int(input("请输入选项:"))
    if flag == 1:
        VideoDownload.start()


start()

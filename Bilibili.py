import os
import VideoDownload
import settings

def start():
    cookie = input("请输入您的cookie:")
    settings.HEADERS["cookie"] = cookie
    
    os.system("cls")
    print("""
    欢迎使用Bilibili网站分析器
    该软件由ZnWillbur提供！

    分析器有如下功能：
    1.下载视频

    注意事项：
    1.不可以使用系统代理
    """)
    flag = int(input("请输入选项："))
    if flag == 1:
        VideoDownload.start()


start()

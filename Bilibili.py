import VideoDownload
import loggin

def start():
    loggin.loggin()
    print("""
    欢迎使用Bilibili网站分析器v1.0
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
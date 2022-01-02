import VideoDownload
import loggin

def start():
    print("请扫码登录，此过程不要使用系统代理！")
    loggin.loggin()
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

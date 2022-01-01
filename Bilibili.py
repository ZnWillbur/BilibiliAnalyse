import VideoDownload


def start():
    print("""
    欢迎使用Bilibili网站分析器v1.0
    该软件由ZnWillbur提供！

    分析器有如下功能：
    1.下载视频

    """)
    flag = int(input("请输入选项："))
    if flag == 1:
        VideoDownload.start()
start()
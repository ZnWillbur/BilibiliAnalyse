import os
# 请求头
HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "referer": "https://www.bilibili.com/"
}
# 默认下载路径
DownloadDefaultPath = os.path.abspath(__file__).rsplit("\\", 1)[0]
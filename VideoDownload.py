from re import T
import re
import requests
import time
import math
import os

import settings


def resolver(request, string):
    """解析器"""
    if request == 1:
        # 电影网址去参数
        return string.rsplit("?", 1)[0]
    elif request == 2:
        # 解析视频的avid和cvid
        id_info = re.search('"epList":\[(.*?)\]', string, re.S)
        avid = re.findall('"aid":(\d+)', id_info.group(1))[0]
        cvid = re.findall('"cid":(\d+)', id_info.group(1))[0]
        return [avid, cvid]
    elif request == 3:
        # 解析视频详细信息
        name = string["data"]["title"]
        desc = string["data"]["desc"]
        return [name, desc]
    elif request == 4:
        # 去除字符串中的特殊字符
        string = string.replace(" ", "")
        string = string.replace("。", "")
        string = string.replace("/", "")
        string = string.replace("|", "")
        return string
    elif request == 5:
        # 提取BV号
        return string.rsplit("?", 1)[0].rsplit("/", 1)[1]
    elif request == 6:
        # 获取多次cid
        vid_list = []
        for page in string["data"]["pages"]:
            cid, part = page["cid"], page["part"]
            vid_list.append([part, cid])
        return vid_list
        

def get_qn():
    os.system("cls")
    print("""
    键  值
    6	240P 极速	
    16	360P 流畅	
    32	480P 清晰	
    64	720P 高清/720P60
    74	720P60 高帧率	
    80	1080P 高清	(推荐)
    112	1080P+ 高码率	
    116	1080P60 高帧率	
    120	4K 超清	
    """)
    return int(input("请输入清晰度(键)："))

def storage_unit(Byte):
    if Byte < 1024:
        return "%.2fB/s" % Byte
    elif 1024 <= Byte < 1024 ** 2:
        KB = Byte / 1024
        return "%.2fKB/s" % KB
    elif 1024 ** 2 <= Byte < 1024 ** 3:
        MB = Byte / (1024 ** 2)
        return "%.2fMB/s" % MB
    else:
        GB = Byte / (1024 ** 3)
        return "%.2fGB/s" % GB

def storage(Byte):
    if Byte < 1024:
        return "%.2fB" % Byte
    elif 1024 <= Byte < 1024 ** 2:
        KB = Byte / 1024
        return "%.2fKB" % KB
    elif 1024 ** 2 <= Byte < 1024 ** 3:
        MB = Byte / (1024 ** 2)
        return "%.2fMB" % MB
    else:
        GB = Byte / (1024 ** 3)
        return "%.2fGB" % GB

def download(vid_name, desc, stream_url, vid_size):
    os.system("cls")
    url = stream_url
    video_dw = requests.get(url=url, headers=settings.HEADERS, stream=True)
    current_size = 0
    vid_name = resolver(4, string=vid_name)
    with open(fr"{vid_name}.flv", "wb") as f:
        total = 0
        start_time = time.time()
        try:
            print(f"正在下载...{vid_name}\n")
            print(f"简介：{desc}\n")
            for chunk in video_dw.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    current_size += 1024
                    total += 1
                    f.flush()

                    speed = (1024 * total) / \
                        math.ceil(time.time() - start_time + 0.001)
                    done = int(math.ceil(20 * current_size / vid_size))
                    print("[{}{}], 已下载{}, 总共{}, 速度{}    ".format(
                        "#" * done, " " * (20-done),
                        storage(current_size), storage(vid_size),
                        storage_unit(speed)), end="\r")
        except Exception as e:
            print(e)
            print("网络不稳定，建议换一个清晰度!")

class Movie(object):

    def __init__(self, vid_url):
        self.vid_url = vid_url
        self.stream_url = None
        self.vid_size = None

    def get_movie_data(self):
        requests.get(url=self.vid_url, headers=settings.HEADERS)
        resp = requests.get(url=self.vid_url, headers=settings.HEADERS)
        return resolver(2, resp.text)

    def get_movie_info(self):
        url = "http://api.bilibili.com/x/web-interface/view"
        avid, cvid = self.get_movie_data()
        resp = requests.get(url=url, headers=settings.HEADERS, params={"aid":avid})
        vid_name, desc = resolver(3, resp.json())
        return [avid, cvid, vid_name, desc]

    def get_movie(self, avid, cvid, qn):
        url = "https://api.bilibili.com/pgc/player/web/playurl"
        params = {
            "aid": avid,
            "cid": cvid,
            "qn": qn,
        }
        resp = requests.get(url=url, headers=settings.HEADERS, params=params)
        self.stream_url = resp.json()["result"]["durl"][0]["url"]
        self.vid_size = resp.json()["result"]["durl"][0]["size"]

    def start(self):
        self.vid_url = resolver(1, self.vid_url)
        avid, cvid, vid_name, desc = self.get_movie_info()
        self.get_movie(avid, cvid, get_qn())
        download(vid_name, desc, self.stream_url, self.vid_size)

class Video(object):
    def __init__(self, vid_url):
        self.vid_url = vid_url
        self.bvid = None
        self.cid = None
        self.stream_url = None
        self.vid_size = None
    
    def get_vid_info(self, flag=0):
        url = "http://api.bilibili.com/x/web-interface/view"
        resp = requests.get(url=url, headers=settings.HEADERS, params={"bvid":self.bvid})
        if flag == 1:
            self.cid = resp.json()["data"]["cid"]
            return resolver(3, resp.json())
        elif flag == 2:
            vid_name, desc = resolver(3, resp.json())
            vid_list = resolver(6, resp.json())
            return vid_name, desc, vid_list
        else:
            self.cid = resp.json()["data"]["cid"]
            vid_name, desc = resolver(3, resp.json())
            return (vid_name, desc, resp.json()["data"]["videos"])
    
    def get_vid_stream(self, qn=0):
        url = "http://api.bilibili.com/x/player/playurl"
        resp = requests.get(url=url, headers=settings.HEADERS, params={
            "bvid": self.bvid,
            "cid" : self.cid,
            "qn" : qn if qn else get_qn()
        })
        self.stream_url = resp.json()["data"]["durl"][0]["url"]
        self.vid_size = resp.json()["data"]["durl"][0]["size"]


    def start(self):
        self.bvid = resolver(5, self.vid_url)
        vid_name, desc = self.get_vid_info(1)
        self.get_vid_stream()
        download(vid_name, desc, self.stream_url, self.vid_size)

class ListVideo(Video):
    def __init__(self, vid_url):
        self.vid_list = None
        super().__init__(vid_url)

    def loop(self):
        qn = get_qn()
        for part in self.vid_list:
            self.cid = part[1]
            self.get_vid_stream(qn)
            part.append(self.vid_size)
            part.append(self.stream_url)
        
        for part in self.vid_list:
            download(part[0], self.desc, part[3], part[2])
        

    def start(self):
        self.bvid = resolver(5, self.vid_url)
        vid_name, self.desc, self.vid_list = self.get_vid_info(2)
        print(f"正在下载...{vid_name}")
        self.loop()

class Drama(Movie):
    def __init__(self, vid_url):
        self.vid_url = vid_url
    
    def start(self):
        pass


def start():
    os.system("cls")
    print("""
    视频类型：
    1.普通视频
    2.电影
    3.番剧(不支持)
    4.分p视频(开发中)
    """)
    type = int(input("请输入视频类型："))
    vid_url = input("请输入网址：")
    if type == 1:
        Video(vid_url).start()
    elif type == 2:
        Movie(vid_url).start()
    elif type == 3:
        Drama(vid_url).start()
    elif type == 4:
        ListVideo(vid_url).start()
    
    
start()

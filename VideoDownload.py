import re
import requests
import time
import math
import os
from threading import Thread

import settings

#清晰度字典
definition = {
    127: '8K超高清',
    126: '杜比视界',
    125: 'HDR真彩',
    120: '4K超清',
    116: '1080P60帧',
    112: '1080P+高码率',
    80: '1080P',
    74: '720P60帧',
    64: '720P',
    32: '480P清晰',
    16: '320P流畅'
}
# 线程对象列表
t_lis = list()
# 所有视频的大小的列表
vids_sizes = list()


def resolver(request, string):
    """解析器"""
    if request == 1:
        # 电影网址去参数
        return string.rsplit("?", 1)[0]
    elif request == 2:
        # 解析电影的avid和cvid
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
    elif request == 7:
        # 获取每集番剧的所有aid、cid、标题；并获取番剧简介和标题
        vid_list = []
        for part in string["result"]["episodes"]:
            aid, cid, title = part["aid"], part["cid"], part["share_copy"]
            vid_list.append([aid, cid, title])
        return vid_list, string["result"]["evaluate"], string["result"]["season_title"]
    elif request == 8:
        # 番剧网址去参数
        return string.rsplit("?", 1)[0]


def get_qn():
    os.system("cls")
    print("""
    键  值
    127: '8K超高清'
    126: '杜比视界'
    125: 'HDR真彩'
    120: '4K超清'
    116: '1080P60帧'
    112: '1080P+高码率'(推荐)
    80: '1080P'
    74: '720P60帧'
    64: '720P'
    32: '480P清晰'
    16: '320P流畅'
    """)
    return int(input("请输入清晰度(键):"))


def storage_unit(Byte):
    """速度进制转换"""
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
    """进制转换"""
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


def bar(dir_name, desc, vid_num):
    while True:
        print(f"正在生成线程中...已生成{len(vids_sizes)}/{vid_num}个线程...", end="\r")
        if vid_num == len(vids_sizes):
            vid_size = sum(vids_sizes)
            break
    os.system("cls")
    print(f"正在下载...{dir_name}\n")
    print(f"简介:{desc}\n")
    # 初始化
    start_time = time.time()
    current_size = 0
    file_name = os.path.join(settings.DownloadDefaultPath, dir_name)

    # 进度条
    while True:
        current_size = 0
        # 获取信息
        for root, folder, files in os.walk(file_name):
            current_size += sum([os.path.getsize(os.path.join(root, file))
                                for file in files])
        speed = math.ceil(current_size / (time.time() - start_time + 0.001))
        done = int(math.ceil(40 * current_size / vid_size))
        # 如果饱和，则退出
        if current_size >= vid_size:
            break
        print("[{}{}], 已下载{}, 总共{}, 平均速度{}    ".format(
            "#" * done, " " * (40-done),
            storage(current_size), storage(vid_size),
            storage_unit(speed)), end="\r")


def download(file_name, desc, stream_url, vid_size):
    """下载器"""
    os.system("cls")
    # 初始化
    url = stream_url
    current_size = 0
    flag = False
    # 获取视频流
    video_dw = requests.get(url=url, headers=settings.HEADERS, stream=True)
    # 将路径名转化为文件名
    vid_name = os.path.basename(file_name)
    # 判断是否已经下载过视频
    if os.path.exists(file_name):
        if int(input(f"你已经下载过{vid_name}了，请问是否继续下载?（0:否,1:是）")):
            alreadly_size = os.path.getsize(file_name)
            settings.HEADERS["Range"] = f"bytes={alreadly_size + 1}-{vid_size}"
            flag = True
            vid_size = vid_size - alreadly_size
    with open(file_name, "ab") as f:
        total = 0
        start_time = time.time()
        try:
            print(f"正在下载...{vid_name}\n")
            print(f"简介:{desc}\n")
            # 分段写入
            for chunk in video_dw.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    current_size += 1024
                    total += 1
                    f.flush()

                    speed = (1024 * total) / \
                        (math.ceil(time.time() - start_time + 0.001))
                    done = int(math.ceil(20 * current_size / vid_size))
                    # 进度条
                    print("[{}{}], 已下载{}, 总共{}, 平均速度{}    ".format(
                        "#" * done, " " * (20-done),
                        storage(current_size), storage(vid_size),
                        storage_unit(speed)), end="\r")
        except Exception as e:
            print(e)
            print("网络不稳定，建议换一个清晰度!")
    # 重置请求头
    if flag:
        settings.HEADERS.pop("Range")


def t_download(file_name, stream_url):
    os.system("cls")
    video_dw = requests.get(
        url=stream_url, headers=settings.HEADERS, stream=True)
    with open(file_name, "wb") as f:
        for chunk in video_dw.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


class Movie(object):
    """电影的下载"""

    def __init__(self, vid_url):
        self.vid_url = vid_url
        self.stream_url = None
        self.vid_size = None
        self.file_name = None
        self.desc = None
        self.dir_name = None

    def get_movie_data(self):
        # 获取电影的avid和cvid
        requests.get(url=self.vid_url, headers=settings.HEADERS)
        resp = requests.get(url=self.vid_url, headers=settings.HEADERS)
        return resolver(2, resp.text)

    def get_movie_info(self):
        url = "http://api.bilibili.com/x/web-interface/view"
        avid, cvid = self.get_movie_data()
        resp = requests.get(
            url=url, headers=settings.HEADERS, params={"aid": avid})
        # 获取名字和简介
        vid_name, desc = resolver(3, resp.json())
        return [avid, cvid, vid_name, desc]

    def get_movie(self, avid, cvid, qn, is_t=False):
        # 获取视频流地址
        url = "https://api.bilibili.com/pgc/player/web/playurl"
        params = {
            "aid": avid,
            "cid": cvid,
            "qn": qn,
        }
        resp = requests.get(url=url, headers=settings.HEADERS, params=params)
        self.stream_url = resp.json()["result"]["durl"][0]["url"]
        self.vid_size = resp.json()["result"]["durl"][0]["size"]
        vids_sizes.append(self.vid_size)
        if is_t:
            t = Thread(target=t_download, args=(
                self.file_name, self.stream_url))
            t.start()
            t_lis.append(t)
        else:
            download(self.file_name, self.desc, self.stream_url, self.vid_size)
        

    def start(self):
        self.vid_url = resolver(1, self.vid_url)
        avid, cvid, vid_name, self.desc = self.get_movie_info()
        # 获取清晰度
        qn_key = get_qn()
        qn = definition[qn_key]
        # 拼接将要下载的文件名
        self.file_name = os.path.join(
            settings.DownloadDefaultPath, f"{vid_name}-{qn}.flv")
        self.file_name = resolver(4, self.file_name)
        self.get_movie(avid, cvid, qn_key)


class Drama(Movie):
    def __init__(self, vid_url):
        self.vid_url = vid_url
        self.vid_list = None
        self.desc = None

    def get_all_link(self):
        url = "https://api.bilibili.com/pgc/view/web/season"
        season_id = self.vid_url.rsplit("ss", 1)[1]
        resp = requests.get(url=url, headers=settings.HEADERS,
                            params={"season_id": season_id})
        self.vid_list, self.desc, self.dir_name = resolver(7, resp.json())

    def ruleToDownload(self):
        print("""
        下载集数规则:
        1-5   表示下载1到5集
        -5    表示从第一集（从头）下载到第五集
        5-    表示从第五集下载到最后
        5     表示下载第五集
        回车  表示下载所有
        """)
        flag = input("请输入规则:")
        try:
            if not flag:
                return
            elif flag.startswith("-"):
                self.vid_list = self.vid_list[:int(flag.strip("-"))]
            elif flag.endswith("-"):
                self.vid_list = self.vid_list[int(flag.strip("-"))-1:]
            elif flag.isdecimal():
                self.vid_list = [self.vid_list[int(flag)-1]]
            else:
                nums = flag.split("-")
                self.vid_list = self.vid_list[int(nums[0])-1:int(nums[1])]
        except Exception as e:
            print(e)
            print("请输入正确的规则!")
            os.system("pause")
            self.rule()

    def loop(self):
        qn = get_qn()
        vid_num = len(self.vid_list)
        # 开启进度条线程
        pb = Thread(target=bar, args=(self.dir_name, self.desc, vid_num))
        pb.start()
        t_lis.append(pb)
        for part in self.vid_list:
            self.file_name = os.path.join(
                settings.DownloadDefaultPath, self.dir_name, f"{part[2]}-{definition[qn]}.flv")
            self.file_name = resolver(4, self.file_name)
            self.get_movie(part[0], part[1], qn, is_t=True)

    def start(self):
        self.vid_url = resolver(8, self.vid_url)
        self.get_all_link()
        # 创建专门存放该番剧的文件夹
        self.dir_name = resolver(4, self.dir_name)
        path = os.path.join(settings.DownloadDefaultPath, self.dir_name)
        if not os.path.exists(path):
            os.mkdir(path)
        self.ruleToDownload()
        self.loop()


class Video(object):
    def __init__(self, vid_url):
        self.vid_url = vid_url
        self.bvid = None
        self.cid = None
        self.stream_url = None
        self.vid_size = None
        self.file_name = None
        self.desc = None
        self.dir_name = None

    def get_vid_info(self, flag=0):
        url = "http://api.bilibili.com/x/web-interface/view"
        resp = requests.get(url=url, headers=settings.HEADERS,
                            params={"bvid": self.bvid})
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

    def get_vid(self, qn, is_t=False):
        url = "http://api.bilibili.com/x/player/playurl"
        resp = requests.get(url=url, headers=settings.HEADERS, params={
            "bvid": self.bvid,
            "cid": self.cid,
            "qn": qn
        })
        self.stream_url = resp.json()["data"]["durl"][0]["url"]
        self.vid_size = resp.json()["data"]["durl"][0]["size"]
        vids_sizes.append(self.vid_size)
        if is_t:
            t = Thread(target=t_download, args=(
                self.file_name, self.stream_url))
            t.start()
            t_lis.append(t)
        else:
            download(self.file_name, self.desc, self.stream_url, self.vid_size)

    def start(self):
        self.bvid = resolver(5, self.vid_url)
        vid_name, self.desc = self.get_vid_info(1)
        #　替换视频名中的特殊字符
        vid_name = resolver(4, string=vid_name)
        # 获取清晰度
        qn_key = get_qn()
        qn = definition[qn_key]
        # 拼接将要下载的文件名
        self.file_name = os.path.join(
            settings.DownloadDefaultPath, f"{vid_name}-{qn}.flv")
        self.get_vid(qn_key)


class ListVideo(Video):
    def __init__(self, vid_url):
        self.vid_list = None
        super().__init__(vid_url)

    def loop(self):
        qn_key = get_qn()
        qn = definition[qn_key]
        vid_num = len(self.vid_list)
        # 开启进度条线程
        pb = Thread(target=bar, args=(self.dir_name, self.desc, vid_num))
        pb.start()
        t_lis.append(pb)
        # 循环下载视频
        for part in self.vid_list:
            self.file_name = os.path.join(
                settings.DownloadDefaultPath, self.dir_name, f"{part[0]}-{qn}.flv")
            self.file_name = resolver(4, self.file_name)
            self.cid = part[1]
            self.get_vid(qn_key, is_t=True)

    def ruleToDownload(self):
        print("""
        下载集数规则:
        1-5   表示下载1到5集
        -5    表示从第一集（从头）下载到第五集
        5-    表示从第五集下载到最后
        5     表示下载第五集
        回车  表示下载所有
        """)
        flag = input("请输入规则:")
        try:
            if not flag:
                return
            elif flag.startswith("-"):
                self.vid_list = self.vid_list[:int(flag.strip("-"))]
            elif flag.endswith("-"):
                self.vid_list = self.vid_list[int(flag.strip("-"))-1:]
            elif flag.isdecimal():
                self.vid_list = [self.vid_list[int(flag)-1]]
            else:
                nums = flag.split("-")
                self.vid_list = self.vid_list[int(nums[0])-1:int(nums[1])]
        except Exception as e:
            print(e)
            print("请输入正确的规则!")
            os.system("pause")
            self.rule()

    def start(self):
        self.bvid = resolver(5, self.vid_url)  # 　提取BV号
        self.dir_name, self.desc, self.vid_list = self.get_vid_info(2)
        # 创建专门存放该番剧的文件夹
        self.dir_name = resolver(4, self.dir_name)  # 除特殊字符
        path = os.path.join(settings.DownloadDefaultPath, self.dir_name)
        if not os.path.exists(path):
            os.mkdir(path)
        self.ruleToDownload()
        self.loop()


def start():
    os.system("cls")
    print("""
    视频类型:
    1.普通视频
    2.电影
    3.番剧
    4.分p视频(只要视频分P就要选这个)
    """)
    type = int(input("请输入视频类型:"))
    vid_url = input("请输入网址:")
    if type == 1:
        Video(vid_url).start()
    elif type == 2:
        Movie(vid_url).start()
    elif type == 3:
        Drama(vid_url).start()
    elif type == 4:
        ListVideo(vid_url).start()
    else:
        return

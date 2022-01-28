import os
import requests
import asyncio
import settings


like_nums = 0
coins_nums = 0
fav_nums = 0
view_nums = 0
share_nums = 0
danmaku_nums = 0
reply_nums = 0


class People(object):
    def __init__(self, space_url):
        self.space_url = space_url
        self.mid = None
        self.matchMid()

    def matchMid(self):
        self.mid = self.space_url.rsplit("/", 1)[0].split("/")[-1]


class Up(People):
    def __init__(self, space_url):
        self.space_url = space_url
        self.matchMid()
        super().__init__(space_url)

    def getBvids(self):
        # 查询用户投稿视频明细
        url = f"http://api.bilibili.com/x/space/arc/search"
        resp = requests.get(url, headers=settings.HEADERS,
                            params={"mid": self.mid, "ps": 1, "pn": 1})
        # 获取用户投稿的视频数目
        self.vid_count = resp.json()["data"]["page"]["count"]
        # 再次发送请求，保证获取所有视频
        resp = requests.get(url, headers=settings.HEADERS,
                            params={"mid": self.mid, "ps": self.vid_count, "pn": 1,
                                    })
        # 获取所有视频的bvid号
        bvid_list = [vid["bvid"]
                     for vid in resp.json()["data"]["list"]["vlist"]]
        tasks = [self.getVideoInfos(bvid) for bvid in bvid_list]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        global like_nums, coins_nums, fav_nums, view_nums, share_nums, danmaku_nums, reply_nums
        print("""总点赞数:{}\n总被投币数:{}\n总被收藏数:{}\n总视频播放量:{}\n视频总分享数:{}\n视频总弹幕数:{}\n总评论数:{}\n
        """.format(like_nums, coins_nums, fav_nums, view_nums, share_nums, danmaku_nums, reply_nums))

    async def getVideoInfos(self, bvid):
        # 初始化
        global like_nums, coins_nums, fav_nums, view_nums, share_nums, danmaku_nums, reply_nums

        # 批量发送请求
        loop = asyncio.get_event_loop()
        url = "http://api.bilibili.com/x/web-interface/view"
        future = loop.run_in_executor(None, requests.get, url, {"bvid": bvid})
        resp = await future

        # 获取数据
        like_nums += resp.json()["data"]["stat"]["like"]
        coins_nums += resp.json()["data"]["stat"]["coin"]
        fav_nums += resp.json()["data"]["stat"]["favorite"]
        view_nums += resp.json()["data"]["stat"]["view"]
        share_nums += resp.json()["data"]["stat"]["share"]
        danmaku_nums += resp.json()["data"]["stat"]["danmaku"]
        reply_nums += resp.json()["data"]["stat"]["reply"]

def start():
    os.system("cls")
    url = input("请输入up主的空间地址:")
    Up(url).getBvids()
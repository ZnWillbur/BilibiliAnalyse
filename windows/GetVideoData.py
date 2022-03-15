import requests
import settings


def getAid(bvid):
    url = "http://api.bilibili.com/x/web-interface/view"
    resp = requests.get(url, headers=settings.HEADERS, params={"bvid": bvid})
    return resp.json()["data"]["aid"]


def getReplysInfo(aid):
    url = "https://api.bilibili.com/x/v2/reply/main"
    resp = requests.get(url, headers=settings.HEADERS,
                        params={"oid": aid, "type": 1, "next":100})
    # with open("b.json", "w", encoding="utf8") as f:
    #     f.write(resp.text)
    data = [{"name": p["member"]["uname"],
             "mid":p["member"]["mid"],
             "sex":p["member"]["sex"],
             "viptype":p["member"]["vip"]["label"]["text"],
             "content":p["content"]["message"]}
            for p in resp.json()["data"]["replies"]]


getReplysInfo(getAid("BV1AZ4y1Z7ev"))

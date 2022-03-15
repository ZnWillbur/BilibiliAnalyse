import os
# 请求头
HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "referer": "https://www.bilibili.com/",
        "cookie" : "buvid3=DCE346A2-AB21-5A5F-3375-EA6EED8901CD53505infoc; i-wanna-go-back=-1; _uuid=6E31BC79-A866-11810-6769-1BB23B106A39654443infoc; blackside_state=0; rpdid=|(J~RYulml|u0J'uYRkkJRk)J; LIVE_BUVID=AUTO2816422611902632; bp_t_offset_548284877=616000015072295897; CURRENT_QUALITY=112; buvid4=822F30E4-ECD1-776D-6DB8-B30A508FAA7E83277-022012117-M/nkCpuCJYm5d411FbOnMw%3D%3D; fingerprint3=fd255356088ec99e93bfa27609f450b9; buvid_fp_plain=undefined; fingerprint=48e2329417f74b2bca6923edeaa1f31e; buvid_fp=93769538f6c66270aae3cd8dd21de771; SESSDATA=0c860123%2C1658922591%2Cac64c%2A11; bili_jct=d893b76b86764210502b5d378b71523b; DedeUserID=548284877; DedeUserID__ckMd5=0da2c57bf0551c31; sid=4she2yd3; b_ut=5; PVID=1; bp_video_offset_548284877=621191956229280800; b_lsid=6F541939_17EA8AE914E; CURRENT_BLACKGAP=0; innersign=1; CURRENT_FNVAL=4048"
}
# 默认下载路径
DownloadDefaultPath = os.path.abspath(__file__).rsplit("\\", 1)[0]
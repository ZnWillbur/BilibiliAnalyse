# Bilibili Analyse
这是一个B站的分析器，目前阶段只有下载视频的功能，其他功能会在以后慢慢完善

作者：ZnWillbur

## 使用方法
- 拥有python环境
- 安装依赖包
  ```
  pip install opencv-python
  pip install qrcode
  pip install requests
  ```
- 在文件夹中输入以下命令`python Bilibili.py`即可


## 目前的缺点
- 不支持断点续传
- 网络不稳定就会退出程序（特别是下载高清视频的时候，需要强大的WLAN）
- 登录方式为cookie手动登录
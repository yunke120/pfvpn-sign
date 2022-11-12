#coding=utf-8
import requests
import datetime

class Notify:
    def __init__(self) -> None:

        pass

# server酱
    def server(self, sckey, msg):
        self.url = 'https://sctapi.ftqq.com/' + sckey + '.send'
        data = {
            "text":"PFvpn每日签到",
            "desp":msg
        }
        requests.post(self.url, data=data, headers={'Content-type': 'application/x-www-form-urlencoded'})

# 息知
    def xizhi(self, key, msg):
        self.url = f'https://xizhi.qqoq.net/{key}.send'
        data = {
            "title":"PFvpn每日签到",
            "content":msg
        }
        requests.post(self.url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})

# 发送接口
    def send(self, key, msg):
        if key.startswith('SCT'):
            self.server(key, msg)
        elif key.startswith('XZ'):
            self.xizhi(key, msg)
        else:
            pass

#! usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
# import schedule
from notify import Notify
import time
import os

session = requests.session()
server = Notify()

print(os.environ)
print(os.environ['TEST'])
print(os.environ['USERS'])
print(os.environ['PASSWRDD'])
print(os.environ['SCKEY'])

def read_json(json_file):
    obj = json.load(open(json_file, 'r', encoding='utf-8'))
    return obj

def get_user_info(json_file):
    users = []
    try:
        USERS = os.environ['USERS']
        PASSWRDD = os.environ['PASSWRDD']
        SCKEY = os.environ['SCKEY']
        user_list = USERS.split('&')
        pwd_list = PASSWRDD.split('&')
        sckey_list = SCKEY.split('&')
        # assert len(user_list) == len(pwd_list)
        print("os")
        
        for u, p, k in zip(user_list,pwd_list,sckey_list):
            print(u,p,k)
            user = dict()
            user['username'] = u
            user['password'] = p
            user['sckey'] = k
            users.append(user)
        print(users)
    except KeyError:
        users = read_json(json_file)
        print("json")
    
    return users


def login(data):
    url = 'https://purefast.net/auth/login'
    headers = {
        'Host':'purefast.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Origin': 'https://purefast.net',
        'Referer': 'https://purefast.net/auth/login'
    }
    res = session.post(url=url, data=data, headers=headers)
    return res.status_code

def get_html():
    url = 'https://purefast.net/user'
    headers = {
        'Host': 'purefast.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Referer': 'https://purefast.net/auth/login'
    }
    res = session.get(url=url, headers=headers)
    return res.status_code, res.text

def sign():
    url = 'https://purefast.net/user/checkin'
    headers = {
        'Host': 'purefast.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Origin': 'https://purefast.net',
        'Referer': 'https://purefast.net/user',
    }
    res = session.post(url=url, headers=headers)
    return res.status_code

def get_dead_time(soup):
    data = {
        'class':'breadcrumb-item active',
        'aria-current':'page'
    }
    dead_time = soup.find_all('li', data)[0].get_text()
    dead_time = dead_time.replace('\n','').replace(' ','')
    return dead_time

def job():
    users = get_user_info('user.json') # list
    for user in users:
        print(user['username'], user['password'])
        data = {
            'email':user['username'],
            'passwd':user['password'],
            'code':''
        }
        # 登录
        login_code = login(data)
        if login_code != 200:
            continue
        # 获取网页元素
        code, html = get_html()
        if code != 200:
            continue
        # 解析
        soup = BeautifulSoup(html, 'lxml')
        try:
            sign_state = soup.select('#checkin-div > a > div > h1')[0].get_text()
        except IndexError:
            continue
        # 签到
        msg = ''
        if sign_state == "每日签到":
            sign_code = sign()
            if sign_code != 200:
                continue
            msg += "签到成功"
        else:
            msg += sign_state
        dead_time = get_dead_time(soup)
        msg += "\n"
        msg += dead_time
        # 发送通知
        server.server(user['sckey'], user['username'], msg)
        time.sleep(10*60) # 账号之间间隔一段时�?


if __name__ == '__main__':
    # job()
    pass


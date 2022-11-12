#! usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
# import schedule
from notify import Notify
import time
import os
import datetime


session = requests.session()
notify = Notify()


def read_json(json_file):
    obj = json.load(open(json_file, 'r', encoding='utf-8'))
    return obj

def get_user_info(json_file):
    users = []
    try:
        USERS = os.environ['USERS']
        PASSWRDD = os.environ['PASSWORD']
        KEY = os.environ['KEY']
        user_list = USERS.split('&')
        pwd_list = PASSWRDD.split('&')
        key_list = KEY.split('&')
        # assert len(user_list) == len(pwd_list)
        
        for u, p, k in zip(user_list,pwd_list,key_list):
            print(u)
            user = dict()
            user['username'] = u
            user['password'] = p
            user['key'] = k
            users.append(user)
    except KeyError:
        users = read_json(json_file)
    
    return users


def login(data):
    url = 'https://purefast.net/auth/login'
    headers = {
        'Host':'purefast.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Origin': 'https://purefast.net',
        'Referer': 'https://purefast.net/auth/login'
    }
    try:
        time.sleep(2) # 服务器在请求时会编译一些热点或服务数据，请求过快会导致连接失败 error 104
        res = session.post(url=url, data=data, headers=headers)
        return res.status_code
    except ConnectionError:
        return -1
    

def get_html():
    url = 'https://purefast.net/user'
    headers = {
        'Host': 'purefast.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Referer': 'https://purefast.net/auth/login'
    }
    time.sleep(2)
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
    time.sleep(2)
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

def get_link_id(soup):
    links = soup.find_all('a', {"href":"##"})
    link = ''
    for l in links:
        link = l.attrs.get('data-clipboard-text')
        if link:
            break
    return link[41:57]

def get_addr(id):
    return f'https://whoisyourdady.gfw-wdnmd.com/link/pRkl1txcHqKLc5Uv?clash=1'

def diy_content(username, msg, id):
    current_time = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    content = {
        "------\n"
        "### PFvpn签到信息\n"
        "- 用户账号：" + str(username) + "\n"
        "- 签到状态：" + str(msg) + "\n"
        "- 签到时间：" + current_time + "\n"
        "\n"
        "### 订阅地址\n"
        "> 若网速不正常，请更新订阅地址\n"
        "\n"
        "- clash：" + f'https://whoisyourdady.gfw-wdnmd.com/link/{id}?clash=1' + "\n"
        "- kitsunebi：" + f'https://whoisyourdady.gfw-wdnmd.com/link/{id}?list=kitsunebi' + "\n"
        "- quantumultx：" + f'https://whoisyourdady.gfw-wdnmd.com/link/{id}?list=quantumultx' + "\n"
        "- shadowrocket：" + f'https://whoisyourdady.gfw-wdnmd.com/link/{id}?list=shadowrocket' + "\n"
        "- trojan：" + f'https://whoisyourdady.gfw-wdnmd.com/link/{id}?sub=3'
    }

    return content

def job():
    users = get_user_info('user.json') # list
    for user in users:
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
        msg += dead_time
        id = get_link_id(soup)
        content = diy_content(user['username'], msg, id)
        # 发送通知
        notify.send(user['key'],  content)
        time.sleep(10) # 账号之间间隔一段时间


if __name__ == '__main__':
    job()

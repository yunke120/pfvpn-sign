# PFvpn-Sign

[PFvpn](https://purefast.net/)每日签到脚本

>分支`main`为`selenium`开发
>
>分支`re`为`requests`开发（推荐）

## 介绍

PFvpn提供了全球网络中继服务，免费版需要每日签到以获取会员天数和流量，国内网速达15Mbps

注册链接：https://purefast.net/auth/register?code=OeJl

## 使用

## 软件使用方式

通过注册[链接](https://purefast.net/auth/register?code=OeJl)进行注册，点击以下按钮复制订阅链接

<img src="figures/image-20221026182104326.png" alt="image-20221026182104326" style="zoom: 50%;" />

下载软件[Winxray](https://github.com/TheMRLL/WinXray.git)，具体使用方式参见其说明文件，将订阅链接拷贝进去更新订阅即可

<img src="figures/image-20221026182500357.png" alt="image-20221026182500357" style="zoom:50%;" />

### 签到脚本使用方式

#### 环境

> Window, Python>3.6

！注意：chromedriver.exe的版本需与自己chrome浏览器版本一致，下载地址：[点击](https://registry.npmmirror.com/binary.html?path=chromedriver/)

#### 步骤

1、克隆仓库

```
$git  clone https://github.com/yunke120/pfvpn-sign.git
```

2、修改`user.json`（将`user_sample.json`拷贝并重命名）

| 属性     | 值                                    |
| -------- | ------------------------------------- |
| username | 用户邮箱                              |
| password | 用户密码                              |
| sckey    | [Server酱](https://sct.ftqq.com/)密钥 |

支持多用户，示例

```json
[
    {
        "username":"example1@163.com",
        "password":"12345678",
        "sckey":"SCT*****"
    },
    {
        "username":"example2@qq.com",
        "password":"1234567890",
        "sckey":"SCT*****"
    }
]
```

3、修改`config.json`

`chrome_path`对应的是你的电脑中chrome浏览器的路径，如

```json
{
    "chrome_path": "C:/Program Files/Google/Chrome/Application/chrome.exe"
}
```

4、运行

```
$python main.py
```

5、运行结果截图

<img src="figures/image-20221027100331016.png" alt="image-20221027100331016" style="zoom:50%;" />

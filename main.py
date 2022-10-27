
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.common import exceptions as ex
import json
import time
import notify

def read_json(json_file):
    obj = json.load(open(json_file, 'r', encoding='utf-8'))
    return obj

def create_browser(chrome_path):
    chrome_options = ChromeOptions()
    chrome_options.binary_location = chrome_path
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    service = Service("chromedriver.exe")

    browser = webdriver.Chrome(service=service, options=chrome_options)
    return browser

if __name__ == '__main__':
    config = read_json('config.json')
    users = read_json('user.json')
    
    path = config['chrome_path']
    browser = create_browser(path)
    
    send = notify.Notify()

    url = 'https://purefast.net/auth/login'
    for user in users:
        # print(user['username'])
        browser.get(url)
        time.sleep(5)
        try:
            browser.find_element(By.ID, 'email').send_keys(user['username'])
            time.sleep(2)
            browser.find_element(By.ID, 'password').send_keys(user['password'])
            time.sleep(2)
            browser.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(3)
            browser.find_element(By.XPATH, '//button[@type="button"]').click()
            time.sleep(2)

            btn_sign = browser.find_element(By.XPATH, '//div[@id="checkin-div"]/a/div/h1')
            state = btn_sign.text
            if state == "今日已签到":
                pass
                #result = browser.find_element(By.XPATH, '//div[@id="app"]/div/div[3]/section/div[3]/div[1]/div/div[3]/div/nav/ol/li')
                
                #msg = result.text
                #send.server(user['sckey'], user['username'], msg)
            else:
                btn_sign.click()
                time.sleep(5)
                browser.refresh()
                time.sleep(5)
                browser.find_element(By.XPATH, '//button[@type="button"]').click()
                time.sleep(2)
                result = browser.find_element(By.XPATH, '//div[@id="app"]/div/div[3]/section/div[3]/div[1]/div/div[3]/div/nav/ol/li')
                
                msg = result.text
                send.server(user['sckey'], user['username'], msg)
        except ex.NoSuchElementException:
            error_log = "错误信息: NoSuchElementException"
            send.server('SCT5575TQTnNQ5vzVzQBuOQ3YtXXlg4D', user['username'], error_log)
        except ex.ElementNotInteractableException:
            error_log = "错误信息: ElementNotInteractableException"
            send.server('SCT5575TQTnNQ5vzVzQBuOQ3YtXXlg4D', user['username'], error_log)
    browser.quit()
        
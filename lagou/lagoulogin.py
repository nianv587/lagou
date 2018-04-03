import requests
import redis
from selenium import webdriver
import time
from lagou.settings import REDIS_URL

session = requests.session()
reds = redis.Redis.from_url(REDIS_URL, db=5, decode_responses=True)
Lagou_Account = [
    ('', ''),
]

HEADERS = {
    'Referer': 'https://passport.lagou.com/login/login.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
}




def get_cookies(username, passwd):
    # 使用selenium模拟登陆并获取cookies
    browser = webdriver.Chrome(executable_path="C:/Scrapy_projects/chromedriver.exe")
    browser.get("https://passport.lagou.com/login/login.html")
    time.sleep(6)
    browser.find_element_by_xpath("//input[@type='text']").clear()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(username)
    browser.find_element_by_xpath("//input[@type='password']").clear()
    browser.find_element_by_xpath("//input[@type='password']").send_keys(passwd)
    browser.find_element_by_xpath("//input[@type='submit']").click()
    time.sleep(5)

    cookie = browser.get_cookies()
    print(cookie)
    browser.close()
    if cookie:
        return cookie
    else:
        return get_cookies()

def init_lagou_cookie(red, spidername):
    for lagou in Lagou_Account:
        if red.get("%s:Cookies:%s" % (spidername, lagou[0])) is None:
            cookie = get_cookies(lagou[0], lagou[1])
            red.set("%s:Cookies:%s" % (spidername, lagou[0]), cookie)

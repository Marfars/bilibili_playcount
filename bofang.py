import time
import traceback
from threading import Thread

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def Change_The_Time_Type(str_time):
    m, s = str_time.split(':')
    return int(m) * 60 + int(s)


# your spider code

def play_one(video_url):
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    delete_proxy(proxy)  # 立刻删除代理池中代理，以后要优化可以改成使用队列，保证多线程安全

    while retry_count > 0:
        try:
            # 设置代理
            # chromeOptions = webdriver.ChromeOptions()
            # chromeOptions.add_argument(f"-proxy-server=http：//{proxy}")
            options = Options()
            options.add_argument(f"-proxy-server=http：//{proxy}")
            options.add_argument('--no-sandbox')

            # 我真是大开眼界，--改成-，冒号改成中文，才能用
            # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
            # browser = webdriver.Chrome(r'C:\Program Files\Google\Chrome\Application/chromedriver.exe',
            #                            options=chromeOptions)

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # 使用代理访问
            # 打开视频播放页
            driver.get(video_url)

            time.sleep(5)

            # 两倍速似乎有bug，b站会认为只播放了一半，取消之
            # 两倍速
            element = driver.find_element(by=By.XPATH,
                                          value="//div[@class='bpx-player-ctrl-btn bpx-player-ctrl-playbackrate']")
            webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
            element = driver.find_element(by=By.XPATH, value="//ul[@class='bpx-player-ctrl-playbackrate-menu']/li[4]")
            webdriver.ActionChains(driver).move_to_element(element).click(element).perform()

            # 获取视频时长
            # element=driver.find_element_by_xpath("//ul[@class='bilibili-player-video-btn-speed-menu']/li[1]")
            # webdriver.ActionChains(driver).move_to_element(element)
            Video_Time = driver.find_element(by=By.CSS_SELECTOR, value="span.bpx-player-ctrl-time-duration").text
            print(Video_Time)
            Total_Second = Change_The_Time_Type(Video_Time)
            print(Total_Second)

            # 点击播放
            # element=driver.find_element_by_xpath("//div[@class='bpx-player-ctrl-btn bpx-player-ctrl-play']")
            # webdriver.ActionChains(driver).move_to_element(element).click(element).perform()

            # 页面最小化
            driver.minimize_window()

            # 看完视频
            time.sleep(Total_Second)  # 留出5秒余度

            # https://blog.csdn.net/HGGshiwo/article/details/107661135
            return

        except Exception as e:
            traceback.print_exc()
            retry_count -= 1
        finally:
            # 关闭页面
            driver.close()

    return None


def always_play(url):
    while True:
        play_one(url)


thread = 5  # 5个线程
url = 'https://www.bilibili.com/video/BV1JQ4y1L7w7'

thread_list = [Thread(target=always_play, args=(url,)) for _ in range(thread)]
for t in thread_list:
    t.start()
    time.sleep(12)

'''
for t in thread_list:
    t.join()
'''

# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

# 打开浏览器：
browser = webdriver.Chrome()

browser.set_page_load_timeout(30)
browser.set_script_timeout(30)

# 在此时间范围内智能等待操作完成
browser.implicitly_wait(30)

# 每次点击链接后等待的秒数，用于观察操作效果
wait_time = 5

# 打开url:
browser.get(r"http://www.baidu.com")
time.sleep(wait_time)

# 获取输入框和提交按钮
search_input = browser.find_element_by_id("kw")
search_submit = browser.find_element_by_id("su")

# 输入Python
search_input.send_keys("Python")

# 点击「百度一下」按钮
search_submit.click()
time.sleep(wait_time)

# 获取百度百科的链接
target = browser.find_element_by_partial_link_text("Python_百度百科")
target.click()

# 关闭
browser.quit()

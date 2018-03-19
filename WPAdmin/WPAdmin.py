#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver

#def save_shot(driver):
#	shot_name = str(int(time.time() * 1000 )) + ".png"
#	driver.get_screenshot_as_file(shot_name)
#	print ""
	
def login(url,user,passwd):
	browser = webdriver.Chrome()
#	browser = webdriver.PhantomJS()
	browser.implicitly_wait(5)

	browser.get(url)
	
	user_login_ele = browser.find_element_by_id("user_login")
	user_login_ele.clear()
	user_login_ele.send_keys(user)

	user_pass_ele = browser.find_element_by_id("user_pass")
	user_pass_ele.clear()
	user_pass_ele.send_keys(passwd)

#	save_shot(browser)

	wp_submit = browser.find_element_by_id("wp-submit")
	wp_submit.submit()

#	save_shot(browser)
	
	return browser
	



#!/usr/bin/python
# -*- coding: utf-8 -*-

import WPAdmin

class PostNew:

	__title_id = "title"
	__content_id = "content"
	__submit_id = "publish"
	__content_html_btn_id = "content-html"

	driver = None
	
	def __init__(self,driver):

		
		self.driver = driver
		self.driver.get("http://www.hsjrzb.com/wp-admin/post-new.php")


	def add_image(self,url):
		self,driver.find_element_by_css_selector("#insert-media-button").click()
		self,driver.find_element_by_css_selector(".media-menu .media-menu-item:last").click()

		url_ele = self.driver.find_element_by_css_selector("#embed-url-field")
		url_ele.clear()
		url_ele.sendKeys(url)

		self.driver.find_element_by_css_selector(".button.media-button.button-large.media-button-select").click()
		#alt_ele = self.driver.find_element_by_css_selector("alignment")


		


	def set_title(self,title):
		ele = self.driver.find_element_by_id(self.__title_id)
		ele.clear()
		ele.send_keys(title)
		
	#	WPAdmin.save_shot(self.driver)	

	def set_html_content(self,content):

		self.driver.find_element_by_id(self.__content_html_btn_id).click()
		
		ele = self.driver.find_element_by_id(self.__content_id)
		ele.send_keys(content)
	
	
	#	WPAdmin.save_shot(self.driver)

	def save(self):
		ele = self.driver.find_element_by_id(self.__submit_id)
		self.driver.execute_script("scrollTo(0,0)")
#		self.driver.execute_script("arguments[0].scrollIntoView();", ele)
			
		ele.click()
	

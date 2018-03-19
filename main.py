#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser,logging,sys,config,news,os,news as news_service
import yahoo_spider.yahoo_spider as yahoo_spider
from WPAdmin.post_new import PostNew
from WPAdmin.WPAdmin import login
reload(sys)
sys.setdefaultencoding("utf-8")
	

driver = login("http://www.hsjrzb.com/wp-admin","root","12qw@#QW")

def update_to_site():

	news_list = os.listdir(config.WAIT_PUBLISH_DIR)
	
	
	for file_name in news_list:

		news = news_service.get_news(config.WAIT_PUBLISH_DIR,file_name)
		
		title = news.get("title")
		article = news.get("article")

		post = PostNew(driver)
		post.set_title(title)
		post.set_html_content(article)
		post.save()
		
		news_service.remove(config.WAIT_PUBLISH_DIR,file_name)


if __name__ == "__main__":

	if False == os.path.exists(config.WAIT_PUBLISH_DIR):
		os.mkdir(config.WAIT_PUBLISH_DIR)
	
	while True:
		try:
	
			logging.getLogger().setLevel(logging.INFO)
			yahoo_spider.start()
			update_to_site()
		except BaseException,e:
			logging.error(repr(e))

#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging,sys,newsdb,WPAdmin.WPAdmin
from yahooSpider.yahooSpider import getList
from translate import english_to_china
from WPAdmin.post_new import PostNew
from WPAdmin.WPAdmin import login



def __new_driver():
	


def save(news):
	


def __save():
	



reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("./WPAdmin")

logging.getLogger().setLevel(logging.INFO)

news_list = getList()
driver = login("http://www.hsjrzb.com/wp-admin","root","12qw@#QW")

for news in news_list:
	title = english_to_china(news.get("title"))
	
	count = newsdb.count_by_title(title)

	if count != 0:
		logging.info("news already exists" + title )
		continue
	
	article = english_to_china(news.get("article"))
	
	post = PostNew(driver)
	post.set_title(title)
	post.set_html_content(article)
	post.save()
	
		
	

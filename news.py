#!/usr/bin/sh
# -*- coding: utf-8 -*-

import json,os,hashlib,sys
reload(sys)
sys.setdefaultencoding("utf-8")

def name_generate(src):
	md5 = hashlib.md5()
	md5.update(src)
#	src = src.replace("/","").replace("\\","").replace("?","")

	return md5.hexdigest()
def remove(path,file_name):
#	file_name = name_generate(title)
	os.remove(path + file_name)

def save_to_file(path,title,data):
		
	file_name = name_generate(title)

	news_file = open(path + file_name,'w')

	content = json.dumps(data)

	news_file.write(content)

	news_file.close()

def get_news_list(d):
	return os.listdir(d)

def exists(d,title):

	
	file_name = name_generate(title)

	return os.path.exists(d + file_name)

def get_news(d,name):

	f = open(d + name)

	content = f.read()
	
	f.close()
	
	return json.loads(content)

def news_list(d):
	return os.listdir(d)

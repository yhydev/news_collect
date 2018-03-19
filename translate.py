#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests,logging,hashlib,time,random,logging,re
from pyquery import PyQuery




__headers = {

	"Host":"fanyi.youdao.com",
	"Connection":"keep-alive",
	"Accept":"application/json, text/javascript, */*; q=0.01",
	"Origin":"http//fanyi.youdao.com",
	"X-Requested-With":"XMLHttpRequest",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
	"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
	"Referer":"http//fanyi.youdao.com/",
	"Accept-Encoding":"gzip, deflate",
	"Accept-Language":"zh-CN,zh;q=0.9",
	"Cookie":"OUTFOX_SEARCH_USER_ID=771637037@10.168.8.61;"
}


__url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

__client = "fanyideskweb"

__code = "ebSeFb%=XZ%T[KZ)c(sy!"
__max_charcter = 5000
language_en = "en"
language_zh_CHS = "zh-CHS"


def __section_slice(src,maxlen):

	if len(src) <=  maxlen:
		return [src]

	i = maxlen
	
	section_arr = [];
	
	while i > 0:
		if src[i] == "." and src[i-1].islower():
			section_arr.append(src[0 : i + 1])
			
			section = __section_slice(src[i + 1:],maxlen)
			section_arr.extend(section)
			break
		i = i - 1
	return section_arr




def __generate_data(content,from_language,to_language):

	salt = int(time.time() * 1000) + int(random.random() * 10)
	
	md5 = hashlib.md5()

	md5.update(__client +  content + str(salt) + __code)
	
	sign = md5.hexdigest()
		

	form_data = {
		"i":content,
		"from":from_language,
		"to":to_language,
		"smartresult":"dict",
		"client":"fanyideskweb",
		"salt":salt,
		"sign":sign,
		"doctype":"json",
		"version":"2.1",
		"keyfrom":"fanyi.web",
		"action":"FY_BY_CLICKBUTTION",
		"typoResult":"false"	
	}

	return form_data
	
def __translate(content,from_language,to_language):
	

	logging.info("start translateing ...")	

	data_param  = __generate_data(content,from_language,to_language)

	resp = requests.post(__url,
		data = data_param,
		headers = __headers)

	if resp.status_code != 200:
		logging.warning("translate failed,response status code " + str(resp.status_code))
		return None
	
	

	resp_json = resp.json()

	errorCode = resp_json.get("errorCode")
	
	if errorCode != 0:
		logging.warning("translate failed,response json errorCode " + str(errorCode))
		return None

	translate_array = resp_json.get("translateResult")
	
	return translate_array





def translate(content,from_language,to_language):

	sections = __section_slice(content,__max_charcter)
	
	translate_res = []	

	for section in sections:
		
		res = __translate(section,from_language,to_language)

		if res == None:
			continue
		
		translate_res.extend(res)
		
	return translate_res


def translate_to_text(content,from_language,to_language):

	trans_res_list = translate(content,from_language,to_language)

	ret_res = "";

	for trans_res in trans_res_list:
		ret_res = ret_res + trans_res[0].get("tgt")
	
	return ret_res


def translate_html(src):
	
	text = PyQuery(src).text()

	text = re.sub(r"<([\s|\S]*)img([\s|\S]*)>","",text);


	sections = __section_slice(text,__max_charcter)
	ret_arr = []

	for section in sections:
		
		result = translate(section)
		if result == None:
			continue
		ret_arr.extend(result)
	
	for ret in ret_arr:


#		print(ret)
		re_str = ret[0].get("src")
		re_rep = ret[0].get("tgt")

#		print("\t\t"+re_str + "\n\n\n\n\n")
#		src = re.sub(re_str,re_rep,text,1)
		src = src.replace(re_str,re_rep,1)
	

	return src;





if __name__ == "__main__":
	logging.getLogger().setLevel(logging.INFO)

	res = 	translate_to_text("""
	fuck you

""",language_en,language_zh_CHS)

	print(res.encode("utf8"))

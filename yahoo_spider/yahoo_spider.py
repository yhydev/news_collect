#!/usr/bin/python

import sys,requests,json,logging,os,thread
sys.path.append("..")
reload(sys)
sys.setdefaultencoding("utf-8")

import translate, news as news_service
from pyquery import PyQuery as pq
from config import TMP_DIR as yahoo_tmp_dir
from config import NEWS_DIR as yahoo_news_dir,WAIT_PUBLISH_DIR as yahoo_wati_publish_dir
headers = {
	"Origin": "https://finance.yahoo.comi",
	"X-Requested-With": "XMLHttpRequest",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
	"Content-Type": "application/json",
	"Referer": "https://finance.yahoo.com/commodities",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "zh-CN,zh;q=0.9",
	"Cookie": "B=5n0fuphd7u0ts&b=3&s=1s; yvapF=%7B%22vl%22%3A29.201426%2C%22rvl%22%3A1%2C%22al%22%3A236.44370499999977%2C%22rcc%22%3A0%2C%22ac%22%3A3%2C%22cc%22%3A1%7D"
}

data = {"requests":{"g0":{"resource":"StreamService","operation":"read","params":{"ui":{"comments":"true","comments_offnet":"true","dispatch_content_store":"true","editorial_featured_count":1,"image_quality_override":"true","link_out_allowed":"true","needtoknow_template":"filmstrip","ntk_bypassA3c":"true","pubtime_maxage":0,"relative_links":"true","show_comment_count":"true","smart_crop":"true","storyline_count":2,"storyline_enabled":"true","storyline_min":2,"summary":"true","thumbnail_size":100,"tiles":{"allowPartialRows":"true","doubleTallStart":0,"featured_label":"false","gradient":"false","height":175,"resizeImages":"false","textOnly":[{"backgroundColor":"#fff","foregroundColor":"#000"}],"width_max":300,"width_min":200},"view":"mega","editorial_content_count":6,"enable_lead_fallback_image":"true","lead_fallback_image":"https://s.yimg.com/dh/ap/my/themes/dark_1366x854_01_prog.jpg"},"forceJpg":"true","offnet":{"include_lcp":"true","use_preview":"true","url_scheme":"domain"},"video":{"enable_video_enrichment":"true"},"ads":{"ad_polices":"true","contentType":"video/mp4,application/x-shockwave-flash,application/vnd.apple.mpegurl","count":25,"frequency":4,"inline_video":"true","partial_viewability":"true","pu":"finance.yahoo.com","se":4492794,"spaceid":97327075,"start_index":1,"timeout":0,"type":"STRM,STRM_CONTENT,STRM_VIDEO","useHqImg":"true","useResizedImages":"true"},"batches":{"pagination":"true","size":10,"timeout":1500,"total":170},"enableAuthorBio":"true","max_exclude":0,"min_count":3,"service":{"specRetry":{"enabled":"false"}},"category":"YFINANCE:GC=F,ZG=F,SI=F,ZI=F,PL=F,HG=F,PA=F,CL=F,HO=F,NG=F,RB=F,BZ=F,B0=F,C=F,O=F,KW=F,RR=F,SM=F,BO=F,S=F,FC=F,LH=F,LC=F,CC=F,KC=F,CT=F,LB=F,OJ=F,SB=F","pageContext":{"pageType":"yfinlist","eventName":"","topicName":"","category":"","quoteType":"","calendarType":"","screenerType":""}}}},"context":{"feature":"canvassOffnet,enableChartiqFeedback,newContentAttribution,relatedVideoFeature,videoNativePlaylist,enableESG,enableCrypto,livecoverage,enableSingleRail,enableSKTVLrec,savingsMmaRates","bkt":["fn-sa-3","fdw-stream-curated-10-ss"],"crumb":"1.i/N6Lrrf0","device":"desktop","intl":"us","lang":"en-US","partner":"none","prid":"45hmjcdd9psoa","region":"US","site":"finance","tz":"Asia/Hong_Kong","ver":"0.102.1151"}}

url = "https://finance.yahoo.com/_finance_doubledown/api/resource?bkt=fn-sa-3%2Cfdw-stream-curated-10-ss&crumb=1.i%2FN6Lrrf0&device=desktop&feature=canvassOffnet%2CenableChartiqFeedback%2CnewContentAttribution%2CrelatedVideoFeature%2CvideoNativePlaylist%2CenableESG%2CenableCrypto%2Clivecoverage%2CenableSingleRail%2CenableSKTVLrec%2CsavingsMmaRates&intl=us&lang=en-US&partner=none&prid=45hmjcdd9psoa&region=US&site=finance&tz=Asia%2FHong_Kong&ver=0.102.1151"


yahoo_news_title = "title"
yahoo_news_summary = "summary"
yahoo_news_url = "url"
yahoo_news_article = "article"

from_language = translate.language_en
to_language = translate.language_zh_CHS

#yahoo_tmp_dir = "tmp/"
#yahoo_news_dir = "news/"

def __article_handle(content):
	
	dou_hao = u'\u3002'	
	rep = u'\u3002</p><p>'	

	return content.replace(dou_hao,rep) + "http://www.hsjrzb.com";

def __save_to_tmp():

	logging.info("---yahoo spider start work---")

	# post data
	response = requests.post(url,data = json.dumps(data),headers = headers)

	# Is response success
	if(response.status_code != 200):
		logging.warning("yahoo site response status code is %d" % response.status_code)
		return 
	
	# get data for json
	resp_content = response.json()

	newsList = resp_content.get("g0").get("data").get("stream_items")

	logging.info("start parse news ..")
	
	# parse data and append $yahoo_news_list
	for news in newsList:
		
		news_title = news.get(yahoo_news_title)
		
		if news_service.exists(yahoo_tmp_dir,news_title):
			continue
			
		news_url = news.get(yahoo_news_url)

		if(news_url == None):
			continue	
			
		isNews = news_url.find("https://finance.yahoo.com/") 		
	
		if isNews == 0:

			logging.info("parseing..")

			news_summary = news.get(yahoo_news_summary)
			logging.info("parse success, title:\t" + news_title)				
			yahoo_news = {
					yahoo_news_title: news_title,
					yahoo_news_url: news_url,
					yahoo_news_summary: news_summary,
				}

			news_service.save_to_file(yahoo_tmp_dir,news_title,yahoo_news)




def __get_content(url):
	
	resp = requests.get(url)

	if resp.status_code != 200:
		logging.info("parse content fail,response error code is %d" % resp.status_code)
		return 

	html = pq(resp.text)
	html = html(yahoo_news_article).text()
	
	return html


def __save_to_news():

	tmp_news_list = os.listdir(yahoo_tmp_dir)
	
	for tmp_news in tmp_news_list:
		
		file_name = yahoo_tmp_dir + tmp_news

		news_file = open(file_name,"r")
		news_content = news_file.read()
		news = json.loads(news_content)

		news_title = news.get(yahoo_news_title)
		
		if news_service.exists(yahoo_news_dir,news_title):
			logging.info("news already exists")
			continue
						
		content = __get_content(news.get(yahoo_news_url))	

		if content == None:
			logging.info("news content not collect")
			continue
			
		translate_content = translate.translate_to_text(content,from_language,to_language)
		translate_title = translate.translate_to_text(news_title,from_language,to_language)

	
		translate_content = __article_handle(translate_content)



		translate_res =  {
			yahoo_news_article:translate_content,
			yahoo_news_title:translate_title
		}

		news_service.save_to_file(yahoo_wati_publish_dir,news_title,translate_res)
		news_service.save_to_file(yahoo_news_dir,news_title,translate_res)


def start():

	if False == os.path.exists(yahoo_tmp_dir):
		os.mkdir(yahoo_tmp_dir)


	if False == os.path.exists(yahoo_news_dir):
		os.mkdir(yahoo_news_dir)

	__save_to_tmp()
	__save_to_news()


if __name__ == "__main__":
	logging.getLogger().setLevel(logging.INFO)
	start()
	
	




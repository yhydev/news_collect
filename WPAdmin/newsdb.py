#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb,logging,time

DB_HOST = "hk01.hsjrzb.com"
DB_USER = "root"
DB_PORT = 3306
DB_PASS = "mysqlpasswd"
DB_NAME = "wordpress"

def get_conn():
	return MySQLdb.connect(host = DB_HOST,port = 3306, user = DB_USER,passwd = DB_PASS,
	db = DB_NAME, use_unicode = True, charset = "utf8")



def count_by_title(title):
	conn = get_conn()
	cursor = conn.cursor()
	
	sql = "select count(1) from wp_posts where post_title = '%s'" % (title)
	cursor.execute(sql)
	result = cursor.fetchall()
	count = 0
	for row in result:
		count = row[0]
	cursor.close()
	conn.close()
	return count	

def find_max_id():
	conn = get_conn()
	cursor = conn.cursor()
	
	sql = "select max(id) from wp_posts"
	cursor.execute(sql)
	result = cursor.fetchall()
	maxid = 0
	for row in result:
                count = row[0]
        cursor.close()
        conn.close()
        return count


def create(data):
	conn = get_conn()
	cursor = conn.cursor()

	curr_date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
	curr_id = find_max_id()

	data["curr_date"] = curr_date
	data["curr_id"] = curr_id + 1



	sql = """INSERT INTO `wp_posts` VALUES ({0[curr_id]},1,'{0[curr_date]}','{0[curr_date]}','{0[article]}','{0[title]}','','publish','open','open','','{0[title]}','','','{0[curr_date]}','{0[curr_date]}','',0,'http://www.hsjrzb.com/?p={0[curr_id]}',0,'post','',0)""".format(data)

	logging.info("create news start..")
	cursor.execute(sql)
	conn.commit()
	cursor.close()
        conn.close()
if __name__ == "__main__":
	get_conn()

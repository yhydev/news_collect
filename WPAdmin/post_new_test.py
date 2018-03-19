#!/usr/bin/python
# -*- coding: utf-8 -*-

from post_new import PostNew
import WPAdmin


def start():
	brower = WPAdmin.login("http://www.hsjrzb.com/wp-admin","root","12qw@#QW")

	post = PostNew(brower)

	post.set_title("this is title")
	post.set_html_content("this is content")
	
	post.save()
	return brower


if __name__ == "__main__":
	start()

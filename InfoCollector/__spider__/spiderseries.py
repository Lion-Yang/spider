#!/usr/bin/python
# -*-coding:utf-8-*-
import urllib2
import requests
import sys
import os
from __util__.library import handle_data, mail_notification, TransException, my_retry
from bs4 import BeautifulSoup
from __configure__.ConfigureParser import ConfigureParser
import json
reload(sys)

sys.setdefaultencoding('utf8')

Configure = ConfigureParser('./__configure__/configure.xml')
admin = Configure.get_configure_by_tag_name('admin')


@mail_notification(admin)
@my_retry
def handle_series(url, element, attribute, value, crawl_type, post_urls):
    """
    get data from the baidu api url and post it to post url
    :param url: the api url
    :param element: the element in the html source where the keyword exists
    :param attribute: the attribute of the element which can specify the element
    :param value: the value of the attribute
    :param crawl_type: the type of the target rank we need
    :param post_urls: the post urls
    :return: none
    """
    list_page = urllib2.urlopen(url).read()
    list_page = unicode(list_page, 'GBK').encode('UTF-8')
    list_soup = BeautifulSoup(list_page, "html.parser")
    list_soup = list_soup.find_all(element, {attribute: value})
    data = '{"keywords":['
    for item in list_soup:
        data = data + '"' + item.text + '",'
    data = data[0:len(data) - 1] + '],"nature":"%s"}' % crawl_type
    data = handle_data(data)    # encrypt and update the data
    print data
    for post_url in post_urls:
        print post_url
        response = requests.post(post_url, json=data, verify=False)     # post the data
        js = json.loads(response.text)
        print js
        if js['status'] != 200:
            raise TransException("Something wrong when post the data to {}, the wrong message is {}".format(post_url, js['data']))
        print response.status_code

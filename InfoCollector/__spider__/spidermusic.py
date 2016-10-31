#!/usr/bin/python
# -*-coding:utf-8-*-
import urllib2
import json
import requests
import datetime
import re
import sys
from __util__.library import handle_data, mail_notification, TransException, my_retry
from __configure__.ConfigureParser import ConfigureParser
reload(sys)
sys.setdefaultencoding('utf8')

Configure = ConfigureParser('./__configure__/configure.xml')
admin = Configure.get_configure_by_tag_name('admin')


def get_now_time():
    """
    to get the last date when there is a music rank list on QQ music
    the rank list may update late, so give a timedelta 4 days.
    :return: a string of date such as: 2016-8-20
    """
    now = datetime.datetime.now() - datetime.timedelta(3)
    return now.strftime('%Y-%m-%d')


def get_current_nums():
    """
    get the current number of the rank list
    :return: a string of year and the number such as: 2016_37, presenting the 37th rank list of 2016
    """
    base = 37   # it is 37th during 2016.9.14-2016.9.21, set as the base data
    now = datetime.datetime.now()
    if now.year == 2016:
        time_delta = now - datetime.datetime.strptime('2016-9-15', '%Y-%m-%d')  # minute 2016.9.15 to judge how many days after 9.15
        delta = (time_delta.days-3) / 7
        return '2016_' + str(base + delta)
    else:
        year = now.year
        time_delta = now - datetime.datetime.strptime('{}-1-1'.format(year), "%Y-%m-%d")
        return str(year) + '_' + str(time_delta / 7 + 1)


def get_url(base_url):
    """
    get the api url of QQ music, some url base on the date and some url base on the number.
    :param base_url: the template url of QQ music
    :return: all the api url of QQ music
    """
    urls = []
    base_on_date = [4, 25, 27, 23]  # rank lists update every day
    base_on_num = [26, 28, 5, 6, 3, 16, 17]  # rank lists update every week
    date = get_now_time()
    num = get_current_nums()
    for each in base_on_date:
        urls.append(base_url.format(date, each))
    for each in base_on_num:
        urls.append(base_url.format(num, each))
    return urls


@mail_notification(admin)
@my_retry
def refresh_data(url, post_urls):
    """
    to get music data through the api url and post the data to the post url
    :param url: the api url
    :param post_urls: the post urls
    :return: post the data to the post url
    """
    list_page = urllib2.urlopen(url).read()
    print url
    list_page = list_page[26:len(list_page) - 1]     # get the source of the url, return a json string
    put_data = '['
    data = json.loads(list_page)
    for term in data["songlist"]:
        song = term["data"]["songname"]
        p = re.compile(r'\(.*\)')
        song = p.sub('', song)
        put_data = put_data + '"' + song + '"' + ','
    put_data = put_data[:len(put_data) - 1] + ']'
    print put_data
    put_data = handle_data(put_data)  # encrypt and update the data
    for post_url in post_urls:
        response = requests.post(post_url, json=put_data, verify=False)  # post the data
        js = json.loads(response.text)
        print js
        if js['status'] != 200:
            raise TransException("Something wrong when post the data to {}, the wrong message is {}".format(post_url, js['data']))
        print response.status_code


def handle_music(base_url, post_urls):
    """
    get all QQ music data according to the base url and post it to post url
    :param base_url: the base url
    :param post_urls: post urls
    :return: None
    """
    urls = get_url(base_url)
    for url in urls:
        refresh_data(url, post_urls)

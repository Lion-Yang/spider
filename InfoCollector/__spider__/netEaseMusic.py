#!/usr/bin/python
# -*-coding:utf-8-*-
import json
import requests
from scrapy import Selector
from selenium import webdriver
from __util__.library import handle_data, mail_notification, TransException, my_retry
from __configure__.ConfigureParser import ConfigureParser


Configure = ConfigureParser('./__configure__/configure.xml')
admin = Configure.get_configure_by_tag_name('admin')


@mail_notification(admin)
@my_retry
def handle_netease_music(url, executable_path, element, post_urls):
    """
    get a list of new songs on netEase music website.
    :param url: the target url
    :param executable_path:  the executable path of PhantomJS
    :param element:  the element where the song name exists
    :param post_urls:  the urls where to post the data
    :return: None
    """
    driver = webdriver.PhantomJS(executable_path=executable_path)
    driver.get(url)
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe"))
    html = driver.page_source
    song_sel = Selector(text=html).xpath(element)
    put_data = '['
    for each_song in song_sel:
        put_data += '"' + each_song.extract() + '"' + ','
    put_data = put_data[:-1] + ']'
    print put_data
    put_data = handle_data(put_data)
    for post_url in post_urls:
        response = requests.post(post_url, json=put_data, verify=False)  # post the data
        js = json.loads(response.text)
        print js
        if js['status'] != 200:
            raise TransException("Something wrong when post the data to {}, the wrong message is {}".format(post_url, js['data']))
        print response.status_code
    driver.close()

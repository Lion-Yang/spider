#!/usr/bin/python
# -*-coding:utf-8-*-
import urllib2
import json
import requests
import sys
import re
from bs4 import BeautifulSoup
from __util__.library import handle_data, mail_notification, TransException, my_retry
from __configure__.ConfigureParser import ConfigureParser

reload(sys)
sys.setdefaultencoding('utf8')


Configure = ConfigureParser('./__configure__/configure.xml')
admin = Configure.get_configure_by_tag_name('admin')


@mail_notification(admin)
@my_retry
def handle_movie(base_url, city_url, movie_element, number_element, post_urls):
    """
    get information about movies on screening, the title and the frequency
    :param base_url: the base url of mtime
    :param city_url: specify the city, default Beiging
    :param movie_element: the element where the title of the movie exists
    :param number_element: the element where the frequency of the movie exists
    :param post_urls: the post urls
    :param last_timestamp : the timestamps recorded at last execution to match the sign
    :return: none
    """
    list_page = urllib2.urlopen(base_url + city_url).read()
    list_soup = BeautifulSoup(list_page, "html.parser")
    movies = list_soup.find_all(movie_element)
    numbers = list_soup.find_all(number_element)
    my_list = [9999]
    for num in numbers:
        p = re.compile(r"家影院上映(\w+)+场")
        m = p.search(str(num))
        if m and my_list[len(my_list) - 1] >= int(m.group(1)):
            my_list.append(int(m.group(1)))
    code = movies[4]
    text = code.text
    js = re.findall('var hotplaySvList = (.*);', text)[0]
    data = json.loads(js)
    put_data = '['
    i = 0
    for term in data:
        if i < len(my_list):
            put_data = put_data + '{"freq":"' + str(my_list[i]) + '","name":"' + term['Title'] + '"},'
        else:
            put_data = put_data + '{"freq":"' + str(1) + '","name":"' + term['Title'] + '"},'
        i += 1
    put_data = put_data[:len(put_data) - 1] + ']'
    print put_data
    final_data = handle_data(put_data)  # encrypt and update the data
    for post_url in post_urls:
        response = requests.post(post_url, json=final_data, verify=False)    # post the data
        js = json.loads(response.text)
        print js
        if js['status'] != 200:
            "Something wrong when post the data"
            raise TransException("Something wrong when post the data to {}, the wrong message is {}".format(post_url, js['data']))
        print response.status_code

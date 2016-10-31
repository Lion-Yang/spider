# coding:utf-8
import re
import os
import requests
import sys
import time
import json
import random
from retrying import retry
from __configure__.ConfigureParser import ConfigureParser
from __util__.library import get_specific_element, get_url
reload(sys)
sys.setdefaultencoding('utf-8')


class BlockedException(Exception):
    pass

conf = ConfigureParser('./__configure__/configure.xml')
input_file = conf.get_configure_by_tag_name_simple('input_file')
temp_file = conf.get_configure_by_tag_name_simple('temp_file')
output_file = conf.get_configure_by_tag_name_simple('output_file')


def get_movie_ids():
    """
    get all the tv ids from douban website through the tags
    :return: tv ids such as 25837700
    """
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:46.0) Gecko/20100101 Firefox/46.0",
               }
    ids = []
    tags = [u'美剧', u'英剧', u'韩剧', u'日剧', u'国产剧', u'港剧', u'日本动画']
    if not os.path.exists(input_file):
        for each in tags:
            api = 'https://movie.douban.com/j/search_subjects?type=tv&tag='+each+'&sort=recommend&page_limit=500&page_start=20'
            content = requests.get(api, headers=headers).text
            ids += re.findall('subject[^0-9]+(\d{6,8})', content)
            time.sleep(2)
        with open(input_file, 'wb') as f:
            for id in ids:
                f.write(id+'\n')
            return ids
    else:
        if not os.path.exists(temp_file):
            with open(input_file, 'rb') as f:
                ids = [each.strip() for each in f.readlines()]
                return ids
        else:
            with open(temp_file, 'rb') as f1:
                with open(input_file, 'rb') as f2:
                    id1 = [each.strip() for each in f1.readlines()]
                    id2 = [each.strip() for each in f2.readlines()]
                    ids = [each for each in id2 if each not in id1]
                    return ids


@retry
def handle_one_movie(movie_id):
    """
    crawl the info of a movie by the id
    :param movie_id: the id of the movie
    :return: a json string including the info
    """
    info = {}
    info['basic_info'] = {}
    info['name'] = {}
    info['movie_id'] = movie_id
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:46.0) Gecko/20100101 Firefox/46.0"}
    res = requests.get(get_url(movie_id), headers=headers)
    html = res.text
    if res.status_code != 200:
        print 'Be blocked'
        raise BlockedException
    name = get_specific_element('name', html)
    info['rate'] = get_specific_element('rate', html)
    info['rate_num'] = get_specific_element('rate_num', html)
    nickname = get_specific_element('nickname', html).split('/')
    nickname.append(name)
    name = [each.strip() for each in nickname]
    info['basic_info']['area'] = get_specific_element('openarea', html)
    info['basic_info']['director'] = get_specific_element('director', html)
    info['basic_info']['actors'] = get_specific_element('actor', html)
    info['basic_info']['init_time'] = get_specific_element('init_time', html)
    info['basic_info']['type'] = get_specific_element('movie_type', html)
    for i, data in enumerate(name):
        info['name'][i] = data
    with open(output_file, 'ab') as f:
        f.write(json.dumps(info, encoding='utf8', ensure_ascii=False).encode('utf8'))
        f.write('\n')
    with open(temp_file, 'ab') as f:
        f.write(movie_id+'\n')
    print 'ok'
    time.sleep(random.randint(3, 5))



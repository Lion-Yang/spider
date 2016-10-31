# coding:utf-8
import requests
import Levenshtein
from scrapy import Selector


class MyException(Exception):
    pass


def retry(func):
    """
    a simple function to realize retry function
    :param func: the protected function
    :return: a protected function
    """
    def _retry(*args):
        max_attempt = 10
        while max_attempt > 0:
            try:
                return func(*args)
            except Exception as e:
                print e
                continue
            finally:
                max_attempt -= 0
    return _retry


@retry
def get_html(url):
    """
    get the html source of a url
    :param url: the url
    :return: the html source
    """
    res = requests.get(url)
    if res.status_code == 403:
        raise MyException
    return res.text


def test(name, key):
    """
    test if the two names are the same
    :param name: one of the name
    :param key: another name
    :return: bool result
    """
    if Levenshtein.jaro(name, key) == 1:
        return 1


def simple_judge(html):
    """
    judge if it is a tv series
    :param html: html source
    :return: bool result
    """
    info_sel = Selector(text=html).xpath('//div[@id="info"]')
    info = info_sel.extract()[0]
    if u'集数' in info:
        return 1
    return 0

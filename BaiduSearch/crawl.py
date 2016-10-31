# coding:utf-8
"""
The definition of the BaiduCrawl class
"""
from __util__.library import get_cookie, handle_keys, create_thread
import time
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class CookieExpiredException(Exception):
    pass

class BaiduCrawler:
    def __init__(self, keys, base_url, pattern, output_file, threads):
        """
        init the class
        :param keys: the key word to be search
        :param base_url: base url of the result page
        :param pattern: the regular expression pattern
        :param output_file: the output file to store the result
        :param threads: how many threads in the mean time
        """
        self.keys = keys
        self.base_url = base_url
        self.pattern = pattern
        self.output_file = output_file
        self.threads = int(threads)

    def handle(self, keys):
        """
        main function to handle series of keywords and get, store the result
        :param keys: a series of keywords
        :return: none
        """
        cookie = {'Cookie': get_cookie()}
        print cookie
        for key in keys:
            try:
                head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                        'Connection': 'keep - alive'}
                key_hand = handle_keys(key)
                res = requests.get(self.base_url.format(key_hand[0]), cookies=cookie, headers=head)
                source = res.text
                if res.encoding == 'ISO-8859-1':
                    raise CookieExpiredException
                try:
                    num = re.findall(unicode(self.pattern), source)[0]
                    num = re.sub(',', '', num)
                    num = re.findall('\d+', num)[0]
                except:
                    num = '0'
                print key, num
                with open(self.output_file, 'ab') as f:
                    f.write(key + '\t' + num + '\n')
            except CookieExpiredException:
                print 'Cookie expired'
                print key
                time.sleep(5)
                cookie = {'Cookie': get_cookie()}
                continue

    def start(self):
        """
        begin crawl process with multiple threads
        :return: none
        """
        create_thread(self.threads, self.handle, self.keys)
        time.sleep(30)


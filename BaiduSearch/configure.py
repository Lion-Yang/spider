# coding:utf-8
"""
A small function to get the configuration
"""
from scrapy import Selector

# TODO: extend it to a standard class


def get_configure():
    """
    parse the xml file using Selector module
    :return: none
    """
    dic = {'s': 'mainpage', 'v': 'video', 'n': 'news'}
    f = open('./__configure__/configure.xml', 'r')
    text = f.read()
    f.close()    # read the file
    sel = Selector(text=text)
    input_file = sel.xpath('//input_file/text()').extract()[0]
    output_file = sel.xpath('//output_file/text()').extract()[0]
    crawl_type = sel.xpath('//crawl_type/text()').extract()[0]
    t = dic[crawl_type]
    threads = sel.xpath('//thread_control/text()').extract()[0]
    base_url = sel.xpath('//{}/base_url/text()'.format(t)).extract()[0]
    pattern = sel.xpath('//{}/pattern/text()'.format(t)).extract()[0]
    return [input_file, output_file, threads, base_url, pattern]

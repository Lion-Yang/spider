# coding:utf-8
import sys
from scrapy import Selector
from __util__.library import get_html, test, retry, simple_judge

reload(sys)
sys.setdefaultencoding("utf-8")


class DoubanJudge:

    def __init__(self, key, output_file):
        self.key = key
        self.url = 'https://movie.douban.com/subject_search?search_text={}'.format(key)
        self.html = get_html(self.url)
        self.relate_url = {}
        self.get_name()
        self.file = output_file

    def get_name(self):
        title_sel = Selector(text=self.html).xpath('//div[@class="pl2"]/a')
        for each_sel in title_sel:
            title_string = each_sel.xpath('string(.)').extract()[0]
            relate_url = each_sel.xpath('@href').extract()[0]
            name = [each.strip() for each in title_string.split('/')]
            self.relate_url[relate_url] = name

    def test_name(self):
        urls = []
        for url, names in self.relate_url.items():
            for name in names:
                if test(name, self.key):
                    urls.append(url)
                    break
        return urls

    @retry
    def handle(self):
        series = movie = 0
        urls = self.test_name()
        if urls:
            with open(self.file, 'a') as f:
                for url in urls:
                    relate_html = get_html(url)
                    if simple_judge(relate_html):
                        series += 1
                    else:
                        movie += 1
                if series and movie:
                    print self.key + '\t电影&电视剧'
                    f.write(self.key + '\t电影&电视剧\n')
                elif series:
                    print self.key + '\t电视剧'
                    f.write(self.key + '\t电视剧\n')
                elif movie:
                    print self.key + '\t电影'
                    f.write(self.key + '\t电影\n')
                else:
                    print self.key, 'Unknown type'
        else:
            print self.key+"没找到"



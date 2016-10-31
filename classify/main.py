import time
import random
from __spider__.doubanJudge import DoubanJudge
from __configure__.ConfigureParser import ConfigureParser


if __name__ == '__main__':
    conf = ConfigureParser('./__configure__/configure.xml')
    input_file = conf.get_configure_by_tag_name_simple('input_file')
    output_file = conf.get_configure_by_tag_name_simple('output_file')
    with open(input_file, 'r') as f:
        for each in f:
            key = each.rsplit('\t', 1)[0].strip()
            crawler = DoubanJudge(unicode(key), output_file)
            crawler.handle()
            time.sleep(random.randint(3, 5))

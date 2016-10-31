import re
from __configure__.ConfigureParser import ConfigureParser
from scrapy import Selector


def get_regex_res(pattern, text):
    """
    get the match result of a regular expression
    :param pattern: the regular expression
    :param text: the text waiting be matched
    :return: the matched result
    """
    try:
        res = re.findall(pattern, text)[0]
        res = res.decode('utf-8')
    except:
        res = "None"
    return res


def get_xpath_res(xpath, text):
    """
    find the element by the xpath
    :param xpath: the xpath
    :param text: the text waiting to be parsed
    :return: the value of the element
    """
    try:
        res = Selector(text=text).xpath(xpath).extract_first()
    except:
        res = ''
    return res


def get_res(choice, pattern, text):
    """
    find element by xpath or regular expression
    :param choice: xpath or regular expression
    :param pattern: the match pattern
    :param text: the text waiting to be matched
    :return: the matched result
    """
    if choice == 'regex':
        return get_regex_res(pattern, text)
    else:
        return get_xpath_res(pattern, text)


def get_specific_element(element, text):
    """
    get specific info from the text
    :param element: the info to be crawled
    :param text: the html source
    :return: the value of the info
    """
    conf = ConfigureParser('./__configure__/configure.xml')
    [choice, pattern] = conf.get_configure_by_tag_name(element)
    return get_res(choice, pattern, text)


def get_url(id):
    """
    return the url according by the id
    :param id: the movie id
    :return: the url of the movie on douban
    """
    return 'https://movie.douban.com/subject/{}'.format(id)
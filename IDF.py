import re
import requests
from bs4 import BeautifulSoup
import math


class IDF(object):
    """
    用谷歌搜索中搜索'的'字的网页数作为文档总数，而其他词的搜索结果总数为其文档数
    """
    sum_word = '的'

    def __init__(self, word):
        self.word = word

    def get(self):
        sum_count = GetCount(self.sum_word).get_count_by_search_google_by_key_word()
        count = GetCount(self.word).get_count_by_search_google_by_key_word()
        # 避免除0
        count += 1
        return math.log(sum_count/count)


class GetCount(object):
    url_google = 'https://www.google.com.hk/search?q='
    # url_baidu = ''  TODO: 从百度爬结果

    def __init__(self, word):
        self.word = word

    def get_count_by_search_google_by_key_word(self):
        url = self.url_google + self.word
        print(url)
        r = requests.get(url)
        b = BeautifulSoup(r.content)
        text = b.select('div#resultStats')
        print(text)
        text = text[0].text

        num_list = re.findall('\d+', text)
        return get_real_num(num_list)

    def get_count_by_search_baidu_by_key_word(self):
        pass


def get_real_num(num):
    _n = reversed(num)
    _r = 0
    for index, n in enumerate(_n):
        _r += int(n) * math.pow(10, index*3)

    return _r


def get_real_num2(num):
    num = [str(int(i)) for i in num]
    return int(''.join(num))

if __name__ == '__main__':
    g = IDF('中国')
    print(g.get())
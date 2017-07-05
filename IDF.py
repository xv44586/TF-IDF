import re
import requests
from bs4 import BeautifulSoup
import math


class Descriptor(object):
    word = '的'

    def get_cache_key(self, instance):
        return 'cache_{}'.format(instance.word)

    def __get__(self, instance, owner):
        if hasattr(owner, 'sum_word_cache'):
            print('---return---')
            return owner.sum_word_cache

        print('-----get------')
        count = GetCount(self.word).get_count()
        # setattr(owner, 'sum_count', count)
        setattr(owner, 'sum_word_cache', count)
        return count


class IDF(object):
    """
    用谷歌搜索中搜索'的'字的网页数作为文档总数，而其他词的搜索结果总数为其文档数
    """
    sum_word = Descriptor()

    def __init__(self, word_list):
        self.word_list = word_list

    def get(self):
        result = {}
        for word in self.word_list:

            count = GetCount(word).get_count()
            # 避免除0
            count += 1
            result.update({word: math.log(self.sum_word/count)})
        return result


class GetCount(object):
    url_google = 'https://www.google.com.hk/search?q='
    url_baidu = 'http://www.baidu.com/s?ie=utf-8&wd='

    def __init__(self, word, google=True):
        self.word = word
        self.google = google

    def get_count(self):
        if self.google:
            return self.get_count_by_search_google_by_key_word()

        return self.get_count_by_search_baidu_by_key_word()

    def get_count_by_search_google_by_key_word(self):
        url = self.url_google + self.word
        # print(url)
        r = requests.get(url)
        b = BeautifulSoup(r.content)
        text = b.select('div#resultStats')
        # print(text)
        text = text[0].text

        num_list = re.findall('\d+', text)
        return get_real_num(num_list)

    def get_count_by_search_baidu_by_key_word(self):
        url = self.url_baidu + self.word
        r = requests.get(url)
        b = BeautifulSoup(r.content)
        text =b.select('div.nums')[0].text
        num_list = re.findall('\d+', text)
        return get_real_num(num_list)


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
    print(IDF('祖国').get())
from utils import LoadFile
import jieba
from IDF import IDF


class TF(object):
    def __init__(self, file_path, key_words_count=20, stop_words_path='stop_words.txt'):
        self.file_path = file_path
        self.key_words_count = key_words_count
        self.stop_words_path = stop_words_path

    def get_key_words(self):
        words = self.get_words()
        data = {}
        sum = 0
        for word in words:
            if data.get(word, ''):
                data[word] += 1
            else:
                data[word] = 1

            sum += 1

        data = {key: value / sum for key, value in data.items()}
        sorted_data = sorted(data.items(), key=lambda data: data[1], reverse=True)
        return sorted_data[: self.key_words_count * 2]

    def get_stop_words(self):
        data = LoadFile(self.stop_words_path).load_data()
        return data

    def get_words(self):
        stop_words = self.get_stop_words()
        data = LoadFile(self.file_path).load_data()
        result = []
        for d in data:
            words = self._get_words_by_jieba(d)
            result.extend(list(set(words) - set(stop_words)))

        return result

    def _get_words_by_jieba(self, line):
        data = jieba.cut(line)
        return data


if __name__ == '__main__':
    # tf = TF('answer_spam.txt')
    tf = TF('test.txt')
    # tf.get_words()
    keywords = tf.get_key_words()
    keywords_list = [i[0] for i in keywords]
    idf_keywords = IDF(keywords_list).get()
    print('----keywords----')
    print(keywords)
    print('---keywords----')
    print(keywords_list)
    print('-------idf-------')
    print(idf_keywords)
    _re = {i[0]: i[1] * idf_keywords[i[0]] for i in keywords}
    sorted_data = sorted(_re.items(), key=lambda _re: _re[1], reverse=True)
    print('------result--------')
    print(sorted_data)

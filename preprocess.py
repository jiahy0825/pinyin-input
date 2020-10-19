from collections import defaultdict
import json
import re
import codecs
import chardet

class Preprocess:
    def __init__(self):
        self.pinyin2word = defaultdict(list)
        self.vocabulary = set()
        self.wordcnt = defaultdict(int)
        self.blacklist = set()

    # 读取拼音到汉字映射
    def read_pinyin2word(self, path, filtpath):
        with open(filtpath) as fd:
            for line in fd.readlines():
        # for line in open(filtpath, mode="r", encoding="utf8", errors="ignore"):
                for word in line:
                    self.vocabulary.add(word)

        with open(path) as fd:
            for line in fd.readlines():
        # for line in codecs.open(path, mode="r", encoding="utf8", errors="ignore"):
                data = line.strip().split(" ")
                self.pinyin2word[data[0]] = list(filter(lambda x: x in self.vocabulary, data))
                # self.pinyin2word[data[0]] = data[1:]

    # 更新黑名单符号等
    def update_blacklist(self):
        # 不考虑数字
        self.blacklist.update({chr(ord('0') + i) for i in range(10)})
        self.blacklist.update({" ", "\t", "\n"})

    # 统计二元组和汉字计数
    def train(self, paragraph):
        # 找到所有中文句子
        sentences = re.findall('[\u4E00-\u9FA5]+', paragraph)
        # 此句子中可能有空格
        for sentence in sentences:
            for sent in re.split("\\s+", sentence.strip()):
                cur = "B"
                for ch in sent:
                    self.wordcnt[cur + ch] += 1
                    self.wordcnt[ch] += 1
                    cur = ch

    # 读取训练数据
    def read_train_file(self, path):
        with open(path) as fd:
            for line in fd.readlines():
                news = json.loads(line)
                self.train(news["title"])
                self.train(news["html"])

    # 保存汉字计数
    def save_word_cnt(self):
        json.dump(self.wordcnt, open('wordcnt.json', "w"), ensure_ascii=False, indent=4)

    # 读取汉字计数
    def load_word_cnt(self):
        self.wordcnt = json.load(open('wordcnt.json'))


def cut_sentences(content):
    # 筛选中文符号
    sentences = re.split(r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]', content)
    # 找到所有中文句子
    sentences = re.findall('[ \u4E00-\u9FA5]+', content)
    return sentences


if __name__ == "__main__":
    prep = Preprocess()
    pinyin_word_file = "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\拼音汉字表.txt"
    filter_path = "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\一二级汉字表.txt"
    train_path = "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\sina_news_gbk\\2016-02.txt"
    prep.read_pinyin2word(pinyin_word_file, filter_path)
    print(prep.pinyin2word['beng'][0])

    prep.read_train_file(train_path)
    # prep.load_word_cnt()
    print(prep.wordcnt["中"])
    print(prep.wordcnt["其中"])
    print(list(prep.wordcnt.keys())[:10])
    # prep.save_word_cnt()

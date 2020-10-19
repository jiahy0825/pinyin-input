from collections import defaultdict

class Preprocess:
    def __init__(self):
        self.pinyin2word = defaultdict(list)
        self.words = set()

    def read_pinyin2word(self, path, filtpath):
        with open(filtpath) as fd:
            for line in fd.readlines():
                for word in line:
                    self.words.add(word)

        with open(path) as fd:
            for line in fd.readlines():
                data = line.strip().split(" ")
                self.pinyin2word[data[0]] = list(filter(lambda x: x in self.words, data))
                # self.pinyin2word[data[0]] = data[1:]


if __name__ == "__main__":
    prep = Preprocess()
    pinyin_word_file = "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\拼音汉字表.txt"
    filt_path = "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\一二级汉字表.txt"
    prep.read_pinyin2word(pinyin_word_file, filt_path)
    print(prep.pinyin2word['beng'][0])

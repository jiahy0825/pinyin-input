from preprocess import Preprocess
from tqdm import tqdm

class Model:
    def __init__(self):
        self.prep = Preprocess()
        self._init_prep()

    def _init_prep(self):
        pinyin_word_file = "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\拼音汉字表.txt"
        filter_path = "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\一二级汉字表.txt"
        self.prep.read_pinyin2word(pinyin_word_file, filter_path)
        self.prep.load_word_cnt()

        # train_path = "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\sina_news_gbk\\"
        # self.prep.read_train_file(train_path + "2016-02.txt")
        # for month in tqdm(range(4, 12)):
        #     self.prep.read_train_file(train_path + "2016-" + str(month).zfill(2) + ".txt")
        # self.prep.save_word_cnt()

    def predict_sentence(self, inputs):
        pinyins = inputs.strip().split(" ")
        output = ""
        cur = "B"
        for pinyin in pinyins:
            pinyin2word = self.prep.pinyin2word[pinyin]
            prob = [0] * len(pinyin2word)
            for idx, word in enumerate(pinyin2word):
                prob[idx] = self.prep.wordcnt[cur + word] / (self.prep.wordcnt[cur] + 1)
            max_index = prob.index(max(prob))
            output += pinyin2word[max_index]
            cur = pinyin2word[max_index]
        return output

    def predict(self, input_path):
        with open(input_path) as fd:
            for line in fd.readlines():
                output = self.predict_sentence(line)
                print(output)


if __name__ == "__main__":
    model = Model()
    # print(model.prep.pinyin2word["ji"])
    # print(model.prep.wordcnt["学去"])
    # print(model.prep.wordcnt["学区"])
    input_file = "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\input.txt"
    output_file = "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\output.txt"
    model.predict(input_file)

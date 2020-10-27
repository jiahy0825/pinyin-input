from preprocess import Preprocess
from tqdm import tqdm
from param import args

import numpy as np


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


class Model:
    def __init__(self):
        self.prep = Preprocess()
        self.train()

    def train(self):
        self.prep.read_pinyin2word(args.pinyin_word_file, args.filter_path)
        self.prep.load_word_cnt()

        # self.prep.read_train_file(args.train_path + "2016-02.txt")
        # for month in tqdm(range(4, 12)):
        #     self.prep.read_train_file(args.train_path + "2016-" + str(month).zfill(2) + ".txt")
        # self.prep.save_word_cnt()

    def predict_sentence(self, inputs):
        pinyins = inputs.strip().split(" ")
        output = ""
        if args.type == "bigram":
            cur = "B"
            for pinyin in pinyins:
                pinyin2word = self.prep.pinyin2word[pinyin]
                prob = [0] * len(pinyin2word)
                for idx, word in enumerate(pinyin2word):
                    prob[idx] = self.prep.wordcnt[cur + word] / (self.prep.wordcnt[cur] + 1)
                max_index = prob.index(max(prob))
                output += pinyin2word[max_index]
                cur = pinyin2word[max_index]
        elif args.type == "trigram":
            c1, c2 = "B1", "B2"
            for pinyin in pinyins:
                pinyin2word = self.prep.pinyin2word[pinyin]
                prob = [0] * len(pinyin2word)
                for idx, word in enumerate(pinyin2word):
                    prob[idx] = self.prep.wordcnt[c1 + c2 + word] / (self.prep.wordcnt[c1 + c2] + 1)
                max_index = prob.index(max(prob))
                output += pinyin2word[max_index]
                c1, c2 = c2, pinyin2word[max_index]

        return output

    def hmm_predict_sentence(self, inputs):
        pinyins = inputs.strip().split(" ")
        output = ""
        if args.type == "bigram":
            dp = [[("B", -1, 1)]]
            # word, pre_index, prob
            for pinyin in pinyins:
                pinyin2word = self.prep.pinyin2word[pinyin]
                dp_cur = [("B", -1, 0)] * len(pinyin2word)
                for word_idx, (preword, _, p) in enumerate(dp[-1]):
                    prob = np.zeros((len(pinyin2word)))
                    for idx, word in enumerate(pinyin2word):
                        prob[idx] = self.prep.wordcnt[preword + word] / (self.prep.wordcnt[preword] + 1)
                    prob = softmax(prob)
                    for i in range(len(pinyin2word)):
                        if p * prob[i] > dp_cur[i][2]:
                            dp_cur[i] = (pinyin2word[i], word_idx, p * prob[i])
                dp.append(dp_cur)
        elif args.type == "trigram":
            dp = [[("B1", "B2", -1, 1)]]
            # word, pre_index, prob
            for pinyin in pinyins:
                pinyin2word = self.prep.pinyin2word[pinyin]
                dp_cur = [("B1", "B2", -1, 0)] * len(pinyin2word)
                for word_idx, (b1word, b2word, _, p) in enumerate(dp[-1]):
                    prob = np.zeros((len(pinyin2word)))
                    for idx, word in enumerate(pinyin2word):
                        prob[idx] = self.prep.wordcnt[b1word + b2word + word] / (self.prep.wordcnt[b1word + b2word] + 1)
                    prob = softmax(prob)
                    for i in range(len(pinyin2word)):
                        if p * prob[i] > dp_cur[i][2]:
                            dp_cur[i] = (dp_cur[i][1], pinyin2word[i], word_idx, p * prob[i])
                dp.append(dp_cur)
        if args.type == "bigram":
            tmp = [x[2] for x in dp[-1]]
            idx = tmp.index(max(tmp))
            for i in range(len(dp) - 1, 0, -1):
                output = dp[i][idx][0] + output
                idx = dp[i][idx][1]
        elif args.type == "trigram":
            tmp = [x[3] for x in dp[-1]]
            idx = tmp.index(max(tmp))
            for i in range(len(dp) - 1, 0, -1):
                output = dp[i][idx][1] + output
                idx = dp[i][idx][2]
            print(dp[1])
            print(dp[-1])
        return output

    def predict(self, input_path, output_path):
        out = open(output_path, "w")
        with open(input_path) as fd:
            for line in fd.readlines():
                # output = self.predict_sentence(line)
                output = self.hmm_predict_sentence(line)
                out.write(output + "\n")
        out.close()


if __name__ == "__main__":
    model = Model()
    # print(model.prep.pinyin2word["ji"])
    # print(model.prep.wordcnt["学去"])
    # print(model.prep.wordcnt["学区"])

    model.predict(args.input_file, args.output_file)

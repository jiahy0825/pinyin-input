import argparse

parser = argparse.ArgumentParser(description='pinyin_word_model')

# -- Basic --
parser.add_argument('--pinyin_word_file', type=str,
                    default='D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\拼音汉字表.txt',
                    help='pinyin transform to words')
parser.add_argument('--filter_path', type=str,
                    default="D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\一二级汉字表.txt",
                    help='valid vocabulary')
parser.add_argument('--train_path', type=str,
                    default="D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\sina_news_gbk\\",
                    help='train sentence')
parser.add_argument('--wordcnt_file', type=str,
                    default="pinyin_wordcnt.json",
                    help='file to save word_cnt')
parser.add_argument('--input_file', type=str,
                    # "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\input.txt"
                    default="input.txt",
                    help='input sentence file')
parser.add_argument('--output_file', type=str,
                    # "D:\研二上课程\人工智能\第一次作业-拼音输入法\拼音输入法作业\拼音汉字表_12710172\output.txt"
                    default="output.txt",
                    help='output sentence file')
parser.add_argument('--type', type=str,
                    default="trigram",
                    help='model type(bigram or trigram)')
parser.add_argument('--pretrain', type=int, default=1,
                    help='finish count word')

args = parser.parse_args()

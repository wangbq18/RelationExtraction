#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2019/2/27 19:52
@Author  : Erisu-
@contact: guoyu01988@163.com
@File    : test2.py
@Software: PyCharm
@Desc:
'''


import os

LTP_DATA_DIR = 'D:/python/project/ltpModel/ltp_data_v3.4.0'  # ltp路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`

from pyltp import Segmentor

segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, 'test.txt')  # 加载模型，第二个参数是您的外部词典文件路径
words = segmentor.segment('恶化的经济状况导致高层次人才的相对稀缺。')
print('\t'.join(words))
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`

from pyltp import Postagger

postagger = Postagger()  # 初始化实例
postagger.load(pos_model_path)  # 加载模型
postags = postagger.postag(words)  # 词性标注
print('\t'.join(postags))
postagger.release()  # 释放模型
# import jieba.posseg as poseg
# import jieba
# jieba.load_userdict('all_word_dict.txt')
# # # jieba.del_word('时所')
# # # print()
# # # jieba.suggest_freq('时所', False)
# print(poseg.lcut('双重职业通道有利于激励在'))
# import re

# temp_pattern = '(.*)又称(.*)'
# small_sentence = '合作医疗保障模式又称社区合作医疗保险或基层医疗保险和集资医疗保障制度'
# r = re.search(temp_pattern, small_sentence)
# print(poseg.lcut(small_sentence))
# print(r)

# def sort_by_something(words_file):
#     words = []
#     for line in words_file.readlines():
#         line = line.strip('\n')
#         words.append(line)
#     words.sort(key=lambda x: (len(x), x), reverse=True)
#     f2 = open('sorted_words', 'w', encoding='utf8')
#     for word in words:
#         f2.write(word + '\n')
#
#
# f = open('all_word_dict.txt', 'r', encoding='utf8')
# sort_by_something(f)
# f.close()

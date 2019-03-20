#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2019/2/17 1:06
@Author  : Erisu-
@contact: guoyu01988@163.com
@File    : words_to_vec.py
@Software: PyCharm
@Desc:  生成词向量
'''
from gensim.models.word2vec import Word2Vec
import pickle


def word2vec(all_words):
    model = Word2Vec(all_words, size=128, window=5,
                     workers=3,
                     sg=1,
                     batch_words=10000, min_count=1)

    pickle.dump(model, open('result/word2vec_xinchou.pkl', 'wb'))
    # model.save('../data/relation_model')


def read_file():
    all_words_file = open('all_words.txt', 'r', encoding='utf8')
    all_words = list()
    for words in all_words_file.readlines():
        word_list = words.strip('\n').split('\t')
        all_words.append(word_list)
    return all_words


if __name__ == '__main__':
    all_words = read_file()
    word2vec(all_words)

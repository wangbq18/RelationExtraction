#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2019/2/13 16:05
@Author  : Erisu-
@contact: guoyu01988@163.com
@File    : word2vec_relation_prepare.py
@Software: PyCharm
@Desc:  对书中的动词进行模型训练并持久化
'''
import os
import re
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
import time

LTP_DATA_DIR = 'D:/python/project/ltpModel/ltp_data_v3.4.0'  # ltp路径
sentences = set()  # 分离出的句子组
entity_words = list()  # 用以后续词扩展的初始词
relation_words = list()  # 关系词list
all_words = list()  # 分词后的所有词，用以模型训练


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)


def initialize(entity_file):
    """ 领域词存储

    :param entity_file: 领域词文件（包括扩展词）
    :return:
    """
    for word in entity_file.readlines():
        if word.strip() != '':
            entity_words.append(word.strip())
    # 进行领域词词排序（降序）
    entity_words.sort(reverse=True);
    str = "领域词存储完成"
    print("=" * 10, str, "=" * 10)
    return str


def deal_data(sentence):
    """ 对于明显无法确定关系的段落删除。

    :param sentence:
    :return:
    """
    # 1.去除括号中的内容（因为多半为补充声明没什么大用）
    sentence = re.sub("（.*）\.*|\(.*\)\.*", "", sentence)
    # 2.去除例如："图1-6　2006年的总体报酬模型"这样的句子
    # paragraph = re.sub("图\d+-\d+.+ ", "", paragraph)
    # 3.去除文献
    pattern = re.compile("\[.*\]")
    m = pattern.match(sentence)
    if m:
        if m.span(0)[0] == 0:
            sentence = ""
    # 4.判断一段话是否全是英文
    if re.sub(' ', "", sentence).encode('UTF-8').isalpha():
        sentence = ""
    # 5.去除开头是如果的话
    if sentence.find("如果") == 0:
        sentence = ""
    # 6.去除问句
    if sentence.find("？") != -1:
        sentence = ""
    return sentence


def sentence_split(read_file):
    """ 对段落中的句子进行基于符号的划分

    :param read_file:   文件txt
    :return:    分好的句子存入到sequences了，所以只需要返回状态信息就好了
    """
    for paragraph in read_file.readlines():
        # 太短的段落（词？）没有分的必要了
        if paragraph == '' or len(paragraph) <= 4:
            continue
        sentence_splitter = SentenceSplitter.split(paragraph)
        for sentence in sentence_splitter:
            # 去除空行
            if sentence == '':
                continue
            # 二次分隔
            second_sentences = re.split('[，,]', sentence)
            for second_sentence in second_sentences:
                # 对于句子的筛选工作
                second_sentence = deal_data(second_sentence)
                if second_sentence == '' or len(second_sentence) <= 4:
                    continue
                sentences.add(second_sentence)
    str = "分句步骤已完成"
    print("=" * 10, str, "=" * 10)
    return str


def words_split():
    """ 对于句子进行分词

    :return:
    """
    segmentor = Segmentor()
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    segmentor.load_with_lexicon(cws_model_path, '../data/all_word_dict.txt')
    for sentence in sentences:
        words = segmentor.segment(sentence)
        postags = postaggers(words)
        index = 0
        for word, postag in zip(words, postags):
            if postag == 'v':
                relation_words.append(word)
                # print(word)
        all_words.append(words)
    relation_words_file = open('relation_words.txt', 'w+', encoding='utf8')
    for word in relation_words:
        relation_words_file.write(word + '\n')
    # 将当前扫描的所有词加入file
    all_words_file = open('all_words.txt', 'w+', encoding='utf8')
    for words in all_words:
        temp_words = '\t'.join(words)
        all_words_file.write(temp_words + '\n')
    segmentor.release()


def postaggers(words):
    postagger = Postagger()  # 初始化实例
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
    postagger.load_with_lexicon(pos_model_path, 'data/postagger.txt')  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    # print('\t'.join(postags))
    postagger.release()  # 释放模型
    return postags


if __name__ == '__main__':
    entity_file = open('../data/all_word_dict.txt', 'r', encoding='utf8')
    # 初始化读词
    initialize(entity_file)
    # 读取关系词
    relation_file = open("../data/key_word.txt", "r", encoding="utf8")
    # create_relation(relation_file)
    # 文件夹下读取待扩展的文件路径
    bookList = list()
    listdir("../book", bookList)
    for i in range(len(bookList)):
        read_file = open(bookList[i], "r", encoding='utf-8')
        # 分句
        sentence_split(read_file)
        # 分词和词性标注
        words_split()
        # # word2vec模型训练
        # word2vec()

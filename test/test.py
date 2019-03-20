#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2019/3/20 14:15
@Author  : Erisu-
@contact: guoyu01988@163.com
@File    : test.py
@Software: PyCharm
@Desc:
'''
import jieba
import jieba.posseg as posseg

jieba.load_userdict("a.txt")
str = "企业薪酬制度的执行促进了金币消耗"
seg = jieba.cut(str)
print("\t".join(seg))
jieba.load_userdict("a.txt")
seg = posseg.lcut(str)
for word, flag in seg:
    print(word, end='\t')

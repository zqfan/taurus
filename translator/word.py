#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import sys
import time
from multiprocessing import Process

import translator

def get_words():
    fp = open('/home/zqfan/Downloads/gre-words.txt')
    lines = fp.readlines()
    fp.close()
    words = []
    length = len(lines)
    for i in xrange(length):
        if i % 2 == 0:
            words.append(lines[i].strip())
    return words

def agent(*words):
    dic = translator.Translator()
    for word in words:
        dic.find(word)
        dic.print_interprets()
        return
        dic.save_interprets()

def main1():
    words = get_words()
    words_len = len(words)
    p_count = 100
    task_word_len = ((words_len-1)/100)+1
    ps = []
    for i in xrange(p_count):
        start = i * task_word_len
        if start >= words_len:
            continue
        end = start + task_word_len
        if end > words_len:
            end = words_len
        task_word = words[start:end]
        p = Process(target=agent, args=(task_word))
        ps.append(p)
        p.start()
    for p in ps:
        p.join();

def main():
    dic = translator.Translator()
    words = get_words()
    for word in words:
        dic.find(word,net=True)
        dic.print_interprets()
        dic.dump()
        if dic.interprets_from_file:
            sys.sleep(3)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

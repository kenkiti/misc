# -*- coding: sjis -*-
import os, sys, random, logging, time

from ctypes import *
import google

def sparse(s, opt):
    # ���C�u�����̏ꏊ���w��
    libpath = 'c:/mecab/bin/libmecab.dll'
    # ���C�u������ ctypes ���g���ēǂݍ���
    lib = cdll.LoadLibrary(libpath)

    # ��͊평�����p�̈������w��i-Owakati �ŕ���������)
    argc = c_int(2)
    argv = (c_char_p * 2)("mecab", opt)

    # ��͊�̃I�u�W�F�N�g�����
    tagger = lib.mecab_new(argc, argv)

    """ �w�肳�ꂽ������𕪂����������ĕԂ��B """
    s = lib.mecab_sparse_tostr(tagger, s)
    ret = c_char_p(s).value

    # �I�������A�ꉞ�A�E���Ă��� 
    lib.mecab_destroy(tagger)

    return ret

def getGoogleTotalResultsCount(s):
    google.setLicense('...') # must get your own key!
    ustr = unicode(s,'shiftjis')
    flg = True
    while flg:
        try:
            data = google.doGoogleSearch(ustr)
        except:
            print sys.exc_info()
            time.sleep(5)
        else:
            flg = False

    return data.meta.estimatedTotalResultsCount

def wordcount(s):
    sound = ("����")#, "������")
    noise = ("��", "�ڔ�", "�㖼��", "����", "�����񎩗��I", "�񎩗�", "�L��")

    # word count
    s = sparse(s, "")
    count = {}
    lines = s.split("\n")
    for line in lines:
        if line == "EOS":
            break
        buf = line.split("\t")
        word = buf[0]
        wordclass = buf[1].split(",")[0]
        wordclass2 = buf[1].split(",")[1]

        if wordclass in sound and wordclass2 not in noise and len(word) > 2:
            if count.has_key(word):
                count[word] += 1
            else:
                count[word] = 1

    # sort
    lst = count.items()
    for i in range(len(lst)):
        for j in range(i):
            if lst[i][1] > lst[j][1]:
                lst[i], lst[j] = lst[j], lst[i]
    return lst

def getKeyword_rank(lst):
    """ calculate TF-IDF """
    from math import *

    keywordlist = []
    N = 18210000000 # google��index��
    limit = min(50, len(lst))
    for i in range(limit):
        word = lst[i][0]
        tf = lst[i][1]
        print "Google searching ...", word
        df = getGoogleTotalResultsCount(word)
        tf_idf = tf * log( N / df )
        keywordlist.append([word, tf_idf])

    # keyword sort
    for i in range(len(keywordlist)):
        for j in range(i):
            if keywordlist[i][1] > keywordlist[j][1]:
                keywordlist[i], keywordlist[j] = keywordlist[j], keywordlist[i]

    return keywordlist

def markov(sentence, limit=0):

    # �킩�����������P������X�g�Ɋi�[����
    wordlist = sparse(sentence, "-Owakati").rstrip(" \n").split(" ")

    # �}���R�t�A���e�[�u���̍쐬 prefix2��, suffix��1���o�[�W����
    markov = {}
    p1w, p2w = "", "" # p1w - previous one word,  p2w - previous two word, cw - current word
    for cw in wordlist:
        if p1w:
            if markov.has_key(p2w + p1w):
                lst = markov[p2w + p1w]
            else:
                lst = []
            lst.append(cw)
            markov[p2w + p1w] = lst
        p2w, p1w = p1w, cw

    # �}���R�t�A���ŕ��͍쐬
    prefix1, prefix2 = wordlist[0], wordlist[1]
    markov_sentence = prefix1
    count = 0
    if limit==0:
        limit = len(wordlist)
    while limit > count or prefix1 != "�B":
        markov_sentence += prefix2
        if markov.has_key(prefix1 + prefix2) == False:
            errmsg =  "\n error! [" + prefix1 + prefix2 + "] dictionary length " + str(len(markov))
            warn(errmsg)
            return markov_sentence
        
        prefix1, prefix2 = prefix2, random.choice(markov[prefix1 + prefix2])
        count += 1

    return markov_sentence

if __name__ == "__main__":
    def m(s):
        """ �}���R�t�A���ŕ��͕ϊ� """
        print markov(s, 10)

    def wc(s):
        """ �p�o�P��̏W�v """
        dat = wordcount(s)
        for k, v in dat:
            print k, v

    def kw(s):
        """ TF-IDF�A���S���Y���ŃL�[���[�h���o """
        dat = wordcount(s)
        keylst = getKeyword_rank(dat)
        fh = open("keyword_" + sys.argv[1:][1],"w")
        for k, v in keylst:
            fh.write(k + "\t" + str(v) + "\n")

    def test(s):
        print getGoogleTotalResultsCount("�Ŗ��ь�")

    cmd = {'-m' : m, '-c' : wc, "-k" : kw ,"-t" : test}

    # �����`�F�b�N
    if len(sys.argv[1:]) < 2:
        print "Usage : markov.py [-mck] [source file]"
        print "-k:�L�[���[�h���o�A-m:�}���R�t�A�� -c:�p�o�P��W�v"
        sys.exit(0)
    elif os.path.isfile(sys.argv[1:][1]) == False:
        print '"' + sys.argv[1:][0] + '" is not exist.'
        sys.exit(0)
    elif cmd.has_key(sys.argv[1:][0]) == False:
        print "invalid option"

    # �R�}���h���s
    s = open(sys.argv[1:][1], "r").read()
    cmd[sys.argv[1:][0]](s)



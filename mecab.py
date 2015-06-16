# -*- coding: sjis -*-
import os, sys, random, time
from ctypes import *

def markov(sentence, limit=0):
    # �킩�����������P������X�g�Ɋi�[����
    #wordlist = mecab(sentence, "-Owakati").rstrip(" \n").split(" ")
    wordlist = sentence.split(" ")

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
    #while limit > count or prefix1 != "�B":
    while limit > count:
        markov_sentence += prefix2
        if markov.has_key(prefix1 + prefix2) == False:
            errmsg =  "\n error! [" + prefix1 + prefix2 + "] dictionary length " + str(len(markov))
            return markov_sentence + errmsg
        
        prefix1, prefix2 = prefix2, random.choice(markov[prefix1 + prefix2])
        count += 1

    return markov_sentence

def mecab(s, opt):
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

if __name__ == "__main__":
    def m(s):
        """ �}���R�t�A�� """
        dat = mecab(s,"-Owakati")
        print markov(dat, 200)

    def wakati(s):
        """ �킩������ """
        print mecab(s,"-Owakati")

    def hinshi(s):
        """ �i������ """
        print mecab(s,"")
        
    cmd = {'-m' : m, "-w" : wakati, "-h" : hinshi}

    # �����`�F�b�N
    if len(sys.argv[1:]) < 2:
        print "Usage : mecab.py [-mwh] [source file]"
        print "-m:�}���R�t�A�� -w:���������� -h:�i������"
        sys.exit(0)
    elif os.path.isfile(sys.argv[1:][1]) == False:
        print '"' + sys.argv[1:][0] + '" is not exist.'
        sys.exit(0)
    elif cmd.has_key(sys.argv[1:][0]) == False:
        print "invalid option"

    # �R�}���h���s
    s = open(sys.argv[1:][1], "r").read()
    cmd[sys.argv[1:][0]](s)

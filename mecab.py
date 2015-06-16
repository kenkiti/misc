# -*- coding: sjis -*-
import os, sys, random, time
from ctypes import *

def markov(sentence, limit=0):
    # わかち書きした単語をリストに格納する
    #wordlist = mecab(sentence, "-Owakati").rstrip(" \n").split(" ")
    wordlist = sentence.split(" ")

    # マルコフ連鎖テーブルの作成 prefix2こ, suffixが1こバージョン
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


    # マルコフ連鎖で文章作成
    prefix1, prefix2 = wordlist[0], wordlist[1]
    markov_sentence = prefix1
    count = 0
    if limit==0:
        limit = len(wordlist)
    #while limit > count or prefix1 != "。":
    while limit > count:
        markov_sentence += prefix2
        if markov.has_key(prefix1 + prefix2) == False:
            errmsg =  "\n error! [" + prefix1 + prefix2 + "] dictionary length " + str(len(markov))
            return markov_sentence + errmsg
        
        prefix1, prefix2 = prefix2, random.choice(markov[prefix1 + prefix2])
        count += 1

    return markov_sentence

def mecab(s, opt):
    # ライブラリの場所を指定
    libpath = 'c:/mecab/bin/libmecab.dll'
    # ライブラリを ctypes を使って読み込み
    lib = cdll.LoadLibrary(libpath)

    # 解析器初期化用の引数を指定（-Owakati で分かち書き)
    argc = c_int(2)
    argv = (c_char_p * 2)("mecab", opt)

    # 解析器のオブジェクトを作る
    tagger = lib.mecab_new(argc, argv)

    """ 指定された文字列を分かち書きして返す。 """
    s = lib.mecab_sparse_tostr(tagger, s)
    ret = c_char_p(s).value

    # 終わったら、一応、殺しておく 
    lib.mecab_destroy(tagger)

    return ret

if __name__ == "__main__":
    def m(s):
        """ マルコフ連鎖 """
        dat = mecab(s,"-Owakati")
        print markov(dat, 200)

    def wakati(s):
        """ わかち書き """
        print mecab(s,"-Owakati")

    def hinshi(s):
        """ 品詞分類 """
        print mecab(s,"")
        
    cmd = {'-m' : m, "-w" : wakati, "-h" : hinshi}

    # 引数チェック
    if len(sys.argv[1:]) < 2:
        print "Usage : mecab.py [-mwh] [source file]"
        print "-m:マルコフ連鎖 -w:分かち書き -h:品詞分類"
        sys.exit(0)
    elif os.path.isfile(sys.argv[1:][1]) == False:
        print '"' + sys.argv[1:][0] + '" is not exist.'
        sys.exit(0)
    elif cmd.has_key(sys.argv[1:][0]) == False:
        print "invalid option"

    # コマンド実行
    s = open(sys.argv[1:][1], "r").read()
    cmd[sys.argv[1:][0]](s)

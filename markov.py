# -*- coding: sjis -*-
import os, sys, random, logging, time

from ctypes import *
import google

def sparse(s, opt):
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
    sound = ("名詞")#, "感動詞")
    noise = ("数", "接尾", "代名詞", "特殊", "動詞非自立的", "非自立", "記号")

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
    N = 18210000000 # google総index数
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

    # わかち書きした単語をリストに格納する
    wordlist = sparse(sentence, "-Owakati").rstrip(" \n").split(" ")

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
    while limit > count or prefix1 != "。":
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
        """ マルコフ連鎖で文章変換 """
        print markov(s, 10)

    def wc(s):
        """ 頻出単語の集計 """
        dat = wordcount(s)
        for k, v in dat:
            print k, v

    def kw(s):
        """ TF-IDFアルゴリズムでキーワード抽出 """
        dat = wordcount(s)
        keylst = getKeyword_rank(dat)
        fh = open("keyword_" + sys.argv[1:][1],"w")
        for k, v in keylst:
            fh.write(k + "\t" + str(v) + "\n")

    def test(s):
        print getGoogleTotalResultsCount("椎名林檎")

    cmd = {'-m' : m, '-c' : wc, "-k" : kw ,"-t" : test}

    # 引数チェック
    if len(sys.argv[1:]) < 2:
        print "Usage : markov.py [-mck] [source file]"
        print "-k:キーワード抽出、-m:マルコフ連鎖 -c:頻出単語集計"
        sys.exit(0)
    elif os.path.isfile(sys.argv[1:][1]) == False:
        print '"' + sys.argv[1:][0] + '" is not exist.'
        sys.exit(0)
    elif cmd.has_key(sys.argv[1:][0]) == False:
        print "invalid option"

    # コマンド実行
    s = open(sys.argv[1:][1], "r").read()
    cmd[sys.argv[1:][0]](s)



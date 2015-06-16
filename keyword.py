# -*- coding: sjis -*-
import os, sys, random, time
import mecab

from math import *
import google

def getGoogleTotalResultsCount(s):
    keys = open("./googlelicense.txt","r").read().rstrip("\n").split("\n")
    google.setLicense(random.choice(keys)) # must get your own key!
    ustr = unicode(s,'shiftjis')
    fsuccess = False
    while fsuccess == False:
        try:
            data = google.doGoogleSearch(ustr)
        except:
            print sys.exc_info()
            time.sleep(5)
        else:
            fsuccess = True

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


if __name__ == "__main__":
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

    cmd = {'-c' : wc, "-k" : kw ,"-t" : test}

    # 引数チェック
    if len(sys.argv[1:]) < 2:
        print "Usage : markov.py [-ckt] [source file]"
        print "-k:キーワード抽出, -c:頻出単語集計 -t:googleテスト"
        sys.exit(0)
    elif os.path.isfile(sys.argv[1:][1]) == False:
        print '"' + sys.argv[1:][0] + '" is not exist.'
        sys.exit(0)
    elif cmd.has_key(sys.argv[1:][0]) == False:
        print "invalid option"

    # コマンド実行
    s = open(sys.argv[1:][1], "r").read()
    cmd[sys.argv[1:][0]](s)



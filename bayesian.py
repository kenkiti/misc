# -*- encoding: sjis -*-
# bayesian fillter

import os
import sys

import MeCab

def wakati(dat):
    arg = [sys.argv[0], "-Owakati"]
    m = MeCab.Tagger(" ".join(arg))
    dat = m.parse(dat)
    lst = dat.split(" ")
    return lst

def getFilelist(path):
    filelist = []
    for root, directories, files in os.walk(path):
        for f in files:
            filelist.append(path + "/" + f)
    return filelist

def analysisWord(dic, word, lst, opt=0):
    counter = 0
    for l in lst:
        dat = open(l).read()
        lst = wakati(dat)
        counter += lst.count(word)

    probability = float(counter) / float(len(lst))
    if dic.has_key(word):
        dic[word][opt] += probability
    else:
        dic[word] = [0,0,0]
        dic[word][opt] = probability

    return dic

# Initialize
GOOD, BAD = 0, 1
bad = "./spam"
good = "./nonspam"
target = "./target.txt"

badlst = getFilelist(bad)
goodlst = getFilelist(good)

dat = open(target).read()
wordlist = wakati(dat)
worddic = {} # {word: [ngood, nbad]}

# Analysis
for word in wordlist:
    print word
    worddic = analysisWord(worddic, word, goodlst, GOOD)
    worddic = analysisWord(worddic, word, badlst, BAD)

# Calculate pg(w)
pgwlist = []

for w, v in worddic.items():
    check = float(v[GOOD])*len(goodlst)*2 + float(v[BAD])*len(badlst)
    if check >= 5:
        if v[GOOD] != 0 and v[BAD] == 0: # good
            pg_w = (0.01, 0.49, w)
        elif v[GOOD] == 0 and v[BAD] != 0: # bad
            pg_w = (0.99, 0.49, w)
        elif v[GOOD] == 0 and v[BAD] == 0: # token is not in database
            pg_w = (0.4, 0.1, w)
        else:
            tmp = v[BAD] / (2 * v[GOOD] + v[BAD])
            pg_w = (tmp, abs(0.5 - tmp), w)

        pgwlist.append(pg_w)

pgwlist.sort(lambda x, y: cmp(float(y[1]), float(x[1])))
pgwlist = pgwlist[:15]
for pgw in pgwlist:
    print pgw[2], "\t", pgw[0]

p1, p2 = 1.00, 1.00
for pgw in pgwlist:
    p1 = p1 * float(pgw[0])
    p2 = p2 * (1 - float(pgw[0]))

print "spam probability = ", p1 / (p1 + p2)


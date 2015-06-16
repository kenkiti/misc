# -*- coding: euc-jp -*-
"""
LNB autopilot script
[2006-02-25] create
"""
import os
import time
import urllib2
import formatter
from htmllib import HTMLParser

class MyParser(HTMLParser):
    imglist = []
    htmllist = []
    body = ""

    def handle_data(self, data):
        data = data.strip(" 　\t\r\n")
        self.body = self.body + " " + data

    def anchor_bgn(self, href, name, type):
        # aタグのURLの拡張子がjpg or htmlの行だけ拾う
        if href[-3:] == "jpg":
            self.imglist.append(href)
        elif href[-4:] == "html":
            self.htmllist.append(href)

    def handle_image(self, src, alt, *args):
        #print "src=",src
        pass

    def init(self):
        self.imglist = []
        self.htmllist = []
        self.body = ""

def open_page(url):
    """Open index page url

    Keyword argument:
    url -- the url string

    Return value:
    success -- web page data
    failed  -- return None
    """
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    req = urllib2.Request(url,"",txheaders)
    try:
        dat = urllib2.urlopen(req).read()
        time.sleep(5)
        return dat
    except IOError, e:
        print str(e)
        time.sleep(20)
        return None

def wget(ref, url):
    header = '--header=REFERER:' + ref
    agent = '-U "Mozilla/4.06 [ja] (Win98; I)"'
    cmd = "wget -nc " + header + " " + agent + " " + url
    print cmd
    os.system(cmd)
    time.sleep(2)

def wget2(ref, url):
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    pos = url.rfind("/") + 1
    filename = url[pos:]

    if os.path.isfile(filename):
        print filename + " is exist."
        return

    try:
        req = urllib2.Request(url, "", txheaders)
        dat = urllib2.urlopen(req).read()
    except IOError, e:
        print str(e)
    else:
        open(filename, "wb").write(dat)
        print "Got " + filename
        time.sleep(1)

def main(pagenumber=10,pagelist=[]):
    """ Get picture of Licentious Notice board

    Keyword argument:
    pagenumber -- number of getting pages
    pagelist   -- specified getting pages list
    """
    # get top page
    print "Getting top page"
    dat = open_page("http://violet.homeip.net/noticeboard/incoming/")
    if dat == None: return 0

    # html parsing...
    print "Html parsing..."
    p = MyParser(formatter.NullFormatter())
    p.feed(dat)

    # 通し番号が振ってあるindex.htmlの番号が大きい方から上位nページを取得する。
    if len(pagelist) == 0:
        print "Get recent " + str(pagenumber) + " page"
        max_value = [x for x in range(pagenumber)]
        max_index = [x for x in range(pagenumber)]
        for index, x in enumerate(p.htmllist):
            x = x.replace("index","")
            x = x.replace(".html","")
            x = int(x)
            m = int(min(max_value))
            if x > m:
                minidx = max_value.index(m) 
                if max_value.count(x) == 0:
                    max_index[minidx] = index
                    max_value[minidx] = x
        # 取得したページの整理
        print "Get each pages..." , len(max_index)
        url_list = ["http://violet.homeip.net/noticeboard/incoming/"]
        for x in max_index:
            url_list.append("http://violet.homeip.net/noticeboard/incoming/" + p.htmllist[x])

    else:
        print "Get " , pagelist, " page list"
        url_list = []
        for x in pagelist:
            x = "index" + str(x) + ".html"
            url_list.append("http://violet.homeip.net/noticeboard/incoming/" + x)

    # download済みのファイルリスト取得
    logfile = "log-lnb.txt"
    if os.path.isfile(logfile):
        dat = open(logfile,"r").read()
        image_list = dat.rstrip("\n").split("\n")
    else:
        image_list = []

    # で、画像を持ってくる。
    for page_url in url_list:
        dat = open_page(page_url)
        if dat == None: return 0

        print page_url
        mp = MyParser(formatter.NullFormatter())
        mp.init() # ???
        mp.feed(dat)
        for image_path in mp.imglist:
            pos = image_path.rfind("/") + 1
            image_file = image_path[pos:]
            # download済みの画像はdownloadしない
            if image_list.count(image_file) == 0:
                image_list.append(image_file)
                image_url = "http://violet.homeip.net" + image_path
                wget2(page_url, image_url)

    # ログ保存
    f = open(logfile, "w")
    f.write("\n".join(image_list))
    f.close()
    print 'pilot done.'
    return 1

if __name__ == "__main__":
    import sys

    def errmsg():
        print "usage: LNB.py [-np] [number...]"
        print "   -n: get number of newest pages"
        print "   -p: get specified pages (list)"
        sys.exit(0)

    cmd = {"-n" : "number", "-p" : "page" }
    if len(sys.argv) < 3:
        errmsg()
    elif cmd.has_key(sys.argv[1]) is False:
        errmsg()

    if sys.argv[1] == "-n":
        ret = main(int(sys.argv[2]))
    elif sys.argv[1] == "-p":
        ret = main(1, sys.argv[2:])

    # When finished, make a sound
    import winsound
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

#    import sendmane
#     if ret == 0:
#         sendmane.mail("LNB_downloader","nanka error detayo.")


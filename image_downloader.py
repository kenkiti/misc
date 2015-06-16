#! -*- conding: euc-jp -*-

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
        data = data.strip(" \t\r\n")
        self.body = self.body + " " + data

    def anchor_bgn(self, href, name, type):
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

def urlopen(url):
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

def wget(url):
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

def main():
    # get top page
    print "Getting top page..."
    dat = urlopen("http://g-idol.com/ra/Leah_Dizon.htm")
    if dat == None: return 0

    print "Parse page..."
    p = MyParser(formatter.NullFormatter())
    p.feed(dat)

    for url in p.imglist:
        print "getting images...", url
        wget("http://g-idol.com/ra/" + url)

if __name__ == "__main__":
    main()


# -*- coding:euc-jp -*-

import mechanize
import urllib2
import time
import datetime

def get_image(url):
    filename = url.split("/")[-1]
    dat = urllib2.urlopen(url)
    open(filename,"wb").write(dat.read())
    print "[%s] %s was downloaded." % (datetime.datetime.now().strftime("%H:%M:%S"), filename)
    time.sleep(1)

br = mechanize.Browser()
br.open('http://blog.livedoor.jp/akanehotaru/archives/cat_736051.html')
next_page = unicode('次のページへ', 'euc-jp').encode(br.encoding())

while True:
    for link in br.links(url_regex="image"):
        get_image(link.url)

    try:
        br.follow_link(text_regex=next_page)
    except:
        break


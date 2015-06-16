# -*- encoding: euc-jp -*-
# utamap downloader
#
# [2006-03-03]:create
import sys, re, time
import urllib, urllib2, cookielib
import os.path

uta = '''http://www.utamap.com/showkasi.php?surl=B01171
http://www.utamap.com/showkasi.php?surl=B01171
http://www.utamap.com/showkasi.php?surl=B05439
http://www.utamap.com/showkasi.php?surl=B05439
http://www.utamap.com/showkasi.php?surl=55782
http://www.utamap.com/showkasi.php?surl=55782
http://www.utamap.com/showkasi.php?surl=B09087
http://www.utamap.com/showkasi.php?surl=B09087
http://www.utamap.com/showkasi.php?surl=B09944
http://www.utamap.com/showkasi.php?surl=B09944
http://www.utamap.com/showkasi.php?surl=57138
http://www.utamap.com/showkasi.php?surl=57138
http://www.utamap.com/showkasi.php?surl=35938
http://www.utamap.com/showkasi.php?surl=35938
http://www.utamap.com/showkasi.php?surl=B09942
http://www.utamap.com/showkasi.php?surl=B09942
http://www.utamap.com/showkasi.php?surl=B08149
http://www.utamap.com/showkasi.php?surl=B08149
http://www.utamap.com/showkasi.php?surl=B05440
http://www.utamap.com/showkasi.php?surl=B05440
http://www.utamap.com/showkasi.php?surl=37674
http://www.utamap.com/showkasi.php?surl=37674
http://www.utamap.com/showkasi.php?surl=57711
http://www.utamap.com/showkasi.php?surl=57711
http://www.utamap.com/showkasi.php?surl=B08144
http://www.utamap.com/showkasi.php?surl=B08144
http://www.utamap.com/showkasi.php?surl=35658
http://www.utamap.com/showkasi.php?surl=35658
http://www.utamap.com/showkasi.php?surl=57672
http://www.utamap.com/showkasi.php?surl=57672
http://www.utamap.com/showkasi.php?surl=B12592
http://www.utamap.com/showkasi.php?surl=B12592
http://www.utamap.com/showkasi.php?surl=55783
http://www.utamap.com/showkasi.php?surl=55783
http://www.utamap.com/showkasi.php?surl=B08152
http://www.utamap.com/showkasi.php?surl=B08152
http://www.utamap.com/showkasi.php?surl=B08153
http://www.utamap.com/showkasi.php?surl=B08153
http://www.utamap.com/showkasi.php?surl=B05442
http://www.utamap.com/showkasi.php?surl=B05442
http://www.utamap.com/showkasi.php?surl=55785
http://www.utamap.com/showkasi.php?surl=55785
http://www.utamap.com/showkasi.php?surl=B01169
http://www.utamap.com/showkasi.php?surl=B01169
http://www.utamap.com/showkasi.php?surl=B12596
http://www.utamap.com/showkasi.php?surl=B12596
http://www.utamap.com/showkasi.php?surl=B09085
http://www.utamap.com/showkasi.php?surl=B09085
http://www.utamap.com/showkasi.php?surl=B08151
http://www.utamap.com/showkasi.php?surl=B08151
http://www.utamap.com/showkasi.php?surl=B01173
http://www.utamap.com/showkasi.php?surl=B01173
http://www.utamap.com/showkasi.php?surl=B01165
http://www.utamap.com/showkasi.php?surl=B01165
http://www.utamap.com/showkasi.php?surl=37665
http://www.utamap.com/showkasi.php?surl=37665
http://www.utamap.com/showkasi.php?surl=36034
http://www.utamap.com/showkasi.php?surl=36034
http://www.utamap.com/showkasi.php?surl=39957
http://www.utamap.com/showkasi.php?surl=39957
http://www.utamap.com/showkasi.php?surl=B09093
http://www.utamap.com/showkasi.php?surl=B09093
http://www.utamap.com/showkasi.php?surl=B09086
http://www.utamap.com/showkasi.php?surl=B09086
http://www.utamap.com/showkasi.php?surl=66057
http://www.utamap.com/showkasi.php?surl=66057
http://www.utamap.com/showkasi.php?surl=57137
http://www.utamap.com/showkasi.php?surl=57137
http://www.utamap.com/showkasi.php?surl=65078
http://www.utamap.com/showkasi.php?surl=65078
http://www.utamap.com/showkasi.php?surl=57136
http://www.utamap.com/showkasi.php?surl=57136
http://www.utamap.com/showkasi.php?surl=33973
http://www.utamap.com/showkasi.php?surl=33973
http://www.utamap.com/showkasi.php?surl=B01166
http://www.utamap.com/showkasi.php?surl=B01166
http://www.utamap.com/showkasi.php?surl=B12597
http://www.utamap.com/showkasi.php?surl=B12597
http://www.utamap.com/showkasi.php?surl=57692
http://www.utamap.com/showkasi.php?surl=57692
http://www.utamap.com/showkasi.php?surl=B08145
http://www.utamap.com/showkasi.php?surl=B08145
http://www.utamap.com/showkasi.php?surl=37977
http://www.utamap.com/showkasi.php?surl=37977
http://www.utamap.com/showkasi.php?surl=36993
http://www.utamap.com/showkasi.php?surl=36993
http://www.utamap.com/showkasi.php?surl=B09089
http://www.utamap.com/showkasi.php?surl=B09089
http://www.utamap.com/showkasi.php?surl=B05441
http://www.utamap.com/showkasi.php?surl=B05441
http://www.utamap.com/showkasi.php?surl=B09947
http://www.utamap.com/showkasi.php?surl=B09947
http://www.utamap.com/showkasi.php?surl=B01168
http://www.utamap.com/showkasi.php?surl=B01168
http://www.utamap.com/showkasi.php?surl=39953
http://www.utamap.com/showkasi.php?surl=39953
http://www.utamap.com/showkasi.php?surl=59515
http://www.utamap.com/showkasi.php?surl=59515
http://www.utamap.com/showkasi.php?surl=B09090
http://www.utamap.com/showkasi.php?surl=B09090
http://www.utamap.com/showkasi.php?surl=56354
http://www.utamap.com/showkasi.php?surl=56354
http://www.utamap.com/showkasi.php?surl=37084
http://www.utamap.com/showkasi.php?surl=37084
http://www.utamap.com/showkasi.php?surl=65847
http://www.utamap.com/showkasi.php?surl=65847
http://www.utamap.com/showkasi.php?surl=B05443
http://www.utamap.com/showkasi.php?surl=B05443
http://www.utamap.com/showkasi.php?surl=B09949
http://www.utamap.com/showkasi.php?surl=B09949
http://www.utamap.com/showkasi.php?surl=B09945
http://www.utamap.com/showkasi.php?surl=B09945
http://www.utamap.com/showkasi.php?surl=57694
http://www.utamap.com/showkasi.php?surl=B12595
http://www.utamap.com/showkasi.php?surl=B12595
http://www.utamap.com/showkasi.php?surl=B05438
http://www.utamap.com/showkasi.php?surl=B05438
http://www.utamap.com/showkasi.php?surl=B12591
http://www.utamap.com/showkasi.php?surl=B12591
http://www.utamap.com/showkasi.php?surl=B09941
http://www.utamap.com/showkasi.php?surl=B09941
http://www.utamap.com/showkasi.php?surl=B09088
http://www.utamap.com/showkasi.php?surl=B09088
http://www.utamap.com/showkasi.php?surl=B04214
http://www.utamap.com/showkasi.php?surl=B04214
http://www.utamap.com/showkasi.php?surl=B12594
http://www.utamap.com/showkasi.php?surl=B12594
http://www.utamap.com/showkasi.php?surl=B12593
http://www.utamap.com/showkasi.php?surl=B12593
http://www.utamap.com/showkasi.php?surl=B08148
http://www.utamap.com/showkasi.php?surl=B08148
http://www.utamap.com/showkasi.php?surl=57676
http://www.utamap.com/showkasi.php?surl=57676
http://www.utamap.com/showkasi.php?surl=B09946
http://www.utamap.com/showkasi.php?surl=B09946
http://www.utamap.com/showkasi.php?surl=B05437
http://www.utamap.com/showkasi.php?surl=B05437
http://www.utamap.com/showkasi.php?surl=B04215
http://www.utamap.com/showkasi.php?surl=B04215
http://www.utamap.com/showkasi.php?surl=B09943
http://www.utamap.com/showkasi.php?surl=B09943
http://www.utamap.com/showkasi.php?surl=B09948
http://www.utamap.com/showkasi.php?surl=B09948
http://www.utamap.com/showkasi.php?surl=B08146
http://www.utamap.com/showkasi.php?surl=B08146
http://www.utamap.com/showkasi.php?surl=B08150
http://www.utamap.com/showkasi.php?surl=B08150
http://www.utamap.com/showkasi.php?surl=37693
http://www.utamap.com/showkasi.php?surl=37693
http://www.utamap.com/showkasi.php?surl=55786
http://www.utamap.com/showkasi.php?surl=55786
http://www.utamap.com/showkasi.php?surl=B01172
http://www.utamap.com/showkasi.php?surl=B01172
http://www.utamap.com/showkasi.php?surl=63869
http://www.utamap.com/showkasi.php?surl=63869
http://www.utamap.com/showkasi.php?surl=B09091
http://www.utamap.com/showkasi.php?surl=B09091
http://www.utamap.com/showkasi.php?surl=36575
http://www.utamap.com/showkasi.php?surl=36575
http://www.utamap.com/showkasi.php?surl=37102
http://www.utamap.com/showkasi.php?surl=37102
http://www.utamap.com/showkasi.php?surl=37690
http://www.utamap.com/showkasi.php?surl=37690
http://www.utamap.com/showkasi.php?surl=36736
http://www.utamap.com/showkasi.php?surl=36736
http://www.utamap.com/showkasi.php?surl=37678
http://www.utamap.com/showkasi.php?surl=37678
http://www.utamap.com/showkasi.php?surl=35642
http://www.utamap.com/showkasi.php?surl=35642
http://www.utamap.com/showkasi.php?surl=B01170
http://www.utamap.com/showkasi.php?surl=B01170
http://www.utamap.com/showkasi.php?surl=B08143
http://www.utamap.com/showkasi.php?surl=B08143
http://www.utamap.com/showkasi.php?surl=B08147
http://www.utamap.com/showkasi.php?surl=B08147
http://www.utamap.com/showkasi.php?surl=64815
http://www.utamap.com/showkasi.php?surl=64815
http://www.utamap.com/showkasi.php?surl=55784
http://www.utamap.com/showkasi.php?surl=55784
http://www.utamap.com/showkasi.php?surl=37927
http://www.utamap.com/showkasi.php?surl=37927
http://www.utamap.com/showkasi.php?surl=B01174
http://www.utamap.com/showkasi.php?surl=B01174
http://www.utamap.com/showkasi.php?surl=B01167
http://www.utamap.com/showkasi.php?surl=B01167
http://www.utamap.com/showkasi.php?surl=57674
http://www.utamap.com/showkasi.php?surl=57674
http://www.utamap.com/showkasi.php?surl=B05444
http://www.utamap.com/showkasi.php?surl=B05444
http://www.utamap.com/showkasi.php?surl=B13253
http://www.utamap.com/showkasi.php?surl=B13253
'''
log_file = "./__utamap.log"

def uniq(lst):
    uniqlst = []
    for x in lst:
        if x not in uniqlst:
            uniqlst.append(x)

    loglst = open(log_file, "r").read().split("\n")
    retlst = []
    for x in uniqlst:
        if x not in loglst:
            retlst.append(x)

    return retlst

uta = uta.split("\n")
utamaplst = uniq(uta)
print len(uta),len(utamaplst)

headers =  {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1'}

for utamap in utamaplst:
    print "get " + utamap # = "http://www.utamap.com/showkasi.php?surl=B09088"
    params = {'q' : utamap, 'c' : 'on' }
    params = urllib.urlencode(params)

    url = "http://strange.toheart.to/lyrics/lyrics.cgi"
    req = urllib2.Request(url, params, headers)
    dat = urllib2.urlopen(req).read()
    kashi = dat.split("<hr>")[2]
    kashi = kashi.replace("</body>","")
    kashi = kashi.replace("</html>","")
    kashi = kashi.replace("</pre>","")

    # output lyrics
    fh_kashi = open("lyrics/" + utamap.split("=")[1] + ".txt","w")
    fh_kashi.write(kashi)
    fh_kashi.close()

    # output log file
    fh_log = open(log_file, "a")
    fh_log.write(utamap + "\n")
    fh_log.close()
    time.sleep(2)

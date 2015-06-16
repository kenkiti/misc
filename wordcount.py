import sys,re,codecs
prog_u_wd=re.compile(u"\s+")
src=codecs.getreader("CP932")(file(sys.argv[1])).read()
chars=len(src)
lines=src.count("\n")
words=len(prog_u_wd.findall(src))
print "char:%d, lines:%d, words:%d" %(chars,lines,words)

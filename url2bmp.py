import os, sys, datetime
import Image
from ftplib import FTP
path = "c:\\path\\to\\temp\\"
screenshot = "c:\\path\\to\\temp\\screenshot\\"
thumbnail = "c:\\path\\to\\temp\\thumb\\"
os.chdir(path)

# crop and save image
filename =  str(datetime.datetime.now())[:17].replace("-","").replace(":","").replace(" ","") + ".png"
box = (140,110,865,560)
thumb_size = (100, 62)

im = Image.open(os.path.join(path, "temp.png")).crop(box)
im.save(os.path.join(screenshot, filename))
im.thumbnail(thumb_size)
im.save(os.path.join(thumbnail, filename))

# upload image
server = FTP("your_server_address")
print server.login("your_username", "your_password")

server.cwd("/public_html/hoge/screenshot")
stream = file(os.path.join(screenshot, filename), "rb")
server.storbinary("stor " + filename, stream)

server.cwd("/public_html/hoge/thumbnail")
stream = file(os.path.join(thumbnail, filename), "rb")
server.storbinary("stor " + filename, stream)

server.quit()
print "upload done."
stream.close()
server.close()

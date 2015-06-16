#-*- coding: euc-jp -*-
$KCODE='u'
require 'rubygems'
require 'mechanize'
require 'hpricot'
require 'kconv'
require 'uri'

$path_to_img = "megurulove.com/"

def get_image(thread_url, prefix)
  agent = WWW::Mechanize.new
  agent.user_agent_alias = 'Windows IE 6'
  agent.redirect_ok = true
  page = agent.get(thread_url)
  
  doc = Hpricot(page.body)
  images = (doc/:html/:body/"a[@href*='\/img\/']")
  
  images.each {|image|
    base = "http://megurulove.com/bbs/etc/img/"
    file = image["href"].split("/")[3]
    url = base + file
    file_path = prefix + file
    if File.exists?(file_path)
      puts "File exists. " + file_path
    else
      puts "Downloading... " + file_path
      page = agent.get(url)
      handle = File.open(file_path, 'wb')
      handle.puts page.body
      handle.close
    end
  }
end

def get_thread_list
  url = 'http://megurulove.com/bbs/etc/subback.html'

  agent = WWW::Mechanize.new
  agent.user_agent_alias = 'Windows IE 6'
  agent.redirect_ok = true
  page = agent.get(url)
  
  items = []
  doc = Hpricot(page.body)
  threads = (doc/:html/:body/"a[@href*='l50']")
  threads.each {|thread|
    prefix = $path_to_img + thread.inner_text.toutf8.split(" ")[1] + " - "
    thread_url = 'http://megurulove.com/bbs/test/read.php/etc/' 
    thread_url += thread['href'].split('/')[-2]
    item = {:prefix => prefix, :url => thread_url}
    items << item
  }
  return items
end

if not FileTest::directory?($path_to_img)
  Dir::mkdir($path_to_img)
end

items = get_thread_list
items.each {|item|
  puts item[:url], item[:prefix]
  get_image(item[:url], item[:prefix])
}

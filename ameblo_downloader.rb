# -*- coding: utf-8 -*-
# Author: kenkiti (INOUE Tadashi)
# $Id$
require 'kconv'
require 'uri'
require 'logger'
require 'rubygems'
require 'mechanize'
Version = "0.0.1"

class ImageSaver < WWW::Mechanize::File
  def initialize(uri=nil, response=nil, body=nil, code=nil)
    super(uri, response, body, code)
  end

  def save(file_path)
    File.open(file_path, 'wb') {|h| h.puts body } unless File.exists?(file_path)
  end
end

class AmebloDownloader
  def initialize(opt)
    @agent = WWW::Mechanize.new
    @agent.user_agent_alias = 'Windows IE 7'
    @agent.log = Logger.new($stdout)
    @agent.log.level = Logger::INFO
    @agent.redirect_ok = true
    @agent.max_history = 1
    @agent.pluggable_parser['image/jpeg'] = ImageSaver

    @path = opt[:path] || "image"
    Dir::mkdir(@path) unless FileTest::directory?(@path)
  end

  def get_page(uri, reffer=nil)
    @agent.get(uri, reffer)
  rescue TimeoutError
    @agent.log.warn 'Connection timeout.'; nil
  rescue WWW::Mechanize::ResponseCodeError => e
    @agent.log.warn "#{e.message} #{uri}"; nil
  else
    sleep 3
    @agent.page
  end

  def imagelist(uri, to_next)
    page = get_page(uri)
    while page
      page.root.search("html body a").select {|a| a['href'].include?("image-") }.map {|a|
        download(a['href'])
      }
      uri = page.link_with(:text => /#{to_next}/)
      page = uri ? @agent.click(uri) : nil
    end
  end

  def download(uri)
    page = get_page(uri)
    page.root.search("html body img#imageMain").each do |img|
      file_path = File.join(@path, img['src'].split("/")[-1])
      unless File.exists?(file_path)
        if get_page(img['src'], @agent.visited_page(uri))
          @agent.page.save(file_path)
          @agent.log.info "Downloaded #{img['src']}"
        end
      end
    end
  end

  def self.get(uri, path)
    downloader = self.new(:path => path)
    downloader.imagelist(uri, "次ページ")
  end
end

if $0 == __FILE__
  require 'optparse'
  parser = OptionParser.new
  opt = {}
  parser.banner = "Usage: #{File.basename($0)} options"
  parser.on('-u URL', '--url URL', "Specify the URL of ameba-blog to download image.") {|u| opt[:url] = u }
  parser.on('-p PATH','--path PATH', "Directory path name to save image.") {|p| opt[:path] = p }
  parser.on('-h', '--help', 'Prints this message and quit') {
    puts parser.help
    exit 0;
  }
  if ARGV[0].nil?
    puts parser.help
    exit 0 
  end
  
  begin
    parser.parse!(ARGV)
  rescue OptionParser::ParseError => e
    $stderr.puts e.message
    $stderr.puts parser.help
    exit 1
  else
    AmebloDownloader.get(opt[:url], opt[:path])
  end
end

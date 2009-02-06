# -*- coding: utf-8 -*-
# Created: 
# Author: kenkiti (INOUE Tadashi)
# $Id: blog_image_crawler.rb 87 2008-12-24 14:21:50Z rocky $

require 'kconv'
require 'uri'
require 'logger'
require 'rubygems'
require 'mechanize'

class ImageSaver < WWW::Mechanize::File
  def initialize(uri=nil, response=nil, body=nil, code=nil)
    super(uri, response, body, code)
  end

  def save(file_path)
    File.open(file_path, 'wb') {|h| h.puts body } unless File.exists?(file_path)
  end
end

class BlogImageDownloader
  def initialize(opt)
    @agent = WWW::Mechanize.new
    @agent.user_agent_alias = 'Windows IE 6'
    @agent.log = Logger.new($stdout)
    @agent.log.level = Logger::INFO
    @agent.redirect_ok = true
    @agent.max_history = 1
    @agent.pluggable_parser['image/jpeg'] = ImageSaver

    @path = opt[:path] || "image"
    Dir::mkdir(@path) unless FileTest::directory?(@path)
  end

  def download(uri, to_next)
    page = @agent.get(uri)
    while page
      page.root.search("html body a").each do |a|
        a.search("img").select {|img| a['href'].include?("jpg") }.map do |img|
          file_path = File.join(@path, URI.parse(a['href']).path.gsub("/","_"))
          unless File.exists?(file_path)
            @agent.get(a['href'], @agent.visited_page(uri))
            @agent.page.save(file_path)
          end
        end
      end
      uri = page.link_with(:text => /#{to_next}/)
      page = uri ? @agent.click(uri) : nil
    end
  end

  def self.get(uri, to_next, path)
    downloader = self.new(:path => path)
    downloader.download(uri, to_next)
  end

end

if $0 == __FILE__
  require 'optparse'
  parser = OptionParser.new
  opt = {}
  parser.banner = "Usage: #{File.basename($0)} options"
  parser.on('-u URL', '--url URL', "Specify the URL of ameba-blog to download image.") {|u| opt[:url] = u }
  parser.on('-p PATH','--path PATH', "Directory path name to save image.") {|p| opt[:path] = p }
  parser.on('-t TEXT','--text TEXT', "Text of next-page anchor.") {|t| opt[:text] = t }
  parser.on('-h', '--help', 'Prints this message and quit.') {
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
    BlogImageDownloader.get(opt[:url], opt[:text], opt[:path])
  end
end

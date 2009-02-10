require 'rubygems'
require 'mechanize'
require 'logger'

class ImageSaver < WWW::Mechanize::File
  def initialize(uri=nil, response=nil, body=nil, code=nil)
    super(uri, response, body, code)
  end
  
  def save(file_path)
    File.open(file_path, 'wb') {|h| h.puts body } unless File.exists?(file_path)
  end
end

class PhotoDownloader
  def initialize(opt)
    @path = opt[:path] || "queen8"
    @agent = WWW::Mechanize.new
    @agent.user_agent_alias = 'Windows IE 7'
    @agent.log = Logger.new($stdout)
    @agent.log.level = Logger::INFO
    @agent.redirect_ok = true
    @agent.max_history = 1
    Dir::mkdir(@path) unless FileTest::directory?(@path)
  end

  def get_page(uri, reffer=nil)
    @agent.get(uri, reffer)
  rescue TimeoutError
    @agent.log.warn 'Connection timeout.'; nil
  rescue WWW::Mechanize::ResponseCodeError => e
    @agent.log.warn "#{e.message} #{uri}"; nil
  else
    @agent.page
  end

  def download(url)
    @agent.log.info "open #{url}..."
    page = get_page(url)
    photos = page.links.inject([]) {|xs, x| xs << x.href if /jpg$/ =~ x.href; xs }
    photos.each do |u|
      file_path = File.join(@path, u)
      unless File.exists?(file_path)
        if get_page("#{url}#{u}")
          @agent.page.save(file_path)
        end
      end
    end
  end
end

def test
  d = PhotoDownloader.new(:path => "mao")
  #d.crawl("http://www11.kinghost.com/asian/cute82/JGG/0437zd/")
  d.crawl("http://www8.kinghost.com/asian/pacific/Q8/mao/")
end

if $0 == __FILE__
  require 'optparse'
  parser = OptionParser.new
  opt = {}
  parser.banner = "Usage: #{File.basename($0)} options"
  parser.on('-u URL', '--url URL', "Specify the URL of image site.") {|u| opt[:url] = u }
  parser.on('-p PATH','--path PATH', "Directory path name to save image.") {|p| opt[:path] = p }
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
    d = PhotoDownloader.new(:path => opt[:path])
    d.download(opt[:url])
  end
end

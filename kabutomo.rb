# -*- coding: utf-8 -*-
require 'rubygems'
require 'mechanize'
require 'kconv'
require 'pit'
require 'logger'

class Kabutomo
  def initialize
    @path = "kabutomo"
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
    sleep 3 * rand(10)
    @agent.page
  end

  def login
    @agent.log.info "logging..."
    config = Pit.get("kabutomo.net", :require => { 
        "username" => "your email in kabutomo",
        "password" => "your password in kabutomo"
      })
    page = get_page('http://kabutomo.net/')
    form = page.forms[0]
    form.field_with(:name => 'username').value = config['username']
    form.field_with(:name => 'password').value = config['password']
    page = @agent.submit(form, form.buttons.first)
    sleep 5
    self
  end

  def get_diary(url)
    page = get_page(url)

    diary = ""
    while page
      # Firefox は table 直下に tr がある場合、DOM 上で tbody を補完します。
      # Firebug で取得した XPath には tbody が含まれているので、Mechanize 上では tbody を省いた XPath を使用します。
      title = (page/'/html/body/div/table/tr/td/table/tr[3]/td/table/tr/td[4]/table/tr[2]/td[2]/table/tr/td/table/tr[2]/td/table[2]/tr[2]/td').inner_text
      body = (page/'//*[@id="DOM_fh_diary_body"]').inner_text.toutf8.gsub(/<br \/>/, "\n")
      @agent.log.info "#{title}"
      diary += "-" * 80 + "\n#{title}\n#{body}"
      uri = page.link_with(:text => /次の日記/)
      page = uri.nil? ? nil : get_page(uri.href)
    end

    open("kabutomo.html","w").write(diary)
    system("open kabutomo.html")
  end
end

if $0 == __FILE__
  k = Kabutomo.new
  k.login.get_diary("http://kabutomo.net/?m=pc&a=page_fh_diary&target_c_diary_id=134641")
end

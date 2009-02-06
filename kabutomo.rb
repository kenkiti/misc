# -*- coding: utf-8 -*-
require 'rubygems'
require 'mechanize'
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
        "username" => "your email in mixi",
        "password" => "your password in mixi"
      })
    page = get_page('http://kabutomo.net/')
    form = page.forms[0]
    form.field_with(:name => 'username').value = config['username']
    form.field_with(:name => 'password').value = config['password']
    page = @agent.submit(form, form.buttons.first)
    sleep 5
    open("kabutomo.html","w").write(page.body)
    system("open kabutomo.html")
    self
  end

  def get_diary(url)
    page = get_page(url)
    uri = page.link_with(:text => /次を表示/)
  end

end

if $0 == __FILE__
  k = Kabutomo.new
  k.login
end

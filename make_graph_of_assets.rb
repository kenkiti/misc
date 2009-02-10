# -*- coding: utf-8 -*-
#!/usr/bin/env ruby
require 'kconv'
require 'date'
require 'logger'

require 'rubygems'
require 'mechanize'
require 'hatena/api/graph'
require 'pit'

class RakutenSec
  def initialize
    @agent = WWW::Mechanize.new
    @agent.user_agent_alias = 'Windows IE 7'
    @agent.log = Logger.new($stdout)
    @agent.log.level = Logger::INFO
    @agent.redirect_ok = true
    @agent.max_history = 1
    @page = nil
  end

  def _debug
    open("test.html","w").write(@agent.page.body); `open test.html`
  end

  def login
    config = Pit.get("rakuten-sec.co.jp", :require => { 
      "id" => "your id in rakuten",
      "password" => "your password in rakuten"
    })
    url = "https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html"
    page = @agent.get(url)
    form = page.form_with(:name => 'loginform')
    form.field_with(:name => 'loginid').value = config['id']
    form.field_with(:name => 'passwd').value = config['password']
    @agent.submit(form, form.buttons.first)
    @agent.page.frame_with(:name => 'middleframe').click
    @agent.page.frame_with(:name => 'rightframe').click
    self
  end

  def get_assets
    link = @agent.page.link_with(:text => /商品別資産残高へ/)
    @agent.click(link)
    @agent.page.frame_with(:name => 'middleframe').click
    @agent.page.frame_with(:name => 'rightframe').click

    @agent.page.root.search("table[@class='ta1']").each do |t|
      ta1h = t.at("td[@class='ta1h']")
      next if ta1h.nil? or ta1h.inner_text != "評価額合計±信用建玉評価損益"
      return t.search("td[@align='right']").inner_text.gsub(/,/,"")
    end
  end

  def self.assets
    rakuten = RakutenSec.new
    rakuten.login.get_assets
  end
end

def post_hatena_graph(title, value)
  log = Logger.new($stdout)
  config = Pit.get("hatena.ne.jp", :require => { 
      "id" => "your id in hatena",
      "password" => "your password in hatena"
    })
  graph = Hatena::API::Graph.new(config['id'], config['password'])
  graph.post_data(title, 'date' => Date.today, 'value' => value)
  log.info "Posted a graph data of assets."
end

def main(graph_title)
  assets = RakutenSec.assets
  post_hatena_graph(graph_title, assets)
end

if $0 == __FILE__
  main("テスト")
end

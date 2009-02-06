#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
# test
$KCODE='u'
require 'kconv'
require 'ostruct'
require 'date'

require 'rubygems'
require 'mechanize'
require 'hpricot'
require 'hatena/api/graph'

HATENA_ID = 'kenkitii'
HATENA_PASSWORD = 'kenkiti'

def get_yesterday_spots_data
  url = "http://www.data.jma.go.jp/obd/stats/data/mdrr/synopday/data2.html"
  agent = WWW::Mechanize.new
  agent.user_agent_alias = 'Windows IE 6'
  page = agent.get(url)
  
  h = {}
  doc = Hpricot(page.body)
  places = (doc/:html/:body/:table/"tr.o1|tr.o2")
  places.each do |place|
    spot_infos = (place/"td.oR")
    break unless spot_infos[11]
    
    spot = (place/"td.o0").inner_html.toutf8 # 地点
    low = spot_infos[4].inner_html.toutf8 # 最低気温
    high = spot_infos[3].inner_html.toutf8 # 最高気温
    avg = spot_infos[2].inner_html.toutf8 # 平均気温
    rainfall = spot_infos[11].inner_html.toutf8 # 降水量
    rainfall = 0 if rainfall == '--'
    h[spot] = OpenStruct.new({:low => low, :high => high, :avg => avg, :rainfall => rainfall})
  end
  h
end

def post_graph(spot)
  d = get_yesterday_spots_data
  yesterday = Date.today - 1

  graph = Hatena::API::Graph.new(HATENA_ID, HATENA_PASSWORD)
  graph.post_data("#{spot}の最高気温", 'date' => yesterday, 'value' => d[spot].high)
  graph.post_data("#{spot}の最低気温", 'date' => yesterday, 'value' => d[spot].low)
  graph.post_data("#{spot}の平均気温", 'date' => yesterday, 'value' => d[spot].avg)
  graph.post_data("#{spot}の降水量", 'date' => yesterday, 'value' => d[spot].rainfall)
end

d = get_yesterday_spots_data
pp d.map {|k, v| [k, v.rainfall.to_f]}.sort {|x, y| y[1] <=> x[1]}[0...10]

# post_graph("東京")

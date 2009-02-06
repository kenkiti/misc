# -*- coding: utf-8 -*-
require 'rubygems'
require 'graphviz'

GraphViz::new( "G", { :type => "digraph", :use => "dot", :output => "png",
    :charset=>"utf8", :file => "vf.png"}) {|g|

  g.node[:fontname] = "osaka"
  g.node[:style] = "filled"
  g.edge[:fontname] = "osaka"

  akira      = g.add_node("結城アキラ")
  sara       = g.add_node("サラ・ブライアント")
  jacky      = g.add_node("ジャッキー・ブライアント")
  wolf       = g.add_node("ウルフ・ホークフィールド")
  aoi        = g.add_node("梅小路葵")
  j6         = g.add_node("JUDGEMENT6")
  dural      = g.add_node("デュラル")
  pai        = g.add_node("パイ・チェン")
  lau        = g.add_node("ラウ・チェン")
  lei        = g.add_node("レイフェイ")
  kage       = g.add_node("影丸")
  jeffry     = g.add_node("ジェフリー・マクワイルド")
  shun       = g.add_node("シュン")
  lion       = g.add_node("リオン")
  takaarashi = g.add_node("鷹嵐")
  jean       = g.add_node("ジャン紅篠")
  eileen     = g.add_node("アイリーン")
  blaze      = g.add_node("エル・ブレイズ")
  blad       = g.add_node("ブラッド・バーンズ")
  vanessa    = g.add_node("バネッサ・ルイス")
  goh        = g.add_node("日守剛")

  g.add_edge(wolf, akira, :label => "対戦を熱望")
  g.add_edge(sara, jacky, :label => "兄妹", :dir => "both")
  g.add_edge(j6, sara, :label => "ターゲット")
  g.add_edge(aoi, akira, :label => "幼少期に共に修行", :dir => "both")
  g.add_edge(pai, lau, :label => "父娘", :dir => "both")
  g.add_edge(lei, lau, :label => "狙う")
  g.add_edge(j6, dural, :label => "戦闘兵器開発")
  g.add_edge(dural, kage, :label => "母子", :dir => "both")
  g.add_edge(jean, lion, :label => "幼馴染み", :dir => "both")
  g.add_edge(eileen, pai, :label => "憧れ")
  g.add_edge(blaze, wolf, :label => "羨望と嫉妬")
  g.add_edge(blad, aoi, :label => "恋仲", :dir => "both")
  g.add_edge(vanessa, sara, :label => "警護")

  g.add_edge(akira     , j6, :label => "修行の成果を試す")
  g.add_edge(lau       , j6, :label => "後継者探し")
  g.add_edge(jacky     , j6, :label => "組織壊滅")
  g.add_edge(sara      , j6, :label => "兄を超える")
  g.add_edge(pai       , j6, :label => "ラウと戦う")
  g.add_edge(wolf      , j6, :label => "エル・ブレイズから挑戦状")
  g.add_edge(kage      , j6, :label => "母の仇")
  g.add_edge(jeffry    , j6, :label => "賞金を狙う")
  g.add_edge(shun      , j6, :label => "さらわれた弟子を探す")
  g.add_edge(lion      , j6, :label => "父との関係を調べる")
  g.add_edge(takaarashi, j6, :label => "自分の限界を試してみたい")
  g.add_edge(j6, jean  , :label => "暗殺部隊")
  g.add_edge(j6, goh   , :label => "暗殺部隊")

}.output()
system("open vf.png")

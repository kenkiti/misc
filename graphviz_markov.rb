# -*- coding: utf-8 -*-
require 'MeCab'
require 'kconv'
require 'rubygems'
require "graphviz"

c = MeCab::Tagger.new("-O wakati")
lyrics = open(ARGV[0]).read.toutf8
words = c.parse(lyrics).split(" ")

nodes = Hash.new([].freeze)
preword = ""
words.each do |word|
  nodes[preword] += [word] if preword != ""
  preword = word
end

GraphViz::new("G", {:type => "digraph", :use => "dot", :output => "png", :charset=>"utf8", :file => "#{ARGV[0]}.png"}) {|g|
  g.node[:fontname] = "osaka"

  nodes.each do |parent, children|
    p = g.add_node(parent)
    children.map {|child| g.add_edge(p, g.add_node(child)) }
  end

}.output()
system("open #{ARGV[0]}.png")

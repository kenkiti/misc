# -*- coding: euc-jp -*-
require 'open-uri'
require 'kconv'
$KCODE = 'e'

pages_data = [
  [1..20, "http://www.geocities.jp/tomomi965/ko-jien01/a%02d.html"],
  [1..22, "http://www.geocities.jp/tomomi965/ko-jien02/ka%02d.html"],
  [1..19, "http://www.geocities.jp/tomomi965/ko-jien03/sa%02d.html"],
  [1..20, "http://www.geocities.jp/tomomi965/ko-jien04/ta%02d.html"],
  [1..11, "http://www.geocities.jp/tomomi965/ko-jien05/na%02d.html"],
  [1..17, "http://www.geocities.jp/tomomi965/ko-jien06/ha%02d.html"],
  [1..14, "http://www.geocities.jp/tomomi965/ko-jien07/ma%02d.html"],
  [1..6, "http://www.geocities.jp/tomomi965/ko-jien08/ya%02d.html"],
  [1..5, "http://www.geocities.jp/tomomi965/ko-jien08/ra%02d.html"],
  [1..2, "http://www.geocities.jp/tomomi965/ko-jien08/wa%02d.html"],
]
PAGES = pages_data.inject([]){|ary, (range, fmt)| ary.concat range.map{|x| fmt % x }}

class String
  def untag!
    gsub!(/<.+?>/, '')
  end
end

def gather
  entries = []
  PAGES.each do |page|
    html = URI(page).read.toeuc
    html.scan(%r!^ +・([^<]+?)</B>（(.+?)）.+$!).each do |kanji,kanas|
      kanji.untag!
      kanas.untag!
      kanas.gsub!(/、/,'')
      next if kanji =~ /^[ぁ-んァ-ンー]+$/
      next if kanas =~ /〜|[ァ-ン]/
      kanas.split(/・/).each do |kana|
        puts "#{kana.toutf8}, #{kanji.toutf8}"
        entries << [kana, kanji]
      end
    end
    sleep 1
  end
  entries
end

# def generate_skk_entry(ary)
#   entries = [ ";; okuri-ari entries.\n", ";; okuri-nasi entries.\n" ]
#   entries.concat ary.map{|kana, kanji|
#     "#{kana} /#{kanji}/\n"
#   }.sort
# end

ary = gather()
p ary

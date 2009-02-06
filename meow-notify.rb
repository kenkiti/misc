# -*- coding: utf-8 -*-
require 'rubygems'
require 'meow'
require 'osx/cocoa'

def notify(title, description)
  m = Meow.new("test")
  m.notify(title, description)
  OSX::NSSound.soundNamed('Submarine').play
end

if $0 == __FILE__
  notify("こんにちは","こんにちははあ")
end

# -*- coding: utf-8 -*-
require 'rubygems'
require 'meow'
require 'osx/cocoa'

def notify(title, description)
  m = Meow.new("test")
  iconImage = Meow.import_image("/Applications/Emacs.app/Contents/Resources/Emacs.icns")
  m.notify(title, description, {:icon => iconImage, :sticky => false, :priority => 2}) do
    system "open -a Firefox http://www.google.com/search?q=clickme"
  end
  OSX::NSSound.soundNamed('Submarine').play
end

if $0 == __FILE__
  notify("こんにちは","こんにちははあ")
end

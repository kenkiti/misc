require 'osx/cocoa'
# names = Dir['/System/Library/Sounds/*.aiff'].grep(/([^\/]+)\.aiff/){ |i| $1 }
# p names
# OSX::NSSound.soundNamed(names[0]).play
# OSX::NSSound.soundNamed(names[1]).play
sound = OSX::NSSound.soundNamed("Blow")
sound.play
# #["Basso", "Blow", "Bottle", "Frog", "Funk", "Glass", "Hero", "Morse", "Ping", "Pop", "Purr", "Sosumi", "Submarine", "Tink"]
#a

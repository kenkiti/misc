#!/opt/local/bin/ruby -w
# -*- coding: utf-8 -*-
require 'rubygems'
require 'ruby-growl'

msg = "#{ Time.now.hour }時ですよ！"

g = Growl.new "localhost", "time_bell", ["time_bell Notification"]
g.notify "time_bell Notification", "Time bell!", msg, 0, true

# -*- coding: utf-8 -*-
require 'pp'

class Array
  def sum
    self.inject(0){|r, i| r += i }
  end
end

class KnightTourFast
  attr_accessor :board

  def initialize(size)
    @board = []
    @square_size = size
  end

  def in_range_and_empty(ty, tx)
    ty>=0 && tx>=0 && ty<@square_size && tx<@square_size && @board[ty][tx] == 0
  end
  
  def fill(y, x, counter)
    @board[y][x] = counter
    exit 0 if counter == @square_size ** 2
    
    empty_neighbours = []
    jumps = [[-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1]]
    jumps.each do |jump|
      ty, tx = y + jump[0], x + jump[1]
      empty_neighbours << [ty, tx] if in_range_and_empty(ty, tx)
    end
    empty_neighbours.sort_by {|v| jumps.map {|j| in_range_and_empty(v[0]+j[0], v[1]+j[1]) ? 1 : 0 }.sum }.each do |ty, tx|
      fill(ty, tx, counter+1)
    end

    @board[y][x] = 0
  end

  def init_board
    1.upto(@square_size) {|i| @board << [0] * @square_size }
  end

  def self.start(size)
    k = self.new(size)
    k.init_board
    k.fill(0, 0, 1)
  rescue SystemExit
    k.board
  else
    "no solution found."
  end
end

class KnightTourNormal
  attr_accessor :board

  def initialize(size)
    @board = []
    @square_size = size
  end

  def in_range_and_empty(ty, tx)
    ty>=0 && tx>=0 && ty<@square_size && tx<@square_size && @board[ty][tx] == 0
  end
  
  def fill(y, x, counter)
    @board[y][x] = counter
    exit 0 if counter == @square_size ** 2
    
    empty_neighbours = []
    jumps = [[-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1]]
    jumps.each do |jump|
      ty, tx = y + jump[0], x + jump[1]
      if in_range_and_empty(ty, tx)
        fill(ty, tx, counter+1)
      end
    end

    @board[y][x] = 0
  end

  def init_board
    1.upto(@square_size) {|i| @board << [0] * @square_size }
  end

  def self.start(size)
    k = self.new(size)
    k.init_board
    k.fill(0, 0, 1)
  rescue SystemExit
    k.board
  else
    "no solution found."
  end
end

def bench(size)
  require 'benchmark'
  Benchmark.bmbm do |b|
    b.report("KnightTourFast") { KnightTourFast.start(size) }
    b.report("KnightTourNormal") { KnightTourNormal.start(size) }
  end
end

if $0 == __FILE__
  if ARGV[0].to_i == 0
    puts "Usage: #{$0} <square size>"
    exit 0
  end
  bench(ARGV[0].to_i)
end


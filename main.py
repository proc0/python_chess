#!/usr/bin/env python
import os
import pygame as pg
from pygame import Surface
from pprint import pprint
# from functools import map

from src.game import Game
from src.board import Board
from src.player import Player

SIZE = (800,640)
PLAYERS = ['white', 'black']

new_player = lambda color: Player({ 'color': color })

def main(): 
  # init
  pg.init()
  pg.font.init()
  # setup
  board = Board((SIZE[1], SIZE[1]))
  game = Game(SIZE, board)
  # ready
  players = list(map(new_player, PLAYERS))
  # begin
  game.run(board, players)
  # gg
  pg.quit()
  return quit()

if __name__=="__main__":
  main()
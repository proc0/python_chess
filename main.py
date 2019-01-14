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

summon = lambda color: Player({ 'color': color })

def main(): 
  # init pygame
  pg.init()
  pg.font.init()
  size = SIZE
  # init game
  board = Board((size[1], size[1]))
  game = Game(size, board)
  # init render
  # board.draw()
  # game.draw(board)
  # summon players
  players = list(map(summon, PLAYERS))
  # begin game
  game.loop(board, players)
  # end
  pg.quit()
  quit()

if __name__=="__main__":
  main()
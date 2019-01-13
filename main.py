#!/usr/bin/env python
import os
import pygame as pg
from pygame import Surface
from pprint import pprint

from src.game import Game
from src.board import Board
from src.player import Player

def main(): 
  # init pygame
  pg.init()
  pg.font.init()
  size = (800,640)
  # init game
  game = Game(size)
  board = Board(size)
  # init render
  board.draw()
  game.draw(board)
  # summon players
  players = [
    Player({'color':'white'}), 
    Player({'color':'black'})
  ]
  # begin game
  game.loop(board, players)
  # end
  pg.quit()
  quit()

if __name__=="__main__":
  main()
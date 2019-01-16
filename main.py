#!/usr/bin/env python
import pygame as pg
from src.game import Game
from src.board import Board
from src.player import new_players

SIZE = (800,640)
PLAYERS = ['white', 'black']

def main(): 
  # init
  pg.init()
  pg.font.init()
  # setup
  board = Board(SIZE[1])
  game = Game(SIZE)
  # ready
  players = new_players(PLAYERS)
  # begin
  game.run(board, players)
  # gg
  pg.quit()
  return quit()

if __name__=="__main__":
  main()
import os
import pygame as pg

_HAND_CURSOR = (
"        XX      ",
"    XX X..XXX   ",
"   X..XX..X.XX  ",
"   X..XX..X.X.X ",
"   X..XX..X.X.X ",
"   X..XX..X.X.X ",
" XX X..X..X.X.X ",
"X..XX.........X ",
"X...X.........X ",
" X.....X.X.X..X ",
"  X....X.X.X..X ",
"  X....X.X.X.X  ",
"   X...X.X.X.X  ",
"    XXXXXXXXX   ",
"     X......X   ",
"     XXXXXXXX   ")
_HCURS, _HMASK = pg.cursors.compile(_HAND_CURSOR, ".", "X")
HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)

_GRAB_CURSOR = (
"                ",
"                ",
"                ",
"     XX XX X X  ",
"    X..X..X.X.X ",
"    X..X..X.X.X ",
"    X.........X ",
"  XXX.........X ",
"  X.X.........X ",
" X.....X.X.X..X ",
" X.....X.X.X..X ",
"  X....X.X.X.X  ",
"   X...X.X.X.X  ",
"    XXXXXXXXX   ",
"     X......X   ",
"     XXXXXXXX   ")
_GCURS, _GMASK = pg.cursors.compile(_GRAB_CURSOR, ".", "X")
GRAB_CURSOR = ((16, 16), (5, 1), _GCURS, _GMASK)
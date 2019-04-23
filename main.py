#!/usr/bin/env python3
import sys
from maze_solver import *

algorithm = "BFS"

# print(sys.argv)
if len(sys.argv)>1:
	algorithm = sys.argv[1].upper()

if len(sys.argv)>2:
	m = Maze(sys.argv[2])
else:
	m = Maze()

m.printMaze(True)
solveMazeGeneral(m, algorithm)

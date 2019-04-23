#!/usr/bin/env python3
import sys
from maze import Maze, Room
from fringe import Fringe
from state import State

def solveMazeGeneral(maze, algorithm):
	#select the right queue for each algorithm
	if algorithm == "BFS":
		fr = Fringe("FIFO")
	elif algorithm == "DFS":
		fr = Fringe("STACK")
	else:
		print("algorithm not found/implemented, exit")
		return;
	
	room = maze.getRoom(*maze.getStart())
	state = State(room, None)
	fr.push(state)		

	while not fr.isEmpty():
	
		state = fr.pop()
		room = state.getRoom()
	
		if room.isGoal():
			print("solved")
			fr.printStats()
			state.printPath()
			maze.printMazeWithPath(state)
			return

		#loop through every possible move
		for d in room.getConnections():
			#get new room after move and cost to get there
			newRoom, cost = room.makeMove(d, state.getCost())
			newState = State(newRoom, state, cost)
			fr.push(newState)  

	print("not solved")
	fr.printStats()


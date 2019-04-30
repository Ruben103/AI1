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
	elif algorithm == "UCS":
		fr = Fringe("PRIO")
	else:
		print("algorithm not found/implemented, exit")
		return
	
	room = maze.getRoom(*maze.getStart())
	state = State(room, None)
	fr.push((0, state))	
	
	#creates a list of all visited rooms
	visited_rooms = [str(room.coords)]

	while not fr.isEmpty():
	
		state = fr.pop()[1]
		room = state.getRoom()
		print(str(room.coords))

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
			priority_tuple = (cost, newState)
			#before pushing a new state, checks if it's in our list
			if not str(newRoom.coords) in visited_rooms:
				visited_rooms.append(str(newRoom.coords))
				fr.push((cost, newState))

	print("not solved")
	fr.printStats()

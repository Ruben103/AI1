#!/usr/bin/env python3
import sys
from maze import Maze, Room
from fringe import Fringe
from state import State

# Calculates straight distance from room to goal. 
# Keeps cost of level changes in mind.
def estimatedDistance(maze, room):
	goal = maze.getGoal()
	loc = room.coords
	estCost = 0
	for x in range(0,3):
		dist = goal[x] - loc[x]
		if x == 2 and dist:
			dist *= 3 if dist > 0 else 2
		estCost += dist ** 2
	return estCost ** 0.5

def solveMazeGeneral(maze, algorithm):
	ASTAR = True if algorithm == "ASTAR" else False
	GREEDY= True if algorithm == "GREEDY" or ASTAR else False
	# Select the right queue
	if algorithm == "BFS":
		fr = Fringe("FIFO")
	elif algorithm == "DFS":
		fr = Fringe("STACK")
	elif algorithm == "UCS" or GREEDY:
		fr = Fringe("PRIO")
	else:
		print("algorithm not found/implemented, exit")
		return

	room = maze.getRoom(*maze.getStart())
	state = State(room, None, 0, estimatedDistance(maze, room))
	fr.push((state.prio, state))	
	
	# Create list of visited rooms
	visited_rooms = [str(room.coords)]

	while not fr.isEmpty():
	
		priority_tuple = fr.pop()
		cost = priority_tuple[0]
		state = priority_tuple[1]
		room = state.getRoom()
		print(str(room.coords))

		if room.isGoal(): # Maze completed.
			print("solved")
			fr.printStats()
			state.printPath()
			maze.printMazeWithPath(state)
			return

		# Loop over every possible move
		for d in room.getConnections():
			# Create new room and determine cost
			newRoom, cost = room.makeMove(d, state.getCost())
			newState = State(newRoom, state, cost)
			# for GREEDY/A*
			if GREEDY:
				cost = estimatedDistance(maze, newRoom)
				cost += state.cost if ASTAR else 0 # add path so far for A*
			priority_tuple = (cost, newState)
			#before pushing a new state, checks if it's in our list
			if not str(newRoom.coords) in visited_rooms:
				visited_rooms.append(str(newRoom.coords))
				fr.push(priority_tuple)

	print("not solved")
	fr.printStats()
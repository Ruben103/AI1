#!/usr/bin/env python3
import sys
from maze import Maze, Room
from fringe import Fringe
from state import State

# Calculates straight distance from room to goal. 
# Keeps cost of level changes in mind.
# Heuristic function for Greedy & A*
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

def solveMazeGeneral(maze, algorithm, l = 1, maxL = 1000):
	ASTAR = True if algorithm == "ASTAR" else False
	GREEDY= True if algorithm == "GREEDY" or ASTAR else False
	IDS   = True if algorithm == "IDS" else False
	# Select the right queue
	if algorithm == "BFS":
		fr = Fringe("FIFO")
	elif algorithm == "DFS" or IDS:
		fr = Fringe("STACK")
	elif algorithm == "UCS" or GREEDY:
		fr = Fringe("PRIO")
	else:
		print("algorithm not found/implemented, exit")
		return

	room = maze.getRoom(*maze.getStart())
	prio = estimatedDistance(maze, room) if GREEDY or ASTAR else 0
	state = State(room, None, 0, prio)
	# Create priority tuple in case of prio queue
	priority_tuple = (prio, state)
	fr.push(priority_tuple)	
	
	# Create list of visited rooms
	visited_rooms = [str(room.coords)]

	while not fr.isEmpty():
		
		# Pop Tuple from fring
		priority_tuple = fr.pop()
		# Read cost and state from tuple
		cost = priority_tuple[0]
		state = priority_tuple[1]
		room = state.getRoom()

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
			newState = State(newRoom, state, cost, state.prio + 1)

			if GREEDY: #or A*
				cost = estimatedDistance(maze, newRoom)
				# add path so far in case of A*
				cost += state.cost if ASTAR else 0
			
			priority_tuple = (cost, newState)
			# If state was not visited beforre
			if not str(newRoom.coords) in visited_rooms:
				# Add to list of visited state
				visited_rooms.append(str(newRoom.coords))
				if not IDS or newState.prio <= l:
					fr.push(priority_tuple)
	# In case of IDS in																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																				```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````																	```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
	if IDS and fr.isEmpty and l < maxL:
		solveMazeGeneral(maze, algorithm, l+1, maxL)
	else: 
		print("not solved")
		fr.printStats()
#!/usr/bin/env python3
from state import State


class Room:
	"""Class to save all the characteristics of a room"""
	def __init__(self, coords, maze):
		# order: UP, DOWN, NORTH, SOUTH, EAST, WEST
		self.connections = []
		self.heuristicValue = 0
		self.costs = dict()
		self.coords = coords
		self.__goal = False
		self.__start = False
		self.maze = maze
	
	# returns true if a move is possible in this room
	def canMoveTo(self,d):
		return d in self.connections

	# returns all the possible moves
	def getConnections(self):
		return self.connections

	# returns true if the room is the goal room
	def isGoal(self):
		return self.__goal

	# sets the room as goal
	def setGoal(self):
		self.__goal =  True
	
	# returns true if the room is the start room
	def isStart(self):
		return self.__start

	# sets the room as start point
	def setStart(self):
		self.__start =  True

	# returns the coordinates of the room 
	def getCoords(self):
		return self.coords

	# returns the heuristic value of the rooms
	def getHeuristicValue(self):
		return self.heuristicValue

	# returns the new room + cost if move is possible, returns None otherwise
	def makeMove(self, direction, cost):
		x,y,z = self.coords
		# if move is not valid, return None
		if not self.canMoveTo(direction):
			return None
		cost += self.costs[direction]
		if direction is "UP":
			z += 1
		if direction is "DOWN":
			z -= 1
		if direction is "EAST":
			x += 1
		if direction is "WEST":
			x -= 1
		if direction is "NORTH":
			y -= 1
		if direction is "SOUTH":
			y += 1
		return (self.maze.rooms[x][y][z],cost)

	
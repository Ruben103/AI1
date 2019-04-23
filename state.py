#!/usr/bin/env python3

class State:
	"""Class to save the possible states in"""
	def __init__(self, room, parent, cost=0, prio=0):
		self.parent = parent
		self.room = room
		self.cost = cost
		self.prio = prio

	# returns the current room
	def getRoom(self):
		return self.room

	# returns the previous state
	def getParent(self):
		return self.parent

	# returns the cost of the state
	def getCost(self):
		return self.cost

	# sets the cost of the state
	def setCost(self, cost):
		self.cost = cost

	# helper function to print the path
	def printPathHelper(self):
		s = ""
		if self.parent is not None:
			self.parent.printPathHelper()
			s =  str(self.parent.room.coords) + " -> "
			s += str(self.room.coords)
			s += " cost: "+str(self.cost)
			print(s)

	# prints the found path
	def printPath(self):
		self.printPathHelper()
		print()

	# function used to compare two states for the priority queue
	def __lt__(self, other):
		return self.prio < other.prio
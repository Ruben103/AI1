#!/usr/bin/env python3
import sys
from state import State
from room import Room

class Maze:
	"""Class to save all the characteristics of a maze"""
	def __init__(self, fileName="default.maze"):
		self.readMaze(fileName)
		super(Maze, self).__init__()
		
	def getGoal(self):
		return self.goal

	def getStart(self):
		return self.start

	def getRoom(self, floor, col, row):
		return self.rooms[floor][col][row]


	""" The part below is only for reading the maze files and printing the maze
		it is not needed to look through it or to understand it """

	def getMoveDir(self, fromCoords, toCoords):
		if fromCoords[2]-toCoords[2]==-1:
			return "UP"
		if fromCoords[2]-toCoords[2]==1:
			return "DOWN"
		if fromCoords[0]-toCoords[0]==-1:
			return "EAST"
		if fromCoords[0]-toCoords[0]==1:
			return "WEST"
		if fromCoords[1]-toCoords[1]==1:
			return "NORTH"
		if fromCoords[1]-toCoords[1]==-1:
			return "SOUTH"
		return ""

	def getDir(self, room, toFrom, direction):
		coords = room.getCoords()
		if coords in direction and toFrom in direction[coords]:
			return direction[room.getCoords()][toFrom]
		return ""

	def readMaze(self, fileName):
		try:
			f = open(fileName, "r")
		except FileNotFoundError:
			print("File: "+fileName+" not found, exit")
			sys.exit(-1)
		self.width 	= int(f.readline().split("Width:")[1].strip())
		self.height = int(f.readline().split("Height:")[1].strip())
		self.floors = int(f.readline().split("Floors:")[1].strip())
		self.rooms = [[[None for _ in range(self.floors)] \
		for _ in range(self.height)] for _ in range(self.width)]

		for idx in range(self.floors):
			self.readFloor(f)

	def getHeuristic(self,row):
		s = (str(row[1])+str(row[2])).strip()
		try:
			return int(s)
		except ValueError:
			return None

	def checkConnection(self,room, cell, direction):
		check = " "
		cost = 1
		if direction == "UP":
			check = "U"
			cost += 2
		if direction == "DOWN":
			check = "D"
			cost += 1
		if cell == check or cell.isnumeric():
			room.connections.append(direction)
			if cell.isnumeric():
				room.costs[direction]=int(cell)
			else:
				room.costs[direction]=cost

	def readFloor(self, f):
		line = f.readline()
		#get rid of empty lines
		while("Floor #" not in line):
			line = f.readline() 
		floor = int(line.split("Floor #")[1].strip())
		lines = [None]*5
		# order:0 UP, 1 DOWN,2 NORTH,3 SOUTH,4 EAST,5 WEST

		#read first row
		lines[0] = f.readline()
		#loop through each row
		for idy in range(self.height):
			for i in range(1,5):
				lines[i] = f.readline()
			for idx in range(self.width):
				#create room and add to array
				room = Room((idx,idy,floor), self)
				self.rooms[idx][idy][floor] = room
				start = idx*8
				#get part of input for one room
				r = [row[start:start+9] for row in lines]
				room.heuristicValue = self.getHeuristic(r[1]);
				self.checkConnection(room, r[2][2], "UP")
				self.checkConnection(room, r[2][6], "DOWN")
				self.checkConnection(room, r[0][4], "NORTH")
				self.checkConnection(room, r[4][4], "SOUTH")
				self.checkConnection(room, r[2][8], "EAST")
				self.checkConnection(room, r[2][0], "WEST")
				if "G" in r[2]:
					self.goal=(idx,idy,floor)
					room.setGoal()
				if "X" in r[2]:
					self.start=(idx,idy,floor)
					room.setStart()
			#last line is first line for next row
			lines[0] = lines[4]

	def getRoomLineOne(self, room, printCoords, direction):
		# value_when_true if condition else value_when_false
		c = " "
		if self.getDir(room, 'from', direction) is "NORTH":
			c = "v" 
		if self.getDir(room, 'to',direction) is "NORTH":
			c = "^" 

		return ("|--|%s|--" % c) if room.canMoveTo("NORTH") else ("|-------")

	def getRoomLineTwo(self, room, printCoords, direction):
		west = "-" if room.canMoveTo("WEST") else "|"
		c = " "
		if self.getDir(room, 'from', direction) is "NORTH":
			c = "v" 
		if self.getDir(room, 'to',direction) is "NORTH":
			c = "^" 
		heuristic = "  "
		if room.getHeuristicValue() is not None:
			heuristic = '{:>2}'.format(room.getHeuristicValue())
		cost = "   "
		coords = room.getCoords() 
		if coords in direction and 'cost' in direction[coords]:
			cost = '{:>3}'.format(direction[room.getCoords()]['cost'])
		return ("%s%s %s%s" % (west, heuristic, c, cost) )


	def getMiddleChar(self, room, direction):
		if room.isStart():
			return "X"
		if room.isGoal():
			return "G"
		if self.getDir(room, 'to', direction) is "UP":
			return "o" 
		if self.getDir(room, 'to', direction) is "DOWN":
			return "o" 
		if self.getDir(room, 'from', direction) is "UP":
			return "o" 
		if self.getDir(room, 'from', direction) is "DOWN":
			return "o" 
		return " "

	def getRoomLineThree(self, room, printCoords, direction):
		up = "U" if room.canMoveTo("UP")  else " "
		down = "D" if room.canMoveTo("DOWN")  else " "
		west = " " if room.canMoveTo("WEST") else "|"
		fromToWest = " "
		fromToEast = " "
		if self.getDir(room, 'from', direction) is "WEST":
			fromToWest = ">"
		if self.getDir(room, 'to', direction) is "WEST":
			fromToWest = "<" 
		if self.getDir(room, 'from', direction) is "EAST":
			fromToEast = "<"
		if self.getDir(room, 'to', direction) is "EAST":
			fromToEast = ">"

		mid = self.getMiddleChar(room, direction)
		return ("%s%s%s%s%s%s%s%s" % \
		(west, fromToWest, up, fromToWest ,mid, fromToEast, down, fromToEast))

	def getRoomLineFour(self, room, printCoords, direction):
		west = "-" if room.canMoveTo("WEST") else "|"
		if printCoords:
			return ("%s %s %s %s " % ((west,)+room.getCoords()) )
		c = " "
		if self.getDir(room, 'from' ,direction) is "SOUTH":
			c = "^"
		if self.getDir(room, 'to', direction) is "SOUTH":
			c = "v" 
		return ("%s   %s   " % (west, c) )

	def getDirections(self, state):
		direction = {}
		while state is not None:
			parent = state.getParent()
			if parent is None:
				break;
			coords = state.getRoom().getCoords()
			if coords not in direction:
				direction[coords] = {}
			direction[coords]['from'] =	\
			self.getMoveDir( coords, parent.getRoom().getCoords())
			direction[coords]['cost'] = state.getCost()

			if parent.getRoom().getCoords() not in direction:
				direction[parent.getRoom().getCoords()] = {}
			direction[parent.getRoom().getCoords()]['to'] =	\
			self.getMoveDir( parent.getRoom().getCoords(), coords)
			
			state=parent		
		return (direction)


	def getFloorString(self,idz, printCoords, direction={}):
		
		#create total number of lines for floor
		lines = [""]*(4*self.height+1)
		yLine = 0
		for idy in range(self.height):
			yLine = idy*4
			for idx in range(self.width):
				r = self.rooms[idx][idy][idz]
				lines[yLine] += self.getRoomLineOne(r, printCoords, direction)
				lines[yLine+1] += self.getRoomLineTwo(r, printCoords, direction)
				lines[yLine+2] += self.getRoomLineThree(r, printCoords, direction)
				lines[yLine+3] += self.getRoomLineFour(r, printCoords, direction)
					
			for i in range(4):
				lines[yLine+i] += "|"
		lines[yLine+4] += "|-------"*self.width + "|"
		return lines

		
	def printMaze(self, printCoords=False):

		self.printMazeWithPath(None, printCoords=printCoords)

	def printMazeWithPath(self, state, printCoords=False):
		d = self.getDirections(state)
		print("Width: %d \nHeight: %d \nFloors: %d" %\
		(self.width, self.height, self.floors))

		#loop descending through all floors
		for f in range(self.floors-1, -1,-1):
			print("\nFloor #"+str(f))
			for line in self.getFloorString(f, printCoords, direction=d):
				print(line)

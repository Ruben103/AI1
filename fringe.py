#!/usr/bin/env python3
import queue, sys

class Fringe(object):
	"""wrapper for queue lib from python to keep track of some statistics"""

	### DO NOT CHANGE MAXFRINGESIZE
	__MAXFRINGESIZE = 500000
	__fringe = None
	__insertions = 0
	__deletions = 0
	__maxSize = 0

	def createFringe(self, type):
		if type is "STACK":
			return queue.LifoQueue(self.__MAXFRINGESIZE)
			
		if type is "FIFO":
			return queue.Queue(self.__MAXFRINGESIZE)

		if type is "PRIO":
			return queue.PriorityQueue(self.__MAXFRINGESIZE)

	def __init__(self, type='FIFO'):
		self.__type = type
		super(Fringe, self).__init__()
		self.__fringe = self.createFringe(self.__type)


	# push item in fringe
	def push(self, item):
		#if fringe is full, print error and exit
		if self.__fringe.full():
			#item.getRoom().maze.printMazeWithPath(item)
			print("Error: trying to apply push on an fringe "\
				"that already contains MAX(="+str(self.__MAXFRINGESIZE)+") elements")
			self.printStats()
			sys.exit(1)
		self.__fringe.put(item, block=False)
		if self.__fringe.qsize() > self.__maxSize:
			self.__maxSize = self.__fringe.qsize()
		self.__insertions += 1
	
	# returns item from fringe. Returns None object if fringe is empty
	def pop(self):
		if self.__fringe.empty():
			return None
		self.__deletions += 1
		return self.__fringe.get()

	# returns true if fringe is empty
	def isEmpty(self):
		return self.__fringe.empty()

	# returns the number of insertions
	def getInsertions(self):
		return self.__insertions

	#returns the number of deletions
	def getDeletions(self):
		return self.__deletions

	def printStats(self):
		print("#### fringe statistics:")
		print("size: {0:>15d}".format(self.__fringe.qsize()))
		print("maximum size: {0:>7d}".format(self.__maxSize))
		print("insertions: {0:>9d}".format(self.getInsertions()))
		print("deletions: {0:>10d}".format(self.getDeletions()))


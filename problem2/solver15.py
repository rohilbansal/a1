#!/usr/local/bin/python3
# Developed by vpatani

'''

15 puzzle Problem Abstraction:

• Initial State: A random/user input state with 15 tiles on the board, each occupying exactly one place
on the board. No duplicates are allowed. The board may often times be unsolvable.

• Goal State: Tiles arranged in the correct order from 1 to 15 and the blank space at the end after the
15th tile, wherein one tile exactly occupies one place.

• Valid State: Any state generated by the successor() is valid, where each tiles occupies exactly one
place.

• State State: State Space is the collection of all the states that have been discovered but not visited,
they are stored in a fringe, which constantly pops the state with the lowest cost (i.e. the sum of g(s) +
f(s)).

• Successor Functions: Through each state there are 4 possible states, wherein the tile can slide D,
U, R, L into the empty place. Technically only 3 would be good to use depending upon the previous
state, otherwise you would be replicating the parent state by moving back in the same position. Eg:
If your parent is L, then moving in the Right direction would lead you back to the same state, hence
we can eliminate that.

• Cost Functions: Cost Function is the cost of travelling from one state to another which is 1 for
each movement. Also we use a heuristic to estimate the length of the goal which helps us get to the
solution quicker than the brute force way.
Implementation Details: Try to make your solver as fast as possible. Which heuristic functions did you
try, and which works best?

• We tried three different heuristics:

– Hamming Distance: This heuristic calculates the number of misplaced tiles. In other words,
all it does is that it checks whether if a tile is in its location, if not adds 1 to the cost. This is
not a particularly good estimate of how far are we from the solution. The idea of a heuristic is to
estimate the distance from the goal which in turn allows us to select a good probable path. Even
though this is admissible since it does not overestimate the cost, it duly underestimates it most
of the times.

– Permutation Inversion: This heuristic particularly checks for inversion, which means it checks
how many pairs are out of order. This is often times not admissible and hence can be discarded,
since heuristic functions do not allow us to overestimate the distance to the goal.
Problem 2 continued on next page. . .
Page 4 of 8bansalro/vpatani/zehzhang

– Manhattan Distance: This heuristic calculates the steps for each tile to reach its correct
position when no other tiles is on the table. This is the best of the three, since it does not over
estimate (admissible) but also gives us a fair amount of idea as to how far are we from the solution.
Manhattan distance is also consistent because it generates a heuristic better than the current state for, 
its neighbours. Also, the cases for edge movements have been handled for the flip tile moves otherwise
it would have been over estimated because we can travel 3 moves in the x direction, but with the flip tile
movement if at all you have to travel 3 steps, you could always do it one step and the same goes for y.

• We implemented A* search algorithm to find the optimal path to the solution, code would be present
in the problem2 folder. We have used tuples to enhance efficiency and also because it can be easily 
hashed which in turn reduces the access times to check visited states and storing the elements in the fringe set.

Algorithm:

if (current_state is goal_state) return initial state
fringe.add (initial_state)
Repeat until fringe is empty:
	fringe.pop() <- current
	visited.add (current)
	if current == goal: return path
	for each_successor in successor_list(s):
		if successor in visited: ignore
		calc_heuristic()
		if successor in fringe: old_successor = fringe.pop()
			compare successors and insert smaller one
		if not in fringe, insert.


• Tests carried for professors input, we obtain a path of 24 steps (LLUURULULDRDRDRRULDRUUUL)
within about 2 seconds (0:00:02.189130) on our local machines. There are various test cases we tried,
some take a while and some happen quickly, it fairly depends upon the complexity of the input.
'''

import sys
import os
import copy
import math
import numpy as np
import datetime
from operator import itemgetter

# Defines the n for (n^2 - 1) puzzle
n = 4


class State(object):
	"""
	Defines the state each of obect along with its properties
	"""
	puzzle = tuple()
	link = ''
	total = 0
	
	def __init__(self, puzzle, cost, link):
		"""
		Constructor
		"""
		self.puzzle = puzzle
		self.heuristic = self.manhattan()
		self.cost = cost
		self.link = link

	def __eq__ (self, other):
		"""
		Overrides the default equal to
		"""
		return self.puzzle == other.puzzle

	def __ne__ (self, other):
		"""
		Overrides the default not equal to
		"""
		return self.puzzle != other.puzzle

	def __hash__ (self):
		"""
		Overrides the hash, needed to store a state in a tuple/dictionary
		"""
		return hash(self.puzzle)

	def successors(self):
		"""
		Obtains the successors for the current state, it only uses 3/4 L,R,D,U
		We check the previous move and eliminate the opposite move, otherwise it would anyway
		replicate the parent state.
		"""

		# Obtain coordinates of 0
		conv = np.asarray(self.puzzle)
		blank = np.where(conv == 0)
		x = blank[0][0]
		y = blank[1][0]

		successor_list = []

		"""
		Just to make sure, we do not repeat the parent state.
		"""
		if (self.link[-1] != 'U'):
			successor_list.append(self.move_down(np.asarray(copy.deepcopy(self.puzzle)), x, y, x-1, y)) # Move Down
		if (self.link[-1] != 'D'):
			successor_list.append(self.move_up(np.asarray(copy.deepcopy(self.puzzle)), x, y, x+1, y)) # Move Up
		if (self.link[-1] != 'R'):
			successor_list.append(self.move_left(np.asarray(copy.deepcopy(self.puzzle)), x, y, x, y+1)) # Move Left
		if (self.link[-1] != 'L'):
			successor_list.append(self.move_right(np.asarray(copy.deepcopy(self.puzzle)), x, y, x, y-1)) # Move right

		return successor_list

	def move_down(self, newstate, x0, y0, x1, y1):
		"""
		Returns the down movement of tile/Up movement of space
		"""
		temp = newstate[x0][y0]
		if (x1 < 0):
			newstate[x0][y0] = newstate[n-1][y1]
			newstate[n-1][y1] = temp
		else:
			newstate[x0][y0] = newstate[x1][y1]
			newstate[x1][y1] = temp

		# Return a deep copied new state preserving the old state
		return State(tuple(map(tuple, newstate)), self.cost + 1, self.link + 'D')

	def move_up(self, newstate, x0, y0, x1, y1):
		"""
		Returns the up movement of tile/down movement of space
		"""
		temp = newstate[x0][y0]
		if (x1 > (n-1)):
			newstate[x0][y0] = newstate[0][y1]
			newstate[0][y1] = temp
		else:
			newstate[x0][y0] = newstate[x1][y1]
			newstate[x1][y1] = temp

		# Return a deep copied new state preserving the old state
		return State(tuple(map(tuple, newstate)), self.cost + 1, self.link + 'U')

	def move_right(self, newstate, x0, y0, x1, y1):
		"""
		Returns the right movement of tile/left movement of space
		"""
		temp = newstate[x0][y0]
		if (y1 < 0):
			newstate[x0][y0] = newstate[x1][n-1]
			newstate[x1][n-1] = temp
		else:
			newstate[x0][y0] = newstate[x1][y1]
			newstate[x1][y1] = temp

		return State(tuple(map(tuple, newstate)), self.cost + 1, self.link + 'R')

	def move_left(self, newstate, x0, y0, x1, y1):
		"""
		Returns the left movement of tile/right movement of space
		"""
		temp = newstate[x0][y0]
		if (y1 > (n-1)):
			newstate[x0][y0] = newstate[x1][0]
			newstate[x1][0] = temp
		else:
			newstate[x0][y0] = newstate[x1][y1]
			newstate[x1][y1] = temp

		return State(tuple(map(tuple, newstate)), self.cost + 1, self.link + 'L')

	def manhattan (self):
		"""
		Returns the manhattan distance for a particular state.
		"""
		goal = {0:None,
			1:[0,0], 2:[0,1], 3:[0,2], 4:[0,3],
			5:[1,0], 6:[1,1], 7:[1,2], 8:[1,3],
			9:[2,0], 10:[2,1], 11:[2,2], 12:[2,3],
			13:[3,0], 14:[3,1], 15:[3,2]}


		current = {}
		conv = np.asarray(self.puzzle)

		for each_row in range(len(conv)):
			for each_column in range(len(conv[each_row])):
				temp = []
				output = np.where(conv == conv[each_row][each_column])
				for each_section in output:
					temp.append(each_section[0])
				current[conv[each_row][each_column]] = temp

		total = 0
		for key in goal:
			a = current[key]
			b = goal[key]
			if b:
				x = abs(a[0] - b[0])
				y = abs(a[1] - b[1])
				if x >= 3: x = 1 # To incorpotate the flip tile movement.
				if y >= 3: y = 1 # To incorpotate the flip tile movement.
				total += (x+y)
		return total

	def hamming (self):
		"""
		Returns hamming distance between goal state and current state.
		Hamming distance is when a tile is not in place the count is incremented by 1
		"""
		goal_state = tuple(((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0)))
		total = 0
		for each_row in range(len(goal_state)):
			for each_column in range(len(goal_state[each_row])):
				if (goal_state[each_row][each_column] != self.puzzle[each_row][each_column]):
					total += 1
		return total

def get_puzzle():

    """
    Get puzzle, returns the default state board,
    if no input is found then a default input is provided
    """

    if (sys.argv[1] and os.path.isfile(sys.argv[1])):
        file = open(sys.argv[1])
    else:
        print("No file found, using default file!")
        file = open('input.txt','r',encoding='utf-8')

    reader = file.read()
    file.close()

    reader = get_list(reader)
    return reader

def get_list(reader, n=4):
    """
    Returns an integer list of the input
    """
    lst = reader.split()

    #This step is done to avoid utf-8 encoding
    lst[-1] = lst[-1].replace('\ufeff','')

    matrix = [[0 for x in range(n)] for y in range(n)]
    counter = 0;
    for each_row in range(n):
        for each_column in range(n):
            matrix[each_row][each_column] = int(lst[counter])
            counter += 1;

    for each_item in range(len(matrix)):
        matrix[each_item] = tuple(matrix[each_item])

    return tuple(matrix)

def is_solvable(puzzle):
	"""
	Checks for the solvability of a certain state.
	"""

	# Flatten the puzzle
	items = [element for tupl in puzzle for element in tupl]
	
	# Count the number of inversions
	count = 0
	for item in range(len(items)-1):
		current = items[item]
		for each in range(item + 1, len(items)):
			if (items[item] and items[each] and items[item] > items[each]):
				count+=1

	# Find the location of blank tile.
	blank = 0
	for row in reversed(range(len(puzzle))):
		if 0 in puzzle[row]:
			blank = row

	# Conditions
	if (len(puzzle) & 1):
		#print(puzzle)
		return not (count & 1)

	else:
		if (blank & 1):
			return not (count & 1)
		else:
			return count & 1

def main():

	"""
	A* implementation to solve 15 puzzle problem.
	"""
	#a = datetime.datetime.now()

	# GOOOAAAAALLLLLLL STATE
	goal_state = tuple(((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0)))
	goal = State(goal_state, 0, '')

	# Initial State from file, a default input.txt needs to be given
	start_state = get_puzzle()
	start = State(start_state, 0, '0')

	# If the input is goal! That would be awesome!
	if (start == goal):
		return start

	# Check for solvability
	if not is_solvable(start.puzzle):
		print("No solution")
		return

	# To store the state
	start_data = (start.heuristic, start)

	#To check for visited states/nodes
	visited = set()

	items = []

	# A dictionary to store state data
	fringe = {start: start_data}
	items.append(start_data)
	
	# Keep looping until there are states to explore
	while items:

		# The items is our fringe, it is sorted by the cost, so everytime you pop(0) you get
		# the state which has the least total cost
		current_data = items.pop(0)
		heuristic_cost, current_state = current_data
		
		# GOOOOAAAALLLLLL STATE
		if (current_state == goal):
			#print(current_state.link[1:])
			# To add spaces, if your test case fails, please uncomment the line above
			# and comment the line below
			print(current_state.link.replace("", " ")[2: -1][1:-1])
			#b = datetime.datetime.now()
			#print(b-a)
			break

		# Once visited, remove from dictionary and add it to closed/visited
		del fringe[current_state]
		visited.add(current_state.puzzle)

		# Fetches all the successors for current state.
		for successor in current_state.successors():

			# If it exists in visited, ignore it.
			if successor.puzzle in visited:
				continue

			# Cost Calculation
			successor.total = successor.cost + successor.heuristic
			successor_data = (successor.total, successor)
			
			# If successor is not in fringe, add it
			if successor not in fringe:
				fringe[successor] = successor_data
				items.append(successor_data)
			else:
			# If it is, check for the same element and compare priorities
			# If priority of current successor is less, replace that successor with this
				previous = fringe[successor]
				if successor.total < previous[1].total:
					previous = successor_data

			# Sort it, so that you always get the smallest state.
			items = sorted(items,key=itemgetter(0))


if __name__ == "__main__":
	"""
	Boilerplate Python
	"""
	main()

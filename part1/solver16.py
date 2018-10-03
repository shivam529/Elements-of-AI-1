#!/usr/bin/env python3
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
#
from queue import PriorityQueue
from random import randrange, sample
import sys
import string
import math

# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row*4):(row*4+4)]
    return ( state[:(row*4)] + change_row[-dir:] + change_row[:-dir] + state[(row*4+4):], ("L" if dir == -1 else "R") + str(row+1) )

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print ('%3d %3d %3d %3d'  %(row[j:(j+4)]))

# return a list of possible successor states
def successors(state):
    return [ shift_row(state, i, d) for i in range(0,4) for d in (1,-1) ] + [ shift_col(state, i, d) for i in range(0,4) for d in (1,-1) ] 

# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))

# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)


def heuristic(board):
    h = 0
    for i in range(16):
        h += mandist(board, i)
    return h
    

'''
The following function calculates the Manhattan distance for the heuristic.
In this, a is the index of the current state of the board and b is the index of the goal state.
At first, it calculates the value of b as per the goal state. Then, for that b, it calculates the Manhattan distance.
a_row and b_row are the row values of a and b respectively and a_col and b_col are the column values of a and b respectively.
Now, while calculating man_dist, it considers the min value of the differnces of rows and columns for satisfying the wrapping
condition.

'''
def mandist(board, a):
    b = 0
    count = 0
    while(sorted(board)[b] != board[a]):
        b += 1

    a_row = a//4
    a_col = a % 4
    b_row = b//4
    b_col = b % 4
    row_d = abs(a_row-b_row)
    col_d = abs(a_col-b_col)
    man_dist = min(row_d, 4-row_d)+min(col_d, 4-col_d)
    return man_dist




    
# The solve function uses priority queue and takes calculated heuristic value as the priority.
def solve(initial_board):
    fringe = PriorityQueue();
    fringe.put((0,initial_board, ""))
    while not fringe.empty():
        (state, route_so_far) = fringe.get()[1:]
        for (succ, move) in successors( state ):
            h=heuristic(succ)
            if is_goal(succ):
                return( route_so_far + " " + move )
            fringe.put((h,succ, route_so_far + " " + move ) )
    return False

# test cases
start_state = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [ int(i) for i in line.split() ]

if len(start_state) != 16:
    print ("Error: couldn't parse start state file")

print ("Start state: ")
print_board(tuple(start_state))

print ("Solving...")
route = solve(tuple(start_state))

print ("Solution found in " + str(len(route)/3) + " moves:" + "\n" + route)

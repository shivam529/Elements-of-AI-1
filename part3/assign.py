#!/usr/bin/env python3

import sys
from queue import PriorityQueue

myfile = str(sys.argv[1])
K = int(sys.argv[2])
M = int(sys.argv[3])
N = int(sys.argv[4])
Preferances = []
myclass = []


class student:
    def __init__(self, name,group_size,p_members,np_members):
        self.name = name
        self.group_size = group_size
        self.p_members = p_members
        self.np_members = np_members

def read():
    path=myfile
    file = open(path)
    i = 0
    while( True ):
        a = file.readline().split()
        if a == []:
            break
        sample = student(a[0],int(a[1]),a[2].split(","),a[3].split(","))
        Preferances.append([sample])
        myclass.append([sample])
    file.close()

def time_calculator(a_class,k,m,n):
    k_count = len(a_class)
    g_count = 0
    n_count = 0
    m_count = 0
    for group in a_class:
        for each in group:
            if each.group_size != len(group) and each.group_size != 0:
                g_count += 1 
            n_count += len(set(each.p_members) - set("_") - set(i.name for i in group))
            m_count += len((set(each.np_members) - set("_")).intersection((set(i.name for i in group))))
    return ((k_count * k) + g_count + (n_count * n) + (m_count * m))

def successors(sample_class):
    N = len(sample_class)
    Successor_states = []
    for i in range(0,N-1):
        if (len(sample_class[i])+len(sample_class[i+1])) < 4:
            if len(sample_class[i]) > 1:
                if Preferances.index([sample_class[i][1]]) < Preferances.index(sample_class[i+1]):
                    Successor_states.append(sample_class[0:i] + [sample_class[i] + sample_class[i+1]] + sample_class[i+2:])
                else:
                    Successor_states.append(sample_class[0:i] + [[sample_class[i][0]] + sample_class[i+1] + [sample_class[i][1]]] + sample_class[i+2:])
            else:
                Successor_states.append(sample_class[0:i] + [sample_class[i] + sample_class[i+1]] + sample_class[i+2:])
        for j in range(i+1,N-1):
            if (len(sample_class[i])+len(sample_class[j+1])) < 4:
                if len(sample_class[i]) > 1:
                    if Preferances.index([sample_class[i][1]]) < Preferances.index(sample_class[j+1]):
                        Successor_states.append(sample_class[0:i] + [sample_class[i] + sample_class[j+1]] + sample_class[i+1:j+1] + sample_class[j+2:])
                    else:
                        Successor_states.append(sample_class[0:i] + [[sample_class[i][0]] + sample_class[j+1] + [sample_class[i][1]]] + sample_class[i+1:j+1] + sample_class[j+2:])
                else:
                    Successor_states.append(sample_class[0:i] + [sample_class[i] + sample_class[j+1]] + sample_class[i+1:j+1] + sample_class[j+2:])
    return Successor_states

def print_my_class(a_class):
    for group in a_class:
        for each in group:
            print("%s" %(each.name), end = " ")
        print("")

def solve(myclass):
    Fringe = PriorityQueue()
    checkFringe = PriorityQueue()
    All_states = [myclass]
    Fringe.put((time_calculator(myclass,K,M,N),1,[myclass]))
    checkFringe.put((time_calculator(myclass,K,M,N),1,[myclass]))
    counter = 1
    while not Fringe.empty():
        x = Fringe.get()
        Fringe = PriorityQueue()
        for each in successors(x[2][0]):
            if each not in All_states:
                counter += 1
                time = time_calculator(each,K,M,N)
                Fringe.put((time,counter,[each]))            
                checkFringe.put((time,counter,[each]))
                All_states.append(each)
    Best_Class = checkFringe.get()
    print_my_class(Best_Class[2][0])
    print(Best_Class[0])

def solve2(myclass):
    Fringe = PriorityQueue()
    checkFringe = PriorityQueue()
    All_states = [myclass]
    Fringe.put((time_calculator(myclass,K,M,N),1,[myclass]))
    checkFringe.put((time_calculator(myclass,K,M,N),1,[myclass]))
    counter = 1
    while not Fringe.empty():
        x = Fringe.get()
        for each in successors(x[2][0]):
            if each not in All_states:
                counter += 1
                time = time_calculator(each,K,M,N)
                Fringe.put((time,counter,[each]))            
                checkFringe.put((time,counter,[each]))
                All_states.append(each)
    Best_Class = checkFringe.get()
    print("Best Class is :")
    print_my_class(Best_Class[2][0])
    print("Time needed for this class is ",Best_Class[0])
    print(counter)

def solve1(myclass):
    Fringe = [myclass]
    checkFringe = [myclass]
    while len(Fringe) > 0:
        for each in successors(Fringe.pop(0)):
            if each not in checkFringe:
                Fringe.append(each)            
                checkFringe.append(each)
    
    Best_Time = 10000
    Best_Class = []
    for each in checkFringe:
        #print_my_class(each)
        time = time_calculator(each,K,M,N)
        if Best_Time > time:
            Best_Time = time
            Best_Class = each
    print(len(checkFringe))
    print("Best Class is :")
    print_my_class(Best_Class)
    print("Time needed for this class is ",Best_Time)

# MAIN

read()
solve(myclass)

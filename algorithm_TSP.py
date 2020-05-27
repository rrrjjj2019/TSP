# Implementation of the Branch and Bound Algorithm
from itertools import *
from time import clock
from Branch_and_bound import travel
import numpy as np
import random
#from BruteForce import GeneratePaths

# Implementation of the Brute Force algorithm
# from itertools import *
# from time import clock

def GeneratePaths(BF_arrMatrix):
    # Extracting the nodes of the TSP
    lstNodes = [node for node in range(len(BF_arrMatrix))]
    #print(lstNodes)
    # Remove the last city to generate non cyclic permutations
    last_node = lstNodes.pop()

    # Enumerating all the paths from the nodes
    lstPermutations = list(permutations(lstNodes))
    #print(lstPermutations)
    # Constructing a tree
    lstTree = list(map(list, lstPermutations))
    #print(lstTree)
    
    # Closing the paths / Constructing full cycles
    for path in lstTree:
        path.append(last_node)
        path.append(path[0])
    
    #print(lstTree)

    return lstNodes, lstTree

def BruteForce(BF_arrMatrix):
    #print(BF_arrMatrix)
    # Start time
    start = clock()
    
    # Generate all the possible paths
    lstNodes, lstTree = GeneratePaths(BF_arrMatrix)
    # print(lstNodes)
    # print(lstTree)
    
    # Calculating the cost of each cycle
    lstCostList = []
    for cycle in lstTree:
        #print("cycle = " + str(cycle))
        # Initialize cost for each cycle
        numCostPerCycle = 0
        # Convert each 2 nodes in a cycle to an index in the input array
        for index in range(0,(len(lstNodes) + 1)):
            # CostPerCycle is calculated from the input Matrix between 
            #   each 2 nodes in a cycle
            #print("index = " + str(index))
            numCostPerCycle = numCostPerCycle + BF_arrMatrix[cycle[index]][cycle[index+1]]
        lstCostList.append(numCostPerCycle)
    
    # Calculating the least cost cycle
    numLeastCost = min(lstCostList)
    numLeastCostIndex = lstCostList.index(numLeastCost)
    
    BF_time = clock() - start

    BF_output = ["Brute Force", numLeastCost, lstTree[numLeastCostIndex], BF_time]
    
    return(BF_output)



def BranchNBound(BnB_arrMatrix):
    # Start timer
    start = clock()
    # Generate the TSP nodes and all the possible paths
    lstNodes, lstTree = GeneratePaths(BnB_arrMatrix)
    
    # Calculating the cost of each cycle
    lstCostList = []
    # Initialize the current best/optimal cost to infinity
    numCurrentBestCost = float("inf")    
    for cycle in lstTree:
        # Initialize cost for each cycle
        numCostPerCycle = 0
        # Convert each 2 nodes in a cycle to an index in the input array
        for index in range(0,(len(lstNodes) + 1)):
            # CostPerCycle is calculated from the input Matrix between 
            #   each 2 nodes in a cycle
            numCostPerCycle = numCostPerCycle + BnB_arrMatrix[cycle[index]][cycle[index+1]]
            # Check the current accumlated cost against the Current Best Cost
            if (numCostPerCycle >= numCurrentBestCost):
                numCostPerCycle = float("inf")
                break
            
        # Add the first cycle cost as the best one
        if (numCurrentBestCost == float("inf")):
            numCurrentBestCost = numCostPerCycle
        # if a better cost is found, update the numCurrentBestCost variable
        elif (numCostPerCycle < numCurrentBestCost):
            numCurrentBestCost = numCostPerCycle
        # Add the current cycle cost to the cost list
        lstCostList.append(numCostPerCycle)

    # Calculating the least cost cycle
    numLeastCost = min(lstCostList)
    numLeastCostIndex = lstCostList.index(numLeastCost)

    BnB_time = clock() - start
    
    BnB_output = ["Branch and Bound", numLeastCost, lstTree[numLeastCostIndex], BnB_time]
    
    return(BnB_output)

filename = 'input.txt'

def write_input_txt(n):
    with open(filename, 'w') as file:
        file.write(str(n) + "\n")
    with open(filename, 'a') as file:
        random_list = np.random.randint(100, size = (n, n))
        for i in range(0, n):
            random_list[i][i] = -1
        for line in random_list:
            string_line = list(map(str, line))
            for element in string_line:
                file.write(element + " ")
            file.write("\n")

#write_input_txt(8)

elements = []
firstline = True
with open(filename) as file:
   for line in file:
        if(firstline == False):
            line = line.strip().split()
            float_line = list(map(float, line))
            for i in range(len(float_line)):
                if(float_line[i] == -1):
                    float_line[i] = float('inf')
            elements.append(float_line)
        firstline = False
       
      

ele_array = np.array(elements)
#print ('%s\nshape is %s' % (type(ele_array), ele_array.shape))
#print (ele_array)

# ele_array = np.array([[float('inf'), 1, 2, 2, 1],
# [1, float('inf'), 1, 2, 2],
# [2, 1, float('inf'), 1, 2], 
# [2, 2, 1, float('inf'), 100], 
# [1, 2, 2, 100, float('inf')]])

BF_output = BruteForce(ele_array)
BnB_output = travel(ele_array)
print("#########################BruteForce########################")
print(BF_output)
print("#######################Branch and Bound####################")
print(BnB_output)


BF_file = 'BF.txt'
with open(BF_file, 'w') as bf_file:
    bf_file.write("solution: " + str(BF_output[2]) + "\n")
    bf_file.write("cost    : " + str(BF_output[1]) + "\n")
    bf_file.write("time    : " + str(BF_output[3]) + "\n")

BB_file = 'BB.txt'
with open(BB_file, 'w') as bb_file:
    bb_file.write("solution: " + str(BnB_output[2]) + "\n")
    bb_file.write("cost    : " + str(BnB_output[1]) + "\n")
    bb_file.write("time    : " + str(BnB_output[3]) + "\n")

print("finish writing BF.txt & BB.txt")
input();
#Generic Ant Colony Optimization (ACO) Algorithm
#Bruno Sampaio Leite - UNIFESP

import numpy.random as nprand

if __name__ == "__main__":
    graph = [[int(x) for x in input("Input graph as a weighted adjacency matrix:\n").split()]]
    for i in range(len(graph[0])-1):
        graph.append([int(x) for x in input().split()])

    alpha, beta, rho, tau0 = [float(x) for x in input("Input alpha, beta, rho and tau(0):\n").split()]

    feromoneTable = [[tau0]*len(graph)]*len(graph)

    iterations = int(input("Input number of iterations per ant:\n"))

    #Iterate iterations times
    for i in range(iterations):
        #For each ant (every node has an ant)
        print(f"Iteration {iterations}:")
        for k in range(len(graph)):
            #Optionally restart feromone table for every ant
            #Usado pra que a saída corresponda as respostas do exercicio teorico
            feromoneTable = [[tau0]*len(graph)]*len(graph)
            print(f"Ant {chr(k+65)}:")
            nextNode = k
            visited = [0]*len(graph)
            nodeList = []
            while(nextNode != -1):
                #Insert node being explored to the path list
                nodeList.append(nextNode)
                #Mark node as already visited
                visited[nextNode] = -1
                #For every adjacent node that has not been visited, calc probability of visiting node
                probability = [(alpha*feromoneTable[nextNode][j]*beta*(1/graph[nextNode][j]))\
                    /sum(alpha*feromoneTable[nextNode][z]*beta*(1/graph[nextNode][z])\
                        for z in range(len(graph)) if visited[z] == 0)\
                             if visited[j] == 0 else 0 \
                                 for j in range(len(graph))]

                #print("Probabilities:")
                #print([f"{p:.4f}" for p in probability])

                #If every node has been visited
                if sum(probability) == 0 :
                    nextNode = -1
                else:
                    #If we want the ant to choose randomly by probability
                    #nextNode = nprand.choice(len(graph), replace=False, p=probability)

                    #If we want the ant to always choose the highest probability path
                    #Usado pra que as saidas correspondam as respostas do exercicio teorico
                    nextNode = probability.index(max(probability))
            
            #Update all feromones adjacent to starting node
            feromoneTable[k] = [(1-rho)*feromoneTable[k][j]\
                    +rho*1/graph[k][j] if k != j else 0 for j in range(len(graph))]

            print("Feromone table:")
            print([f"{f:.4f}" for f in feromoneTable[k]])

            print(f"Path taken by ant {chr(k+65)}:")
            print([f"{chr(n+65)}" for n in nodeList])

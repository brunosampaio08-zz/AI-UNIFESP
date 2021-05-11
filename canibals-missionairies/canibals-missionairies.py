from collections import deque

class state():
    def __init__(self, leftCanibals, rightCanibals, leftMissionaries, rightMissionaries, boatSide):
        self.leftCanibals = leftCanibals
        self.rightCanibals = rightCanibals
        self.leftMissionaries = leftMissionaries
        self.rightMissionaries = rightMissionaries
        self.boatSide = boatSide
        self.father = None

    def __eq__(self, finalState):
        #If finalState is not an instance of state, can't compare
        if not isinstance(finalState, state):
            return NotImplemented

        #If all attributes are equal, return True
        return (self.leftCanibals == finalState.leftCanibals and \
            self.rightCanibals == finalState.rightCanibals and \
                self.leftMissionaries == finalState.leftMissionaries and \
                    self.rightMissionaries == finalState.rightMissionaries and \
                        self.boatSide == finalState.boatSide)

    def isValidState(self):
        #If the number of canibals exceed the number of missionaries and number of missionaries > 0, not a valid state
        if (self.leftCanibals > self.leftMissionaries and self.leftMissionaries > 0) or \
            (self.rightCanibals > self.rightMissionaries and self.rightMissionaries > 0):
            return False
        
        #If number of canibals < 0 or missionaries < 0, not a valid state
        if self.leftCanibals < 0 or self.rightCanibals < 0 or \
            self.rightMissionaries < 0 or self.leftMissionaries < 0:
            return False

        #If number of canibals > 3 or missionaries > 3, not a valid state        
        if self.leftCanibals > 3 or self.rightCanibals > 3 or \
            self.rightMissionaries > 3 or self.leftMissionaries > 3:
            return False

        return True

def findChildrenStates(currState):
    childrenStates = []
    leftC = currState.leftCanibals
    leftM = currState.leftMissionaries
    rightC = currState.rightCanibals
    rightM = currState.rightMissionaries

    #If boat is on the left, we can pass 2 canibals, 1 canibal, 2 missionaries, 1 missionary or 1 of each to the right
    if currState.boatSide == "left":
        childrenStates.append(state(leftC-2,rightC+2,leftM,rightM,"right"))
        childrenStates.append(state(leftC-1,rightC+1,leftM,rightM,"right"))
        childrenStates.append(state(leftC,rightC,leftM-2,rightM+2,"right"))
        childrenStates.append(state(leftC,rightC,leftM-1,rightM+1,"right"))
        childrenStates.append(state(leftC-1,rightC+1,leftM-1,rightM+1,"right"))
    #If boat is on the right, we can pass 2 canibals, 1 canibal, 2 missionaries, 1 missionary or 1 of each to the left
    elif currState.boatSide == "right":
        childrenStates.append(state(leftC+2,rightC-2,leftM,rightM,"left"))
        childrenStates.append(state(leftC+1,rightC-1,leftM,rightM,"left"))
        childrenStates.append(state(leftC,rightC,leftM+2,rightM-2,"left"))
        childrenStates.append(state(leftC,rightC,leftM+1,rightM-1,"left"))
        childrenStates.append(state(leftC+1,rightC-1,leftM+1,rightM-1,"left"))

    return childrenStates

def bidirectionalSearch():
    #Instantiates the first state
    firstState = state(3, 0, 3, 0, "left")

    #Instantiates the final state
    finalState = state(0, 3, 0, 3, "right")
    
    #States queue coming from the start
    startStates = deque()
    startStates.append(firstState)

    #States queue coming from the end
    endStates = deque()
    endStates.append(finalState)

    #Already explored states coming from the beginning
    startExplored = []

    #Already explored states coming from the end
    endExplored = []

    while startStates and endStates:
        #Search from the start
        currState = startStates.popleft()

        #If state to be explored has already been found coming from the opposite side, we found an intersection
        #and thus the bidirectional search should end
        if currState in (endExplored + list(endStates)):
            #Return currentState coming from the beginning and equivalent state coming from the end 
            return currState, \
                (endExplored + list(endStates))[(endExplored + list(endStates)).\
                    index(currState)], "start"

        #Current state is marked as explored
        startExplored.append(currState)
        #Find states possible to be obtained from currentState
        childrenStates = findChildrenStates(currState)
        
        for childState in childrenStates:
            #If child state hasn't been explored coming from the start
            if childState not in (startExplored + list(startStates)):
                #And if child state is valid
                if childState.isValidState():
                    #Mark it as to be explored and add currentState as it's father
                    childState.father = currState
                    startStates.append(childState)
        
        #Search from the end
        currState = endStates.popleft()

        #If state to be explored has already been found coming from the opposite side, we found an intersection
        #and thus the bidirectional search should end
        if currState in (startExplored + list(startStates)):
            #Return currentState coming from the end and equivalent state coming from the beginning 
            return currState, \
                (startExplored + list(startStates))[(startExplored + list(startStates)).\
                    index(currState)], "end"

         #Current state is marked as explored
        endExplored.append(currState)
        #Find states possible to be obtained from currentState
        childrenStates = findChildrenStates(currState)

        for childState in childrenStates:
            #If child state hasn't been explored coming from the end
            if childState not in (endExplored + list(endStates)):
                #And if child state is valid
                if childState.isValidState():
                    #Mark it as to be explored and add currentState as it's father
                    childState.father = currState
                    endStates.append(childState)

    return None

if __name__ == "__main__":
    intersectState = bidirectionalSearch()
    if intersectState[2] == "end":
        L = deque()
        aux = intersectState[1]
        while aux:
            L.append(aux)
            aux = aux.father
        L.reverse()
        aux = intersectState[0].father
        while aux:
            L.append(aux)
            aux = aux.father
        i = 0
        while L:
            aux = L.popleft()
            print(f'Iterarion {i}: \nBoat: {aux.boatSide}')
            print(f"Missionaries left: {aux.leftMissionaries};"\
                f"Canibals left: {aux.leftCanibals}; \nMissionaries right: {aux.rightMissionaries};"\
                    f"Canibals right: {aux.rightCanibals};\n")
            i += 1
    elif intersectState[2] == "start":
        L = deque()
        aux = intersectState[1]
        while aux:
            L.append(aux)
            aux = aux.father
        L.reverse()
        aux = intersectState[0].father
        while aux:
            L.append(aux)
            aux = aux.father
        i = 0
        while L:
            aux = L.popleft()
            print(f'Iterarion {i}:; Boat: {aux.boatSide}')
            print(f"Missionaries left: {aux.leftMissionaries};"\
                f"Canibals left: {aux.leftCanibals}; Missionaries right: {aux.rightMissionaries};"\
                    f"Canibals right: {aux.rightCanibals};\n")
            i += 1

    if intersectState:
        print("Intersection state leads to a solution!")
    else:
        print("No solution found :(")
    
    
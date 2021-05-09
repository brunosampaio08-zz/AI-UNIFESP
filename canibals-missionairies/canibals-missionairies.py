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
        if not isinstance(finalState, state):
            return NotImplemented

        return (self.leftCanibals == finalState.leftCanibals and \
            self.rightCanibals == finalState.rightCanibals and \
                self.leftMissionaries == finalState.leftMissionaries and \
                    self.rightMissionaries == finalState.rightMissionaries and \
                        self.boatSide == finalState.boatSide)

    def isIntersection(self, lastState):
        #If the last state searched coming from opposite direction is equal to last state
        #searched coming from current direction, end the search
        if self == lastState:
            return True

        return False

    def isValidState(self):
        #If the number of canibals exceed the number of missionaires, kill search from current state
        if (self.leftCanibals > self.leftMissionaries and self.leftMissionaries > 0) or \
            (self.rightCanibals > self.rightMissionaries and self.rightMissionaries > 0):
            return False
        
        if self.leftCanibals < 0 or self.rightCanibals < 0 or \
            self.rightMissionaries < 0 or self.leftMissionaries < 0:
            return False
        
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

    if currState.boatSide == "left":
        childrenStates.append(state(leftC-2,rightC+2,leftM,rightM,"right"))
        childrenStates.append(state(leftC-1,rightC+1,leftM,rightM,"right"))
        childrenStates.append(state(leftC,rightC,leftM-2,rightM+2,"right"))
        childrenStates.append(state(leftC,rightC,leftM-1,rightM+1,"right"))
        childrenStates.append(state(leftC-1,rightC+1,leftM-1,rightM+1,"right"))
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

        if currState in (endExplored + list(endStates)):
            return currState, \
                (endExplored + list(endStates))[(endExplored + list(endStates)).\
                    index(currState)], "start"

        startExplored.append(currState)
        childrenStates = findChildrenStates(currState)
        
        for childState in childrenStates:
            if childState not in (startExplored + list(startStates)):
                if childState.isValidState():
                    childState.father = currState
                    startStates.append(childState)
        
        #Search from the end
        currState = endStates.popleft()

        if currState in (startExplored + list(startStates)):
            return currState, \
                (startExplored + list(startStates))[(startExplored + list(startStates)).\
                    index(currState)], "end"

        endExplored.append(currState)
        childrenStates = findChildrenStates(currState)

        for childState in childrenStates:
            if childState not in (endExplored + list(endStates)):
                if childState.isValidState():
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
            print(f'Iterarion {i}:; Boat: {aux.boatSide}')
            print(f"Missionaries left: {aux.leftMissionaries};"\
                f"Canibals left: {aux.leftCanibals}; Missionaries right: {aux.rightMissionaries};"\
                    f"Canibals right: {aux.rightCanibals};")
            i += 1

    if intersectState:
        print("Intersection state leads to a solution!")
    else:
        print("No solution found :(")
    
    
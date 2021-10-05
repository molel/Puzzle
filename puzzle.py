class State:
    def __init__(self, currentState, finalState, depth, manhattanDistance=False, weight=False):
        self.currentState = currentState
        self.finalState = finalState
        self.depth = depth
        self.manhattanDistance = self.calculateManhattanDistance() if manhattanDistance is False else manhattanDistance
        self.weight = self.calculateWeight() if weight is False else weight

    def __str__(self):
        return "\n".join([self.currentState[0:3], self.currentState[3:6], self.currentState[6:9]])

    def fullPrint(self):
        print(self)
        print(f"Manhattan distance is: {self.manhattanDistance}")
        print(f"Depth is: {self.getDepth()}")
        print(f"Function is: {self.getWeight()}\n")

    def getCurrentState(self):
        return self.currentState

    def getFinalState(self):
        return self.finalState

    def getManhattanDistance(self):
        return self.manhattanDistance

    def getDepth(self):
        return self.depth

    def getWeight(self):
        return self.weight

    @staticmethod
    def getX(index):
        return index % 3

    @staticmethod
    def getY(index):
        return index // 3

    @staticmethod
    def getIndex(x, y):
        return y * 3 + x

    def calculateWeight(self):
        return self.manhattanDistance + self.depth

    def compare(self):
        return self.getCurrentState() == self.getFinalState()

    def isSolvable(self):
        startStateIsOdd = self.countInversions() % 2 == 1
        finalStateIsOdd = self.countInversions(False) % 2 == 1
        return startStateIsOdd == finalStateIsOdd

    @staticmethod
    def isEqual(string, states):
        for state in states:
            if state.getCurrentState() == string:
                return False
        return True

    def calculateManhattanDistance(self):
        distance = 0
        for i in range(len(self.getCurrentState())):
            x1, x2 = self.getX(i), 0
            y1, y2 = self.getY(i), 0
            for j in range(len(self.getFinalState())):
                if self.currentState[i] == self.finalState[j]:
                    x2 = self.getX(j)
                    y2 = self.getY(j)
                    distance += abs(x2 - x1) + abs(y2 - y1)
        return distance

    def countInversions(self, start=True):
        count = 0
        iterObj = self.getCurrentState() if start else self.getFinalState()
        for i in range(len(iterObj)):
            for j in range(len(iterObj)):
                el1 = iterObj[i]
                el2 = iterObj[j]
                if el1 == "0" or el2 == "0":
                    continue
                elif el2 < el1:
                    count += 1
        return count

    def minPath(self, tempVector):
        minWeight = tempVector[0].getWeight()
        j = 0
        for i in range(len(tempVector)):
            if tempVector[i].getWeight() <= minWeight:
                minWeight = tempVector[i].getWeight()
                j = i
        return minWeight, j

    def move(self, direction):
        zIndex = self.getCurrentState().find("0")
        zX = self.getX(zIndex)
        zY = self.getY(zIndex)
        if direction == "left" and zX == 0 \
                or direction == "right" and zX >= 2 \
                or direction == "down" and zY >= 2 \
                or direction == "up" and zY == 0:
            return [False, self]
        index = 0
        if direction == "left":
            index = self.getIndex(zX - 1, zY)
        elif direction == "up":
            index = self.getIndex(zX, zY - 1)
        elif direction == "down":
            index = self.getIndex(zX, zY + 1)
        elif direction == "right":
            index = self.getIndex(zX + 1, zY)
        tempCurrentState = self.getCurrentState()
        tempFinalState = self.getFinalState()
        tempCurrentState = self.swap(tempCurrentState, index, zIndex)
        state = State(tempCurrentState, tempFinalState, self.getDepth() + 1)
        return [True, state]

    @staticmethod
    def swap(string, index1, index2):
        string = list(string)
        string[index1], string[index2] = string[index2], string[index1]
        return "".join(string)

    def path(self):
        openPath = []
        allPaths = [self]
        correctPath = [State(*vars(self).values())]
        step = 1
        while not self.compare():
            print(f"Step {step}")
            tempVector = []
            print(f"Possible movement options ")
            for direction in ["left", "right", "up", "down"]:
                temp = self.move(direction)
                if temp[0] and temp[1] != allPaths:
                    tempVector.append(temp[1])
                    temp[1].fullPrint()
                    allPaths.append(temp[1])
            self.changeState(self.getMinElement(tempVector, openPath))
            minPath = self.minPath(openPath)
            if self.getWeight() > minPath[0]:
                print("Encountered the terminal node ")
                for k in range(self.getDepth() - openPath[minPath[1]].getDepth()):
                    try:
                        correctPath.pop()
                    except:
                        continue
                print("Back to state: ")
                self.changeState(openPath[minPath[1]])
                openPath[-1], openPath[minPath[1]] = openPath[minPath[1]], openPath[-1]
                print(openPath.pop())
                print(self)
            else:
                correctPath.append(State(*vars(self).values()))
                print("Selected state: ")
                self.fullPrint()
            step += 1
        return correctPath

    def changeState(self, state):
        self.currentState = state.currentState
        self.finalState = state.finalState
        self.depth = state.depth
        self.manhattanDistance = state.manhattanDistance
        self.weight = state.weight

    @staticmethod
    def getMinElement(tempVector, paths):
        minWeight = tempVector[0].getWeight()
        index = 0
        for i in range(1, len(tempVector)):
            if tempVector[i].getWeight() < minWeight:
                index = i
                minWeight = tempVector[i].getWeight()
        for i in range(len(tempVector)):
            if i != index:
                paths.append(tempVector[i])
        return tempVector[index]


def main():
    print("Only 3x3")
    # startState = input("Enter start state:\n")
    # finalState = input("Enter final state:\n")
    startState = "384670125"
    finalState = "804375612"
    state = State(startState, finalState, 0)
    if state.isSolvable():
        path = state.path()
        print("Path is")
        for i in range(len(path)):
            print(f"Step {i + 1}:\n{path[i]}\n")
    else:
        print("Unsolvable")


if __name__ == '__main__':
    main()

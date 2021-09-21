def minPath(tempVector):
    minWeight = tempVector[0].getWeight
    j = 0
    for i in range(len(tempVector)):
        if tempVector[i].getWeight() <= minWeight:
            minWeight = tempVector[i].getWeight()
            j = i
    return minWeight, j


class State:
    def __init__(self, currentState, finalState, depth):
        self.currentState = currentState
        self.finalState = finalState
        self.depth = depth
        self.manhattanDistance = self.calculateManhattanDistance()
        self.weight = self.calculateWeight()

    def __print__(self):
        for i in range(len(self.currentState) // 3):
            print(f"{self.currentState[i * 3]} {self.currentState[i * 3 + 1]} {self.currentState[i * 3] + 2} ")

    def fullPrint(self):
        print(self)
        print(f"Manhattan distance is: {self.manhattanDistance}")
        print(f"Depth is: {self.depth}")
        print(f"Function is: {self.weight}")

    def getCurrentState(self):
        return self.currentState

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
        return self.currentState == self.finalState

    def isSolvable(self):
        startStateIsOdd = self.countInversions() % 2 == 1
        finalStateIsOdd = self.countInversions(False) % 2 == 1
        return startStateIsOdd == finalStateIsOdd

    def isEqual(self, string, states):
        for state in states:
            if state.getCurrentState() == string:
                return False
        return True

    def calculateManhattanDistance(self):
        distance = 0
        for i in range(len(self.currentState)):
            x1, x2 = self.getX(i), 0
            y1, y2 = self.getY(i), 0
            for j in range(len(self.finalState)):
                if self.currentState[i] == self.finalState[j]:
                    x2 = self.getX(j)
                    y2 = self.getY(j)
                    distance += abs(x2 - x1) + abs(y2 - y1)
        return distance

    def countInversions(self, start=True):
        count = 0
        iterObj = self.currentState if start else self.finalState
        for el1 in iterObj:
            for el2 in iterObj:
                if el1 != el2:
                    count += 1
        return count

    def move(self, direction):
        zIndex = len(self.currentState) - 1 - self.currentState[::-1].index("0")
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
        elif direction == "right":
            index = self.getIndex(zX, zY - 1)
        elif direction == "down":
            index = self.getIndex(zX, zY + 1)
        elif direction == "up":
            index = self.getIndex(zX + 1, zY)
        tempCurrentState = self.currentState
        tempCurrentState = self.swap(tempCurrentState, index, zIndex)
        self.currentState = tempCurrentState
        self.depth += 1
        return [True, self]

    @staticmethod
    def swap(string, index1, index2):
        string = string.split("")
        string[index1], string[index2] = string[index2], string[index1]
        return "".join(string)

    def path(self):
        openPath = []
        allPaths = [self]
        correctPath = [self]
        step = 1
        while not self.compare():
            print(f"Step {step}")
            tempVector = []
            print(f"Possible movement options ")
            for direction in ["left", "right", "ip", "down"]:
                temp = self.move(direction)
                if temp[0] and temp[1] != allPaths:
                    tempVector.append(temp[1])
                    temp[1].fullPrint()
                    allPaths.append(temp[1])
            minElement = self.getMinElement(tempVector, openPath)
            minPath = minPath(openPath)
            if self.getWeight() > minPath[0]:
                print("Encountered the terminal node ")
                for k in range(self.getDepth() - openPath[minPath[1]].getDepth()):
                    correctPath.pop()
                print("Back to state: ")
                self.currentState = openPath[minPath[1]]
                openPath[-1], openPath[minPath[1]] = openPath[minPath[1]], openPath[-1]
                openPath.pop()
                print(self)
            else:
                correctPath.append(self)
                print("Selected state: ")
                self.fullPrint()
            step += 1
        return correctPath

    @staticmethod
    def getMinElement(tempVector, paths):
        minWeight = min(tempVector)
        index = tempVector.find(minWeight)
        for i in range(len(tempVector)):
            if i != index:
                paths.append(tempVector[i])
        return tempVector[index]


def main():
    print("Only 3x3")
    startState = input("Enter start state:\n")
    finalState = input("Enter final state:\n")
    state = State(startState, finalState, 0)
    if state.isSolvable():
        path = state.path()
        print("Path is")
        for i in path:
            print(i)
    else:
        print("Unsolvable")


main()

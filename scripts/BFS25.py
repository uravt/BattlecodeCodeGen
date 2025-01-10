from enum import Enum

package = "PathfindingTest"


class MapLocation:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.order = -1

    def assignOrder(self, order):
        self.order = order

    def add(self, dx, dy):
        return MapLocation(self.x + dx, self.y + dy)

    def addMapLocation(self, other):
        return MapLocation(self.x + other.x, self.y + other.y)

    def addDirection(self, direction):
        match direction:
            case Directions.NORTH:
                return self.add(0, 1)
            case Directions.NORTHEAST:
                return self.add(1, 1)
            case Directions.EAST:
                return self.add(1, 0)
            case Directions.SOUTHEAST:
                return self.add(1, -1)
            case Directions.SOUTH:
                return self.add(0, -1)
            case Directions.SOUTHWEST:
                return self.add(-1, -1)
            case Directions.WEST:
                return self.add(-1, 0)
            case Directions.NORTHWEST:
                return self.add(-1, 1)

    def __sub__(self, other):
        return MapLocation(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return str(self.toIndex(7))

    def InBounds(self, size):
        if (self.x < 0 or self.x >= size):
            return False
        if (self.y < 0 or self.y >= size):
            return False
        return True

    def toIndex(self, size):
        return ((size - 1 - self.y) * size + self.x)

    @staticmethod
    def directionFromDxDy(other):
        if other.x == 0 and other.y == 1:
            return Directions.NORTH
        if other.x == 1 and other.y == 1:
            return Directions.NORTHEAST
        if other.x == 1 and other.y == 0:
            return Directions.EAST
        if other.x == 1 and other.y == -1:
            return Directions.SOUTHEAST
        if other.x == 0 and other.y == -1:
            return Directions.SOUTH
        if other.x == -1 and other.y == -1:
            return Directions.SOUTHWEST
        if other.x == -1 and other.y == 0:
            return Directions.WEST
        if other.x == -1 and other.y == 1:
            return Directions.NORTHWEST

class Directions(Enum):
    NORTH = 1
    NORTHEAST = 2
    EAST = 3
    SOUTHEAST = 4
    SOUTH = 5
    SOUTHWEST = 6
    WEST = 7
    NORTHWEST = 8


class FileWriter:
    def __init__(self, file):
        self.file = file
        self.indent_level = 0

    def writeLine(self, string):
        self.__addIndents__()
        self.file.write(string + "\n")

    def openBracket(self):
        self.__addIndents__()
        self.file.write("{" + "\n")
        self.indent_level += 1

    def closeBracket(self):
        self.indent_level -= 1
        self.__addIndents__()
        self.file.write("}" + "\n")

    def __addIndents__(self):
        for i in range(self.indent_level):
            self.file.write("   ")

    def close(self):
        self.file.close()


def indexToMapLocation(index, center):
    corner = MapLocation(center.x - 3, center.y - 3)
    return MapLocation(corner.x + index % 7, corner.y + 6 - index // 7)


neighbors7x7 = [
    [1, 7, 8],
    [0, 2, 7, 8, 9],
    [1, 3, 8, 9, 10],
    [2, 4, 9, 10, 11],
    [3, 5, 10, 11, 12],
    [4, 6, 11, 12, 13],
    [5, 12, 13],
    [0, 1, 8, 14, 15],
    [0, 1, 2, 7, 9, 14, 15, 16],
    [1, 2, 3, 8, 10, 15, 16, 17],
    [2, 3, 4, 9, 11, 16, 17, 18],
    [3, 4, 5, 10, 12, 17, 18, 19],
    [4, 5, 6, 11, 13, 18, 19, 20],
    [5, 6, 12, 19, 20],
    [7, 8, 15, 21, 22],
    [7, 8, 9, 14, 16, 21, 22, 23],
    [8, 9, 10, 15, 17, 22, 23, 24],
    [9, 10, 11, 16, 18, 23, 24, 25],
    [10, 11, 12, 17, 19, 24, 25, 26],
    [11, 12, 13, 18, 20, 25, 26, 27],
    [12, 13, 19, 26, 27],
    [14, 15, 22, 28, 29],
    [14, 15, 16, 21, 23, 28, 29, 30],
    [15, 16, 17, 22, 24, 29, 30, 31],
    [16, 17, 18, 23, 25, 30, 31, 32],
    [17, 18, 19, 24, 26, 31, 32, 33],
    [18, 19, 20, 25, 27, 32, 33, 34],
    [19, 20, 26, 33, 34],
    [21, 22, 29, 35, 36],
    [21, 22, 23, 28, 30, 35, 36, 37],
    [22, 23, 24, 29, 31, 36, 37, 38],
    [23, 24, 25, 30, 32, 37, 38, 39],
    [24, 25, 26, 31, 33, 38, 39, 40],
    [25, 26, 27, 32, 34, 39, 40, 41],
    [26, 27, 33, 40, 41],
    [28, 29, 36, 42, 43],
    [28, 29, 30, 35, 37, 42, 43, 44],
    [29, 30, 31, 36, 38, 43, 44, 45],
    [30, 31, 32, 37, 39, 44, 45, 46],
    [31, 32, 33, 38, 40, 45, 46, 47],
    [32, 33, 34, 39, 41, 46, 47, 48],
    [33, 34, 40, 47, 48],
    [35, 36, 43],
    [35, 36, 37, 42, 44],
    [36, 37, 38, 43, 45],
    [37, 38, 39, 44, 46],
    [38, 39, 40, 45, 47],
    [39, 40, 41, 46, 48],
    [40, 41, 47]]

# traverse nodes and set paths
# check if any of the nodes within vision are the destination and do something if that's the case
# calculate lowest distance from all traversable nodes
# XbyX

cardinalDirections = [Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST]
ordinalDirections = [Directions.NORTHWEST, Directions.NORTHEAST, Directions.SOUTHEAST, Directions.SOUTHWEST]
visitedNodes = []
unvisitedNodesQueue = []
backtrackList = []
size = 7

fw = FileWriter(open("../java_files/BFS7x7.java", "w"))
fw.writeLine("""package """ + package + """;
import battlecode.common.*;""")
fw.writeLine("public class BFS \n")
for i in range(0, size * size):
    fw.writeLine("static MapLocation l" + str(i) + ";")
    fw.writeLine("static int dist" + str(i) + ";")
    fw.writeLine("static int h" + str(i) + ";")
    fw.writeLine("static boolean exists" + str(i) + ";")
    fw.writeLine("static int cost" + str(i) + ";")
    fw.writeLine("")
fw.openBracket()
fw.writeLine("static Direction[][] lookup;")
fw.writeLine("")
fw.writeLine("""public static MapLocation getLocationFromIndex(int nodeIndex, MapLocation center)
   {
        return new MapLocation(center.x - 3 + nodeIndex % 7, center.y - 3 + 6 - nodeIndex / 7);
   }\n""")
fw.writeLine("""
   public static int indexToLocalX(int nodeIndex)
   {
         return nodeIndex % 7;
   }

   public static int indexToLocalY(int nodeIndex)
   {        
         return nodeIndex / 7;
   }\n""")
fw.writeLine("""public static Direction dirToMove(int nodeIndex)
   {
        int currentNodeIndex = nodeIndex;
        Direction currentDirection = lookup[indexToLocalY(nodeIndex)][indexToLocalX(nodeIndex)];
        while (currentDirection != null)
        {
            Direction tempDirection = currentDirection;
            switch(currentDirection)
            {
                case NORTH:
                    currentNodeIndex = currentNodeIndex - 7;
                    break;
                case NORTHEAST:
                    currentNodeIndex = currentNodeIndex - 6;
                    break;
                case EAST:
                    currentNodeIndex = currentNodeIndex + 1;
                    break;
                case SOUTHEAST:
                    currentNodeIndex = currentNodeIndex + 8;
                    break;
                case SOUTH:
                    currentNodeIndex = currentNodeIndex + 7;
                    break;
                case SOUTHWEST:
                    currentNodeIndex = currentNodeIndex + 6;
                    break;
                case WEST:
                    currentNodeIndex = currentNodeIndex - 1;
                    break;
                case NORTHWEST:
                    currentNodeIndex = currentNodeIndex - 8;
                    break;
            }
            currentDirection = lookup[currentNodeIndex / 7][currentNodeIndex % 7];
            if(currentDirection == null) return tempDirection.opposite();
        }
        return null;
  }\n""")
fw.writeLine("public static void pathfind(RobotController rc, MapLocation destination) throws GameActionException")
fw.openBracket()
fw.writeLine("MapLocation start = rc.getLocation();")
fw.writeLine("lookup = new Direction[" + str(size) + "][" + str(size) + "];")
fw.writeLine("")
center = MapLocation(size // 2, size // 2)
currentLocation = MapLocation(size // 2, size // 2)
for i in range(0, size * size):
    if i == currentLocation.toIndex(size):
        fw.writeLine("l" + str(i) + " = getLocationFromIndex(" + str(i) + ", start);")
        fw.writeLine("dist" + str(i) + " = 0;")
        fw.writeLine("h" + str(i) + " = start.distanceSquaredTo(destination);")
        fw.writeLine("exists" + str(i) + " = true;")
        fw.writeLine("cost" + str(i) + " = 0;")
        fw.writeLine("")
        continue
    fw.writeLine("l" + str(i) + " = getLocationFromIndex(" + str(i) + ", start);")
    fw.writeLine("dist" + str(i) + " = 1000000;")
    fw.writeLine("h" + str(i) + " = l" + str(i) + ".distanceSquaredTo(destination);")
    fw.writeLine("exists" + str(i) + " = " + "rc.onTheMap(l" + str(i) + ") && rc.sensePassability(l" + str(i) + ") && " +
                 "!rc.canSenseRobotAtLocation(l" + str(i) + ");")
    fw.writeLine("cost" + str(i) + " = " + "exists" + str(i) + " && rc.senseMapInfo(l" + str(i) + ").getPaint().isAlly() ? 1 : 2;")
    fw.writeLine("")
fw.writeLine("int closestDistance = Integer.MAX_VALUE;")
fw.writeLine("int closestIndex = -1;")
unvisitedNodesQueue.append(currentLocation)
while len(unvisitedNodesQueue) > 0:
    currentLocation = unvisitedNodesQueue.pop(0)
    visitedNodes.append(currentLocation)
    nodeIndex = currentLocation.toIndex(size)
    # if distance is lower change distance, assign direction
    fw.writeLine("if(exists" + str(nodeIndex) + ")")
    fw.openBracket()
    for neighbor in neighbors7x7[nodeIndex]:
        neighborLocation = indexToMapLocation(neighbor, center)
        if (neighborLocation not in visitedNodes and neighborLocation not in unvisitedNodesQueue):
            unvisitedNodesQueue.append(neighborLocation)
        fw.writeLine("if(exists" + str(neighbor) + " && dist" + str(nodeIndex) + " + cost" + str(neighbor) +" < dist" + str(neighbor) + ")")
        fw.openBracket()
        fw.writeLine("dist" + str(neighbor) + " = dist" + str(nodeIndex) + " + cost" + str(neighbor) + ";")
        # FIX HOW CENTER CALCULATED
        fw.writeLine("lookup[indexToLocalY(" + str(neighbor) + ")][indexToLocalX(" + str(neighbor) + ")] = Direction." + MapLocation.directionFromDxDy(currentLocation - neighborLocation).name + ";")
        fw.writeLine("if(h" + str(neighbor) + " < closestDistance)")
        fw.openBracket()
        fw.writeLine("closestDistance = h" + str(neighbor) + ";")
        fw.writeLine("closestIndex = " + str(neighbor) + ";")
        fw.closeBracket()
        #convert neighbor to location, subtract location from other location, write switch case to determine direction based on dx and dy
        fw.closeBracket()
    fw.closeBracket()
fw.writeLine("")
fw.writeLine("switch(closestIndex)")
fw.openBracket()
for i in range(0, size * size):
    fw.writeLine("case " + str(i) + ":")
    fw.openBracket()
    fw.writeLine("Direction dirToMove = dirToMove(" + str(i) +");")
    fw.writeLine("if(rc.canMove(dirToMove))")
    fw.openBracket()
    fw.writeLine("rc.move(dirToMove);")
    fw.closeBracket()
    fw.writeLine("break;")
    fw.closeBracket()
    fw.writeLine("")
fw.closeBracket()
fw.closeBracket()
fw.closeBracket()
"""
    public static String printDirectionMatrix(Direction[][] matrix)
    {
        String tempStr = "";
        for(int i = 0; i < matrix.length; i++)
        {
            tempStr += "\n";
            for(int j = 0; j < matrix[i].length; j++)
            {
                tempStr += matrix[i][j] + " ";
            }
        }
        return tempStr;
    }
"""


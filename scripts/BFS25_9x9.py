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

    @staticmethod
    def costFromDxDy(other):
        if other.x == 0 and other.y == 1:
            return costStraight
        if other.x == 1 and other.y == 1:
            return costDiagonal
        if other.x == 1 and other.y == 0:
            return costStraight
        if other.x == 1 and other.y == -1:
            return costDiagonal
        if other.x == 0 and other.y == -1:
            return costStraight
        if other.x == -1 and other.y == -1:
            return costDiagonal
        if other.x == -1 and other.y == 0:
            return costStraight
        if other.x == -1 and other.y == 1:
            return costDiagonal

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
    corner = MapLocation(center.x - 4, center.y - 4)
    return MapLocation(corner.x + index % 9, corner.y + 8 - index // 9)

banned_nodes = [0,1,9,7,8,17,63,72,73,71,79,80]

neighbors9x9 = [
[1,9,10],
[0,2,9,10,11],
[1,3,10,11,12],
[2,4,11,12,13],
[3,5,12,13,14],
[4,6,13,14,15],
[5,7,14,15,16],
[6,8,15,16,17],
[7,16,17],
[0,1,10,18,19],
[0,1,2,9,11,18,19,20],
[1,2,3,10,12,19,20,21],
[2,3,4,11,13,20,21,22],
[3,4,5,12,14,21,22,23],
[4,5,6,13,15,22,23,24],
[5,6,7,14,16,23,24,25],
[6,7,8,15,17,24,25,26],
[7,8,16,25,26],
[9,10,19,27,28],
[9,10,11,18,20,27,28,29],
[10,11,12,19,21,28,29,30],
[11,12,13,20,22,29,30,31],
[12,13,14,21,23,30,31,32],
[13,14,15,22,24,31,32,33],
[14,15,16,23,25,32,33,34],
[15,16,17,24,26,33,34,35],
[16,17,25,34,35],
[18,19,28,36,37],
[18,19,20,27,29,36,37,38],
[19,20,21,28,30,37,38,39],
[20,21,22,29,31,38,39,40],
[21,22,23,30,32,39,40,41],
[22,23,24,31,33,40,41,42],
[23,24,25,32,34,41,42,43],
[24,25,26,33,35,42,43,44],
[25,26,34,43,44],
[27,28,37,45,46],
[27,28,29,36,38,45,46,47],
[28,29,30,37,39,46,47,48],
[29,30,31,38,40,47,48,49],
[30,31,32,39,41,48,49,50],
[31,32,33,40,42,49,50,51],
[32,33,34,41,43,50,51,52],
[33,34,35,42,44,51,52,53],
[34,35,43,52,53],
[36,37,46,54,55],
[36,37,38,45,47,54,55,56],
[37,38,39,46,48,55,56,57],
[38,39,40,47,49,56,57,58],
[39,40,41,48,50,57,58,59],
[40,41,42,49,51,58,59,60],
[41,42,43,50,52,59,60,61],
[42,43,44,51,53,60,61,62],
[43,44,52,61,62],
[45,46,55,63,64],
[45,46,47,54,56,63,64,65],
[46,47,48,55,57,64,65,66],
[47,48,49,56,58,65,66,67],
[48,49,50,57,59,66,67,68],
[49,50,51,58,60,67,68,69],
[50,51,52,59,61,68,69,70],
[51,52,53,60,62,69,70,71],
[52,53,61,70,71],
[54,55,64,72,73],
[54,55,56,63,65,72,73,74],
[55,56,57,64,66,73,74,75],
[56,57,58,65,67,74,75,76],
[57,58,59,66,68,75,76,77],
[58,59,60,67,69,76,77,78],
[59,60,61,68,70,77,78,79],
[60,61,62,69,71,78,79,80],
[61,62,70,79,80],
[63,64,73],
[63,64,65,72,74],
[64,65,66,73,75],
[65,66,67,74,76],
[66,67,68,75,77],
[67,68,69,76,78],
[68,69,70,77,79],
[69,70,71,78,80],
[70,71,79]]

# traverse nodes and set paths
# check if any of the nodes within vision are the destination and do something if that's the case
# calculate lowest distance from all traversable nodes
# XbyX

cardinalDirections = [Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST]
ordinalDirections = [Directions.NORTHWEST, Directions.NORTHEAST, Directions.SOUTHEAST, Directions.SOUTHWEST]
visitedNodes = []
unvisitedNodesQueue = []
backtrackList = []
size = 9
costDiagonal = 14
costStraight = 10

fw = FileWriter(open("../java_files/BFS_FullVision.java", "w"))
fw.writeLine("""package """ + package + """;
import battlecode.common.*;""")
fw.writeLine("public class BFS_FullVision")
fw.openBracket()
fw.writeLine("static Direction[][] lookup;")
fw.writeLine("")
for i in range(0, size * size):
    if i in banned_nodes:
        continue
    fw.writeLine("static MapLocation l" + str(i) + ";")
    fw.writeLine("static int dist" + str(i) + ";")
    fw.writeLine("static int h" + str(i) + ";")
    fw.writeLine("static boolean exists" + str(i) + ";")
    fw.writeLine("static int cost" + str(i) + ";")
    fw.writeLine("")
fw.writeLine("""public static MapLocation getLocationFromIndex(int nodeIndex, MapLocation center)
   {
        return new MapLocation(center.x - 4 + nodeIndex % 9, center.y - 4 + 8 - nodeIndex / 9);
   }\n""")
fw.writeLine("""
   public static int indexToLocalX(int nodeIndex)
   {
         return nodeIndex % 9;
   }

   public static int indexToLocalY(int nodeIndex)
   {        
         return nodeIndex / 9;
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
                    currentNodeIndex = currentNodeIndex - 9;
                    break;
                case NORTHEAST:
                    currentNodeIndex = currentNodeIndex - 8;
                    break;
                case EAST:
                    currentNodeIndex = currentNodeIndex + 1;
                    break;
                case SOUTHEAST:
                    currentNodeIndex = currentNodeIndex + 10;
                    break;
                case SOUTH:
                    currentNodeIndex = currentNodeIndex + 9;
                    break;
                case SOUTHWEST:
                    currentNodeIndex = currentNodeIndex + 8;
                    break;
                case WEST:
                    currentNodeIndex = currentNodeIndex - 1;
                    break;
                case NORTHWEST:
                    currentNodeIndex = currentNodeIndex - 10;
                    break;
            }
            currentDirection = lookup[currentNodeIndex / 9][currentNodeIndex % 9];
            if(currentDirection == null) return tempDirection.opposite();
        }
        return null;
  }\n""")
fw.writeLine("public static void initializeVariables(RobotController rc, MapLocation destination, MapLocation start) throws GameActionException")
fw.openBracket()
for i in range(0, size * size):
    if i in banned_nodes:
        continue
    if i == size * size // 2:
        fw.writeLine("l" + str(i) + " = getLocationFromIndex(" + str(i) + ", start);")
        fw.writeLine("dist" + str(i) + " = 0;")
        fw.writeLine("h" + str(i) + " = l" + str(i) + ".distanceSquaredTo(destination);")
        fw.writeLine(
            "exists" + str(i) + " = " + "true;")
        fw.writeLine("cost" + str(i) + " = " + "0;")
        fw.writeLine("")
        continue
    fw.writeLine("l" + str(i) + " = getLocationFromIndex(" + str(i) + ", start);")
    fw.writeLine("dist" + str(i) + " = 1000000;")
    fw.writeLine("h" + str(i) + " = l" + str(i) + ".distanceSquaredTo(destination);")
    fw.writeLine("exists" + str(i) + " = " + "rc.onTheMap(l" + str(i) + ") && rc.sensePassability(l" + str(i) + ") && " +
                 "!rc.canSenseRobotAtLocation(l" + str(i) + ");")
    fw.writeLine("cost" + str(i) + " = " + "exists" + str(i) + " && rc.senseMapInfo(l" + str(i) + ").getPaint().isAlly() ? 10 : 20;")
    fw.writeLine("")
fw.closeBracket()
fw.writeLine("")
fw.writeLine("public static Direction pathfind(RobotController rc, MapLocation destination) throws GameActionException")
fw.openBracket()
fw.writeLine("MapLocation start = rc.getLocation();")
fw.writeLine("initializeVariables(rc, destination, start);")
fw.writeLine("lookup = new Direction[" + str(size) + "][" + str(size) + "];")
fw.writeLine("")
center = MapLocation(size // 2, size // 2)
currentLocation = MapLocation(size // 2, size // 2)
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
    for neighbor in neighbors9x9[nodeIndex]:
        if neighbor in banned_nodes:
            continue
        neighborLocation = indexToMapLocation(neighbor, center)
        if (neighborLocation not in visitedNodes and neighborLocation not in unvisitedNodesQueue):
            unvisitedNodesQueue.append(neighborLocation)
        fw.writeLine("if(exists" + str(neighbor) + " && dist" + str(nodeIndex) + " + cost" + str(neighbor) + " + " + str(MapLocation.costFromDxDy(currentLocation-neighborLocation)) + " < dist" + str(neighbor) + ")")
        fw.openBracket()
        fw.writeLine("dist" + str(neighbor) + " = dist" + str(nodeIndex) + " + cost" + str(neighbor) + " + " + str(MapLocation.costFromDxDy(currentLocation-neighborLocation)) + ";")
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
fw.writeLine("return dirToMove(closestIndex);")
# fw.writeLine("Direction dirToMove = dirToMove(closestIndex);")
# fw.writeLine("if(rc.canMove(dirToMove))")
# fw.openBracket()
# fw.writeLine("rc.move(dirToMove);")
# fw.closeBracket()
# fw.writeLine("switch(closestIndex)")
# fw.openBracket()
# for i in range(0, size * size):
#     if i in banned_nodes:
#         continue
#     fw.writeLine("case " + str(i) + ":")
#     fw.openBracket()
#     fw.writeLine("Direction dirToMove = dirToMove(" + str(i) +");")
#     fw.writeLine("if(rc.canMove(dirToMove))")
#     fw.openBracket()
#     fw.writeLine("rc.move(dirToMove);")
#     fw.closeBracket()
#     fw.writeLine("break;")
#     fw.closeBracket()
#     fw.writeLine("")
# fw.closeBracket()
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


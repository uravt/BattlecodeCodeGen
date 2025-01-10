from enum import Enum


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
    corner = MapLocation(center.x - 5, center.y - 5)
    return MapLocation(corner.x + index % 11, corner.y + 10 - index // 11)


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
neighbors11x11 = [
[1,11,12],
[0,2,11,12,13],
[1,3,12,13,14],
[2,4,13,14,15],
[3,5,14,15,16],
[4,6,15,16,17],
[5,7,16,17,18],
[6,8,17,18,19],
[7,9,18,19,20],
[8,10,19,20,21],
[9,20,21],
[0,1,12,22,23],
[0,1,2,11,13,22,23,24],
[1,2,3,12,14,23,24,25],
[2,3,4,13,15,24,25,26],
[3,4,5,14,16,25,26,27],
[4,5,6,15,17,26,27,28],
[5,6,7,16,18,27,28,29],
[6,7,8,17,19,28,29,30],
[7,8,9,18,20,29,30,31],
[8,9,10,19,21,30,31,32],
[9,10,20,31,32],
[11,12,23,33,34],
[11,12,13,22,24,33,34,35],
[12,13,14,23,25,34,35,36],
[13,14,15,24,26,35,36,37],
[14,15,16,25,27,36,37,38],
[15,16,17,26,28,37,38,39],
[16,17,18,27,29,38,39,40],
[17,18,19,28,30,39,40,41],
[18,19,20,29,31,40,41,42],
[19,20,21,30,32,41,42,43],
[20,21,31,42,43],
[22,23,34,44,45],
[22,23,24,33,35,44,45,46],
[23,24,25,34,36,45,46,47],
[24,25,26,35,37,46,47,48],
[25,26,27,36,38,47,48,49],
[26,27,28,37,39,48,49,50],
[27,28,29,38,40,49,50,51],
[28,29,30,39,41,50,51,52],
[29,30,31,40,42,51,52,53],
[30,31,32,41,43,52,53,54],
[31,32,42,53,54],
[33,34,45,55,56],
[33,34,35,44,46,55,56,57],
[34,35,36,45,47,56,57,58],
[35,36,37,46,48,57,58,59],
[36,37,38,47,49,58,59,60],
[37,38,39,48,50,59,60,61],
[38,39,40,49,51,60,61,62],
[39,40,41,50,52,61,62,63],
[40,41,42,51,53,62,63,64],
[41,42,43,52,54,63,64,65],
[42,43,53,64,65],
[44,45,56,66,67],
[44,45,46,55,57,66,67,68],
[45,46,47,56,58,67,68,69],
[46,47,48,57,59,68,69,70],
[47,48,49,58,60,69,70,71],
[48,49,50,59,61,70,71,72],
[49,50,51,60,62,71,72,73],
[50,51,52,61,63,72,73,74],
[51,52,53,62,64,73,74,75],
[52,53,54,63,65,74,75,76],
[53,54,64,75,76],
[55,56,67,77,78],
[55,56,57,66,68,77,78,79],
[56,57,58,67,69,78,79,80],
[57,58,59,68,70,79,80,81],
[58,59,60,69,71,80,81,82],
[59,60,61,70,72,81,82,83],
[60,61,62,71,73,82,83,84],
[61,62,63,72,74,83,84,85],
[62,63,64,73,75,84,85,86],
[63,64,65,74,76,85,86,87],
[64,65,75,86,87],
[66,67,78,88,89],
[66,67,68,77,79,88,89,90],
[67,68,69,78,80,89,90,91],
[68,69,70,79,81,90,91,92],
[69,70,71,80,82,91,92,93],
[70,71,72,81,83,92,93,94],
[71,72,73,82,84,93,94,95],
[72,73,74,83,85,94,95,96],
[73,74,75,84,86,95,96,97],
[74,75,76,85,87,96,97,98],
[75,76,86,97,98],
[77,78,89,99,100],
[77,78,79,88,90,99,100,101],
[78,79,80,89,91,100,101,102],
[79,80,81,90,92,101,102,103],
[80,81,82,91,93,102,103,104],
[81,82,83,92,94,103,104,105],
[82,83,84,93,95,104,105,106],
[83,84,85,94,96,105,106,107],
[84,85,86,95,97,106,107,108],
[85,86,87,96,98,107,108,109],
[86,87,97,108,109],
[88,89,100,110,111],
[88,89,90,99,101,110,111,112],
[89,90,91,100,102,111,112,113],
[90,91,92,101,103,112,113,114],
[91,92,93,102,104,113,114,115],
[92,93,94,103,105,114,115,116],
[93,94,95,104,106,115,116,117],
[94,95,96,105,107,116,117,118],
[95,96,97,106,108,117,118,119],
[96,97,98,107,109,118,119,120],
[97,98,108,119,120],
[99,100,111],
[99,100,101,110,112],
[100,101,102,111,113],
[101,102,103,112,114],
[102,103,104,113,115],
[103,104,105,114,116],
[104,105,106,115,117],
[105,106,107,116,118],
[106,107,108,117,119],
[107,108,109,118,120],
[108,109,119]];

# traverse nodes and set paths
# check if any of the nodes within vision are the destination and do something if that's the case
# calculate lowest distance from all traversable nodes
# XbyX

cardinalDirections = [Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST]
ordinalDirections = [Directions.NORTHWEST, Directions.NORTHEAST, Directions.SOUTHEAST, Directions.SOUTHWEST]
visitedNodes = []
unvisitedNodesQueue = []
backtrackList = []
size = 11

fw = FileWriter(open("../java_files/BFSKernel.java", "w"))
fw.writeLine("""package Version16;
import battlecode.common.*;""")
fw.writeLine("public class BFSKernel")
fw.openBracket()
fw.writeLine("static Direction[][] lookup;")
fw.writeLine("static MapLocation closestFlag;")
fw.writeLine("")
for i in range(0, size * size):
    fw.writeLine("static MapLocation l" + str(i) + ";")
    fw.writeLine("static int dist" + str(i) + ";")
    fw.writeLine("static int h" + str(i) + ";")
    fw.writeLine("static boolean exists" + str(i) + ";")
    fw.writeLine("")
fw.writeLine("""public static MapLocation getLocationFromIndex(int nodeIndex, MapLocation center)
   {
        MapLocation corner = new MapLocation(center.x - 5, center.y - 5);
        return new MapLocation(corner.x + nodeIndex % 11, corner.y + 10 - nodeIndex / 11);
   }\n""")
fw.writeLine("""public static void setClosestFlag(RobotController rc) throws GameActionException
    {
        FlagInfo[] flags = rc.senseNearbyFlags(-1, rc.getTeam().opponent());
        for(int i = 0; i < flags.length; i++)
        {
            if(flags[i].isPickedUp())
            {
                closestFlag = flags[i].getLocation();
            }
        }
    }""")
fw.writeLine("""
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

   public static int indexToLocalX(int nodeIndex)
   {
         return nodeIndex % 11;
   }

   public static int indexToLocalY(int nodeIndex)
   {        
         return nodeIndex / 11;
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
                    currentNodeIndex = currentNodeIndex - 11;
                    break;
                case NORTHEAST:
                    currentNodeIndex = currentNodeIndex - 10;
                    break;
                case EAST:
                    currentNodeIndex = currentNodeIndex + 1;
                    break;
                case SOUTHEAST:
                    currentNodeIndex = currentNodeIndex + 12;
                    break;
                case SOUTH:
                    currentNodeIndex = currentNodeIndex + 11;
                    break;
                case SOUTHWEST:
                    currentNodeIndex = currentNodeIndex + 10;
                    break;
                case WEST:
                    currentNodeIndex = currentNodeIndex - 1;
                    break;
                case NORTHWEST:
                    currentNodeIndex = currentNodeIndex - 12;
                    break;

            }
            currentDirection = lookup[currentNodeIndex / 11][currentNodeIndex % 11];
            if(currentDirection == null) return tempDirection.opposite();
        }
        return null;
  }\n""")
fw.writeLine("public static void BFS(RobotController rc, MapLocation destination) throws GameActionException")
fw.openBracket()
fw.writeLine("MapLocation start = rc.getLocation();")
fw.writeLine("lookup = new Direction[" + str(size) + "][" + str(size) + "];")
fw.writeLine("setClosestFlag(rc);")
fw.writeLine("")
center = MapLocation(size // 2, size // 2)
currentLocation = MapLocation(size // 2, size // 2)
for i in range(0, size * size):
    if i == currentLocation.toIndex(size):
        fw.writeLine("l" + str(i) + " = getLocationFromIndex(" + str(i) + ", start);")
        fw.writeLine("dist" + str(i) + " = 0;")
        fw.writeLine("h" + str(i) + " = start.distanceSquaredTo(destination);")
        fw.writeLine("exists" + str(i) + " = true;")
        fw.writeLine("")
        continue
    fw.writeLine("l" + str(i) + " = getLocationFromIndex(" + str(i) + ", start);")
    fw.writeLine("dist" + str(i) + " = 1000000;")
    fw.writeLine("h" + str(i) + " = l" + str(i) + ".distanceSquaredTo(destination);")
    fw.writeLine("exists" + str(i) + " = " + "rc.onTheMap(l" + str(i) + ") && seenLocations[l" + str(i) + ".y][l" + str(i) + ".x].isPassable() && " +
                 "!rc.canSenseRobotAtLocation(l" + str(i) + ");")
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
    for neighbor in neighbors11x11[nodeIndex]:
        neighborLocation = indexToMapLocation(neighbor, center)
        if (neighborLocation not in visitedNodes and neighborLocation not in unvisitedNodesQueue):
            unvisitedNodesQueue.append(neighborLocation)
        fw.writeLine("if(exists" + str(neighbor) + " && dist" + str(nodeIndex) + " + 1 < dist" + str(neighbor) + ")")
        fw.openBracket()
        fw.writeLine("dist" + str(neighbor) + " = dist" + str(nodeIndex) + " + 1;")
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


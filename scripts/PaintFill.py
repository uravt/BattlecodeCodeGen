import math

from BFS24_11x11 import FileWriter
from BFS25_7x7 import MapLocation
from BFS25_7x7 import indexToMapLocation

fw = FileWriter(open("../java_files/PaintFill.java","w"))
package = "Version8"

radius_squared = 9

fw.writeLine(f"package {package};")
fw.writeLine("import battlecode.common.*;\n")
fw.writeLine("public class PaintFill")
fw.openBracket()
fw.writeLine("""
   public static MapLocation getLocationFromIndex(int nodeIndex, MapLocation center)
   {
      return new MapLocation(center.x - 3 + nodeIndex % 7, center.y - 3 + 6 - nodeIndex / 7);
   }
""")
fw.writeLine("public static void attemptFill(RobotController rc, MapLocation center) throws GameActionException")
fw.openBracket()
fw.writeLine("boolean[][] pattern = rc.getResourcePattern();")
size = 2 * math.isqrt(radius_squared) + 1
count = 0
for i in range(size * size):
    location = indexToMapLocation(i, MapLocation(size // 2, size // 2))
    if location.distanceSqr(MapLocation(size // 2, size // 2)) > radius_squared:
        continue
    fw.writeLine(f"MapLocation l{count} = getLocationFromIndex({i}, center);")
    fw.writeLine(f"if(rc.canPaint(l{count}) && !rc.senseMapInfo(l{count}).getPaint().isAlly())")
    fw.openBracket()
    fw.writeLine(f"rc.attack(l{count}, Utilities.getColorFromOriginPattern(center, pattern));")
    fw.closeBracket()
    count += 1
fw.closeBracket()
fw.closeBracket()
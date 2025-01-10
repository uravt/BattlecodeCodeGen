from scripts.BFS24_11x11 import FileWriter

fw = FileWriter(open("../java_files/UnrolledScan.java", "w"))

def main():
    fw.writeLine("""package Version16;
    import battlecode.common.*;""")
    fw.writeLine("import static Version16.RobotPlayer.*;")
    fw.writeLine("public class UnrolledScan")
    fw.openBracket()
    fw.writeLine("public static void updateSeenLocations(MapInfo[] locations)")
    fw.openBracket()
    fw.writeLine("switch(locations.length)")
    fw.openBracket()
    for i in range(22,70):
        fw.writeLine("case " + str(i) + ": ")
        fw.openBracket()
        for j in range(0, i):
            fw.writeLine("seenLocations[locations[" + str(j) + "].getMapLocation().y][locations[" + str(j) + "].getMapLocation().x] = locations[" + str(j) + "];")
        fw.writeLine("break;")
        fw.closeBracket()
    fw.closeBracket()
    fw.closeBracket()
    fw.closeBracket()

if __name__ == "__main__":
    main()

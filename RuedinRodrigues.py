import sys

def ga_solve(file=None, gui=True, maxtime=0):
    
    pass

if __name__ == '__main__':
    filename = None;
    gui = True;
    maxtime = 0;

    if("--nogui" in sys.argv):
        gui = False;
    if("--maxtime" in sys.argv):
        try:
            maxtime = int(sys.argv[sys.argv.index("--maxtime") + 1])
        except:
            print("Maxtime not a number ! (default value = 0)")

    for i in range(1, len(sys.argv)):
        if sys.argv[i-1][0] != '-' and sys.argv[i][0] != '-':
            filename = sys.argv[i]


    # print(filename)
    # print(gui)
    # print(maxtime)

    ga_solve(filename, gui, maxtime)

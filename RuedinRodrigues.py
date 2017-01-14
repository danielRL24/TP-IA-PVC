import sys

import random
import math
import time

import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE

from collections import deque
from copy import copy

# **************************************************************************** #
# CLASS CITY
# **************************************************************************** #
class City(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = int(x)
        self.y = int(y)

    # def __iter__(self):
    #     return iter(self.connections.items())

    # def __hash__(self):
    #     return str(self).__hash__()

    # def __str__(self):
    #     return str(self.name)

    # def __eq__(self, other):
    #     return self.name == other.name

    # def __gt__(self, other):
    #     return self.g > other.g

# **************************************************************************** #
# CLASS PATH
# **************************************************************************** #
class Candidate(object):
    def __init__(self, path, length):
        self.length = int(length)
        # self.path = deepcopy(path)
        self.path = path

# **************************************************************************** #
# SHOW A PATH
# **************************************************************************** #
def showPath(path):
    ''' Affichage du chemin '''
    result = ""
    for p in path:
        if p != "*" :
            result += p.name
        else :
            result += "*"
        result += " | "
    print(result)

# **************************************************************************** #
# GENETIC ALGORITHM
# **************************************************************************** #
def generatePopulation(cities, nCandidates):
    ''' Generation de la population '''
    path = []
    population = []
    for city in cities:
        path.append(city)
    for i in range(nCandidates):
        randomPath = random.sample(path, len(path))
        population.append(Candidate(randomPath, eval(randomPath)))

    # for a in population:
    #     print()
    #     for w in a.cities:
    #         print(w.name)
    #     print(a.length)

    return population

def eval(path):
    ''' Evaluation '''
    lenght = 0
    oldCity = None
    for city in path:
        if(oldCity is not None):
            lenght += math.sqrt((oldCity.x+city.x)**2 + (oldCity.y+city.y)**2)
        oldCity = city
    lenght += math.sqrt((path[0].x+path[-1].x)**2 + (path[0].y+path[-1].y)**2)

    return lenght

def selection(population, size):
    ''' Sélection '''
    population.sort(key=lambda x: x.length, reverse=False)
    del population[-(len(population)-size+1):]
    # random.seed();
    # choice = random.randint(0, len(population)-2)
    # return [population[choice], population[choice+1]]

def crossover(path1, path2, bInf, bSup):
    ''' Croisement '''
    crossValues = []
    crossValues = [path2[i] for i in range(bInf, bSup+1)]
    # print("inf " + str(bInf) + " sup" + str(bSup))
    # print("-> x")
    # showPath(path1)
    # print("-> y")
    # showPath(path2)
    # print("-> cv")
    # showPath(crossValues)

    path3 = []
    for x in path1:
        if(x not in set(crossValues)):
            path3.append(x)
        else:
            path3.append("*")
    # path3 = [x if x not in set(crossValues) else "*" for x in path1]
    pathLength = len(path1)
    #
    # print("-> x'")
    # showPath(path3)

    tmp = deque()

    j = 0
    for i in range(0, pathLength) :
        indexSup = (bSup-i) % pathLength
        if path3[indexSup] != "*" :
            indexInf = (bInf-1-j) % pathLength
            if path3[indexInf] != "*" :
                tmp.append(path3[indexInf])
            if indexSup < bInf or indexSup > bSup :
                if len(tmp) != 0:
                    path3[indexInf] = tmp.popleft()
            else :
                path3[indexInf] = path3[indexSup]
            j += 1

    for i, j in zip(range(bInf, bSup+1), range(0, (bSup-bInf)+1)) :
        path3[i] = crossValues[j]

    # print("-> x''")
    #
    #
    # showPath(path3)
    return Candidate(path3, eval(path3))

def mutate(path):
    ''' Mutation '''
    newpath = copy(path)
    a = random.randint(0, len(path)-1)
    b = random.randint(0, len(path)-1)
    newpath[a], newpath[b] = newpath[b], newpath[a]
    return Candidate(newpath, eval(newpath))

# **************************************************************************** #
# FUNCTION TO SHOW GUI
# **************************************************************************** #
def showGUI(cities, collecting=True):
    screen_x = 500
    screen_y = 500

    city_color = [10,10,200] # blue
    city_radius = 3

    font_color = [255,255,255] # white

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Exemple')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None,30)

    def draw(positions):
        screen.fill(0)
        for pos in positions:
            pygame.draw.circle(screen,city_color,(pos.x, pos.y),city_radius)
            # pygame.draw.circle(screen,city_color,pos,city_radius)
        text = font.render("Nombre: %i" % len(positions), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

    def travel():
        screen.fill(0)
        for i in range(0, len(cities)-1):
            pygame.draw.line(screen, city_color, [cities[i].x, cities[i].y], [cities[i+1].x, cities[i+1].y])
        # pygame.draw.lines(screen,city_color,True,cities)
        text = font.render("Un chemin, pas le meilleur!", True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

    # cities = []
    draw(cities)

    if not collecting :
        travel()


    i = len(cities)
    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
            elif event.type == MOUSEBUTTONDOWN:
                cities.append(City("v"+str(i), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                # cities.append(pygame.mouse.get_pos())
                draw(cities)
                i += 1

    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN: break

# **************************************************************************** #
# FUNCTION TO READ A FILE
# **************************************************************************** #
def readFile(filename, cities):
    ''' Load cities from file and put in a list '''
    try:
        with open (filename, 'r', encoding='utf-8') as input_file:
            for line in input_file:
                city = line.split(" ")
                cities.append(City(city[0], city[1], city[2]))
    except FileNotFoundError:
        sys.exit("File positions.txt not found !")

# **************************************************************************** #
# GA_SOLVE => MAIN FUNCTION
# **************************************************************************** #
def ga_solve(file=None, gui=True, maxtime=0.05):
    cities = []
    if file is not None:
        readFile(file, cities)
    if gui:
        showGUI(cities)

    # for city in cities:
    #     print(city.name + "(" + str(city.x) +  ", " + str(city.y) + ")")

    i = 0
    # while(i < 10) :

    # TODO Nombre impaire
    sizePop = 60
    maxRepeat = 10000


    survivorPop = int(sizePop/2)



    population = generatePopulation(cities, sizePop)
    nCities = len(population[0].path)

    startTime = time.time()

    once = True

    lastLength = 0
    lastLengthRepeat = 0


    while((time.time()-startTime) < maxtime and once):

        once = True

        selection(population, survivorPop+1)
        # print("sel" + str(len(population)))
        # print(population[0].length)
        if(population[0].length == lastLength):
            lastLengthRepeat+=1

        else:
            lastLengthRepeat = 0

        if(lastLengthRepeat > maxRepeat):
            print("break " + str(time.time()-startTime))
            break

        lastLength = population[0].length

        for i in range(0, survivorPop-1, 2):
            # print("act" + str(len(population)))
            crossBegin = random.randint(1,nCities-2)
            crossEnd = random.randint(crossBegin+1, nCities-1)
            # print(crossBegin)
            # print("end " + str(crossEnd))
            population.append(crossover(population[random.randint(0,int(survivorPop-1))].path, population[random.randint(0,survivorPop-1)].path, crossBegin, crossEnd))
            # population.append(mutate(population[random.randint(0,survivorPop-1)].path))
            # population.append(mutate(population[0].path))
            population.append(mutate(population[random.randint(0,int(survivorPop/9)-1)].path))

    # for p in population:
        # showPath(p.path)


        # candidate1, candidate2 = selection(population)
        # candidate1.path = deepcopy(crossover(candidate1.path, candidate2.path, 1, 2))
        # candidate2.path = deepcopy(crossover(candidate2.path, candidate1.path, 1, 2))
        # for c in population :
        #     mutate(c.path)

        # i += 1

    selection(population, 4)
    showPath(population[0].path)
    print(population[0].length)
    if(gui):
        showGUI(population[0].path, False)
# **************************************************************************** #
# ENTRY POINT
# **************************************************************************** #
if __name__ == '__main__':
    filename = None;
    gui = True;
    maxtime = 5;

    if("--nogui" in sys.argv):
        gui = False;
    if("--maxtime" in sys.argv):
        try:
            maxtime = int(sys.argv[sys.argv.index("--maxtime") + 1])
        except:
            print("Maxtime not a number ! (default value = 0)")

    for i in range(1, len(sys.argv)):
        if sys.argv[i][0] != '-' and sys.argv[i-1] != "--maxtime":
            filename = sys.argv[i]


    # print(filename)
    # print(gui)
    # print(maxtime)

    ga_solve(filename, gui, maxtime)

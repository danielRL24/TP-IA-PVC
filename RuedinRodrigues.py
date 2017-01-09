import sys

import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE

import random
import math

from collections import deque

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
class Path(object):
    def __init__(self, cities):
        self.length = eval(cities)
        self.cities = cities

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
def generatePopulation(cities, nPath):
    ''' Generation de la population '''
    path = []
    population = []
    for city in cities:
        path.append(city)
    for i in range(nPath):
        population.append(Path(random.sample(path, len(path))))

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
        else:
            oldCity = city

    return lenght

def selection(population):
    ''' Sélection '''
    population.sort(key=lambda x: x.length, reverse=False)

    for i in range(0, len(population)):
        pass

def crossover(path1, path2, bInf, bSup):
    ''' Croisement '''
    crossValues = []
    crossValues = [path2[i] for i in range(bInf, bSup+1)]
    print("-> x")
    showPath(path1)
    print("-> y")
    showPath(path2)
    print("-> cv")
    showPath(crossValues)

    path3 = []
    path3 = [x if x not in set(crossValues) else "*" for x in path1]
    pathLength = len(path1)

    print("-> x'")
    showPath(path3)

    stack = deque()

    j = 0
    for i in range(0, pathLength) :
        indexSup = (bSup-i) % pathLength
        if path3[indexSup] != "*" :
            indexInf = (bInf-1-j) % pathLength
            if path3[indexInf] != "*" :
                stack.append(path3[indexInf])
            if indexSup < bInf or indexSup > bSup :
                if len(stack) != 0:
                    path3[indexInf] = stack.popleft()
            else :
                path3[indexInf] = path3[indexSup]
            j += 1

    for i, j in zip(range(bInf, bSup+1), range(0, (bSup-bInf)+1)) :
        path3[i] = crossValues[j]

    print("-> x''")
    showPath(path3)
    return path3

def mutate(path):
    ''' Mutation '''
    a = random.randint(0, len(path))
    b = random.randint(0, len(path))
    path[a], path[b] = path[b], path[a]

# **************************************************************************** #
# FUNCTION TO SHOW GUI
# **************************************************************************** #
def showGUI(cities):
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

    # cities = []
    draw(cities)

    collecting = True

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

    screen.fill(0)
    # pygame.draw.lines(screen,city_color,True,cities)
    text = font.render("Un chemin, pas le meilleur!", True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

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
def ga_solve(file=None, gui=True, maxtime=0):
    cities = []
    if file is not None:
        readFile(file, cities)
    if gui:
        showGUI(cities)

    for city in cities:
        print(city.name + "(" + str(city.x) +  ", " + str(city.y) + ")")

    population = generatePopulation(cities, 8)
    # for i in population:
    #     print(i.length)
    #
    # print()

    # selection(population)
    # eval(population[0])
    # population0 = crossover(population[0], population[1], 1, 2)
    # population1 = crossover(population[1], population[0], 1, 2)
    # mutate(population[0])

# **************************************************************************** #
# ENTRY POINT
# **************************************************************************** #
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
        if sys.argv[i][0] != '-' and sys.argv[i-1] != "--maxtime":
            filename = sys.argv[i]


    print(filename)
    # print(gui)
    # print(maxtime)

    ga_solve(filename, gui, maxtime)

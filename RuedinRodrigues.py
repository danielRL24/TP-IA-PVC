import sys

import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys

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

    i = 0
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

def readFile(filename, cities):
    ''' Load cities from file and put in a list '''
    try:
        with open (filename, 'r', encoding='utf-8') as input_file:
            for line in input_file:
                city = line.split(" ")
                cities.append(City(city[0], city[1], city[2]))
    except FileNotFoundError:
        sys.exit("File positions.txt not found !")

def ga_solve(file=None, gui=True, maxtime=0):
    cities = []
    if gui:
        showGUI(cities)
    else:
        readFile(file, cities)

    for city in cities:
        print(city.name + "(" + str(city.x) +  ", " + str(city.y) + ")")

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

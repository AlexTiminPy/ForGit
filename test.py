import math
import random
import sys

import pygame

COUNTER = 0
DEAD = 0


class Color:
    BLACK = (40, 40, 40)
    WHITE = (215, 215, 215)
    RED = (200, 50, 50)
    GREEN = (50, 200, 50)
    BLUE = (30, 67, 76)
    YELLOW = (200, 200, 50)
    GRAY = (125, 125, 125)
    List_color = [RED, WHITE, GREEN, BLUE]

    @staticmethod
    def random_color():
        return random.choice(Color.List_color)


width, height = 1800, 900
win = pygame.display.set_mode((width, height))
CLOCK = pygame.time.Clock()
fps = 60


class Enemy:
    def __init__(self, coord: [int, int], size: int, hp: int):  # speed - pixel per fps
        self.coord = coord
        self.size = size
        self.old_hp = hp
        self.hp = hp
        # self.speed = 3
        self.speed = random.randrange(0, 5)

    def __repr__(self):
        return str(self.coord)

    def draw(self):
        if self.hp <= 0:
            global DEAD
            pygame.draw.circle(win, Color.RED, self.coord, self.size * 3)
            DEAD += 1
            self.coord = [random.randrange(200, 1750), random.randrange(0, 900)]
            self.hp = self.old_hp
        if self.hp == self.old_hp:
            pygame.draw.circle(win, Color.GREEN, self.coord, self.size)
        elif self.hp > self.old_hp / 2:
            pygame.draw.circle(win, Color.YELLOW, self.coord, self.size)
        else:
            pygame.draw.circle(win, Color.RED, self.coord, self.size)

        # self.coord[0] -= self.speed
        if self.coord[0] < 0:
            global COUNTER
            COUNTER += 1
            self.coord = [random.randrange(200, 1750), random.randrange(0, 900)]


class Patron:
    def __init__(self, coord: [int, int], size: int, speed: int,
                 dx: float, dy: float, dead):  # speed - pixel per fps
        self.coord = coord
        self.size = size
        self.speed = speed
        self.dx = dx + round(random.uniform(-0.01, 0.01), 3)
        self.dy = dy + round(random.uniform(-0.01, 0.01), 3)
        self.gravitation = 1
        self.dead = dead

    def check(self):
        for i in enemy:
            if math.hypot(self.coord[0] - i.coord[0], self.coord[1] - i.coord[1]) < i.size + self.size:
                i.hp -= self.size
                if self.dead:
                    return False
        if width > self.coord[0] > 0 and height > self.coord[1] > 0:
            return True
        return False

    def draw(self):
        pygame.draw.circle(win, Color.BLACK, self.coord, self.size)

    def calculate(self):
        self.coord[0] += self.dx * self.speed
        self.coord[1] += self.dy * self.speed
        self.coord[1] += self.gravitation - 1
        # self.gravitation *= 1.006
        # self.speed *= 0.999999

    def __call__(self):
        self.draw()
        self.calculate()


class Gun:
    def __init__(self, coord: [int, int], size: int,
                 warhead: int, reload_time: int, patron_size: int, patron_speed: int,
                 patr_dead):  # reload time - fps
        self.coord = coord
        self.size = size
        self.warhead = warhead
        self.old_warhead = warhead
        self.reload_time = reload_time
        self.color = Color.RED
        self.patrons = []
        self.is_reload = 0
        self.patron_size = patron_size
        self.patron_speed = patron_speed

        self.patr_dead = patr_dead

        self.enemy = sorted(enemy, key=lambda x: math.hypot(x.coord[0] - self.coord[0],
                                                            x.coord[1] - self.coord[1]))[0]

    def draw(self):
        pygame.draw.circle(win, self.color, self.coord, self.size)

    def fire(self):  # , dx, dy
        dx = self.enemy.coord[0]
        dy = self.enemy.coord[1]
        if self.warhead == 0:
            return
        if self.is_reload > 0:
            return
        self.warhead -= 1
        # if self.is_reload > 0:
        #     return
        # if self.warhead <= len(self.patrons):
        #     return
        t = math.atan2(dy - self.coord[1], dx - self.coord[0])
        dx = math.cos(t)
        dy = math.sin(t)
        self.patrons.append(Patron(self.coord[:], self.patron_size, self.patron_speed,
                                   dx, dy, self.patr_dead))
        # self.is_reload = self.reload_time

    def __call__(self):
        self.draw()

        self.enemy = sorted(enemy, key=lambda x: math.hypot(x.coord[0] - self.coord[0],
                                                            x.coord[1] - self.coord[1]))[0]

        self.fire()

        if self.warhead == 0:
            self.is_reload = self.reload_time
            self.warhead = self.old_warhead
        if self.is_reload > 0:
            self.is_reload -= 1
        # if self.is_reload > 0:
        #     self.is_reload -= 1
        for i, patron in enumerate(self.patrons):
            patron()
            if not patron.check():
                self.patrons = self.patrons[:i] + self.patrons[i + 1:]
                continue


enemy = [Enemy([random.randrange(200, 1750), random.randrange(0, 900)], 10, 100) for i in range(50)]

#            coord, size, warhead, reload_time, patron_size, patron_speed

test = [
    Gun([50, 100], 30, 1000, 0, 4, 10, True),
    Gun([50, 200], 30, 1000, 0, 4, 10, True),
    Gun([50, 300], 30, 1000, 0, 4, 10, True),
    Gun([50, 400], 30, 1000, 0, 4, 10, True),
    Gun([50, 500], 30, 1000, 0, 4, 10, True),
    Gun([50, 600], 30, 1000, 0, 4, 10, True),
    Gun([50, 700], 30, 1000, 0, 4, 10, True),
    Gun([50, 800], 30, 1000, 0, 4, 10, True),
]

while True:
    win.fill(Color.GRAY)
    pygame.display.set_caption(str(round(CLOCK.get_fps(), 3)) + "---" +
                               str(round(CLOCK.get_time(), 3)) + "---" +
                               str(COUNTER) + "---" +
                               str(DEAD))
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pass

        if event.type == pygame.MOUSEBUTTONUP:

            # if event.button == 1:
            #     for func in test:
            #         func.fire(mouse[0], mouse[1])

            if event.button == 3:
                print(3)

            if event.button == 4:
                print(4)

            if event.button == 5:
                print(5)

    # if click[0]:
    #     for func in test:
    #         func.fire(mouse[0], mouse[1])

    for gun in test:
        gun()

    for i in enemy:
        i.draw()
    # gamer.work()

    # print(SceneLists.all_list)

    pygame.display.flip()
    CLOCK.tick(fps)

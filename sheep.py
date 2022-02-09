import copy
import math
import random
import sys

import pygame

pygame.init()


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


class Patron:
    def __init__(self, coord: [int, int], size: int, speed: int,
                 dx: float, dy: float):  # speed - pixel per fps
        self.coord = coord
        self.size = size
        self.speed = speed
        self.dx = dx + round(random.uniform(-0.01, 0.01), 3)
        self.dy = dy + round(random.uniform(-0.01, 0.01), 3)

    def check(self):
        if width > self.coord[0] > 0 and height > self.coord[1] > 0:
            return True
        return False

    def draw(self):
        pygame.draw.circle(win, Color.GREEN, self.coord, self.size)

    def calculate(self):
        self.coord[0] += self.dx * self.speed
        self.coord[1] += self.dy * self.speed

    def __call__(self):
        self.draw()
        self.calculate()


class Button:
    def __init__(self, coordinates, text, func):
        self.coordinates = coordinates
        self.text = text
        self.func = func

    def draw(self):
        pygame.draw.rect(win, Color.BLACK, self.coordinates)
        font = pygame.font.SysFont("arial", self.coordinates[3])
        text = font.render(str(self.text), False, Color.WHITE)
        win.blit(text, (self.coordinates[0], self.coordinates[1]))

    def check(self, mouse):
        if self.coordinates[0] <= mouse[0] <= self.coordinates[0] + self.coordinates[2] and \
                self.coordinates[1] <= mouse[1] <= self.coordinates[1] + self.coordinates[3]:
            return True
        return False

    def __call__(self, mouse, click):
        self.draw()
        if self.check(mouse) and click[0]:
            self.func()


class ChooseGun:
    def __init__(self, coordinates, text, gun):
        self.coordinates = coordinates
        self.text = text
        self.gun = gun

    def draw(self):
        pygame.draw.rect(win, Color.BLACK, self.coordinates)
        font = pygame.font.SysFont("arial", self.coordinates[3])
        text = font.render(str(self.text), False, Color.WHITE)
        win.blit(text, (self.coordinates[0], self.coordinates[1]))

    def check(self, mouse):
        if self.coordinates[0] <= mouse[0] <= self.coordinates[0] + self.coordinates[2] and \
                self.coordinates[1] <= mouse[1] <= self.coordinates[1] + self.coordinates[3]:
            return True
        return False


class Gun:
    def __init__(self, center: [float, float], size: int, speed, angle):
        self.angle = angle
        self.speed = speed
        self.size = size
        self.center = center
        self.patron = []

    def draw(self):
        pygame.draw.circle(win, Color.BLACK, self.center, self.size)

    def fire(self, mouse=None):
        if mouse is None:
            dx = math.cos(math.radians(self.angle))
            dy = math.sin(math.radians(self.angle))
        else:
            t = math.atan2(mouse[1] - self.center[1], mouse[0] - self.center[0])
            dx = math.cos(t)
            dy = math.sin(t)
        self.patron.append(Patron(copy.copy(self.center), 3, 15, dx, dy))

    def __call__(self):
        for t in self.patron:
            t()


class Sheep:
    def __init__(self, center: [float, float],
                 coordinates: [[float, float], [float, float],
                               [float, float], [float, float]],
                 kernel_energy: int, max_definition: int,
                 max_shield: int, max_speed: int, max_rotate: float, gun: []):
        self.max_rotate = max_rotate
        self.center = center
        self.coordinates = coordinates
        self.gun = gun
        self.max_speed = max_speed
        self.kernel_energy = kernel_energy
        self.energy = self.kernel_energy
        self.max_definition = max_definition
        self.max_shield = max_shield
        self.angle = 0
        self.button = []
        self.is_fire = 0

        self.chosen_gun = None

        for i in range(len(self.gun)):
            self.button.append(ChooseGun([i * 50 + 20, 20, 45, 45], self.gun[i].size, self.gun[i]))

        self.replace_dot = self.center

    def fire(self, mouse):
        if self.energy <= 0:
            return
        if self.is_fire == 0 and self.chosen_gun:
            self.chosen_gun.gun.fire(mouse)
            self.energy -= self.chosen_gun.gun.size * 3
        # for g in self.func:
        #     g.fire()

    def draw(self):
        pygame.draw.polygon(win, Color.GRAY, self.coordinates, 5)
        pygame.draw.circle(win, Color.RED, self.center, 5)
        x = math.cos(math.radians(self.angle)) * 100 + self.center[0]
        y = math.sin(math.radians(self.angle)) * 100 + self.center[1]
        pygame.draw.line(win, Color.RED, self.center, [x, y], 5)
        pygame.draw.line(win, Color.RED, self.center, self.replace_dot, 5)

        for i in self.gun:
            i.draw()

        for i in self.button:
            i.draw()

    def rotate(self, angle_rotate):
        self.energy -= 25
        self.angle += angle_rotate
        self.angle = self.angle % 360
        for dot in self.coordinates:
            distance = math.hypot(dot[0] - self.center[0], dot[1] - self.center[1])
            angle = math.atan2(dot[1] - self.center[1], dot[0] - self.center[0]) + \
                    math.radians(angle_rotate)
            dot[0] = math.cos(angle) * distance + self.center[0]
            dot[1] = math.sin(angle) * distance + self.center[1]

        for gun in self.gun:
            gun.angle += angle_rotate
            gun.angle = gun.angle % 360
            distance = math.hypot(gun.center[0] - self.center[0], gun.center[1] - self.center[1])
            angle = math.atan2(gun.center[1] - self.center[1], gun.center[0] - self.center[0]) + \
                    math.radians(angle_rotate)
            gun.center[0] = math.cos(angle) * distance + self.center[0]
            gun.center[1] = math.sin(angle) * distance + self.center[1]

    def set_replace(self, x, y):
        self.replace_dot = [x, y]

    def replace_center(self, fin_dot):
        for i in self.coordinates:
            i[0] = fin_dot[0] + i[0] - self.center[0]
            i[1] = fin_dot[1] + i[1] - self.center[1]

        for i in self.gun:
            i.center[0] = fin_dot[0] + i.center[0] - self.center[0]
            i.center[1] = fin_dot[1] + i.center[1] - self.center[1]

        self.center = fin_dot

    def replace(self):
        if self.center == self.replace_dot:
            return

        dif = math.degrees(math.atan2(self.replace_dot[1] - self.center[1],
                                      self.replace_dot[0] - self.center[0]))

        if dif < 0:
            dif = dif + 360

        dif = dif - self.angle

        if dif != 0:
            if abs(dif) > 180:
                if dif > 0:
                    dif = -(360 - dif)
                else:
                    dif = 360 + dif

            if dif < 0:
                self.rotate(max(dif, -self.max_rotate))
            else:
                self.rotate(min(dif, self.max_rotate))

            return

        if math.hypot(self.center[0] - self.replace_dot[0],
                      self.center[1] - self.replace_dot[1]) < self.max_speed:
            return

        x = self.max_speed * math.cos(math.radians(self.angle))
        y = self.max_speed * math.sin(math.radians(self.angle))

        self.replace_center([self.center[0] + x, self.center[1] + y])

        self.energy -= 25

    def cancel(self):
        self.replace_dot = self.center

    def __call__(self, mouse):
        if self.is_fire > 0:
            self.is_fire -= 1
        self.draw()
        if self.energy <= 0:
            return
        self.replace()
        for i in self.gun:
            i()

        for i in self.button:
            if i.check(mouse):
                self.chosen_gun = i
                self.is_fire = 10


test = Sheep([900, 450],
             [[1000, 250], [1000, 550],
              [800, 550], [800, 250]],
             40000, 200, 200, 3, 1, [Gun([1000, 300], 15, 5, 0), Gun([1000, 350], 15, 5, 0)])


def max_energy_for_test():
    test.energy = test.kernel_energy


y = Button([0, 100, 100, 50], "New", max_energy_for_test)

while True:
    win.fill(Color.WHITE)
    pygame.display.set_caption(str(round(CLOCK.get_fps(), 3)) + "---" +
                               str(round(CLOCK.get_time(), 3)) + "---" +
                               str(test.energy))
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                test.fire(mouse)

            if event.button == 6:
                test.cancel()

        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 3:
                test.set_replace(mouse[0], mouse[1])

            if event.button == 4:
                print(4)

            if event.button == 5:
                print(5)

    test(mouse)
    y(mouse, click)

    pygame.display.flip()
    CLOCK.tick(fps)

import sys

import pygame

W = 1200
H = 600

A = []

Glob_dx_dy = [0, 0]

X, Y = 0, 0

pygame.init()
win = pygame.display.set_mode((W, H))
CLOCK = pygame.time.Clock()
fps = 60

BLACK = (40, 40, 40)
WHITE = (215, 215, 215)
RED = (255, 0, 0)
GREEN = (50, 130, 70)
BLUE = (0, 0, 255)


class Obj:
    def __init__(self, x, y, wid, hei, col):
        self.x = x
        self.y = y
        self.width = wid
        self.height = hei
        self.x_len = 0
        self.y_len = 0
        self.color = col
        A.append(self)

    def scale(self, xx, yy):
        mouse = pygame.mouse.get_pos()
        self.width *= xx
        self.height *= yy
        self.x_len *= xx
        self.y_len *= yy
        self.x = mouse[0] - self.x_len
        self.y = mouse[1] - self.y_len

    def draw(self):
        mouse = pygame.mouse.get_pos()
        self.x_len = mouse[0] - self.x
        self.y_len = mouse[1] - self.y
        pygame.draw.rect(win, self.color, [self.x + X, self.y + Y,
                                           self.width + 1, self.height + 1])


test = Obj(-100, -100, 56, 70, BLACK)
test2 = Obj(0, 0, 56, 76, RED)
test3 = Obj(-100, 0, 87, 124, BLUE)
test4 = Obj(0, -100, 50, 23, GREEN)
save = [0, 0]
s = False

while True:
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                s = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                s = False
            if event.button == 4:
                for i in A:
                    i.scale(1.05, 1.05)
            if event.button == 5:
                for i in A:
                    i.scale(0.95, 0.95)

    if s:
        for i in A:
            i.x += mouse[0] - save[0]
            i.y += mouse[1] - save[1]

    if key[pygame.K_RIGHT]:
        for i in A:
            i.x += 1
    if key[pygame.K_LEFT]:
        for i in A:
            i.x -= 1
    if key[pygame.K_UP]:
        for i in A:
            i.y -= 1
    if key[pygame.K_DOWN]:
        for i in A:
            i.y += 1

    win.fill(WHITE)
    for i in A:
        i.draw()

    save = mouse[:]
    pygame.display.flip()
    CLOCK.tick(fps)

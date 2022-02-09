import pygame
import datetime
import sys
from math import *

CLOCK = pygame.time.Clock()

screen_width, screen_height = 400, 200
win = pygame.display.set_mode((screen_width, screen_height))
fps = 60

pygame.init()

Button_list = []


class Watch:
    def __init__(self, center_pos: tuple, radius: int, color: tuple, offset_watch: tuple = (0, 0, 0)):
        self.center_pos = center_pos
        self.radius = radius
        self.color = color
        self.offset_watch = offset_watch

        self.hour_arrow = self.Arrow(12, 3, (0, 0, 0), 30)
        self.minute_arrow = self.Arrow(60, 2, (0, 0, 0), 60)
        self.second_arrow = self.Arrow(60, 1, (0, 0, 0), 100)

    def __call__(self):
        now = datetime.datetime.now()

        HOUR = now.hour
        MINUTE = now.minute
        SECONDS = now.second

        self.draw()

        self.hour_arrow(self.center_pos, HOUR, self.center_pos, self.offset_watch[0])
        self.minute_arrow(self.center_pos, MINUTE, self.center_pos, self.offset_watch[1])
        self.second_arrow(self.center_pos, SECONDS, self.center_pos, self.offset_watch[2])

    def draw(self):
        pygame.draw.circle(win, self.color, self.center_pos, self.radius)

    class Arrow:
        def __init__(self, step: int, width: int, color: tuple, arrow_len: int):
            self.step = 360 / step
            self.width = width
            self.color = color
            self.len = arrow_len

        def draw(self, start_pos: tuple, end_pos: tuple):
            pygame.draw.line(win, self.color, start_pos, end_pos, self.width)

        def calculate_end_pos(self, time: int, divergention: tuple, offset: int) -> tuple:
            return (self.len * cos(radians(self.step * (time - offset) - 90)) + divergention[0],
                    self.len * sin(radians(self.step * (time - offset) - 90)) + divergention[1])

        def __call__(self, start_pos: tuple, time: int, divergention: tuple, offset: int):
            self.draw(start_pos, self.calculate_end_pos(time, divergention, offset))


class Button:
    def __init__(self, coord: tuple, color: tuple, offset: tuple, text: str):
        self.coord = coord
        self.color = color
        self.offset = offset
        self.text = text
        Button_list.append(self)

    def draw(self):
        pygame.draw.rect(win, self.color, self.coord)

        font = pygame.font.SysFont("arial", self.coord[3])
        text = font.render(self.text, False, (0, 0, 0))
        win.blit(text, (self.coord[0], self.coord[1]))

    def check(self, mouse: tuple):
        if self.coord[0] <= mouse[0] <= self.coord[0] + self.coord[2] and \
                self.coord[1] <= mouse[1] <= self.coord[1] + self.coord[3]:
            return True
        return False

    def __call__(self, mouse):
        if self.check(mouse):
            watch.offset_watch = self.offset


watch = Watch((100, 100), 100, (255, 255, 255))

Button((200, 0, 200, 19), (255, 255, 0), (0, 0, 0), "Moscow")
Button((200, 20, 200, 19), (255, 255, 0), (3, 10, 30), "Los Angeles")
Button((200, 40, 200, 19), (255, 255, 0), (6, 10, 30), "Mianma")

while True:
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()

    win.fill((127, 127, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in Button_list:
                    button(mouse)

    watch()

    for button in Button_list:
        button.draw()

    CLOCK.tick(fps)
    pygame.display.flip()

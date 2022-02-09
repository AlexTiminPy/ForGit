import random
import sys
from math import cos, sin
import pygame

pygame.init()


class Color:
    BLACK = (40, 40, 40)
    WHITE = (180, 180, 180)
    RED = (200, 50, 50)
    GREEN = (50, 200, 50)
    BLUE = (30, 67, 200)
    YELLOW = (200, 200, 50)
    GRAY = (125, 125, 125)
    List_color = ["RED", "BLUE", 'GREEN', 'GRAY']

    @staticmethod
    def random_color():
        return random.choice(Color.List_color)


width, height = 1800, 900
win = pygame.display.set_mode((width, height))
CLOCK = pygame.time.Clock()
fps = 120
is_true = True

grade = 4
cc = []

left_glob, right_glob, deep = -10, 10, 100

ggg = False


def ttt():
    global grade, cc, ggg
    for i in range(left_glob, right_glob):
        for j in range(left_glob, right_glob):
            for k in range(deep):
                for l in range(deep):
                    # win.fill(Color.WHITE)
                    # pygame.display.set_caption(f"{str(grade)}")
                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            sys.exit()

                        if event.type == pygame.MOUSEBUTTONUP:
                            if event.button == 1:
                                grade += 1
                                cc = []
                                ggg = False
                                win.fill(Color.WHITE)
                                return

                            if event.button == 3:
                                grade -= 1
                                cc = []
                                ggg = False
                                win.fill(Color.WHITE)
                                return

                    pygame.draw.rect(win, Color.BLACK, [0, 450, 1800, 1])
                    pygame.draw.rect(win, Color.BLACK, [900, 0, 1, 900])
                    z = complex(i + k / deep, j + l / deep)
                    z **= grade
                    if 0 < z.real * 2 + 900 < width and 0 < z.imag * 2 + 450 < height:
                        x = z.real * cos(z.imag)
                        y = z.real * sin(z.imag)
                        cc.append([x + 900, y + 450, 10, 10])

                        pygame.draw.rect(win, Color.RED, [x + 900, y + 450, 2, 2])

                        pygame.display.flip()

    ggg = True


while True:
    win.fill(Color.WHITE)
    pygame.display.set_caption(f"{str(round(CLOCK.get_fps(), 3))}  {str(round(CLOCK.get_time(), 3))}")
    mouse = pygame.mouse.get_pos()
    # click = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()

    if not ggg:
        ttt()

    print("fin")

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         pass
        #
        #     if event.key == pygame.K_1:
        #         pass
        #
        #     if event.key == pygame.K_2:
        #         pass
        #
        #     if event.key == pygame.K_3:
        #         pass
        #
        #     if event.key == pygame.K_4:
        #         pass

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                grade += 1
                cc = []
                ggg = False

            if event.button == 3:
                grade -= 1
                cc = []
                ggg = False

            # if event.button == 4:
            #     pass
            #
            # if event.button == 5:
            #     pass

    pygame.draw.rect(win, Color.BLACK, [0, 450, 1800, 1])
    pygame.draw.rect(win, Color.BLACK, [900, 0, 1, 900])

    if cc:
        for i in cc:
            if 0 < i[0] < width and 0 < i[1] < height:
                pygame.draw.rect(win, Color.RED, [i[0], i[1], 2, 2])

    pygame.display.flip()

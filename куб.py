import math
import random
import sys

import numpy
import pygame

pygame.init()


class Color:
    BLACK = (40, 40, 40)
    WHITE = (180, 180, 180)
    RED = (200, 50, 50)
    GREEN = (50, 200, 50)
    BLUE = (30, 67, 255)
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


class Warrior:
    def __init__(self, coordinates, c, place=None):
        if place is None:
            place = [0, 0]
        self.coordinates = coordinates
        self.center = c
        self.old_center = self.center[:]

        self.is_alive = True
        self.is_neighbors = None
        self.place = place

        self.distance = math.hypot(self.coordinates[0], self.coordinates[1])

    def __repr__(self):
        return f"{numpy.array(self.coordinates) + numpy.array(self.center)}"

    def return_pos(self):
        return self.place[0], self.place[1]

    def kill(self):
        self.is_alive = False

    def __eq__(self, other):
        if isinstance(other, Warrior):
            if abs(math.hypot((self.coordinates[0] + self.center[0]) - (other.coordinates[0] + other.center[0]),
                              (self.coordinates[1] + self.center[1]) - (other.coordinates[1] + other.center[1]))) < 5.0:
                return True
            else:
                return False
        return False

    def __hash__(self):
        x = self.coordinates[0] + self.center[0]
        y = self.coordinates[1] + self.center[1]
        return int(x * 10000000 + y)

    def draw(self, father):

        if not self.is_alive:
            self.coordinates[0] = self.coordinates[0] + self.center[0]
            self.coordinates[1] = self.coordinates[1] + self.center[1]
            self.center = [0, 0]

            pygame.draw.circle(win, Color.RED, self.coordinates, 2)

        else:
            c = 0
            try:
                if self.place[0] == 0:
                    pass
                else:
                    if father.warriors[self.place[0] - 1][self.place[1]].is_alive:
                        c += 1
            except:
                pass
            try:
                if self.place[1] == 0:
                    pass
                else:
                    if father.warriors[self.place[0]][self.place[1] - 1].is_alive:
                        c += 1
            except:
                pass
            try:
                if father.warriors[self.place[0] + 1][self.place[1]].is_alive:
                    c += 1
            except:
                pass
            try:
                if father.warriors[self.place[0]][self.place[1] + 1].is_alive:
                    c += 1
            except:
                pass
            if c == 4:
                self.is_neighbors = False
                pygame.draw.circle(win, Color.BLACK, list(numpy.array(self.coordinates) +
                                                          numpy.array(self.center)), 2)
            else:
                self.is_neighbors = True
                pygame.draw.circle(win, Color.GREEN, list(numpy.array(self.coordinates) +
                                                          numpy.array(self.center)), 2)

    def __ne__(self, other):
        if isinstance(other, Warrior):
            if abs((other.coordinates[0] + other.center[0]) - (self.coordinates[0] + self.center[0])) > 6 or \
                    abs((other.coordinates[1] + other.center[1]) - (self.coordinates[1] + self.center[1])) > 6:
                return True
            return False
        return False

    def __lt__(self, other):
        if isinstance(other, Warrior):
            if (self.coordinates[0] + self.center[0]) - (other.coordinates[0] + other.center[0]) > 6:
                return False
            elif (self.coordinates[0] + self.center[0]) - (other.coordinates[0] + other.center[0]) < -6:
                return True
            else:
                if (self.coordinates[1] + self.center[1]) - (other.coordinates[1] + other.center[1]) > 6:
                    return False
                elif (self.coordinates[1] + self.center[1]) - (other.coordinates[1] + other.center[1]) < -6:
                    return True
        # <

    def __gt__(self, other):
        if isinstance(other, Warrior):
            if (self.coordinates[0] + self.center[0]) - (other.coordinates[0] + other.center[0]) > 6:
                return True
            elif (self.coordinates[0] + self.center[0]) - (other.coordinates[0] + other.center[0]) < -6:
                return False
            else:
                if (self.coordinates[1] + self.center[1]) - (other.coordinates[1] + other.center[1]) > 6:
                    return True
                elif (self.coordinates[1] + self.center[1]) - (other.coordinates[1] + other.center[1]) < -6:
                    return False
        # >


class Squad:
    def __init__(self, name, team, center, count, speed, rotate_speed, damage, cooldown_time,
                 color=Color.BLACK, angle=0):
        self.name = name
        self.center = center
        self.count = count
        self.warriors = numpy.array([[Warrior([i, t], self.center)
                                      for i in range(-count[0] * 3, count[0] * 3, 6)]
                                     for t in range(-count[1] * 3, count[1] * 3, 6)])

        for i in range(len(self.warriors)):
            for t in range(len(self.warriors[0])):
                self.warriors[i][t].place = [i, t]

        self.max_distance = max([self.warriors[i][t].distance for i in range(len(self.warriors))
                                 for t in range(len(self.warriors[0]))])

        self.color = color

        self.team = team

        self.speed = speed
        self.health = count[0] * count[1]
        self.damages = damage
        self.angle = angle
        self.max_rotate = rotate_speed

        self.rotate_vector = 0
        self.motion_vector = self.center

        self.counter = 0
        self.old_counter = cooldown_time

        self.collision = []
        self.c = []

    def __repr__(self):
        return f"<{self.name} - {self.warriors.size}: {self.c[-3:-1]}>"

    def damage(self):
        for i in self.collision:
            for t in i:
                x, y = t.return_pos()
                z = random.randint(0, 101)
                if z > 60:
                    try:
                        self.warriors[x][y].kill()
                    except:
                        print(x, y)
        self.collision = []

    def search_target(self, act):
        for enemy in act:
            if enemy.team == self.team or enemy == self:
                continue

            # if abs(math.hypot(self.center[0] - enemy.center[0], self.center[1] - enemy.center[1])) > \
            #         abs(self.max_distance + enemy.max_distance):
            #     continue

            r1 = list(filter(lambda x: (x.is_neighbors and x.is_alive), list(self.warriors.flat)))
            r2 = list(filter(lambda z: (z.is_neighbors and z.is_alive), list(enemy.warriors.flat)))

            collision_1 = [x for x in r2 if x in r1]

            # collision_1 = numpy.array(numpy.intersect1d(r2, r1, assume_unique=True))
            # collision_2 = numpy.array(numpy.intersect1d(r1, r2, assume_unique=True))

            enemy.collision.append(collision_1[:])

    def draw(self, chose):
        if self is chose:
            font = pygame.font.SysFont("arial", 25)
            text = font.render(str(len(self.warriors)) + "--" + str(self.damages), False, Color.RED)
            win.blit(text, (self.center[0] - 50, self.center[1] - 50))

        pygame.draw.line(win, Color.BLACK, self.center, self.motion_vector)

        for i in self.warriors:
            for t in i:
                t.draw(self)

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 360
        angle = math.radians(angle)
        for i in self.warriors:
            for warrior in i:
                if warrior.is_alive:
                    warrior.coordinates = list(numpy.dot([[math.cos(angle), -math.sin(angle)],
                                                          [math.sin(angle), math.cos(angle)]],
                                                         numpy.array(warrior.coordinates).T).T)

    def get_to(self):
        speed = self.speed
        if self.collision:
            speed = self.speed * (1 / max(len(self.collision), 1))
        if (abs(self.motion_vector[0] - self.center[0]) < 1) and (abs(self.motion_vector[1] - self.center[1]) < 1):
            return

        angle_with_target = (math.degrees(math.atan2(self.motion_vector[1] - self.center[1],
                                                     self.motion_vector[0] - self.center[0])) % 360)

        if abs(angle_with_target - self.angle) > 2:

            if angle_with_target < 0:
                angle_with_target = angle_with_target + 360

            angle_with_target = angle_with_target - self.angle

            if angle_with_target != 0:
                if abs(angle_with_target) > 180:
                    if angle_with_target > 0:
                        angle_with_target = -(360 - angle_with_target)
                    else:
                        angle_with_target = 360 + angle_with_target

                if angle_with_target < 0:
                    self.rotate(max(angle_with_target, -self.max_rotate))
                else:
                    self.rotate(min(angle_with_target, self.max_rotate))

                return

        angle = math.atan2(self.motion_vector[1] - self.center[1],
                           self.motion_vector[0] - self.center[0])

        dx = speed * math.cos(angle)
        dy = speed * math.sin(angle)

        self.center[0] += min(dx, abs(self.motion_vector[0] - self.center[0]))
        self.center[1] += min(dy, abs(self.motion_vector[1] - self.center[1]))

    def first_part(self):
        self.get_to()
        self.rotate(self.rotate_vector)

    def second_part(self, list_act):
        act = list_act[:]
        act.remove(self)

        self.search_target(act)

    def third_part(self, chose):
        self.damage()
        self.draw(chose)


test = [Squad(name="warrior", team="s", center=[300, 450], count=[10, 10], speed=1,
              rotate_speed=1, damage=100, cooldown_time=1, angle=0),
        Squad(name="pansers", team="r", center=[400, 450], count=[10, 10], speed=1,
              rotate_speed=1, damage=100, cooldown_time=1, angle=180),
        Squad(name="гыг", team="4", center=[500, 450], count=[10, 10], speed=1,
              rotate_speed=1, damage=100, cooldown_time=1, angle=180),
        Squad(name="пвкпв", team="5", center=[600, 450], count=[10, 10], speed=1,
              rotate_speed=1, damage=100, cooldown_time=1, angle=180),
        Squad(name="сука", team="6", center=[700, 450], count=[10, 10], speed=1,
              rotate_speed=1, damage=100, cooldown_time=1, angle=180),
        ]

chosen_one = test[0] if test else None
num = 0


def sub(chosen_one, num):
    ttt = True
    while ttt:
        win.fill(Color.WHITE)
        mouse_2 = pygame.mouse.get_pos()
        for event_2 in pygame.event.get():
            if event_2.type == pygame.QUIT:
                sys.exit()

            if event_2.type == pygame.KEYDOWN:
                if event_2.key == pygame.K_SPACE:
                    ttt = False

            if event_2.type == pygame.MOUSEBUTTONUP:
                if event_2.button == 1:
                    if chosen_one:
                        chosen_one.motion_vector = list(mouse_2)

                if event_2.button == 3:
                    for i in test:
                        if abs(math.hypot(mouse_2[0] - i.center[0],
                                          mouse_2[1] - i.center[1])) < 50:
                            chosen_one = i
                            break

                if event_2.button == 4:
                    num += 1
                    num %= len(test)
                    chosen_one = test[num]

                if event_2.button == 5:
                    num -= 1
                    num %= len(test)
                    chosen_one = test[num]

        for i in test:
            i.draw(chosen_one)

        pygame.draw.rect(win, Color.BLACK, [0, 450, 1800, 1])
        pygame.draw.rect(win, Color.BLACK, [900, 0, 1, 900])

        pygame.display.flip()
        CLOCK.tick(60)


while True:
    win.fill(Color.WHITE)
    pygame.display.set_caption(str(len(test)) + "  " + str(CLOCK.get_fps()) + "  " + str(test))
    mouse = pygame.mouse.get_pos()
    # click = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()

    for i in test:
        i.first_part()

    for i in test:
        i.second_part(test[:])

    for i in test:
        i.third_part(chosen_one)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sub(chosen_one, num)

            if event.key == pygame.K_UP:
                chosen_one.center[1] -= 1

            if event.key == pygame.K_DOWN:
                chosen_one.center[1] += 1

            if event.key == pygame.K_RIGHT:
                chosen_one.center[0] += 1

            if event.key == pygame.K_LEFT:
                chosen_one.center[0] -= 1

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if chosen_one:
                    chosen_one.motion_vector = list(mouse)

            if event.button == 3:
                chosen_one = None
                for i in test:
                    if abs(math.hypot(mouse[0] - i.center[0],
                                      mouse[1] - i.center[1])) < i.max_distance:
                        chosen_one = i
                        break

            if event.button == 4:
                if chosen_one:
                    chosen_one.rotate(1)
                # num += 1
                # num %= len(test)
                # chosen_one = test[num]

            if event.button == 5:
                if chosen_one:
                    chosen_one.rotate(-1)
                # num -= 1
                # num %= len(test)
                # chosen_one = test[num]

        if key[pygame.K_1]:
            pass

        if key[pygame.K_2]:
            pass

        if key[pygame.K_3]:
            pass

    pygame.draw.rect(win, Color.BLACK, [0, 450, 1800, 1])
    pygame.draw.rect(win, Color.BLACK, [900, 0, 1, 900])

    pygame.display.flip()
    CLOCK.tick(60)

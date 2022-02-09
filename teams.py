# import math
# import random
# import sys
# import copy
# import numpy
# import pygame
#
# pygame.init()
#
#
# class Color:
#     BLACK = (40, 40, 40)
#     WHITE = (215, 215, 215)
#     RED = (200, 50, 50)
#     GREEN = (50, 200, 50)
#     BLUE = (30, 67, 200)
#     YELLOW = (200, 200, 50)
#     GRAY = (125, 125, 125)
#     List_color = ["RED", "BLUE", 'GREEN', 'GRAY']
#
#     @staticmethod
#     def random_color():
#         return random.choice(Color.List_color)
#
#
# width, height = 1800, 900
# win = pygame.display.set_mode((width, height))
# CLOCK = pygame.time.Clock()
# fps = 120
# is_true = True
#
#
# class Patron:
#     def __init__(self, coordinates: [int, int], radius: int, speed: int,
#                  dx: float, dy: float, target):
#         self.coordinates = coordinates
#         self.radius = radius
#         self.speed = speed
#         self.dx = dx + round(random.uniform(-0.1, 0.1), 3)
#         self.dy = dy + round(random.uniform(-0.1, 0.1), 3)
#         self.target = target
#
#         self.color = 0
#
#     def check(self, enemy_list):
#         for i in enemy_list:
#             if (abs(math.hypot(self.coordinates[0] - i.coordinates[0],
#                                self.coordinates[1] - i.coordinates[1])) <
#                     self.radius + i.radius):
#                 i.heals -= 1
#                 # return False
#         if not (width > self.coordinates[0] > 0 and height > self.coordinates[1] > 0):
#             return False
#         return True
#
#     def draw(self):
#         pygame.draw.circle(win, self.color, self.coordinates, self.radius)
#
#     def calculate(self):
#         self.coordinates[0] += self.dx * self.speed
#         self.coordinates[1] += self.dy * self.speed
#
#     def __call__(self):
#         self.calculate()
#
#
# class Warrior:
#     def __init__(self, coordinates: [int, int],
#                  radius: int, heals: int,
#                  attack_distance: int, damage: int,
#                  speed: float):
#         self.coordinates = coordinates
#         self.radius = radius
#         self.heals = heals
#         self.attack_distance = attack_distance
#         self.damage = damage
#         self.speed = speed
#
#         self.color = None
#         self.enemy = None
#         self.patrons = []
#         self.time = 0
#         self.cooldown = 0
#
#         self.neurons = [[random.uniform(-1, 1) for i in range(8)] for t in range(8)]
#
#         self.neurons_2 = [[random.uniform(-1, 1) for i in range(2)] for t in range(8)]
#
#     def calculate_neurons(self, life_time):
#         for i in range(len(self.neurons)):
#             for t in range(len(self.neurons[0])):
#                 w = random.uniform(-1, 1)
#                 c = abs(w)
#                 w = w / abs(w)
#                 while not (10 ** -(life_time + 1)) < c < (10 ** -(life_time - 1)):
#                     if c > 10 ** -(life_time - 1):
#                         # print(f"{grade} > {10 ** -(life_time - 1)}")
#                         c /= 10
#
#                     if c < 10 ** -(life_time + 1):
#                         # print(f"{grade} < {10 ** -(life_time + 1)}")
#                         c *= 10
#                 c *= w
#                 self.neurons[i][t] += c
#
#         for i in range(len(self.neurons_2)):
#             for t in range(len(self.neurons_2[0])):
#                 w = random.uniform(-1, 1)
#                 c = abs(w)
#                 w = w / abs(w)
#                 while not (10 ** -(life_time + 1)) < c < (10 ** -(life_time - 1)):
#                     if c > 10 ** -(life_time - 1):
#                         # print(f"{grade} > {10 ** -(life_time - 1)}")
#                         c /= 10
#
#                     if c < 10 ** -(life_time + 1):
#                         # print(f"{grade} < {10 ** -(life_time + 1)}")
#                         c *= 10
#                 c *= w
#                 self.neurons_2[i][t] += c
#
#     def draw(self):
#         for patron in self.patrons:
#             patron.draw()
#         pygame.draw.circle(win, self.color, self.coordinates, self.radius)
#
#     def search_enemy(self, enemy_list):
#         if not enemy_list:
#             self.enemy = 0
#             return
#         self.enemy = sorted(
#             enemy_list,
#             key=lambda enemy: abs(math.hypot(
#                 enemy.coordinates[0] - self.coordinates[0],
#                 enemy.coordinates[1] - self.coordinates[1])))[0]
#
#     def fire(self):
#         if self.cooldown > 0:
#             return
#         self.cooldown = 30
#         t = math.atan2(self.enemy.coordinates[1] - self.coordinates[1],
#                        self.enemy.coordinates[0] - self.coordinates[0])
#         dx = math.cos(t)
#         dy = math.sin(t)
#         t = Patron(copy.copy(self.coordinates), 3, 15, dx, dy, self.enemy)
#         t.color = self.color
#         self.patrons.append(t)
#
#     def replace(self):
#         angle = math.atan2(self.enemy.coordinates[1] - self.coordinates[1],
#                            self.enemy.coordinates[0] - self.coordinates[0])
#         self.coordinates[0] = math.cos(angle) * self.speed + self.coordinates[0]
#         self.coordinates[1] = math.sin(angle) * self.speed + self.coordinates[1]
#
#     def fire_or_replace(self, enemy_list):
#         self.search_enemy(enemy_list)
#
#         if not self.enemy:
#             return
#         if abs(math.hypot(
#                 self.enemy.coordinates[0] - self.coordinates[0],
#                 self.enemy.coordinates[1] - self.coordinates[1])) > self.attack_distance:
#             self.replace()
#         else:
#             self.fire()
#
#     def __call__(self, enemy_list):
#         if self.cooldown > 0:
#             self.cooldown -= 1
#         for i, patron in enumerate(self.patrons):
#             patron()
#             if not patron.check(enemy_list):
#                 self.patrons = self.patrons[:i] + self.patrons[i + 1:]
#                 continue
#
#         self.time += 1
#         self.fire_or_replace(enemy_list)
#
#     @staticmethod
#     def sigmoid(x):
#         return 1 / (1 + numpy.exp(-x))
#
#     def spawn(self, *inputs):
#         self.calculate_neurons(self.time)
#         coordinates = Warrior.sigmoid(numpy.dot(Warrior.sigmoid(numpy.dot(inputs, self.neurons)), self.neurons_2))
#         coordinates = list(coordinates)
#         angle = coordinates[0] * 360
#         distance = coordinates[1] * 400
#         self.coordinates[0] = math.cos(angle) * distance + 900
#         self.coordinates[1] = math.sin(angle) * distance + 450
#
#
# class Team:
#     def __init__(self, color, warriors: []):
#         self.color = color
#         self.warriors = warriors
#
#         self.count = 0
#
#         for warrior in self.warriors:
#             warrior.color = self.color
#
#     def draw(self):
#         for warrior in self.warriors:
#             warrior.draw()
#
#     def activate_warriors(self, enemy_list):
#         for i, warrior in enumerate(self.warriors):
#             warrior(enemy_list)
#             if warrior.heals <= 0:
#                 self.count += 1
#                 warrior.heals = 150
#
#                 warrior.time = 0
#
#                 x = numpy.mean([i.coordinates[0] for i in team_list[0].warriors])
#                 y = numpy.mean([i.coordinates[1] for i in team_list[0].warriors])
#
#                 x_1 = numpy.mean([i.coordinates[0] for i in team_list[1].warriors])
#                 y_1 = numpy.mean([i.coordinates[1] for i in team_list[1].warriors])
#
#                 x_2 = numpy.mean([i.coordinates[0] for i in team_list[2].warriors])
#                 y_2 = numpy.mean([i.coordinates[1] for i in team_list[2].warriors])
#
#                 x_3 = numpy.mean([i.coordinates[0] for i in team_list[3].warriors])
#                 y_3 = numpy.mean([i.coordinates[1] for i in team_list[3].warriors])
#
#                 warrior.spawn(x, y, x_1, y_1, x_2, y_2, x_3, y_3)
#                 # warrior.dots = [random.randrange(0, width),
#                 #                        random.randrange(0, height)]
#                 # self.warriors = self.warriors[:i] + self.warriors[i + 1:]
#
#     def __call__(self, enemy_list):
#         if is_true:
#             self.activate_warriors(enemy_list)
#         self.draw()
#
#
# team_list = [Team(Color.RED, [Warrior([100, 100], 15, 15, 200, 30, 1)]),
#              Team(Color.BLUE, [Warrior([1700, 100], 15, 15, 200, 30, 1)]),
#              Team(Color.GREEN, [Warrior([100, 800], 15, 15, 200, 30, 1)]),
#              Team(Color.GRAY, [Warrior([1700, 800], 15, 15, 200, 30, 1)])]
#
# while True:
#     win.fill(Color.WHITE)
#     pygame.display.set_caption(f"{str(round(CLOCK.get_fps(), 3))}  {str(round(CLOCK.get_time(), 3))}  "
#                                f"{Color.List_color[0], team_list[0].count}  "
#                                f"{Color.List_color[1], team_list[1].count}  "
#                                f"{Color.List_color[2], team_list[2].count}  "
#                                f"{Color.List_color[3], team_list[3].count}  ")
#     mouse = pygame.mouse.get_pos()
#     click = pygame.mouse.get_pressed()
#     key = pygame.key.get_pressed()
#
#     for event in pygame.event.get():
#
#         if event.type == pygame.QUIT:
#             sys.exit()
#
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 if is_true:
#                     is_true = False
#
#                 elif not is_true:
#                     is_true = True
#
#             if event.key == pygame.K_1:
#                 t = Warrior([mouse[0], mouse[1]], 15, 150,
#                             200, 15, 1)
#                 t.color = team_list[0].color
#                 team_list[0].warriors.append(t)
#
#             if event.key == pygame.K_2:
#                 t = Warrior([mouse[0], mouse[1]], 15, 150,
#                             200, 15, 1)
#                 t.color = team_list[1].color
#                 team_list[1].warriors.append(t)
#
#             if event.key == pygame.K_3:
#                 t = Warrior([mouse[0], mouse[1]], 15, 150,
#                             200, 15, 1)
#                 t.color = team_list[2].color
#                 team_list[2].warriors.append(t)
#
#             if event.key == pygame.K_4:
#                 t = Warrior([mouse[0], mouse[1]], 15, 150,
#                             200, 15, 1)
#                 t.color = team_list[3].color
#                 team_list[3].warriors.append(t)
#
#         if event.type == pygame.MOUSEBUTTONUP:
#             if event.button == 1:
#                 all = team_list[0].warriors + team_list[1].warriors + \
#                       team_list[2].warriors + team_list[3].warriors
#                 for i in range(len(all)):
#                     if math.hypot(all[i].coordinates[0] - mouse[0],
#                                   all[i].coordinates[1] - mouse[1]) <= 150:
#                         all[i].heals = 0
#
#             if event.button == 3:
#                 pass
#
#             if event.button == 4:
#                 pass
#
#             if event.button == 5:
#                 pass
#
#     # print(len(team_list[0].warriors + team_list[1].warriors +
#     #           team_list[2].warriors + team_list[3].warriors))
#     # t = 0
#     # x = 0
#     # for team in team_list:
#     #     t += len(team.warriors)
#     #     for z in team.warriors:
#     #         x += len(z.patrons)
#
#     # print(t, x)
#
#     for team in team_list:
#         enemy_list = []
#         for i in team_list:
#             if i != team:
#                 enemy_list += i.warriors
#         team(enemy_list)
#
#     x = numpy.mean([i.coordinates[0] for i in team_list[0].warriors])
#     y = numpy.mean([i.coordinates[1] for i in team_list[0].warriors])
#     pygame.draw.rect(win, team_list[0].color, [x - 5, y - 5, 10, 10])
#
#     x_1 = numpy.mean([i.coordinates[0] for i in team_list[1].warriors])
#     y_1 = numpy.mean([i.coordinates[1] for i in team_list[1].warriors])
#     pygame.draw.rect(win, team_list[1].color, [x_1 - 5, y_1 - 5, 10, 10])
#
#     x_2 = numpy.mean([i.coordinates[0] for i in team_list[2].warriors])
#     y_2 = numpy.mean([i.coordinates[1] for i in team_list[2].warriors])
#     pygame.draw.rect(win, team_list[2].color, [x_2 - 5, y_2 - 5, 10, 10])
#
#     x_3 = numpy.mean([i.coordinates[0] for i in team_list[3].warriors])
#     y_3 = numpy.mean([i.coordinates[1] for i in team_list[3].warriors])
#     pygame.draw.rect(win, team_list[3].color, [x_3 - 5, y_3 - 5, 10, 10])
#
#     pygame.draw.circle(win, Color.BLACK, mouse, 150, 5)
#     pygame.draw.circle(win, Color.BLACK, [900, 450], 420, 3)
#
#     pygame.display.flip()
#     CLOCK.tick(fps)
string = "dfweewf"


print(string[0: 3] + string[4:])
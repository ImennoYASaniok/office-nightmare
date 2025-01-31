import pygame
from random import shuffle, choice, randint
# from pygame.examples.cursors import image
from pygame.locals import Rect
from collections import deque

from unicodedata import category
THICKNESS_WALL = 30
HEIGHT_WALL = 200
THICKNESS_PARTITION = 10
HEIGHT_PARTITION = 120
DELTA_SIZE_NEAR_OBJECTS = 3
WIDTH_DOOR = 250
UP_WIDTH_DOOR = 150
SPRITES = {
    "comp_size": (200, 125),
    "kuler_size": (40, 140),
    "sofa_size": (200, 100),
    "avtomat_size": (120, 200), # (100, 150)
    "avtomat_y_up": 50,
    'chair_size': (80, 132),
    'clock_size': (40, 40),
    'plant_1_size': (70, 100),
    'plant_2_size': (80, 160),
    "height_dop_table_front": 50,
    'blood_1_size': (70, 70),
    'blood_2_size': (70, 90),
    'blood_3_size': (70, 70),
    'blood_4_size': (70, 70),
    'blood_5_size': (70, 70),
    'bone_1_size': (50, 50),
    'bone_2_size': (50, 50),
    'bone_3_size': (55, 55),
}
BUTTONS = {
    "comp_cord": (77, -5), "comp_size": (83, 47), # (63, 28)
    "avtomat_cord": (10, 23), "avtomat_size": (96, 182),
    "avtomat_green_cord": (15, 33), "avtomat_green_size": (93, 162),
    "tv_ps_cord": (-5, -5), "tv_ps_size": (310, 135),
    "tv_vr_cord": (-5, -5), "tv_vr_size": (110, 60),
    "reception_table_cord": (2, -5), "reception_table_size": (190, 150),
    "color": {
            "inactive": (0, 0, 0, 0), # (0, 0, 0)
            "hover": (200, 208, 200, 200), # (0, 32, 214)
            "pressed": (200, 208, 200),
            "text": (200, 208, 200)
    }
}
# (Пока что двери нет, а имеется ввиду просто проход)
# Размеры двери смотрятся вот так: (------- <- это типо дверь)
#
# Спереди:                                              Cбоку:
#
# WIDTH_DOOR                                   |
#    |                                         | <- WIDTH_DOOR
# ------- <-HEIGHT_DOOR (=THICKNESS_WALL)      |
#                                             /
#                                          HEIGHT_DOOR (=THICKNESS_WALL)
TYPE_AVTOMAT = {
    "green": {"price": 3, "val": 5},
    "yellow": {"price": 6, "val": 10},
    "blue": {"price": 8, "val": 15},
    "type_val":"hp"
}
TYPE_BUTTONS = {
    "color": {
            "inactive": (0, 200, 0, 100), # (0, 0, 0, 0)
            "hover": (200, 208, 200, 200), # (0, 32, 214)
            "pressed": (200, 208, 200),
            "text": (200, 208, 200)
    }
}
ENEMYS = { # Все элементы со значением None или закоменченные ключи, заполняются ниже в коде
    "green_enemy": {
        # "sprite":
        "damage": 5,
        "speed_attack": 8,
        "size": (120, 160),
        "size_rect": (82, 30),
        "speed": [[2, 3], [0, 0]],
    }
}
part_file_path = r"sprites/monster_1" + '/'
def load_CONST():
    ENEMYS["green_enemy"]["sprite"] = {
        "walk": {
            "down": list(map(lambda x: pygame.image.load(part_file_path + "walk/" + f"walk_front_{x}.png").convert_alpha(), range(6))),
            "up": list(map(lambda x: pygame.image.load(part_file_path + "walk/" + f"walk_back_{x}.png").convert_alpha(), range(6))),
            "left": list(map(lambda x: pygame.image.load(part_file_path + "walk/" + f"walk_side_{x}.png").convert_alpha(), range(6))),
            "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path + "walk/" + f"walk_side_{x}.png").convert_alpha(), 1, 0), range(6)))
        },
        "idle": {
            "down": list(
                map(lambda x: pygame.image.load(part_file_path + "idle/" + f"idle_back_{x}.png").convert_alpha(),
                    range(4))),
            "up": list(
                map(lambda x: pygame.image.load(part_file_path + "idle/" + f"idle_front_{x}.png").convert_alpha(),
                    range(4))),
            "left": list(map(lambda x: pygame.transform.flip(
                pygame.image.load(part_file_path + "idle/" + f"idle_side_{x}.png").convert_alpha(), 1, 0),
                             range(4))),
            "right": list(
                map(lambda x: pygame.image.load(part_file_path + "idle/" + f"idle_side_{x}.png").convert_alpha(),
                    range(4)))
        },
        "attack": {
            "down": list(map(lambda x: pygame.image.load(
                part_file_path + "attack/" + f"attack_back_{x}.png").convert_alpha(), range(6))),
            "up": list(map(lambda x: pygame.image.load(
                part_file_path + "attack/" + f"attack_front_{x}.png").convert_alpha(), range(6))),
            "left": list(map(lambda x: pygame.transform.flip(
                pygame.image.load(part_file_path + "attack/" + f"attack_side_{x}.png").convert_alpha(), 1, 0),
                             range(6))),
            "right": list(map(lambda x: pygame.image.load(
                part_file_path + "attack/" + f"attack_side_{x}.png").convert_alpha(), range(6)))
        },
        "hit": {
            "down": list(map(lambda x: pygame.image.load(part_file_path + "hit/" + f"hit_back_{x}.png").convert_alpha(), range(4))),
            "up": list(map(lambda x: pygame.image.load(part_file_path + "hit/" + f"hit_front_{x}.png").convert_alpha(), range(4))),
            "left": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path + "hit/" + f"hit_side_{x}.png").convert_alpha(), 1, 0), range(4))),
            "right": list(map(lambda x: pygame.image.load(part_file_path + "hit/" + f"hit_side_{x}.png").convert_alpha(), range(4)))
        }
    }
    # ENEMYS["boss_wither_enemy"]["sprite"] = {
    #     "walk": {
    #         "down": list(map(lambda x: pygame.image.load(part_file_path + "walk/" + f"walk_front_{x}.png").convert_alpha(), range(6))),
    #         "up": list(map(lambda x: pygame.image.load(part_file_path + "walk/" + f"walk_back_{x}.png").convert_alpha(), range(6))),
    #         "left": list(map(lambda x: pygame.image.load(part_file_path + "walk/" + f"walk_side_{x}.png").convert_alpha(), range(6))),
    #         "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path + "walk/" + f"walk_side_{x}.png").convert_alpha(), 1, 0), range(6)))
    #     },
    #     "idle": {
    #         "down": list(map(lambda x: pygame.image.load(part_file_path + "idle/" + f"idle_back_{x}.png").convert_alpha(), range(4))),
    #         "up": list(map(lambda x: pygame.image.load(part_file_path + "idle/" + f"idle_front_{x}.png").convert_alpha(), range(4))),
    #         "left": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path + "idle/" + f"idle_side_{x}.png").convert_alpha(), 1, 0), range(4))),
    #         "right": list(map(lambda x: pygame.image.load(part_file_path + "idle/" + f"idle_side_{x}.png").convert_alpha(), range(4)))
    #     },
    #     "attack": {
    #         "down": list(map(lambda x: pygame.image.load(part_file_path + "attack/" + f"attack_back_{x}.png").convert_alpha(), range(6))),
    #         "up": list(map(lambda x: pygame.image.load(part_file_path + "attack/" + f"attack_front_{x}.png").convert_alpha(), range(6))),
    #         "left": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path + "attack/" + f"attack_side_{x}.png").convert_alpha(), 1, 0), range(6))),
    #         "right": list(map(lambda x: pygame.image.load(part_file_path + "attack/" + f"attack_side_{x}.png").convert_alpha(), range(6)))
    #     },
    # }



class Object:
    def __init__(self, parent, game, base_style, coords, size, size_button=(0, 0), coords_button=(0, 0), func=None, image=None, size_rect=(0, 20), type_collide="rect"): #absolute_coords_rect=(0, 0)
        self.base_style = base_style
        self.parent = parent
        self.game = game
        self.image = image
        self.func = func

        if size_rect == None:
            size_rect = [0, 0]
        else:
            size_rect = list(size_rect)
            if size_rect != None:
                for i in range(len(size_rect)):
                    if size_rect[i] == 0:
                        size_rect[i] = size[i]
                    elif size_rect[i] < 0:
                        size_rect[i] = size[i] - abs(size_rect[i])
                    else:
                        size_rect[i] = size_rect[i]

        self.data = {
            "color": self.base_style["colors"]["light"],
            "coords": [coords[0], coords[1], size[0], size[1]],  # 50, 70
            "size_rect": size_rect,
            "size_button": size_button, "coords_button": coords_button,
            # "absolute_coords_rect": absolute_coords_rect,
            "type_render": 1, # тип слоя, на котором будет отрисовка
            # "type_collide": type_collide
            # "mask" - коллизия по маске
            # "rect" - коллизия по прямоугольнику
            "flag_func": 0,
            # 0 - не нужно выполнять
            # 1 - нужно выполнять
            "flag_collide": 0,
        }
        if self.image == None:
            self.data["rect"] = Rect(coords[0], coords[1], size[0], size[1])
        else:
            self.data["sprite"] = pygame.image.load(self.image).convert_alpha()
            self.data["sprite"] = pygame.transform.scale(self.data["sprite"], (self.data["coords"][2], self.data["coords"][3]))
            self.data["mask"] = pygame.mask.from_surface(self.data["sprite"])
            self.data["rect"] = self.data["sprite"].get_rect()
        self.set_sprite()

        # Обозначение границ на карте
    def set_object_map(self, name):
        self.game.map.set_object([self.data["rect"].x//self.game.map.rect_cell["size"][0],
                                  self.data["rect"].y//self.game.map.rect_cell["size"][1],
                                  (self.data["rect"].x+self.data["rect"].w)//self.game.map.rect_cell["size"][0], # +1
                                  (self.data["rect"].y+self.data["rect"].h)//self.game.map.rect_cell["size"][1]], # +1
                                 name, [self.data["rect"].x, self.data["rect"].y, self.data["rect"].x+self.data["rect"].w, self.data["rect"].y+self.data["rect"].h])

    def set_sprite(self, coords=None):
        if coords == None:
            self.data["rect"].x = self.data["coords"][0] # + self.data["absolute_coords_rect"][0]
            self.data["rect"].y = self.data["coords"][1] + self.data["coords"][3] - self.data["size_rect"][1] # - self.data["absolute_coords_rect"][1]
            self.data["rect"].w = self.data["size_rect"][0] # self.data["coords"][2]
            self.data["rect"].h = self.data["size_rect"][1] # self.character["coords"][3]
        else:
            self.data["rect"].x = coords[0]  # + self.data["absolute_coords_rect"][0]
            self.data["rect"].y = coords[1] + coords[3] - self.data["size_rect"][1]  # - self.data["absolute_coords_rect"][1]
            self.data["rect"].w = self.data["size_rect"][0]  # self.data["coords"][2]
            self.data["rect"].h = self.data["size_rect"][1]  # self.character["coords"][3]
        # self.data["mask"] = pygame.mask.from_surface(self.data["sprite"])

    def set_rect_to_coords(self):
        self.data["coords"][0] = self.data["rect"].x
        self.data["coords"][1] = self.data["rect"].y - (self.data["coords"][3] - self.data["size_rect"][1])

    def update_sprite(self, image):
        if self.image != None:
            if type(image) == str:
                self.image = image
                self.data["sprite"] = pygame.image.load(self.image).convert_alpha()
            else:
                self.data["sprite"] = image
            self.data["sprite"] = pygame.transform.scale(self.data["sprite"],(self.data["coords"][2], self.data["coords"][3]))
            self.set_sprite()

    def draw(self): # layer
        self.check_click()
        if self.image != None:
            self.game.game_layer.blit(self.data["sprite"], self.data["coords"]) # self.parent.display

    def check_click(self):
        if self.func != None and not self.game.flag_mini_games:
            mouse_pos = pygame.mouse.get_pos()
            rect = Rect(self.game.coords_game_layer[0]+self.data["coords"][0]+self.data["coords_button"][0], self.game.coords_game_layer[1]+self.data["coords"][1]+self.data["coords_button"][1], self.data["coords"][2]+self.data["size_button"][0], self.data["coords"][3]+self.data["size_button"][1])
            # print(rect.x, rect.y, mouse_pos)
            if rect.collidepoint(mouse_pos):
                # Наведение
                self.game.set_rect(layer=self.parent.display, coords=[rect.x, rect.y, rect.w, rect.h], color_base=BUTTONS["color"]["hover"])
                self.data["flag_collide"] = 1
            else:
                self.data["flag_collide"] = 0
            if self.data["flag_collide"] == 1:
                if self.game.val_mouse_state == pygame.MOUSEBUTTONDOWN and self.data["flag_func"] == 1:
                    # Нажатие
                    self.game.set_rect(layer=self.parent.display, coords=[rect.x, rect.y, rect.w, rect.h], color_base=BUTTONS["color"]["pressed"])
                    self.func()
                    self.data["flag_func"] = 0
                elif self.game.val_mouse_state == pygame.MOUSEBUTTONUP:
                    # Выкл нажатие
                    self.data["flag_func"] = 1


class Enemy(Object):
    def __init__(self, parent, game, base_style, category, coords, size, func=None, image=None, size_rect=(0, 20), do_random_spawn=True, do_print=False):
        super().__init__(parent=parent, game=game, base_style=base_style, coords=coords, size=size, func=func, image=image, size_rect=size_rect)
        self.category = category

        # ------- Настройки
        self.do_random_spawn = do_random_spawn
        self.do_print = do_print
        self.do_hide = False

        # ------- Для нахождения кратчайшего путя
        self.way = []
        self.old_way = []
        self.is_start = False

        # ------- Направления и тип
        self.data["dir"] = "down"
        self.data["cond"] = "idle"
        self.data["type_cond"] = ENEMYS[category]["sprite"]
        # print("TYPE_COND:", *self.data["type_cond"].items(), sep="\n")

        # ------- Скорость
        speeds = ENEMYS[category]["speed"][0].copy()
        shuffle(speeds)
        if ENEMYS[category]["speed"][1] == [0] * len(ENEMYS[category]["speed"][1]):
            speed = speeds[0]
        else:
            speed = ENEMYS[category]["speed"][0][ENEMYS[category]["speed"][1].index(min(ENEMYS[category]["speed"][1]))]
        ENEMYS[category]["speed"][1][ENEMYS[category]["speed"][0].index(speed)] += 1
        self.data["speed"] = {"idle": 0, "walk": speed, "attack": 0, "hit": 0} # {"idle": 0, "sneak": 2, "walk": 4, "run": 6}
        self.data["speed_TO_freq"] = {"idle": 20, "walk": 7, "attack": ENEMYS[category]["speed_attack"], "hit": 3} # {"idle": 20, "sneak": 8, "walk": 7, "run": 4}
        self.data["val_speed"] = self.data["speed"][self.data["cond"]]

        # ------- Счётчиков спрайтов
        self.data["number_sprite"] = 0
        self.data["freq_sprite"] = 20
        self.data["counter_sprite"] = 0
        self.data["time_hit"] = 0
        self.data["period_hit"] = 4
        # print(ENEMYS[category]["sprite"])

        # ------- Атака
        self.data["flag_attack"] = 0
        self.test_counter = 0

        # ------- Стандартные данные
        self.data["hp"] = [100, 100]

        # ------- Вывод данных
        self.labels = {}
        self.init_labels()

    def check_random_spawn(self):
        if self.do_random_spawn:
            # print("RANDOM:")
            # print("start:", self.start, self.data["coords"][0], self.data["coords"][1], self.game.map.map[self.start[0]][self.start[1]])
            deltas_coords = [(-1, -1), (0, -1), (1, -1),
                             (-1, 0), (0, 0), (1, 0),
                             (-1, 1), (0, 1), (1, 1)]
            period = []
            for y in range(3, len(self.game.map.map)-3):
                for x in range(3, len(self.game.map.map[0])-3):
                    do_append = True
                    for dx, dy in deltas_coords:
                        if self.game.map.map[y+dy][x+dx] == 1:
                            do_append = False
                            break
                    if do_append:
                        period.append([x, y])
            choice_x, choice_y = choice(period)

            do_1_in = False
            for dx, dy in deltas_coords:
                if self.game.map.map[choice_y + dy][choice_x + dx] == 1:
                    do_1_in = True
                    break
            if do_1_in == False:
                self.data["rect"].x, self.data["rect"].y = choice_x * self.game.map.rect_cell["size"][0], choice_y * self.game.map.rect_cell["size"][1]
                self.set_rect_to_coords()
                # self.set_sprite()
                self.start = self.set_start()

    def init_start(self):
        self.start = self.set_start()
        self.is_start = True

    def set_start(self):
        start = ((self.data["rect"].x) // self.game.map.rect_cell["size"][0] + 1,
                 (self.data["rect"].y) // self.game.map.rect_cell["size"][1])
        return start

    # -------------
    def init_labels(self):
        label_hp = {
            "start_coords": [0, 0],
            "coords": [0, 0],
            "text": f"hp: {self.data["hp"][0]} / {self.data["hp"][1]}",
            "font": pygame.font.Font(self.base_style["font_path"], 20)
        }
        label_hp["label"] = self.parent.label_text(coords=label_hp["coords"],
                                                   text=label_hp["text"],
                                                   font=label_hp["font"],
                                                   color=self.base_style["colors"]["light"],
                                                   type_blit=False)
        self.labels["hp"] = label_hp

    def set_label(self, key, text):
        self.labels[key]["text"] = text
        self.labels[key]["coords"][0] = self.labels[key]["start_coords"][0] + self.data["coords"][0]
        self.labels[key]["coords"][1] = self.labels[key]["start_coords"][1] + self.data["coords"][1]
        self.labels[key]["label"] = self.parent.label_text(coords=self.labels[key]["coords"],
                                                    text=self.labels[key]["text"],
                                                    font=self.labels[key]["font"],
                                                    color=self.base_style["colors"]["light"],
                                                    type_blit=False)
        self.game.game_layer.blit(self.labels[key]["label"], self.labels[key]["coords"])

    def set_labels(self):
        self.set_label("hp", f"hp: {self.data["hp"][0]} / {self.data["hp"][1]}")
    # -------------

    def base_actions(self):
        if self.data["cond"] == "hit":
            if self.data["time_hit"] < self.data["period_hit"]:
                self.data["time_hit"] += 1
            else:
                self.data["cond"] = "idle"
                self.data["time_hit"] = 0
        else:
            self.search_way()
            self.move()
            self.attack()
        self.counting()

    def search_way(self):
        for cell in self.way:
            self.game.map.set_cell(cell[0], cell[1], 0)
        goal = ((self.game.character.character["rect"].x+self.game.character.character["rect"].w//2) // self.game.map.rect_cell["size"][0],
                (self.game.character.character["rect"].y+self.game.character.character["rect"].h//2) // self.game.map.rect_cell["size"][1])

        try:
            self.queue, self.visited = self.game.bfs(start=self.start,
                                                      goal=goal,
                                                      graph=self.game.map.graph)
        except KeyError:
            print('error search way')
            self.start = (len(self.game.map.map[0]) // 2, len(self.game.map.map)//2)
            self.queue, self.visited = self.game.bfs(start=self.start,
                                                     goal=goal,
                                                     graph=self.game.map.graph)
        self.way = []
        path_segment = goal
        # print(path_segment)
        while path_segment and path_segment in self.visited:
            self.way.append(path_segment)
            path_segment = self.visited[path_segment]
        self.way.reverse()
        self.way.append(self.start)


        if len(self.way) <= 2:
            self.way = self.old_way.copy()
            if len(self.old_way) <= 2:
                self.data["cond"] = "attack"
            else:
                self.data["cond"] = "walk"
        else:
            self.data["cond"] = "walk"
        for cell in self.way:
            self.game.map.set_cell(cell[0], cell[1], 2)
            # break
        self.old_way = self.way.copy()
        # print(self.way[0], self.way[1])

    def move(self): # Попробовать: если лево - точка перемещения слева, если право, точка перемещения справа
        dop_coords = self.data["coords"].copy()
        dirs = []
        if self.way[0][0] < self.way[1][0]:
            dirs.append("right")
            dop_coords[0] += self.data["val_speed"]
        elif self.way[0][0] > self.way[1][0]:
            dirs.append("left")
            dop_coords[0] -= self.data["val_speed"]
        self.set_sprite(dop_coords)
        dop_start = self.set_start()
        if dop_start in self.game.map.coords_objects and dirs != []:
            # print("delete:", dirs[-1])
            dirs.pop(-1)

        dop_coords = self.data["coords"].copy()
        if self.way[0][1] > self.way[1][1]:
            dirs.append("up")
            dop_coords[1] -= self.data["val_speed"]
        elif self.way[0][1] < self.way[1][1]:
            dirs.append("down")
            dop_coords[1] += self.data["val_speed"]
        self.set_sprite(dop_coords)
        dop_start = self.set_start()
        if dop_start in self.game.map.coords_objects and dirs != []:
            # print("delete:", dirs[-1])
            dirs.pop(-1)
        # print(dirs, self.way[0][1], self.way[1][1])

        if dirs != []:
            if "right" in dirs:
                self.data["dir"] = "right"
                if self.data["cond"] == "walk": self.data["coords"][0] += self.data["val_speed"]
            elif "left" in dirs:
                self.data["dir"] = "left"
                if self.data["cond"] == "walk": self.data["coords"][0] -= self.data["val_speed"]
            if "up" in dirs:
                self.data["dir"] = "up"
                if self.data["cond"] == "walk": self.data["coords"][1] -= self.data["val_speed"]
            elif "down" in dirs:
                self.data["dir"] = "down"
                if self.data["cond"] == "walk": self.data["coords"][1] += self.data["val_speed"]

    def counting(self):
        if self.data["counter_sprite"] >= self.data["freq_sprite"]:
            if self.data["number_sprite"] >= len(
                    self.data["type_cond"][self.data["cond"]][self.data["dir"]]) - 1:
                self.data["number_sprite"] = 0
            else:
                self.data["number_sprite"] += 1
            self.data["counter_sprite"] = 0
        self.data["counter_sprite"] += 1
        self.data["number_sprite"] = min(self.data["number_sprite"], len(self.data["type_cond"][self.data["cond"]][self.data["dir"]]) - 1)
        self.update_sprite(self.data["type_cond"][self.data["cond"]][self.data["dir"]][self.data["number_sprite"]])
        self.data["val_speed"] = self.data["speed"][self.data["cond"]]
        self.data["freq_sprite"] = self.data["speed_TO_freq"][self.data["cond"]]
        self.start = self.set_start()

        if self.start == self.way[1]:
            self.way.pop(0)
            self.old_way.pop(0)
        # print(self.data["cond"], self.data["dir"], self.data["number_sprite"])

    def attack(self):
        if self.data["cond"] == "attack":
            if self.data["number_sprite"] == 0:
                self.data["flag_attack"] = 1
            if self.data["number_sprite"] == 0 and self.data["flag_attack"]:
                # if self.do_print: print(self.data["flag_attack"], "ATTACK")
                self.game.character.character["hp"][0] -= ENEMYS[self.category]["damage"]
                self.game.character.character["cond"] = "hit"
                self.data["flag_attack"] = 0

    def hit(self, hp, name):
        if self.data["hp"][0] - hp <= 0:
            # print("DEAD")
            self.dead(name)
        else:
            self.data["hp"][0] -= hp
            self.data["cond"] = "hit"
            # print("HP:", self.data["hp"])

    def dead(self, name):
        del self.game.room_now.objects[name]
        self.game.delete_enemys[name] = True
        self.game.character.character["money"][0] += 3
        self.game.set_label("money", f"монеты: {self.game.character.character["money"][0]}")
        # self.data["dead"] = True




class Bullet(Object):
    def __init__(self, parent, game, name, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        # ------ Дополнительные данные
        self.bullet_data = {
            "name": name,
            "speed": 40,
            "dir": "right",
            "delete": 0,
            "damage": 0,
            "type_damage": {
                "pistol": 20
            }
        }
        # -------- Стартовые данные
        start_data = {
            "coords": [
                self.game.character.character["coords"][0] + self.game.character.character["coords"][2] // 2,
                self.game.character.character["coords"][1] + self.game.character.character["coords"][3] // 2,
                7, 14],
            "image": "sprites/bullet.png"
        }

        # -------- Обработка доп данных (перед созданием объекта)
        self.bullet_data["dir"] = {"front": "down", "back": "up", "right": "right", "left": "left"}[self.game.character.character["dir"]]

        if self.bullet_data["dir"] == "right":
            start_data["coords"][0] += self.game.character.character["coords"][2] // 2
        elif self.bullet_data["dir"] == "left":
            start_data["coords"][0] -= self.game.character.character["coords"][2] // 2
        elif self.bullet_data["dir"] == "down":
            start_data["coords"][1] += self.game.character.character["coords"][3] // 2
        elif self.bullet_data["dir"] == "up":
            start_data["coords"][1] -= self.game.character.character["coords"][3] // 2

        for k, v in self.bullet_data["type_damage"].items():
            if k in self.game.character.character["type_weapon"]:
                self.bullet_data["damage"] = v
                break

        # ------ Создание объекта
        super().__init__(parent=parent, game=game, base_style=base_style,
                         image=start_data["image"], coords=[start_data["coords"][0], start_data["coords"][1]],
                         size=(start_data["coords"][2], start_data["coords"][3]),
                         size_rect=(start_data["coords"][2], start_data["coords"][3]))

        # -------- Обработка основных данных (после создания объекта)
        if self.bullet_data["dir"] == "right":
            self.data["sprite"] = pygame.transform.rotate(self.data["sprite"], 90)
        elif self.bullet_data["dir"] == "left":
            self.data["sprite"] = pygame.transform.rotate(self.data["sprite"], 270)
        elif self.bullet_data["dir"] == "down":
            self.data["sprite"] = pygame.transform.rotate(self.data["sprite"], 180)

    def draw(self):
        super().draw()
        self.set_sprite()

    def update(self):
        if self.bullet_data["dir"] == "right": self.data["coords"][0] += self.bullet_data["speed"]
        elif self.bullet_data["dir"] == "left": self.data["coords"][0] -= self.bullet_data["speed"]
        elif self.bullet_data["dir"] == "up": self.data["coords"][1] -= self.bullet_data["speed"]
        elif self.bullet_data["dir"] == "down": self.data["coords"][1] += self.bullet_data["speed"]

        collide_objects = self.game.collide(base_object=self.data,
                                            objects=dict(list(filter(lambda x: "bullet" not in x[0], self.game.room_now.objects.items()))),
                                            draw_rects=False, type_collide="sprite", type_return="objcts")
        if collide_objects != {}:
            name, object = list(collide_objects.items())[0]
            if "enemy" in name:
                object.hit(self.bullet_data["damage"], name)
            self.delete()

    def delete(self):
        self.bullet_data["delete"] = 1





class Level1:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        self.list_rooms = {
            'start_room': Start_room,
            "meeting_room": Meeting_room,
            "final_boss_room": Final_boss_room
        }




class Start_room:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        self.size_room_layer = self.parent.LAYERS["start_room"]
        self.room_layer = pygame.Surface(self.size_room_layer)

        size_hall = [400, 400]
        delta_hall = [0, 0]
        # ------ Пол
        self.floor = pygame.image.load('sprites/floor/floor_start_room.png')
        self.floor_empty_zone = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                       coords=[self.size_room_layer[0] - size_hall[0] + THICKNESS_WALL, size_hall[1] + HEIGHT_WALL],
                                       size=(size_hall[0] - THICKNESS_WALL, self.size_room_layer[1] - size_hall[1] - HEIGHT_WALL),
                                       image=f'sprites/floor_empty_zone.png',
                                       size_rect=(0, 0))
        # ------ Стены
        wall_up = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, 0],
                           size=(self.size_room_layer[0], HEIGHT_WALL),
                           image=f'sprites/walls/wall_red_front.png',
                           size_rect=(0, 0))
        wall_down_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, self.size_room_layer[1]],
                           size=(self.size_room_layer[0], THICKNESS_WALL),
                           image=None, size_rect=(0, 0))
        wall_down_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[self.size_room_layer[0] - size_hall[0] + THICKNESS_WALL, size_hall[1]],
                           size=(size_hall[0] - THICKNESS_WALL, HEIGHT_WALL),
                           image=f'sprites/walls/wall_red_frontdop.png',
                           size_rect=(0, -HEIGHT_WALL + 30))
        wall_left = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, 0],
                           size=(THICKNESS_WALL, self.size_room_layer[1] - HEIGHT_WALL),
                           image=f'sprites/walls/wall_red_top.png',
                           size_rect=(0, 0))
        wall_left_front = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                 coords=[0, self.size_room_layer[1]-HEIGHT_WALL],
                                 size=(THICKNESS_WALL, HEIGHT_WALL),
                                 image=f'sprites/walls/wall_red_front.png',
                                 size_rect=(0, 0))
        wall_right_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[self.size_room_layer[0]-size_hall[0], size_hall[1]],
                              size=(THICKNESS_WALL, self.size_room_layer[1] - size_hall[1] - HEIGHT_WALL),
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, -HEIGHT_WALL+30-DELTA_SIZE_NEAR_OBJECTS))
        wall_right_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                    coords=[self.size_room_layer[0]-size_hall[0], self.size_room_layer[1] - HEIGHT_WALL],
                                    size=(THICKNESS_WALL, HEIGHT_WALL),
                                    image=f'sprites/walls/wall_red_front.png',
                                    size_rect=(0, 0))
        wall_right_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[self.size_room_layer[1] - THICKNESS_WALL, THICKNESS_WALL - DELTA_SIZE_NEAR_OBJECTS],
                              size=(THICKNESS_WALL,  (size_hall[1]-WIDTH_DOOR)//2+delta_hall[1]), #  + THICKNESS_WALL
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, -HEIGHT_WALL + 30 - DELTA_SIZE_NEAR_OBJECTS))
        wall_right_front_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                    coords=[self.size_room_layer[1] - THICKNESS_WALL, THICKNESS_WALL+wall_right_2.data["coords"][3] - DELTA_SIZE_NEAR_OBJECTS],
                                    size=(THICKNESS_WALL, HEIGHT_WALL),
                                    image=f'sprites/walls/wall_red_front.png',
                                    size_rect=(0, 0))
        delta_wall_right_3_x = 30
        wall_right_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[self.size_room_layer[1] - THICKNESS_WALL, THICKNESS_WALL + wall_right_2.data["coords"][ 3] + WIDTH_DOOR - DELTA_SIZE_NEAR_OBJECTS - delta_wall_right_3_x],
                              size=(THICKNESS_WALL, (size_hall[1] - WIDTH_DOOR) // 2 + delta_hall[1] + HEIGHT_WALL),
                              # +100+delta_wall_right_3_x
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, -HEIGHT_WALL + 30))
        # ------ Перегородки
        coords_partition_side_1 = [400, 0]
        partition_side_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                        coords=[THICKNESS_WALL + coords_partition_side_1[0], self.size_room_layer[1] - HEIGHT_PARTITION - coords_partition_side_1[1]],
                                        size=(THICKNESS_PARTITION, HEIGHT_PARTITION),
                                        image='sprites/walls/partition_front.png',
                                        size_rect=(0, 0))
        partition_side_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                  coords=[THICKNESS_WALL + coords_partition_side_1[0], self.size_room_layer[1] - HEIGHT_PARTITION - coords_partition_side_1[1] -partition_side_front_1.data["coords"][3]],
                                  size=(THICKNESS_PARTITION, 150),
                                  image='sprites/walls/partition_top.png',
                                  size_rect=(0, -HEIGHT_PARTITION + 30))
        partition_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                   coords=[THICKNESS_WALL, self.size_room_layer[1] - HEIGHT_PARTITION - partition_side_front_1.data["coords"][3] - 200],
                                   size=(coords_partition_side_1[0] + THICKNESS_PARTITION, HEIGHT_PARTITION),
                                   image='sprites/walls/partition_front.png',
                                   size_rect=(0, -HEIGHT_PARTITION + 30))
        w_partition_front_2 = 350
        y_partition_front_2 = 550
        partition_front_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                   coords=[self.size_room_layer[0] - size_hall[0] - w_partition_front_2, self.size_room_layer[1] - y_partition_front_2],
                                   size=(w_partition_front_2, HEIGHT_PARTITION),
                                   image='sprites/walls/partition_front.png',
                                   size_rect=(0, -HEIGHT_PARTITION + 30))
        partition_side_front_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                  coords=[partition_front_2.data["coords"][0], self.size_room_layer[1] - 100 - HEIGHT_PARTITION],
                                  size=(THICKNESS_PARTITION, HEIGHT_PARTITION),
                                  image='sprites/walls/partition_front.png',
                                  size_rect=(0, 0))
        partition_side_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                  coords=[partition_front_2.data["coords"][0], partition_front_2.data["coords"][1] + THICKNESS_PARTITION - DELTA_SIZE_NEAR_OBJECTS],
                                  size=(THICKNESS_PARTITION, partition_side_front_2.data["coords"][1] - partition_front_2.data["coords"][1]),
                                  image='sprites/walls/partition_top.png',
                                  size_rect=(0, -HEIGHT_PARTITION + 30))
        w_partition_front_3 = 350
        h_partition_side_3 = 250
        partition_front_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                   coords=[THICKNESS_WALL, self.size_room_layer[1] - 1000],
                                   size=(w_partition_front_3, HEIGHT_PARTITION),
                                   image='sprites/walls/partition_front.png',
                                   size_rect=(0, -HEIGHT_PARTITION + 30))
        partition_side_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                  coords=[partition_front_3.data["coords"][0]+partition_front_3.data["coords"][2], partition_front_3.data["coords"][1]],
                                  size=(THICKNESS_PARTITION, h_partition_side_3),
                                  image='sprites/walls/partition_top.png',
                                  size_rect=(0, -HEIGHT_PARTITION + 30))
        partition_side_front_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                        coords=[partition_side_3.data["coords"][0], partition_side_3.data["coords"][1] + partition_side_3.data["coords"][3]],
                                        size=(THICKNESS_PARTITION, HEIGHT_PARTITION),
                                        image='sprites/walls/partition_front.png',
                                        size_rect=(0, 0))
        # ------ Другие объекты
        self.computer_sprites = ['sprites/comp/gaming_comp_1.png', 'sprites/comp/gaming_comp_2.png',
                                 'sprites/comp/gaming_comp_3.png', 'sprites/comp/gaming_comp_4.png',
                                 'sprites/comp/gaming_comp_5.png', 'sprites/comp/gaming_comp_6.png',
                                 'sprites/comp/gaming_comp_7.png', 'sprites/comp/gaming_comp_8.png',
                                 'sprites/comp/gaming_comp_9.png']
        # ------ Комп 1
        coords_computer_1 = [100, 300]
        coords_computer_1 = [THICKNESS_WALL+coords_computer_1[0], self.size_room_layer[1]-SPRITES["comp_size"][1]-coords_computer_1[1]]
        computer_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                            coords=coords_computer_1,
                            size=SPRITES["comp_size"],
                            # +100+delta_wall_right_3_x
                            image=self.computer_sprites[0],
                            func=lambda: self.game.change_game('dino'),
                            size_rect=(0, -100))
        self.sprite_computer_for_1 = [0, 0.1, 8]
        self.sprite_computer_isprite_1 = self.sprite_computer_for_1[0]
        self.sprite_computer_isprite_1_OLD = self.sprite_computer_isprite_1
        # ------ Стул 1
        coords_chair_1 = [80, 20]
        chair_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                            coords=[coords_computer_1[0]+coords_chair_1[0], coords_computer_1[1]+coords_chair_1[1]],
                            size=SPRITES["chair_size"],
                            # +100+delta_wall_right_3_x
                            image="sprites/chair/chair_1.png",
                            size_rect=(0, -100))
        # ------ Комп 2
        coords_computer_2 = [100, 400]
        coords_computer_2 = [self.size_room_layer[0] - size_hall[0] - SPRITES["comp_size"][0] - coords_computer_2[0], self.size_room_layer[1] - SPRITES["comp_size"][1] - coords_computer_2[1]]
        computer_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                            coords=coords_computer_2,
                            size=SPRITES["comp_size"],
                            # +100+delta_wall_right_3_x
                            image=self.computer_sprites[0],
                            func=lambda: self.game.change_game('dash_hex'),
                            size_rect=(0, -100))
        self.sprite_computer_for_2 = [4, 0.2, 8]
        self.sprite_computer_isprite_2 = self.sprite_computer_for_2[0]
        self.sprite_computer_isprite_2_OLD = self.sprite_computer_isprite_2
        # ------ Стул 2
        coords_chair_2 = [40, 20]
        chair_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                         coords=[coords_computer_2[0] + coords_chair_2[0], coords_computer_2[1] + coords_chair_2[1]],
                         size=SPRITES["chair_size"],
                         # +100+delta_wall_right_3_x
                         image="sprites/chair/chair_1.png",
                         size_rect=(0, -100))
        # ------ Комп 3
        coords_computer_3 = [0, 500]
        coords_computer_3 = [THICKNESS_WALL + coords_computer_3[0], THICKNESS_WALL + coords_computer_3[1]]
        computer_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                            coords=coords_computer_3,
                            size=SPRITES["comp_size"],
                            # +100+delta_wall_right_3_x
                            image=self.computer_sprites[0],
                            func=lambda: self.game.change_game('hyper_dash'),
                            size_rect=(0, -100))
        self.sprite_computer_for_3 = [5, 0.1, 8]
        self.sprite_computer_isprite_3 = self.sprite_computer_for_3[0]
        self.sprite_computer_isprite_3_OLD = self.sprite_computer_isprite_3
        # ------ Стул 3
        coords_chair_3 = [40, 20]
        chair_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                         coords=[coords_computer_3[0] + coords_chair_3[0], coords_computer_3[1] + coords_chair_3[1]],
                         size=SPRITES["chair_size"],
                         # +100+delta_wall_right_3_x
                         image="sprites/chair/chair_1.png",
                         size_rect=(0, -100))
        # ------ Доп стол 1
        width_table_1 = 150
        coords_table_front_1 = [20, 0]
        coords_table_front_1 = [self.size_room_layer[0] - size_hall[0] - coords_table_front_1[0] - width_table_1,
                                self.size_room_layer[1] - SPRITES["height_dop_table_front"] - coords_table_front_1[1]]
        table_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                         coords=coords_table_front_1,
                         size=[width_table_1, SPRITES["height_dop_table_front"]],
                         # +100+delta_wall_right_3_x
                         image="sprites/table/table_front.png",
                         size_rect=(0, 0))
        height_table_top_1 = 40
        coords_table_top_1 = [coords_table_front_1[0],
                                coords_table_front_1[1]-height_table_top_1]
        table_top_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                               coords=coords_table_top_1,
                               size=[width_table_1, SPRITES["height_dop_table_front"]],
                               # +100+delta_wall_right_3_x
                               image="sprites/table/table_top.png",
                               size_rect=(0, -height_table_top_1))
        # ------ Растение 1
        coords_plant_1 = [10, 30 + 5]
        coords_plant_1 = [coords_table_top_1[0] + coords_plant_1[0], coords_table_top_1[1] - SPRITES["plant_1_size"][1] + coords_plant_1[1]]
        plant_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                         coords=coords_plant_1,
                         size=SPRITES["plant_1_size"],
                         # +100+delta_wall_right_3_x
                         image="sprites/plant/plant_1.png",
                         size_rect=None)
        # ------ Растение 2
        coords_plant_2 = [0, 30]
        coords_plant_2 = [self.size_room_layer[0] - THICKNESS_WALL - SPRITES["plant_2_size"][0] - coords_plant_2[0],
                          HEIGHT_WALL - SPRITES["plant_2_size"][1] + coords_plant_2[1]]
        plant_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                         coords=coords_plant_2,
                         size=SPRITES["plant_2_size"],
                         # +100+delta_wall_right_3_x
                         image="sprites/plant/plant_2.png",
                         size_rect=(0, 0))
        # ------ Автомат 1
        coords_avtomat_1 = [500, 0]
        coords_avtomat_1 = [THICKNESS_WALL + coords_avtomat_1[0], THICKNESS_WALL + coords_avtomat_1[1]]
        avtomat_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=coords_avtomat_1,
                           size=SPRITES["avtomat_size"],
                           # +100+delta_wall_right_3_x
                           image="sprites/avtomat/avtomat_1.png",
                           func=lambda: self.game.hp_character_up(
                               price=TYPE_AVTOMAT["green"]["price"],
                               val=TYPE_AVTOMAT["green"]["val"], type_val=TYPE_AVTOMAT["type_val"]
                           ),
                           size_button=(-20, -30), coords_button=(10, 30),
                           size_rect=(0, -100))
        coords_avtomat_weapon = [700, 0]
        coords_avtomat_weapon = [THICKNESS_WALL + coords_avtomat_weapon[0], THICKNESS_WALL + coords_avtomat_weapon[1]]
        avtomat_weapon = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=coords_avtomat_weapon,
                           size=SPRITES["avtomat_size"],
                           # +100+delta_wall_right_3_x
                           image="sprites/avtomat/avtomat_weapon.png",
                           func=lambda: self.game.character.give_weapon(
                               type_weapon="give_pistol",
                               price=25,
                           ),
                           size_button=(-20, -30), coords_button=(10, 30),
                           size_rect=(0, -100))
        # ------ Кулер 1
        self.kuler_sprites = ['sprites/kuler/1.png', 'sprites/kuler/2.png', 'sprites/kuler/3.png', 'sprites/kuler/4.png',
                               'sprites/kuler/5.png', 'sprites/kuler/6.png', 'sprites/kuler/7.png', 'sprites/kuler/8.png',
                               'sprites/kuler/9.png']
        coords_kuler_1 = [10, -10]
        coords_kuler_1 = [THICKNESS_WALL + coords_computer_1[0] + SPRITES["comp_size"][0] + coords_kuler_1[0],
                             coords_computer_1[1] + coords_kuler_1[1]]
        kuler_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                            coords=coords_kuler_1,
                            size=SPRITES["kuler_size"],
                            # +100+delta_wall_right_3_x
                            image=self.kuler_sprites[0],
                            size_rect=(0, -100))
        self.sprite_kuler_for_1 = [0, 0.1, 8]
        self.sprite_kuler_isprite_1 = self.sprite_computer_for_1[0]
        self.sprite_kuler_isprite_1_OLD = self.sprite_kuler_isprite_1
        # ------ Кулер 2
        self.kuler_sprites = ['sprites/kuler/1.png', 'sprites/kuler/2.png', 'sprites/kuler/3.png',
                              'sprites/kuler/4.png',
                              'sprites/kuler/5.png', 'sprites/kuler/6.png', 'sprites/kuler/7.png',
                              'sprites/kuler/8.png',
                              'sprites/kuler/9.png']
        coords_kuler_2 = [5, -5]
        coords_kuler_2 = [coords_avtomat_1[0] + SPRITES["avtomat_size"][0] + coords_kuler_2[0],
                          coords_avtomat_1[1] + SPRITES["avtomat_size"][1] - SPRITES["kuler_size"][1] + coords_kuler_2[1]]
        kuler_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                         coords=coords_kuler_2,
                         size=SPRITES["kuler_size"],
                         # +100+delta_wall_right_3_x
                         image=self.kuler_sprites[0],
                         size_rect=(0, -100))
        self.sprite_kuler_for_2 = [2, 0.1, 8]
        self.sprite_kuler_isprite_2 = self.sprite_computer_for_2[0]
        self.sprite_kuler_isprite_2_OLD = self.sprite_kuler_isprite_2
        # ------ Кровь 1
        coords_blood_1 = [0, 30]
        coords_blood_1 = [self.size_room_layer[0] - SPRITES["blood_1_size"][0] - coords_blood_1[0],
                          HEIGHT_WALL + (size_hall[1] - WIDTH_DOOR)//2 + coords_blood_1[1]]
        blood_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                         coords=coords_blood_1,
                         size=SPRITES["blood_1_size"],
                         # +100+delta_wall_right_3_x
                         image="sprites/scary_decor/blood_1.png",
                         size_rect=None)
        # ------ Все объекты
        self.objects = {
            "floor_empty_zone": self.floor_empty_zone,
            # Стены:
            "wall_up": wall_up, "wall_down_1": wall_down_1, "wall_down_2":wall_down_2,
            "wall_left":wall_left, "wall_left_front":wall_left_front,
            "wall_right":wall_right_1, "wall_right_front":wall_right_front_1,
            "wall_right_2": wall_right_2,  "wall_right_front_2": wall_right_front_2, "wall_right_3": wall_right_3,
            # Перегородки:
            "partition_side_1": partition_side_1, "partition_side_front_1": partition_side_front_1, "partition_front_1": partition_front_1,
            "partition_front_2": partition_front_2, "partition_side_front_2": partition_side_front_2, "partition_side_2": partition_side_2,
            "partition_front_3": partition_front_3, "partition_side_front_3": partition_side_front_3, "partition_side_3": partition_side_3,
            # Статичные предметы:
            "computer_1": computer_1, "computer_2": computer_2, "computer_3": computer_3,
            "chair_1": chair_1, "chair_2": chair_2, "chair_3": chair_3,
            "kuler_1": kuler_1, "kuler_2": kuler_2,
            "avtomat_1": avtomat_1, "avtomat_weapon": avtomat_weapon,
            "plant_2": plant_2,
            # Живые объекты:
            # ВАЖНО: Программа отличает живые объекты от статичных по тексту "enemy" в ключу к объекту.
            #        То есть все живые объекты должны создаваться под ключом, в котором будет текст "enemy"!!!
            # (Живые объекты могут создавать for-ом несколько строк ниже)
        }
        # ------ Живые объекты
        load_CONST()
        category_enemy = "green_enemy"
        start_count_enemys = 0
        for i in range(0, self.parent.const["count_enemy"]["curr"][0]):
            green_enemy_i = Enemy(parent=self.parent, game=self.game, base_style=self.base_style,
                                  category=category_enemy,
                                  coords=[200, 200],  # [900, self.size_room_layer[1] - 200], # [700, 500],
                                  size=ENEMYS[category_enemy]["size"],
                                  image='sprites/character/base_choice/idle/idle_front_0.png',
                                  size_rect=ENEMYS[category_enemy]["size_rect"],
                                  do_random_spawn=True)  # do_print=True
            self.objects[f"green_enemy_{i + start_count_enemys}"] = green_enemy_i
        for name, value in self.game.delete_enemys.items():
            if value == True:
                if name in self.objects and "enemy" in name:
                    del self.objects[name]
        # ------------------
        self.dop_objects_up = {
            "blood_1": blood_1
        }
        self.dop_objects_down = {
            "table_front_1": table_front_1, "table_top_1": table_top_1, "plant_1": plant_1
        }
        # ------------------
        doors_right_x = THICKNESS_WALL + self.objects["wall_left_front"].data["coords"][2] + HEIGHT_WALL
        self.doors = {"right": (self.size_room_layer[0], [doors_right_x, doors_right_x + WIDTH_DOOR])}

    def enter_rooms(self):
        self.game.game_layer = self.room_layer
        self.game.coords_game_layer[2] = self.size_room_layer[0]
        self.game.coords_game_layer[3] = self.size_room_layer[1]
        for name, obj in self.objects.items():
            if name not in self.game.delete_enemys and "enemy" in name:
                self.game.delete_enemys[name] = False

    def delete_all(self):
        pass

    def draw(self):
        self.animate_sprite()
        self.game.render_objects() # draw_rects=True
        for name, obj in self.objects.items():
            if "enemy" in name:
                obj.base_actions()
                obj.set_labels()
        if self.game.character.character["absolute_coords_rect"][0] >= self.doors["right"][0] and self.doors["right"][1][0] < self.game.character.character["absolute_coords_rect"][1] < self.doors["right"][1][1]:
            print("start_room -> meeting_room")
            self.game.character.respawn([self.game.character.character["coords"][2], self.parent.display_h // 2])
            self.game.room_change("meeting_room")

    def animate_sprite(self):
        self.sprite_computer_for_1 = self.game.animate_sprite(self.sprite_computer_for_1, reverse=True)
        self.sprite_computer_isprite_1 = int(self.sprite_computer_for_1[0])
        if self.sprite_computer_isprite_1 != self.sprite_computer_isprite_1_OLD:
            self.objects["computer_1"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_1])
        self.sprite_computer_isprite_1_OLD = self.sprite_computer_isprite_1

        self.sprite_computer_for_2 = self.game.animate_sprite(self.sprite_computer_for_2, reverse=True)
        self.sprite_computer_isprite_2 = int(self.sprite_computer_for_2[0])
        if self.sprite_computer_isprite_2 != self.sprite_computer_isprite_2_OLD:
            self.objects["computer_2"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_2])
        self.sprite_computer_isprite_2_OLD = self.sprite_computer_isprite_2

        self.sprite_computer_for_3 = self.game.animate_sprite(self.sprite_computer_for_3, reverse=True)
        self.sprite_computer_isprite_3 = int(self.sprite_computer_for_3[0])
        if self.sprite_computer_isprite_3 != self.sprite_computer_isprite_3_OLD:
            self.objects["computer_3"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_3])
        self.sprite_computer_isprite_3_OLD = self.sprite_computer_isprite_3

        self.sprite_kuler_for_1 = self.game.animate_sprite(self.sprite_kuler_for_1)
        self.sprite_kuler_isprite_1 = int(self.sprite_kuler_for_1[0])
        if self.sprite_kuler_isprite_1 != self.sprite_kuler_isprite_1_OLD:
            self.objects["kuler_1"].update_sprite(self.kuler_sprites[self.sprite_kuler_isprite_1])
        self.sprite_kuler_isprite_1_OLD = self.sprite_kuler_isprite_1

        self.sprite_kuler_for_2 = self.game.animate_sprite(self.sprite_kuler_for_2)
        self.sprite_kuler_isprite_2 = int(self.sprite_kuler_for_2[0])
        if self.sprite_kuler_isprite_2 != self.sprite_kuler_isprite_2_OLD:
            self.objects["kuler_2"].update_sprite(self.kuler_sprites[self.sprite_kuler_isprite_2])
        self.sprite_kuler_isprite_2_OLD = self.sprite_kuler_isprite_2




class Meeting_room:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        self.size_room_layer = self.parent.LAYERS["meeting_room"]  # [3000, 3000]
        self.room_layer = pygame.Surface(self.size_room_layer)
        self.floor = pygame.image.load('sprites/floor/floor_meeting_room.png')
        self.room_layer.blit(self.floor, (0, 0))

        # ------ Проходы
        self.doors = {
            "left": (0, [(self.size_room_layer[1] - WIDTH_DOOR) // 2, (self.size_room_layer[1] + WIDTH_DOOR) // 2 + HEIGHT_WALL]),
            "up": ([(self.size_room_layer[0] - UP_WIDTH_DOOR) // 2, (self.size_room_layer[0] + UP_WIDTH_DOOR) // 2], HEIGHT_WALL // 2)
        }

        # ------ Стены
        wall_up_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, 0],
                           size=(self.doors["up"][0][0], HEIGHT_WALL),
                           image=f'sprites/walls/wall_red_front.png',
                           size_rect=(0, 0))
        wall_up_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[self.doors["up"][0][1], 0],
                           size=(self.doors["up"][0][0], HEIGHT_WALL),
                           image=f'sprites/walls/wall_red_front.png',
                           size_rect=(0, 0))
        wall_down = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, self.size_room_layer[1]],
                           size=(self.size_room_layer[0], THICKNESS_WALL),
                           image=None, size_rect=(0, 0))
        wall_left_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[0, THICKNESS_WALL - DELTA_SIZE_NEAR_OBJECTS],
                              size=(THICKNESS_WALL, (self.parent.display_h - WIDTH_DOOR - HEIGHT_WALL) // 2),
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, 0))
        wall_left_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                    coords=[0, THICKNESS_WALL + wall_left_1.data["coords"][3] - DELTA_SIZE_NEAR_OBJECTS],
                                    size=(THICKNESS_WALL, HEIGHT_WALL),
                                    image=f'sprites/walls/wall_red_front.png',
                                    size_rect=(0, 0))
        delta_wall_left_2_x = 30
        wall_left_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[0, THICKNESS_WALL + wall_left_1.data["coords"][3] + WIDTH_DOOR - DELTA_SIZE_NEAR_OBJECTS - delta_wall_left_2_x],
                              size=(THICKNESS_WALL, (self.parent.display_h - WIDTH_DOOR) // 2),
                              # +100+delta_wall_right_3_x
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, -HEIGHT_WALL + 30))
        wall_left_front_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                             coords=[0, self.size_room_layer[1] - HEIGHT_WALL],
                             size=(THICKNESS_WALL, HEIGHT_WALL),
                             # +100+delta_wall_right_3_x
                             image=f'sprites/walls/wall_red_front.png',
                             size_rect=(0, 0))
        wall_right_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                             coords=[self.size_room_layer[0]-THICKNESS_WALL, THICKNESS_WALL - DELTA_SIZE_NEAR_OBJECTS],
                             size=(THICKNESS_WALL, self.size_room_layer[1] - HEIGHT_WALL - THICKNESS_WALL),
                             image=f'sprites/walls/wall_red_top.png',
                             size_rect=(0, 0))
        wall_right_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                   coords=[wall_right_1.data["coords"][0], wall_right_1.data["coords"][1] + wall_right_1.data["coords"][3]],
                                   size=(THICKNESS_WALL, HEIGHT_WALL + DELTA_SIZE_NEAR_OBJECTS),
                                   image=f'sprites/walls/wall_red_front.png',
                                   size_rect=(0, 0))
        # ------ Автомат 1
        coords_avtomat_1 = [100, 0]
        coords_avtomat_1 = [THICKNESS_WALL + coords_avtomat_1[0], THICKNESS_WALL + coords_avtomat_1[1]]
        avtomat_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=coords_avtomat_1,
                           size=SPRITES["avtomat_size"],
                           # +100+delta_wall_right_3_x
                           image="sprites/avtomat/avtomat_2.png",
                           func=lambda: self.game.hp_character_up(
                               price=TYPE_AVTOMAT["yellow"]["price"],
                               val=TYPE_AVTOMAT["yellow"]["val"], type_val=TYPE_AVTOMAT["type_val"]
                           ),
                           size_button=(-20, -30), coords_button=(10, 30),
                           size_rect=(0, -100))

        # ------------
        self.objects = {
            "wall_up_1": wall_up_1, "wall_up_2": wall_up_2,
            "wall_down": wall_down,
            "wall_left_1":wall_left_1, "wall_left_front_1": wall_left_front_1, "wall_left_2": wall_left_2, "wall_left_front_2": wall_left_front_2,
            "wall_right_1":wall_right_1, "wall_right_front_1": wall_right_front_1,
            "avtomat_1": avtomat_1
        }
        # ------------ Живые объекты
        category_enemy = "green_enemy"
        start_count_enemys = self.parent.const["count_enemy"]["curr"][0]
        for i in range(0, self.parent.const["count_enemy"]["curr"][1]):
            green_enemy_i = Enemy(parent=self.parent, game=self.game, base_style=self.base_style,
                                  category=category_enemy,
                                  coords=[200, 200],  # [900, self.size_room_layer[1] - 200], # [700, 500],
                                  size=ENEMYS[category_enemy]["size"],
                                  image='sprites/character/base_choice/idle/idle_front_0.png',
                                  size_rect=ENEMYS[category_enemy]["size_rect"],
                                  do_random_spawn=True) # do_print=True
            self.objects[f"green_enemy_{i+start_count_enemys}"] = green_enemy_i
        for name, value in self.game.delete_enemys.items():
            if value == True:
                if name in self.objects and "enemy" in name:
                    del self.objects[name]
        # ------------------
        self.dop_objects_up = {}
        self.dop_objects_down = {}
        # ------------ Кровь
        max_blood_w = max(list(map(lambda x: SPRITES[f"blood_{x}_size"][0], range(1, 6))))
        max_blood_h = max(list(map(lambda x: SPRITES[f"blood_{x}_size"][1], range(1, 6))))
        for i in range(6):
            coords_blood_delta = 70
            coords_blood_i = [0, 0]
            coords_blood_i[0] = randint(THICKNESS_WALL + coords_blood_delta, self.size_room_layer[0] - THICKNESS_WALL - max_blood_w - coords_blood_delta)
            coords_blood_i[1] = randint(HEIGHT_WALL + coords_blood_delta, self.size_room_layer[1] - max_blood_h - coords_blood_delta)
            index = choice(list(range(1, 5 + 1)))
            blood_i = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                             coords=coords_blood_i,
                             size=SPRITES[f"blood_{index}_size"],
                             # +100+delta_wall_right_3_x
                             image=f"sprites/scary_decor/blood_{index}.png",
                             size_rect=None)
            self.dop_objects_up[f"blood_{index}"] = blood_i
        # ------------ Кости
        max_bone_w = max(list(map(lambda x: SPRITES[f"bone_{x}_size"][0], range(1, 3+1))))
        max_bone_h = max(list(map(lambda x: SPRITES[f"bone_{x}_size"][1], range(1, 3+1))))
        for i in range(5):
            coords_bone_delta = 70
            coords_bone_i = [0, 0]
            coords_bone_i[0] = randint(THICKNESS_WALL + coords_bone_delta, self.size_room_layer[0] - THICKNESS_WALL - max_bone_w - coords_bone_delta)
            coords_bone_i[1] = randint(HEIGHT_WALL + coords_bone_delta, self.size_room_layer[1] - max_bone_h - coords_bone_delta)
            index = choice(list(range(1, 3+1)))
            if index == 3: size_rect = (0, -8)
            else: size_rect = (0, 15)
            bone_i = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                             coords=coords_bone_i,
                             size=SPRITES[f"bone_{index}_size"],
                             # +100+delta_wall_right_3_x
                             image=f"sprites/scary_decor/bone_{index}.png",
                             size_rect=size_rect)
            self.objects[f"bone_{index}"] = bone_i

    def enter_rooms(self):
        # self.game.floor.blit(self.texture_floor, (0, 0))
        self.game.game_layer = self.room_layer
        self.game.coords_game_layer[2] = self.size_room_layer[0]
        self.game.coords_game_layer[3] = self.size_room_layer[1]
        for name, obj in self.objects.items():
            if name not in self.game.delete_enemys and "enemy" in name:
                self.game.delete_enemys[name] = False

    def delete_all(self):
        pass

    def draw(self):
        self.animate_sprite()
        self.game.render_objects()  # draw_rects=True
        for name, obj in self.objects.items():
            if "enemy" in name:
                obj.base_actions()
                obj.set_labels()
        # print(self.doors["left"][1][0], self.game.character.character["absolute_coords_rect"][1], self.doors["left"][1][1])
        if self.game.character.character["absolute_coords_rect"][0] <= self.doors["left"][0] and self.doors["left"][1][0] < self.game.character.character["absolute_coords_rect"][1] < self.doors["left"][1][1]:
            print("meeting_room -> start_room")
            self.game.character.respawn([self.parent.LAYERS["start_room"][0]-self.game.character.character["coords"][2], self.doors["left"][1][0]])
            self.game.room_change("start_room")
        elif self.doors["up"][0][0] < self.game.character.character["absolute_coords_rect"][0] < self.doors["up"][0][1] and self.game.character.character["absolute_coords_rect"][1] <= self.doors["up"][1]:
            print("meeting_room -> final_boss_room")
            self.game.character.respawn([(self.parent.LAYERS["final_boss_room"][0] - UP_WIDTH_DOOR + self.game.character.character["coords"][2]) // 2, self.parent.LAYERS["final_boss_room"][1] -  self.game.character.character["coords"][3]])
            self.game.room_change("final_boss_room")

    def animate_sprite(self):
        pass




class Final_boss_room:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        self.size_room_layer = self.parent.LAYERS["final_boss_room"]  # [3000, 3000]
        self.room_layer = pygame.Surface(self.size_room_layer)
        self.floor = pygame.transform.rotate(pygame.image.load('sprites/floor/floor_meeting_room.png'), 90)
        self.room_layer.blit(self.floor, (0, 0))

        # ------ Проходы
        self.doors = {
            "up": ([(self.size_room_layer[0] - UP_WIDTH_DOOR) // 2, (self.size_room_layer[0] + UP_WIDTH_DOOR) // 2], HEIGHT_WALL // 2),
            "down": ([(self.size_room_layer[0] - UP_WIDTH_DOOR) // 2, (self.size_room_layer[0] + UP_WIDTH_DOOR) // 2], self.size_room_layer[1])
        }

        # ------ Стены
        wall_up_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, 0],
                           size=(self.doors["up"][0][0], HEIGHT_WALL),
                           image=f'sprites/walls/wall_red_front.png',
                           size_rect=(0, 0))
        wall_up_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[self.doors["up"][0][1], 0],
                           size=(self.doors["up"][0][0], HEIGHT_WALL),
                           image=f'sprites/walls/wall_red_front.png',
                           size_rect=(0, 0))
        wall_down_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, self.size_room_layer[1]],
                           size=(self.doors["down"][0][0], HEIGHT_WALL),
                           image=None, size_rect=(0, 0))
        wall_down_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[self.doors["down"][0][1], self.size_room_layer[1]],
                           size=(self.doors["down"][0][0], HEIGHT_WALL),
                           image=None, size_rect=(0, 0))
        wall_left_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[0, THICKNESS_WALL - DELTA_SIZE_NEAR_OBJECTS],
                              size=(THICKNESS_WALL, self.size_room_layer[1] - HEIGHT_WALL - THICKNESS_WALL),
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, 0))
        wall_left_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                    coords=[wall_left_1.data["coords"][0], wall_left_1.data["coords"][1] + wall_left_1.data["coords"][3]],
                                    size=(THICKNESS_WALL, HEIGHT_WALL + DELTA_SIZE_NEAR_OBJECTS),
                                    image=f'sprites/walls/wall_red_front.png',
                                    size_rect=(0, 0))
        wall_right_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[self.size_room_layer[0] - THICKNESS_WALL, THICKNESS_WALL - DELTA_SIZE_NEAR_OBJECTS],
                              size=(THICKNESS_WALL, self.size_room_layer[1] - HEIGHT_WALL - THICKNESS_WALL),
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, 0))
        wall_right_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                    coords=[wall_right_1.data["coords"][0], wall_right_1.data["coords"][1] + wall_right_1.data["coords"][3]],
                                    size=(THICKNESS_WALL, HEIGHT_WALL + DELTA_SIZE_NEAR_OBJECTS),
                                    image=f'sprites/walls/wall_red_front.png',
                                    size_rect=(0, 0))
        # ------ Дверь 1
        coords_door_1 = [self.doors["up"][0][0],
                            self.doors["up"][1] - HEIGHT_WALL // 2]
        door_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=coords_door_1,
                           size=(UP_WIDTH_DOOR, HEIGHT_WALL),
                           # +100+delta_wall_right_3_x
                           image="sprites/door.png",
                           func=lambda: self.game.set_message("Этот выход. Чтобы выйти убейте всех врагов", delay=1500),
                           # size_button=(-20, -30), coords_button=(10, 30),
                           size_rect=(0, -100))
        # ------ Автомат 1
        coords_avtomat_1 = [20, 0]
        coords_avtomat_1 = [THICKNESS_WALL + coords_avtomat_1[0], self.size_room_layer[1] - coords_avtomat_1[1] - SPRITES["avtomat_size"][1]]
        avtomat_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=coords_avtomat_1,
                           size=SPRITES["avtomat_size"],
                           # +100+delta_wall_right_3_x
                           image="sprites/avtomat/avtomat_3.png",
                           func=lambda: self.game.hp_character_up(
                               price=TYPE_AVTOMAT["blue"]["price"],
                               val=TYPE_AVTOMAT["blue"]["val"], type_val=TYPE_AVTOMAT["type_val"]
                           ),
                           size_button=(-20, -30), coords_button=(10, 30),
                           size_rect=(0, -100))

        # ------------
        self.objects = {
            "wall_up_1": wall_up_1, "wall_up_2": wall_up_2,
            "wall_down_1": wall_down_1, "wall_down_2": wall_down_2,
            "wall_left_1":wall_left_1, "wall_left_front_1": wall_left_front_1,
            "wall_right_1":wall_right_1, "wall_right_front_1": wall_right_front_1,
            "avtomat_1": avtomat_1,
            "DINAMIC_door_1": door_1
        }
        # ------------ Живые объекты
        category_enemy = "green_enemy"
        start_count_enemys = self.parent.const["count_enemy"]["curr"][0] + self.parent.const["count_enemy"]["curr"][1]
        for i in range(0, self.parent.const["count_enemy"]["curr"][2]):
            green_enemy_i = Enemy(parent=self.parent, game=self.game, base_style=self.base_style,
                                  category=category_enemy,
                                  coords=[200, 200],  # [900, self.size_room_layer[1] - 200], # [700, 500],
                                  size=ENEMYS[category_enemy]["size"],
                                  image='sprites/character/base_choice/idle/idle_front_0.png',
                                  size_rect=ENEMYS[category_enemy]["size_rect"],
                                  do_random_spawn=True)  # do_print=True
            self.objects[f"green_enemy_{i + start_count_enemys}"] = green_enemy_i
        for name, value in self.game.delete_enemys.items():
            if value == True:
                if name in self.objects and "enemy" in name:
                    del self.objects[name]

        # category_enemy = "boss_enemy"
        # boss_enemy = Enemy(parent=self.parent, game=self.game, base_style=self.base_style,
        #                       category=category_enemy,
        #                       coords=[200, 200],  # [900, self.size_room_layer[1] - 200], # [700, 500],
        #                       size=ENEMYS[category_enemy]["size"],
        #                       image='sprites/character/base_choice/idle/idle_front_0.png',
        #                       size_rect=ENEMYS[category_enemy]["size_rect"],
        #                       do_random_spawn=True)  # do_print=True
        # self.objects["boss_enemy"] = boss_enemy
        # ------------------
        self.dop_objects_up = {}
        self.dop_objects_down = {}
        # ------------ Кровь
        max_blood_w = max(list(map(lambda x: SPRITES[f"blood_{x}_size"][0], range(1, 6))))
        max_blood_h = max(list(map(lambda x: SPRITES[f"blood_{x}_size"][1], range(1, 6))))
        for i in range(6):
            coords_blood_delta = 70
            coords_blood_i = [0, 0]
            coords_blood_i[0] = randint(THICKNESS_WALL + coords_blood_delta, self.size_room_layer[0] - THICKNESS_WALL - max_blood_w - coords_blood_delta)
            coords_blood_i[1] = randint(HEIGHT_WALL + coords_blood_delta, self.size_room_layer[1] - max_blood_h - coords_blood_delta)
            index = choice(list(range(1, 5 + 1)))
            blood_i = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                             coords=coords_blood_i,
                             size=SPRITES[f"blood_{index}_size"],
                             # +100+delta_wall_right_3_x
                             image=f"sprites/scary_decor/blood_{index}.png",
                             size_rect=None)
            self.dop_objects_up[f"blood_{index}"] = blood_i
        # ------------ Кости
        max_bone_w = max(list(map(lambda x: SPRITES[f"bone_{x}_size"][0], range(1, 3+1))))
        max_bone_h = max(list(map(lambda x: SPRITES[f"bone_{x}_size"][1], range(1, 3+1))))
        for i in range(5):
            coords_bone_delta = 70
            coords_bone_i = [0, 0]
            coords_bone_i[0] = randint(THICKNESS_WALL + coords_bone_delta, self.size_room_layer[0] - THICKNESS_WALL - max_bone_w - coords_bone_delta)
            coords_bone_i[1] = randint(HEIGHT_WALL + coords_bone_delta, self.size_room_layer[1] - max_bone_h - coords_bone_delta)
            index = choice(list(range(1, 3+1)))
            if index == 3: size_rect = (0, -8)
            else: size_rect = (0, 15)
            bone_i = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                             coords=coords_bone_i,
                             size=SPRITES[f"bone_{index}_size"],
                             # +100+delta_wall_right_3_x
                             image=f"sprites/scary_decor/bone_{index}.png",
                             size_rect=size_rect)
            self.objects[f"bone_{index}"] = bone_i

    def enter_rooms(self):
        # self.game.floor.blit(self.texture_floor, (0, 0))
        self.game.game_layer = self.room_layer
        self.game.coords_game_layer[2] = self.size_room_layer[0]
        self.game.coords_game_layer[3] = self.size_room_layer[1]
        for name, obj in self.objects.items():
            if name not in self.game.delete_enemys and "enemy" in name:
                self.game.delete_enemys[name] = False

    def delete_all(self):
        pass

    def draw(self):
        self.animate_sprite()
        self.game.render_objects()  # draw_rects=True

        for name, obj in self.objects.items():
            if "enemy" in name:
                obj.base_actions()
                obj.set_labels()

        # print(self.doors["left"][1][0], self.game.character.character["absolute_coords_rect"][1], self.doors["left"][1][1])
        if self.doors["down"][0][0] < self.game.character.character["absolute_coords_rect"][0] < self.doors["down"][0][1] and self.game.character.character["absolute_coords_rect"][1] >= self.size_room_layer[1]:
            print("final_boss_room -> meeting_room")
            self.game.character.respawn([(self.parent.LAYERS["meeting_room"][0] - UP_WIDTH_DOOR + self.game.character.character["coords"][2]) // 2, self.game.character.character["coords"][3]])
            self.game.room_change("meeting_room")
        elif self.doors["up"][0][0] < self.game.character.character["absolute_coords_rect"][0] < self.doors["up"][0][1] and self.game.character.character["absolute_coords_rect"][1] <= self.doors["up"][1]:
            self.parent.display_change("final", dop_type="victory")

    def animate_sprite(self):
        pass
# import time
# import numpy as np

import pygame
import pygame_widgets

from levels import Level1, Object, Hitbox_Button



class Character:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style
        self.flag_idle = 0
        self.flag_walk = 1

        self.init_shell()
        self.commands = { # если val - list тогда, [(f1, flag1), (f2, flag2)], где 0-ой элемент на нажатие а 1-ый на отпускание,
            pygame.KEYDOWN: {
                (pygame.K_DOWN, pygame.K_s): lambda: self.set_flag("key_down", 1), # lambda: print("character - front"),
                (pygame.K_UP, pygame.K_w): lambda: self.set_flag("key_up", 1), # lambda: print("character - back"),
                (pygame.K_LEFT, pygame.K_a): lambda: self.set_flag("key_left", 1), # lambda: print("character - left"),
                (pygame.K_RIGHT, pygame.K_d): lambda: self.set_flag("key_right", 1), # lambda: print("character - right")
                (pygame.K_RCTRL, pygame.K_LCTRL): lambda: self.set_move("sneak"),
                (pygame.K_RSHIFT, pygame.K_LSHIFT): lambda: self.set_move("run")
            },
            pygame.KEYUP: {
                (pygame.K_DOWN, pygame.K_s): lambda: self.set_flag("key_down", 0),
                (pygame.K_UP, pygame.K_w): lambda: self.set_flag("key_up", 0),
                (pygame.K_LEFT, pygame.K_a): lambda: self.set_flag("key_left", 0),
                (pygame.K_RIGHT, pygame.K_d): lambda: self.set_flag("key_right", 0),
                (pygame.K_RCTRL, pygame.K_LCTRL, pygame.K_RSHIFT, pygame.K_LSHIFT): lambda: self.set_move("walk")
            }
        }
        self.commands = self.parent.format_commands(self.commands)
        #print("CHARACTER: ", self.commands)

    def set_flag(self, key, val):
        self.character["flags"][key] = val
        if self.flag_walk == 1:
            self.set_move("walk")
            self.flag_walk = 0

    def set_move(self, cond):
        if list(self.character["flags"].values()) != [0, 0, 0, 0] or cond == "idle":
            self.character["val_speed"] = self.character["speed"][cond]
            self.character["cond"] = cond
            # print(self.character["cond"])
            self.character["freq_sprite"] = self.character["speed_TO_freq"][cond]


    def respawn(self, coords):
        if coords[0] != None: self.character["coords"][0] = coords[0] - self.character["coords"][2] // 2
        if coords[1] != None: self.character["coords"][1] = coords[1] - self.character["coords"][3] // 2
        self.game.coords_game_layer[0] = -coords[0] + self.parent.display_w // 2
        self.game.coords_game_layer[1] = -coords[1] + self.parent.display_h // 2
        # width, height = self.parent.display_w - self.game.coords_dinamic_zone[0]*2, self.parent.display_h - self.game.coords_dinamic_zone[1]*2
        width, height = abs(self.game.coords_dinamic_zone[0]-self.game.coords_dinamic_zone[2]), abs(self.game.coords_dinamic_zone[1]-self.game.coords_dinamic_zone[3])
        self.game.coords_dinamic_zone[0] = coords[0] - width//2
        self.game.coords_dinamic_zone[1] = coords[1] - height//2
        self.game.coords_dinamic_zone[2] = coords[0] + width//2
        self.game.coords_dinamic_zone[3] = coords[1] + height//2
        for k in self.game.flags_dinamic.keys():
            self.game.flags_dinamic[k] = 0
        self.set_sprite()

    def set_sprite(self):
        self.character["sprite"] = self.character["type_cond"][self.character["cond"]][self.character["dir"]][self.character["number_sprite"]]
        self.character["sprite"] = pygame.transform.scale(self.character["sprite"],(self.character["coords"][2], self.character["coords"][3]))
        self.character["rect"].x = self.character["coords"][0] + self.character["coords_rect"][0]
        self.character["rect"].y = self.character["coords"][1] + self.character["coords"][3] - self.character["coords_rect"][3] - self.character["coords_rect"][1]
        self.character["rect"].w = self.character["coords_rect"][2]
        self.character["rect"].h = self.character["coords_rect"][3] # self.character["coords"][3]
        self.character["absolute_coords_rect"] = (self.character["rect"].x + self.character["rect"].w // 2, self.character["rect"].y + self.character["rect"].h // 2)
        if 1 not in self.game.flags_dinamic.values():
            self.character["coords_display"] = self.character["absolute_coords_rect"]
        # self.character["center_coords"] = (self.character["coords"][0] + self.character["coords"][2]//2, self.character["coords"][1] + self.character["coords"][3]//2)

    def update(self, objects, draw_rects):
        # !!! Если нужно будет, перепишем алгос коллизии в отдельный метод

        # print(set(dir_collides))
        dir_collides = self.game.collide(base_object=self.character, objects=objects, draw_rects=draw_rects)
        flag_change = 0
        flag_changes = {"down": 1, "up": 1, "right": 1, "left": 1}
        if "down" not in dir_collides and self.character["flags"]["key_down"] and flag_changes["down"] == 1:
            self.character["coords"][1] += self.character["val_speed"]
            if self.game.type_dinamic == 0:
                if 1 in self.game.flags_dinamic.values() and self.game.flags_dinamic["up"] != 1:
                    self.game.coords_game_layer[1] -= self.character["val_speed"]
                    self.game.coords_dinamic_zone[3] += self.character["val_speed"]
                    self.game.coords_dinamic_zone[1] += self.character["val_speed"]
                self.game.flags_dinamic["up"] = 0
            elif self.game.type_dinamic == 1:
                self.game.coords_game_layer[1] -= self.character["val_speed"]
            self.character["dir"] = "front"
            flag_changes["down"] = 0
            flag_change, self.flag_idle = 1, 1
        if "up" not in dir_collides and self.character["flags"]["key_up"] and flag_changes["up"] == 1:
            self.character["coords"][1] -= self.character["val_speed"]
            if self.game.type_dinamic == 0:
                if 1 in self.game.flags_dinamic.values() and self.game.flags_dinamic["down"] != 1:
                    self.game.coords_game_layer[1] += self.character["val_speed"]
                    self.game.coords_dinamic_zone[3] -= self.character["val_speed"]
                    self.game.coords_dinamic_zone[1] -= self.character["val_speed"]
                self.game.flags_dinamic["down"] = 0
            elif self.game.type_dinamic == 1:
                self.game.coords_game_layer[1] += self.character["val_speed"]
            self.character["dir"] = "back"
            flag_changes["up"] = 0
            flag_change, self.flag_idle = 1, 1
        if "left" not in dir_collides and self.character["flags"]["key_left"] and flag_changes["left"] == 1:
            self.character["coords"][0] -= self.character["val_speed"]
            if self.game.type_dinamic == 0:
                if 1 in self.game.flags_dinamic.values() and self.game.flags_dinamic["right"] != 1:
                    self.game.coords_game_layer[0] += self.character["val_speed"]
                    self.game.coords_dinamic_zone[2] -= self.character["val_speed"]
                    self.game.coords_dinamic_zone[0] -= self.character["val_speed"]
                self.game.flags_dinamic["right"] = 0
            elif self.game.type_dinamic == 1:
                self.game.coords_game_layer[0] += self.character["val_speed"]
            self.character["dir"] = "left"
            flag_changes["left"] = 0
            flag_change, self.flag_idle = 1, 1
        if "right" not in dir_collides and self.character["flags"]["key_right"] and flag_changes["right"] == 1:
            self.character["coords"][0] += self.character["val_speed"]
            if self.game.type_dinamic == 0:
                if 1 in self.game.flags_dinamic.values() and self.game.flags_dinamic["left"] != 1:
                    self.game.coords_game_layer[0] -= self.character["val_speed"]
                    self.game.coords_dinamic_zone[2] += self.character["val_speed"]
                    self.game.coords_dinamic_zone[0] += self.character["val_speed"]
                self.game.flags_dinamic["left"] = 0
            elif self.game.type_dinamic == 1:
                self.game.coords_game_layer[0] -= self.character["val_speed"]
            self.character["dir"] = "right"
            flag_changes["right"] = 0
            flag_change, self.flag_idle = 1, 1
        if flag_change == 0 and self.flag_idle == 1:
            self.set_move("idle")
            self.flag_idle = 0
            self.flag_walk = 1
            # print(self.character["flags"], self.character["cond"])
        # print(flag_changes)

        if self.character["counter_sprite"] >= self.character["freq_sprite"]:
            if self.character["number_sprite"] >= len(self.character["type_cond"][self.character["cond"]][self.character["dir"]])-1:
                self.character["number_sprite"] = 0
            else:
                self.character["number_sprite"] += 1
            self.character["counter_sprite"] = 0
        self.character["counter_sprite"] += 1
        self.character["number_sprite"] = min(self.character["number_sprite"], len(self.character["type_cond"][self.character["cond"]][self.character["dir"]]) - 1)
        # print(flag_change, self.character["cond"], self.character["freq_sprite"])

        if self.parent.settings_var["character_energy"] == 1:
            # "energy": [70, 20, 100, 1], # текущие, мин, макс, шаг
            # "energy_counter": [0, 10, 20] # текущие, макс для уменьшения, макс для увеличения
            self.character["energy_counter"][0] += 1
            if self.character["cond"] == "run":
                if self.character["energy_counter"][0] >= self.character["energy_counter"][1]:
                    if self.character["energy"][0] > self.character["energy"][1]:
                        self.character["energy"][0] -= self.character["energy"][3]
                    self.character["energy_counter"][0] = 0
            else:
                if self.character["energy_counter"][0] >= self.character["energy_counter"][2]:
                    if self.character["energy"][0] < self.character["energy"][2]:
                        self.character["energy"][0] += self.character["energy"][3]
                    self.character["energy_counter"][0] = 0
            if self.character["energy"][0] == self.character["energy"][1] and self.character["cond"] == "run":
                self.set_move("walk")
            # print(self.character["energy"][0],  self.character["energy_counter"][0])

        self.set_sprite()
        self.draw()  # !!! Для оптиммизации можно добавить основной флаг, который будет отслеживать изменился ли персонаж


    def init_shell(self):
        part_file_path = r"sprites/character/base_choice" + '/'
       # print(part_file_path)
        self.character = {
            "type_cond": {
                # !!! Написать позже отдельную функцию загрузку спрайтов под нужны направления (dir) и cond
                "walk": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_front_{x}.png").convert_alpha(), range(6))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_back_{x}.png").convert_alpha(), range(6))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), range(6))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), 1, 0), range(6)))
                },
                "run": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_front_{x}.png").convert_alpha(), range(6))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_back_{x}.png").convert_alpha(), range(6))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), range(6))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), 1, 0), range(6)))
                },
                "sneak": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_front_{x}.png").convert_alpha(), range(6))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_back_{x}.png").convert_alpha(), range(6))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), range(6))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"walk/"+f"walk_side_{x}.png").convert_alpha(), 1, 0), range(6)))

                },
                "idle": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path+"idle/"+f"idle_front_{x}.png").convert_alpha(), range(5))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path + "idle/" + f"idle_back_{x}.png").convert_alpha(), range(5))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path + "idle/" + f"idle_side_{x}.png").convert_alpha(), range(5))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path+"idle/"+f"idle_side_{x}.png").convert_alpha(), 1, 0), range(5)))
                }
            },
            "flags": {
                "key_down": 0,  # front
                "key_up": 0,  # back
                "key_left": 0,  # left
                "key_right": 0  # right
            },
            "dir" : "front",
            "cond": "idle",
            "number_sprite": 0,
            "freq_sprite": 20,
            "counter_sprite": 0,
            "speed": {"idle": 0, "sneak": 2, "walk": 4, "run": 6},
            "speed_TO_freq": {"idle": 20, "sneak": 8, "walk": 7, "run": 4},
            "val_speed": 4,
            "coords": [self.parent.display_w // 2, self.parent.display_h // 2+100, 100, 140], # 50, 70
            # "center_coords": [0, 0],
            "coords_rect": [7, 0, 82, 20], "absolute_coords_rect": [0, 0], "coords_display": [0, 0],
            "energy": [70, 20, 100, 1], # текущие, мин, макс, шаг
            "energy_counter": [0, 8, 22], # текущие, макс для уменьшения, макс для увеличения
            "hp": [100, 0, 100, 1],  # текущие, мин, макс, шаг
        }
        self.character["sprite"] = self.character["type_cond"][self.character["cond"]][self.character["dir"]][self.character["number_sprite"]]
        self.character["rect"] = self.character["sprite"].get_rect()
        for i in [2, 3]:
            if self.character["coords_rect"][i] == 0:
                self.character["coords_rect"][i] = self.character["coords"][i]
            elif self.character["coords_rect"][i] < 0:
                self.character["coords_rect"][i] = self.character["coords"][i] - abs(self.character["coords_rect"][i])
        #print(self.character)
        self.character["coords"][0] -= self.character["coords"][2] / 2
        self.character["coords"][1] -= self.character["coords"][3] / 2
        for k in self.game.flags_dinamic.keys():
            self.game.flags_dinamic[k] = 0
        self.set_sprite()

    def draw(self):
        # print(self.character["coords"])
        # self.character["rect"] = pygame.Rect(self.character["coords"])
        # Максимально плохая проверка на то что спрайт на вышел за границы
        # if self.character["coords"][0] + self.character["coords"][2] > 1000:
        #     self.character["coords"][0] = 1000 - self.character["coords"][2]
        # if self.character["coords"][1] + self.character["coords"][3] > 800:
        #     self.character["coords"][1] = 800 - self.character["coords"][3]
        # if self.character["coords"][0] < 0:
        #     self.character["coords"][0] = 0
        #     self.character["coords"][0] = 0
        # if self.character["coords"][1] < 0:
        #     self.character["coords"][1] = 0

        self.game.game_layer.blit(self.character["sprite"], self.character["coords"])
        # pygame.draw.rect(self.game.game_layer, self.character["type_cond"][self.character["cond"]][self.character["dir"]], self.character["rect"])




class Game:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent

        # ------ Слои для Hitbox_Button
        self.layer_buttons_1 = pygame.Surface((self.parent.display_w, self.parent.display_h), pygame.SRCALPHA, 32)
        self.layer_buttons_1 = self.layer_buttons_1.convert_alpha()
        self.layer_buttons_2 = pygame.Surface((self.parent.display_w, self.parent.display_h), pygame.SRCALPHA, 32)
        self.layer_buttons_2 = self.layer_buttons_2.convert_alpha()
        self.old_data_layers = []
        self.data_layers = []

        # ------ Уровень
        self.level1 = Level1(self.parent, self, self.base_style)
        # ------ Комната
        self.list_rooms = self.level1.list_rooms
        self.type_room = "start_room" # list(self.list_rooms.keys())[0]  # Здесь указывается первая комната ("start_room")
        self.flag_change_room = 0
        self.room_now = self.list_rooms[self.type_room](self.parent, self, self.base_style)
        # ------ Слой комнаты
        self.game_layer = self.room_now.room_layer
        self.start_spawn = [self.room_now.size_room_layer[0] // 4 + 200, self.room_now.size_room_layer[1] - 100]
        self.coords_game_layer = [0, 0, self.room_now.size_room_layer[0], self.room_now.size_room_layer[1]]
        # ------ Динамическая камера
        self.border_dinamic_zone = [500, 300]
        self.coords_dinamic_zone = [
            self.border_dinamic_zone[0], # x_up
            self.border_dinamic_zone[1], # y_up
            self.parent.display_w - self.border_dinamic_zone[0], # x_down
            self.parent.display_h - self.border_dinamic_zone[1]  # y_down
        ]
        self.start_coords_dinamic_zone = self.coords_dinamic_zone.copy()
        self.flags_dinamic = {
            "up": 0,
            "down": 0,
            "left": 0,
            "right": 0,
        }
        self.type_dinamic = self.parent.settings_var["type_dinamic"]
        self.do_draw_dinamic_zone = self.parent.settings_var["do_draw_dinamic_zone"]
        # значения self.type_dinamic:
        # 0 - динамическая камера с прямоугольной зоной
        # 1 - постоянная динамическая зона
        # ------ Стартовая отрисовка комнаты
        self.room_now.enter_rooms()

        # ------------ Мышка
        self.coords_cursor = pygame.mouse.get_pos()
        self.old_coords_cursor = self.coords_cursor

        # ------ Персонаж
        self.character = Character(self.parent, self, self.base_style)
        self.character.respawn(self.start_spawn)
        self.start2_coords_dinamic_zone = self.coords_dinamic_zone.copy()

        # ------ Команды и горячие клавиши
        self.commands = {
            pygame.KEYDOWN: {
                pygame.K_ESCAPE: lambda: self.parent.display_change("menu"),
                pygame.K_0: lambda: self.parent.display_change("final", dop_type="victory"),
                pygame.K_9: lambda: self.parent.display_change("final", dop_type="fail")
            }
        }
        self.commands = self.parent.format_commands(self.commands)
        # print("GAME: ", self.commands)
        self.list_comands = [self.commands, self.character.commands]

        # ------ Надписи и данные о игре, находящиеся сверху слева
        self.labels = {}
        self.init_labels()
        # ------ Кнопки на экране
        self.buttons = []
        self.init_button_menu()

    def init_labels(self):
        self.labels = {}

        label_fps = {
            "coords": (5, 0),
            "text": f"fps: {self.parent.clock.get_fps():2.0f} / {self.parent.FPS}",
            "font": pygame.font.Font(self.base_style["font_path"], 30)
        }
        label_fps["label"] = self.parent.label_text(coords=label_fps["coords"],
                                                    text=label_fps["text"],
                                                    font=label_fps["font"],
                                                    color=self.base_style["colors"]["light"])
        self.labels["fps"] = label_fps

        label_hp = {
            "coords": (5, 30),
            "text": f"hp: {self.character.character["hp"][0]} / {self.character.character["hp"][2]}",
            "font": pygame.font.Font(self.base_style["font_path"], 30)
        }
        label_hp["label"] = self.parent.label_text(coords=label_hp["coords"],
                                                      text=label_hp["text"],
                                                      font=label_hp["font"],
                                                      color=self.base_style["colors"]["light"])
        self.labels["hp"] = label_hp

        if self.parent.settings_var["character_energy"] == 1:
            label_energy = {
                "coords": (5, 60),
                "text": f"энергия: {self.character.character["energy"][0]} / {self.character.character["energy"][2]}",
                "font": pygame.font.Font(self.base_style["font_path"], 30)
            }
            label_energy["label"] = self.parent.label_text(coords=label_energy["coords"],
                                                       text=label_energy["text"],
                                                       font=label_energy["font"],
                                                       color=self.base_style["colors"]["light"])
            self.labels["energy"] = label_energy

    def set_label(self, key, text):
        self.labels[key]["text"] = text
        self.labels[key]["label"] = self.parent.label_text(coords=self.labels[key]["coords"],
                                                    text=self.labels[key]["text"],
                                                    font=self.labels[key]["font"],
                                                    color=self.base_style["colors"]["light"])

    def init_button_menu(self):
        w, h = 80, 50
        button_ToMenu = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (self.parent.display_w-w, 0, w, h),
            "text": "...",
            "color": {
                "inactive": self.base_style["colors"]["base2"],
                "hover": self.base_style["colors"]["base1"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.display_change('menu')
        }
        button_ToMenu["button"] = self.parent.button(coords=button_ToMenu["coords"],
                                                              text=button_ToMenu["text"],
                                                              color=button_ToMenu["color"],
                                                              font=button_ToMenu["font"],
                                                              func=button_ToMenu["func"])
        self.buttons.append(button_ToMenu)

    def room_change(self, type_room):
        self.type_room = type_room
        self.flag_change_room = 1

    def draw(self):
        # ------ Иницилизация карты, пола
        self.parent.display.fill(self.base_style["colors"]["black"])
        self.parent.display.blit(self.game_layer, (self.coords_game_layer[0], self.coords_game_layer[1]))
        self.game_layer.fill((255, 0, 0))
        self.game_layer.blit(self.room_now.floor, (0, 0))

        # ------ Перемещение карты (динамическая камеры)
        if self.do_draw_dinamic_zone == 1: self.set_dinamic_zone(type_output=1)
        if self.type_dinamic == 0:
            if self.character.character["coords_display"][1] < self.coords_dinamic_zone[1]:
                self.flags_dinamic["up"] = 1
                self.flags_dinamic["down"] = 0
                self.flags_dinamic["left"] = 0
                self.flags_dinamic["right"] = 0
            else: self.flags_dinamic["up"] = 0
            if self.character.character["coords_display"][1] > self.coords_dinamic_zone[3]:
                self.flags_dinamic["up"] = 0
                self.flags_dinamic["down"] = 1
                self.flags_dinamic["left"] = 0
                self.flags_dinamic["right"] = 0
            else: self.flags_dinamic["down"] = 0
            if self.character.character["coords_display"][0] < self.coords_dinamic_zone[0]:
                self.flags_dinamic["up"] = 0
                self.flags_dinamic["down"] = 0
                self.flags_dinamic["left"] = 1
                self.flags_dinamic["right"] = 0
            else: self.flags_dinamic["left"] = 0
            if self.character.character["coords_display"][0] > self.coords_dinamic_zone[2]:
                self.flags_dinamic["up"] = 0
                self.flags_dinamic["down"] = 0
                self.flags_dinamic["left"] = 0
                self.flags_dinamic["right"] = 1
            else: self.flags_dinamic["right"] = 0
        elif self.type_dinamic == 1:
            self.flags_dinamic["up"] = 1
            self.flags_dinamic["down"] = 1
            self.flags_dinamic["left"] = 1
            self.flags_dinamic["right"] = 1

        # ------ Отрисовка всех объектов
        if self.flag_change_room:
            self.flag_change_room = 0
            self.room_now.delete_all()
            self.room_now = self.list_rooms[self.type_room](self.parent, self, self.base_style)
            self.room_now.enter_rooms()
        self.room_now.draw()

        # ------ Вывод значений и данных о игре
        # if self.flag_message_energy == 1: self.set_message()
        for i in self.labels.values(): self.parent.display.blit(i["label"], i["coords"])
        self.set_label("fps", f"fps: {self.parent.clock.get_fps():2.0f} / {self.parent.FPS}")
        # self.set_label("hp", f"hp: {self.character.character["hp"][0]} / {self.character.character["hp"][2]}")
        if self.parent.settings_var["character_energy"] == 1:
            self.set_label("energy", f"энергия: {self.character.character["energy"][0]} / {self.character.character["energy"][2]}")

        # ------ (попробовал - не работает) Обновление кнопок и курсора (нужно было для динмаической камеры)
        # for button in self.room_now.buttons:
        #     button.listen(self.parent.events)
        # pygame_widgets.mouse.Mouse.updateMouseState()
        # self.parent.update_widgets()

        # ------ Мышка
        # self.coords_cursor = pygame.mouse.get_pos()
        # if self.coords_cursor != self.old_coords_cursor:
        #     pygame.mouse.set_pos(self.coords_cursor)
        # pygame_widgets.mouse.Mouse.updateMouseState()
        # self.old_coords_cursor = self.coords_cursor

        # ------ Вывод данных в консоль
        # print("MOUSE", pygame.mouse.get_pos())
        # print(pygame.mouse._get_cursor()) # pygame.mouse.get_pos()

    def set_rect(self, coords, color, layer):
        if len(coords) < 4: raise IndexError("Мало параметров coords, как минимум 4 (x, y, w, h)")
        if len(color) < 3: raise IndexError("Мало параметров RGB цвета color, как минимум 3")
        rect_layer = pygame.Surface((coords[2], coords[3]))
        if len(color) >= 4: rect_layer.set_alpha(color[3])
        rect_layer.fill(color[:3])
        layer.blit(rect_layer, (coords[0], coords[1]))

    def set_dinamic_zone(self, type_output=0):
        if type_output == 1:
            output_flags = list(self.flags_dinamic.values())
            print(f"{output_flags[0]} {int(self.character.character["coords_display"][1] < self.coords_dinamic_zone[1])} {self.character.character["coords_display"][1]}<{self.coords_dinamic_zone[1]}", end=" | ")
            print(f"{output_flags[1]} {int(self.character.character["coords_display"][1] > self.coords_dinamic_zone[3])} {self.character.character["coords_display"][1]}>{self.coords_dinamic_zone[3]}", end=" | ")
            print(f"{output_flags[2]} {int(self.character.character["coords_display"][0] < self.coords_dinamic_zone[0])} {self.character.character["coords_display"][0]}<{self.coords_dinamic_zone[0]}", end=" | ")
            print(f"{output_flags[3]} {int(self.character.character["coords_display"][0] > self.coords_dinamic_zone[2])} {self.character.character["coords_display"][0]}>{self.coords_dinamic_zone[2]}", end=" | ")
            print()
        elif type_output == 2:
            if list(self.flags_dinamic.values())[0] == 0: # up
                print(f"up {self.character.character["coords_display"][1]}<{self.coords_dinamic_zone[1]}")

        self.set_rect(coords=(self.start_coords_dinamic_zone[0],
                              self.start_coords_dinamic_zone[1],
                              self.start_coords_dinamic_zone[2] - self.start_coords_dinamic_zone[0],
                              self.start_coords_dinamic_zone[3] - self.start_coords_dinamic_zone[1]),
                      color=(50, 50, 50, 100), layer=self.parent.display)
        # self.set_rect(coords=(self.start2_coords_dinamic_zone[0],
        #                       self.start2_coords_dinamic_zone[1],
        #                       self.start2_coords_dinamic_zone[2] - self.start2_coords_dinamic_zone[0],
        #                       self.start2_coords_dinamic_zone[3] - self.start2_coords_dinamic_zone[1]),
        #               color=(50, 50, 50, 100), layer=self.game_layer)
        # print((self.coords_dinamic_zone[0],
        #        self.coords_dinamic_zone[1],
        #        self.coords_dinamic_zone[2],
        #        self.coords_dinamic_zone[3]))
        # self.set_rect(coords=(self.coords_dinamic_zone[0],
        #                       self.coords_dinamic_zone[1],
        #                       self.coords_dinamic_zone[2] - self.coords_dinamic_zone[0],
        #                       self.coords_dinamic_zone[3] - self.coords_dinamic_zone[1]),
        #               color=(50, 50, 50, 100), layer=self.game_layer)

    def set_message(self, text, delay=1500):
        label = {
            "coords": (100, 100),
            "text": text,
            "font": pygame.font.Font(self.base_style["font_path"], 50)  # self.base_style["dop_font"]
        }
        label["label"] = self.parent.label_text(coords=label["coords"],
                                                text=label["text"],
                                                font=label["font"],
                                                color=self.base_style["colors"]["light"], type_blit=False)
        label["label"], label["coords"] = self.parent.align(label["label"], label["coords"],
                                            inacurr=-20, type_blit=False, type_align="center")
        bortic = 20
        coords_rect = (label["coords"][0]-bortic,
                       label["coords"][1]-bortic,
                       label["label"].get_width()+bortic,
                       label["label"].get_height()+bortic)
        pygame.draw.rect(self.parent.display, (0, 0, 0), coords_rect) # self.game_layer
        self.parent.display.blit(label["label"], label["coords"]) # self.game_layer
        pygame.display.flip()
        pygame.time.wait(delay)

    def render_objects(self, objects, buttons=None, dop_objects=None, draw_rects=False): # dop_buttons=None,
        if dop_objects is not None: all_objects = objects + dop_objects
        else: all_objects = objects

        # Распределение по слоям
        for obj in objects:
            if self.character.character["rect"].centery > obj.data["rect"].centery:
                obj.data["type_render"] = 1
            else:
                obj.data["type_render"] = 2
        if buttons is not None:
            for i in range(len(buttons)):
                # buttons[i].delete()
                # if i == 1: print(self.character.character["coords"][1], buttons[i].data["coords"][1]-buttons[i].data["coords"][3])
                if self.character.character["coords"][1] > (buttons[i].data["coords"][1]-buttons[i].data["coords"][3]//2):
                    buttons[i].create(self.layer_buttons_1)
                    self.data_layers[i] = 1
                else:
                    buttons[i].create(self.layer_buttons_2)
                    self.data_layers[i] = 2
        # print(self.data_layers)

        # Отрисовка
        if dop_objects is not None:
            for obj in sorted(list(filter(lambda obj: obj.data["type_render"] == 1, dop_objects)), key=lambda obj: (obj.data["rect"].y, obj.data["rect"].h)):
                obj.draw()
        if buttons is not None:
            self.game_layer.blit(self.layer_buttons_1, (0, 0))
        # if dop_buttons is not None:
        #     # c = 85
        #     for dop_but in sorted(list(filter(lambda dop_but: self.character.character["coords"][1] > dop_but.data["coords"][1], dop_buttons)), key=lambda dop_but: (dop_but.data["coords"][1], dop_but.data["coords"][3])):
        #         # print(dop_but.name, end=" ") # .data["coords"][2], dop_but.data["coords"][3]
        #         layer = pygame.Surface((dop_but.data["coords"][2], dop_but.data["coords"][3]), pygame.SRCALPHA, 32).convert_alpha()
        #         # layer = pygame.Surface((dop_but.data["coords"][2], dop_but.data["coords"][3]))
        #         layer.fill((0, 200, 0, 100)) # (c, c, c, 100)
        #         # print(c, end=" ")
        #         # c += 85
        #         dop_but.create(layer)
        #         self.game_layer.blit(layer, (dop_but.data["coords"][0], dop_but.data["coords"][1]))
        #         # layer.fill(pygame.Color(0, 0, 0, 0))
        #     print()
        for obj in sorted(list(filter(lambda obj: obj.data["type_render"] == 1, objects)), key=lambda obj: (obj.data["rect"].y, obj.data["rect"].h)):
            obj.draw()
        self.character.update(all_objects, draw_rects)
        if buttons is not None:
            self.game_layer.blit(self.layer_buttons_2, (0, 0))
        # if dop_buttons is not None:
        #     for dop_but in sorted(list(filter(lambda dop_but: self.character.character["coords"][1] <= dop_but.data["coords"][1], dop_buttons)), key=lambda dop_but: (dop_but.data["coords"][1], dop_but.data["coords"][3])):
        #         layer = pygame.Surface((dop_but.data["coords"][2], dop_but.data["coords"][3]), pygame.SRCALPHA, 32).convert_alpha()
        #         dop_but.create(layer)
        #         self.game_layer.blit(layer, (dop_but.data["coords"][0], dop_but.data["coords"][1]))
        #         layer.fill(pygame.Color(0, 0, 0, 0))
        for obj in sorted(list(filter(lambda obj: obj.data["type_render"] == 2, objects)), key=lambda obj: (obj.data["rect"].y, obj.data["rect"].h)):
            obj.draw()
        # print(self.data_layers, self.old_data_layers)
        if draw_rects:
            for obj in objects + dop_objects:
                pygame.draw.rect(self.game_layer, (255, 255, 255), obj.data["rect"])

        # self.layer_buttons_1.fill(pygame.Color(0, 0, 0, 0))
        # self.layer_buttons_2.fill(pygame.Color(0, 0, 0, 0))
        if buttons is not None:
            if self.data_layers != self.old_data_layers:
                # print("INTO")
                self.layer_buttons_1.fill(pygame.Color(0, 0, 0, 0))
                self.layer_buttons_2.fill(pygame.Color(0, 0, 0, 0))
        self.old_data_layers = self.data_layers.copy()

    def draw_walls(self, color_left, color_up, color_right, thinkess, height, width_door, down="wall"):
        # down="wall" - только стена
        # down="pass" - только проход
        # down="wall, pass" - и стена, и проход
        # down="wall and pass" - и стена, и проход
        # down="wall РАЗДЕЛИТЕЛЬ pass" - и стена, и проход
        # down="passwall" - и стена, и проход
        # ----------------
        # print(color_left, color_up, color_right)
        coords_passage = {}
        walls = {}
        def append(key, obj): walls[key] = obj
        if len(color_up) == 1: # передняя - нет двери
            append("wall_up", Object(self.parent, self, self.base_style, [0, 0],
                      (self.parent.display_w, height), f'sprites/walls/front_{color_up[0]}_wall.png', size_rect=(0, 0)))
        elif len(color_up) == 2: # передняя - есть дверь
            append("wall_up_1", Object(self.parent, self, self.base_style, [0, 0],
                      ((self.parent.display_w-width_door)//2, height), f'sprites/walls/front_{color_up[0]}_wall.png', size_rect=(0, 0)))
            append("wall_up_2", Object(self.parent, self, self.base_style, [(self.parent.display_w+width_door)//2, 0],
                      ((self.parent.display_w+width_door)//2, height), f'sprites/walls/front_{color_up[1]}_wall.png', size_rect=(0, 0)))
            coords_passage["up"] = [[(self.parent.display_w-width_door)//2, (self.parent.display_w+width_door)//2], 0]

        if len(color_left) == 1: # левая - нет двери
            append("wall_left", Object(self.parent, self, self.base_style, [0, 0],
                              (thinkess, self.parent.display_h), f'sprites/walls/side_{color_left[0]}_wall.png', size_rect=(0, 0)))
        elif len(color_left) == 2: # левая - есть стена
            append("wall_left_1", Object(self.parent, self, self.base_style, [0, (self.parent.display_h + width_door) // 2],
                                (thinkess, (self.parent.display_h + width_door) // 2), f'sprites/walls/side_{color_left[0]}_wall.png', size_rect=(0, 0)))
            append("wall_left_2", Object(self.parent, self, self.base_style, [0, 0],
                                (thinkess, (self.parent.display_h-width_door)//2), f'sprites/walls/side_{color_left[1]}_wall.png', size_rect=(0, 0)))
            coords_passage["left"] = [0, [(self.parent.display_h-width_door)//2, (self.parent.display_h+width_door) // 2]]

        if len(color_right) == 1: # правая - нет двери
            append("wall_right", Object(self.parent, self, self.base_style, [self.parent.display_w-thinkess, 0],
                       (thinkess, self.parent.display_h), f'sprites/walls/side_{color_right[0]}_wall.png', size_rect=(0, 0)))
        elif len(color_right) == 2: # правая - есть дверь
            append("wall_right_1", Object(self.parent, self, self.base_style, [self.parent.display_w - thinkess, 0],
                                (thinkess, (self.parent.display_h-width_door)//2), f'sprites/walls/side_{color_right[0]}_wall.png', size_rect=(0, 0)))
            append("wall_right_2", Object(self.parent, self, self.base_style, [self.parent.display_w - thinkess, (self.parent.display_h+width_door)//2],
                                (thinkess, (self.parent.display_h+width_door)//2), f'sprites/walls/side_{color_right[1]}_wall.png', size_rect=(0, 0)))
            coords_passage["right"] = [self.parent.display_w, [(self.parent.display_h - width_door) // 2, (self.parent.display_h + width_door) // 2]]

        # print(down, "wall" in down, "pass" in down)
        if "wall" in down:
            append("wall_down", Object(self.parent, self, self.base_style, [0, self.parent.display_h],
                                        (self.parent.display_w, thinkess),
                                        image=None, size_rect=(0, 0)))
        if "pass" in down:
            coords_passage["down"] = [[(self.parent.display_w-width_door)//2, (self.parent.display_w+width_door)//2], self.parent.display_h-20]
        if len(coords_passage) == 0:
            return walls
        else:
            return walls, coords_passage

    def collide(self, base_object, objects, draw_rects):
        if draw_rects: pygame.draw.rect(self.game_layer, (255, 0, 0), base_object["rect"])
        dir_collides = []
        for obj in objects:
            if base_object["rect"].colliderect(obj.data["rect"]):
                obj_rect = obj.data["rect"]
                collision_area = base_object["rect"].clip(obj_rect)
                if collision_area.width > collision_area.height:
                    if base_object["rect"].centery < obj_rect.centery:
                        dir_collides.append("down")
                    else:
                        dir_collides.append("up")
                else:
                    if base_object["rect"].centerx < obj_rect.centerx:
                        dir_collides.append("right")
                    else:
                        dir_collides.append("left")

        if dir_collides == []: dir_collides = [None]
        dir_collides = list(set(dir_collides))
        return dir_collides

    def animate_sprite(self, for_data, reverse=False):
        for_data[0] += for_data[1]
        # print(for_data[2])
        if for_data[0] > for_data[2] or for_data[0] < 0:
            if reverse:
                for_data[1] = -for_data[1]
                for_data[0] += for_data[1]
            else:
                for_data[0] = 0
        return for_data

    def check_event(self, event):
        for commands in self.list_comands:
            if event.type in commands.keys() and event.key in commands[event.type].keys():
                # print(event.type, event.key)
                commands[event.type][event.key]()

    def delete_all(self):
        # print("GAME ", *list(map(lambda x: x["text"] if "text" in x.keys() else x["texts"], self.buttons)), sep=" ")
        for j in range(len(self.buttons)): del self.buttons[0]
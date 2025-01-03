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
        if coords[0] != None: self.character["coords"][0] = coords[0]
        if coords[1] != None: self.character["coords"][1] = coords[1]

    def set_sprite(self):
        self.character["sprite"] = self.character["type_cond"][self.character["cond"]][self.character["dir"]][self.character["number_sprite"]]
        self.character["sprite"] = pygame.transform.scale(self.character["sprite"],(self.character["coords"][2], self.character["coords"][3]))
        self.character["rect"].x = self.character["coords"][0] + self.character["coords_rect"][0]
        self.character["rect"].y = self.character["coords"][1] + self.character["coords"][3] - self.character["coords_rect"][3] - self.character["coords_rect"][1]
        self.character["rect"].w = self.character["coords_rect"][2]
        self.character["rect"].h = self.character["coords_rect"][3] # self.character["coords"][3]
        self.character["absolute_coords_rect"] = (self.character["rect"].x + self.character["rect"].w // 2, self.character["rect"].y + self.character["rect"].h // 2)
        # self.character["center_coords"] = (self.character["coords"][0] + self.character["coords"][2]//2, self.character["coords"][1] + self.character["coords"][3]//2)

    def update(self, objects, draw_rects):
        # !!! Если нужно будет, перепишем алгос коллизии в отдельный метод

        # print(set(dir_collides))
        self.game.func_collide_other_obj(objects, draw_rects)
        # print(flag_changes)
        if self.character["counter_sprite"] >= self.character["freq_sprite"]:
            if self.character["number_sprite"] >= len(self.character["type_cond"][self.character["cond"]][self.character["dir"]])-1:
                self.character["number_sprite"] = 0
            else:
                self.character["number_sprite"] += 1
            self.character["counter_sprite"] = 0
        self.character["counter_sprite"] += 1
        self.character["number_sprite"] = min(self.character["number_sprite"], len(self.character["type_cond"][self.character["cond"]][self.character["dir"]]) - 1)
        self.set_sprite()
        self.draw() # !!! Для оптиммизации можно добавить основной флаг, который будет отслеживать изменился ли персонаж
        # print(flag_change, self.character["cond"], self.character["freq_sprite"])

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
            "coords_rect": [7, 0, 82, 20],
            "absolute_center_coords_rect": [0, 0]
        }
        self.character["sprite"] = self.character["type_cond"][self.character["cond"]][self.character["dir"]][self.character["number_sprite"]]
        self.character["rect"] = self.character["sprite"].get_rect()
        for i in [2, 3]:
            if self.character["coords_rect"][i] == 0:
                self.character["coords_rect"][i] = self.character["coords"][i]
            elif self.character["coords_rect"][i] < 0:
                self.character["coords_rect"][i] = self.character["coords"][i] - abs(self.character["coords_rect"][i])
        self.set_sprite()
        #print(self.character)
        self.character["coords"][0] -= self.character["coords"][2] / 2
        self.character["coords"][1] -= self.character["coords"][3] / 2

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

        # self.floor.blit(self.default_floor, (0, 0))
        self.parent.display.blit(self.character["sprite"], self.character["coords"])
        # pygame.draw.rect(self.parent.display, self.character["type_cond"][self.character["cond"]][self.character["dir"]], self.character["rect"])




class Game:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent

        self.total_fps = 80
        self.character_hp = 80
        self.character_energy = 30
        self.labels = []
        self.set_labels()

        self.floor = pygame.Surface((self.parent.display_w, self.parent.display_h))

        self.character = Character(self.parent, self, self.base_style)

        self.commands = {
            pygame.KEYDOWN: {
                pygame.K_ESCAPE: lambda: self.parent.display_change("menu"),
                pygame.K_0: lambda: self.parent.display_change("final", dop_type="victory"),
                pygame.K_9: lambda: self.parent.display_change("final", dop_type="fail")
            }
        }
        self.commands = self.parent.format_commands(self.commands)
        #print("GAME: ", self.commands)
        self.list_comands = [self.commands, self.character.commands]

        self.buttons = []
        self.init_button_menu()

        self.layer_buttons_1 = pygame.Surface((self.parent.display_w, self.parent.display_h), pygame.SRCALPHA, 32)
        self.layer_buttons_1 = self.layer_buttons_1.convert_alpha()
        self.layer_buttons_2 = pygame.Surface((self.parent.display_w, self.parent.display_h), pygame.SRCALPHA, 32)
        self.layer_buttons_2 = self.layer_buttons_2.convert_alpha()
        self.old_data_layers = []
        self.data_layers = []

        self.level1 = Level1(self.parent, self, self.base_style)

        self.list_rooms = self.level1.list_rooms
        self.type_room = list(self.list_rooms.keys())[0]
        self.flag_change_room = 0
        self.room_now = self.list_rooms[self.type_room](self.parent, self, self.base_style)
        self.room_now.enter_rooms()
        self.room_now.draw()

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

    def draw(self):
        if self.flag_change_room:
            self.flag_change_room = 0
            self.room_now.delete_all()
            self.room_now = self.list_rooms[self.type_room](self.parent, self, self.base_style)
            self.room_now.enter_rooms()
        self.parent.display.blit(self.floor, (0, 0))
        self.room_now.draw()
        # if self.flag_message_energy == 1: self.set_message()
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])

    def set_labels(self):
        self.labels = []
        label_title = {
            "coords": (30, 0),
            "text": f"FPS: {self.total_fps}",
            "font": pygame.font.Font(self.base_style["font_path"], 30)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                      text=label_title["text"],
                                                      font=label_title["font"],
                                                      color=self.base_style["colors"]["light"])
        #print(label_title["text"])
        self.labels.append(label_title)

        label_title = {
            "coords": (30, 30),
            "text": f"FPS: {self.character_energy}",
            "font": pygame.font.Font(self.base_style["font_path"], 30)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                      text=label_title["text"],
                                                      font=label_title["font"],
                                                      color=self.base_style["colors"]["light"])
        #print(label_title["text"])
        self.labels.append(label_title)

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
        pygame.draw.rect(self.parent.display, (0, 0, 0), coords_rect)
        self.parent.display.blit(label["label"], label["coords"])
        pygame.display.flip()
        pygame.time.wait(delay)

    def render_objects(self, objects, buttons=None, dop_objects=None, draw_rects=False):
        if dop_objects is not None: all_objects = objects + dop_objects
        else: all_objects = objects
        for obj in objects:
            obj.draw()
            if self.character.character["rect"].centery > obj.data["rect"].centery:
                obj.data["type_render"] = 1
            else:
                obj.data["type_render"] = 0
        if buttons is not None:
            for i in range(len(buttons)):
                # buttons[i].delete()
                # if i == 1: print(self.character.character["coords"][1], buttons[i].data["coords"][1]-buttons[i].data["coords"][3])
                if self.character.character["coords"][1] > (buttons[i].data["coords"][1]-buttons[i].data["coords"][3]//2):
                    buttons[i].create(self.layer_buttons_1)
                    self.data_layers[i] = 1
                else:
                    buttons[i].create(self.layer_buttons_2)
                    self.data_layers[i] = 0
        if dop_objects is not None:
            for obj in sorted(list(filter(lambda obj: obj.data["type_render"] == 1, dop_objects)), key=lambda obj: (obj.data["rect"].y, obj.data["rect"].h)):
                obj.draw()
        if buttons is not None:
            self.parent.display.blit(self.layer_buttons_1, (0, 0))
        for obj in sorted(list(filter(lambda obj: obj.data["type_render"] == 1, objects)), key=lambda obj: (obj.data["rect"].y, obj.data["rect"].h)):
            obj.draw()
        self.character.update(all_objects, draw_rects)
        if buttons is not None:
            self.parent.display.blit(self.layer_buttons_2, (0, 0))
        for obj in sorted(list(filter(lambda obj: obj.data["type_render"] == 0, objects)), key=lambda obj: (obj.data["rect"].y, obj.data["rect"].h)):
            obj.draw()
        # print(self.data_layers, self.old_data_layers)
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

    def func_collide_other_obj(self, objects, draw_rects):
        if draw_rects: pygame.draw.rect(self.parent.display, (255, 0, 0), self.character.character["rect"])
        dir_collides = []
        for obj in objects:
            if draw_rects: pygame.draw.rect(self.parent.display, (255, 255, 255), obj.data["rect"])
            if self.character.character["rect"].colliderect(obj.data["rect"]):
                obj_rect = obj.data["rect"]
                collision_area = self.character.character["rect"].clip(obj_rect)
                if collision_area.width > collision_area.height:
                    if self.character.character["rect"].centery < obj_rect.centery:
                        dir_collides.append("down")
                    else:
                        dir_collides.append("up")
                else:
                    if self.character.character["rect"].centerx < obj_rect.centerx:
                        dir_collides.append("right")
                    else:
                        dir_collides.append("left")

        if dir_collides == []: dir_collides = [None]
        dir_collides = list(set(dir_collides))
        flag_change = 0
        flag_changes = {"down": 1, "up": 1, "right": 1, "left": 1}
        if "down" not in dir_collides and self.character.character["flags"]["key_down"] and flag_changes["down"] == 1:
            self.character.character["coords"][1] += self.character.character["val_speed"]
            self.character.character["dir"] = "front"
            flag_changes["down"] = 0
            flag_change, self.character.flag_idle = 1, 1
        if "up" not in dir_collides and self.character.character["flags"]["key_up"] and flag_changes["up"] == 1:
            self.character.character["coords"][1] -= self.character.character["val_speed"]
            self.character.character["dir"] = "back"
            flag_changes["up"] = 0
            flag_change, self.character.flag_idle = 1, 1
        if "left" not in dir_collides and self.character.character["flags"]["key_left"] and flag_changes["left"] == 1:
            self.character.character["coords"][0] -= self.character.character["val_speed"]
            self.character.character["dir"] = "left"
            flag_changes["left"] = 0
            flag_change, self.character.flag_idle = 1, 1
        if "right" not in dir_collides and self.character.character["flags"]["key_right"] and flag_changes["right"] == 1:
            self.character.character["coords"][0] += self.character.character["val_speed"]
            self.character.character["dir"] = "right"
            flag_changes["right"] = 0
            flag_change, self.character.flag_idle = 1, 1
        if flag_change == 0 and self.character.flag_idle == 1:
            self.character.set_move("idle")
            self.character.flag_idle = 0
            self.character.flag_walk = 1
            # print(self.character["flags"], self.character["cond"])

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

    def energy_character_up(self, price, val):
        if self.donats_many - price >= 0:
            self.donats_many -= price
            self.character_energy += val
        else:
            self.set_message(f"Не хватает денег, нужно монет: {price} ")
        self.set_labels()

    def check_event(self, event):
        for commands in self.list_comands:
            if event.type in commands.keys() and event.key in commands[event.type].keys():
                print(event.type, event.key)
                commands[event.type][event.key]()

    def delete_all(self):
        # print("GAME ", *list(map(lambda x: x["text"] if "text" in x.keys() else x["texts"], self.buttons)), sep=" ")
        for j in range(len(self.buttons)): del self.buttons[j]
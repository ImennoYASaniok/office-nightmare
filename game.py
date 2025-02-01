import pygame
from collections import deque

from levels import Level1, Object, Bullet
from mini_games.dino import dino_game
from mini_games.circle import curcle
from mini_games.dash_hex import dash_hex


class Character:
    def __init__(self, parent, game, base_style):
        self.character = None
        self.parent = parent
        self.game = game
        self.base_style = base_style
        self.flag_idle = 0
        self.flag_walk = 1

        self.init_shell()
        self.commands = { # если val - list тогда, [(f1, flag1), (f2, flag2)], где 0-ой элемент на нажатие а 1-ый на отпускание,
            pygame.KEYDOWN: {
                (pygame.K_DOWN, pygame.K_s): lambda: self.set_flag("key_down", 1),
                (pygame.K_UP, pygame.K_w): lambda: self.set_flag("key_up", 1),
                (pygame.K_LEFT, pygame.K_a): lambda: self.set_flag("key_left", 1),
                (pygame.K_RIGHT, pygame.K_d): lambda: self.set_flag("key_right", 1),
                (pygame.K_SPACE, pygame.K_RETURN): lambda: self.set_flag("key_space", 1),
                (pygame.K_RCTRL, pygame.K_LCTRL): lambda: self.set_move("sneak"),
                (pygame.K_RSHIFT, pygame.K_LSHIFT): lambda: self.set_move("run"),
                pygame.K_1: lambda: self.set_type_weapon(1),
                pygame.K_2: lambda: self.set_type_weapon(2),
                pygame.K_3: lambda: self.set_type_weapon(3),
            },
            pygame.KEYUP: {
                (pygame.K_DOWN, pygame.K_s): lambda: self.set_flag("key_down", 0),
                (pygame.K_UP, pygame.K_w): lambda: self.set_flag("key_up", 0),
                (pygame.K_LEFT, pygame.K_a): lambda: self.set_flag("key_left", 0),
                (pygame.K_RIGHT, pygame.K_d): lambda: self.set_flag("key_right", 0),
                # (pygame.K_SPACE, pygame.K_RETURN): lambda: self.set_flag("key_space", 0),
                (pygame.K_RCTRL, pygame.K_LCTRL, pygame.K_RSHIFT, pygame.K_LSHIFT): lambda: self.set_move("walk")
            }
        }
        self.commands = self.parent.format_commands(self.commands)

    def init_shell(self):
        part_file_path = r"sprites/character" + '/'
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
                },
                "hit": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path + "hit/" + f"hit_front_{x}.png").convert_alpha(), range(5))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path + "hit/" + f"hit_back_{x}.png").convert_alpha(), range(5))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path + "hit/" + f"hit_side_{x}.png").convert_alpha(), range(5))),
                    "right": list(map(lambda x: pygame.transform.flip( pygame.image.load(part_file_path + "hit/" + f"hit_side_{x}.png").convert_alpha(), 1, 0), range(5)))
                },
                "attack": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path + "attack/" + f"attack_front_{x}.png").convert_alpha(), range(3))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path + "attack/" + f"attack_back_{x}.png").convert_alpha(), range(3))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path + "attack/" + f"attack_side_{x}.png").convert_alpha(), range(3))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path + "attack/" + f"attack_side_{x}.png").convert_alpha(), 1, 0), range(3)))
                },
                "shoot_pistol": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path + "shoot_pistol/" + f"shoot_pistol_front.png").convert_alpha(), range(1))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path + "shoot_pistol/" + f"shoot_pistol_back.png").convert_alpha(), range(1))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path + "shoot_pistol/" + f"shoot_pistol_side.png").convert_alpha(), range(1))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path + "shoot_pistol/" + f"shoot_pistol_side.png").convert_alpha(), 1, 0), range(1)))
                },
                "shoot_automat": {
                    "front": list(map(lambda x: pygame.image.load(part_file_path + "shoot_automat/" + f"shoot_automat_front.png").convert_alpha(), range(1))),
                    "back": list(map(lambda x: pygame.image.load(part_file_path + "shoot_automat/" + f"shoot_automat_back.png").convert_alpha(), range(1))),
                    "left": list(map(lambda x: pygame.image.load(part_file_path + "shoot_automat/" + f"shoot_automat_side.png").convert_alpha(), range(1))),
                    "right": list(map(lambda x: pygame.transform.flip(pygame.image.load(part_file_path + "shoot_automat/" + f"shoot_automat_side.png").convert_alpha(),1, 0), range(1)))
                }
            },
            "flags": {
                "key_down": 0,  # front
                "key_up": 0,  # back
                "key_left": 0,  # left
                "key_right": 0,  # right
                "key_space": 0  # right
            },
            "dir" : "front",
            "cond": "idle", "old_cond": "idle", "dop_old_cond": "walk",
            "number_sprite": 0,
            "freq_sprite": 20,
            "counter_sprite": 0,
            "speed": {"idle": 0, "sneak": 2, "walk": 4, "run": 5, "attack": 0, "hit": 0, "shoot_pistol": 0, "shoot_automat": 0},
            "speed_TO_freq": {"idle": 20, "sneak": 8, "walk": 7, "run": 4, "attack": 8, "hit": 0, "shoot_pistol": 0, "shoot_automat": 0},
            "val_speed": 4,
            "coords": [self.parent.display_w // 2, self.parent.display_h // 2+100, 100, 140], # 50, 70
            # "center_coords": [0, 0],
            "coords_rect": [7, 0, 82, 20], "absolute_coords_rect": [0, 0], "coords_display": [0, 0],
            "energy": [70, 0, 100, 1], # текущие, мин, макс, шаг
            "energy_counter": [0, 10, 15], # текущие, макс для уменьшения, макс для увеличения
            "hp": [100, 0, 100, 1],  # текущие, мин, макс, шаг
            "money": [40, 0], # текущие, мин # [30, 0]
            "time_hit": 0, "period_hit": 4,
            "time_attack": 0, "period_attack": None,
            "delta_coords_attack": [0, -20],
            # ------- Оружие
            "damage": {
                "arms": 10,
                "pistol": 35,
                "automat": 15,
            },
            "type_weapon": "arms",
            # клавиша 1 - "arms" - руки
            # клавиша 2 - "pistol" - пистолет
            "counter_bullet": 0,
            "bullets": {  # текущие, в обоиме
                "arms": None,
                "pistol": [0, 30],
                "automat": [0, 80]
            },
            "bullets_price": {
                "pistol": [5, 1],
                "automat": [10, 2],
            },
            "shoot1_counter_bullets": {
                "pistol": [0, 1],
                "automat": [0, 5]
            }
        }
        self.character["period_attack"] = self.character["speed_TO_freq"]["attack"] + 1

        self.character["sprite"] = self.character["type_cond"][self.character["cond"]][self.character["dir"]][self.character["number_sprite"]]
        self.character["rect"] = self.character["sprite"].get_rect()

        for i in [2, 3]:
            if self.character["coords_rect"][i] == 0:
                self.character["coords_rect"][i] = self.character["coords"][i]
            elif self.character["coords_rect"][i] < 0:
                self.character["coords_rect"][i] = self.character["coords"][i] - abs(self.character["coords_rect"][i])
        self.character["coords"][0] -= self.character["coords"][2] / 2
        self.character["coords"][1] -= self.character["coords"][3] / 2

        for k in self.game.flags_dinamic.keys():
            self.game.flags_dinamic[k] = 0

        self.set_sprite()

        delta_size = {
            "attack": {
                "right": (40, 10),
                "left": (40, 10),
                "front": (40, 30),
                "back": (40, 30),
            },
            "shoot_automat": {
                "right": (int(self.character["coords"][2]*0.5), 0),
                "left": (int(self.character["coords"][2]*0.5), 0),
            }
        }
        for cond in self.character["type_cond"].keys():
            if cond not in delta_size.keys():
                delta_size[cond] = {}
            for key in self.character["type_cond"][cond].keys():
                if key not in delta_size[cond].keys():
                    delta_size[cond][key] = (0, 0)
        # print("delta_size:", delta_size)
        for name_cond in self.character["type_cond"].keys():
            for name_dir, key in self.character["type_cond"][name_cond].items():
                self.character["type_cond"][name_cond][name_dir] = list(map(lambda x: pygame.transform.scale(x, (self.character["coords"][2] + delta_size[name_cond][name_dir][0], self.character["coords"][3] + delta_size[name_cond][name_dir][1])), self.character["type_cond"][name_cond][name_dir]))

    def set_flag(self, key, val):
        self.character["flags"][key] = val
        if key == "key_space":
            if self.character["type_weapon"] == "arms" and self.character["cond"] != "attack":
                self.set_move("attack")
            elif self.character["type_weapon"] == "pistol" and self.character["cond"] != "shoot_pistol" and self.character["bullets"]["pistol"][0] > 0:
                self.set_move("shoot_pistol")
            elif self.character["type_weapon"] == "automat" and self.character["cond"] != "shoot_automat" and self.character["bullets"]["automat"][0] > 0:
                self.set_move("shoot_automat")
        elif key in ("key_right", "key_left", "key_down", "key_up"):
            self.set_move(self.character["dop_old_cond"])
        else:
            if self.flag_walk == 1:
                self.set_move(self.character["old_cond"])
                self.flag_walk = 0

    def set_type_weapon(self, key_press):
        self.character["type_weapon"] = ["arms", "pistol", "automat"][key_press-1]

    def translate_name_weapon(self):
        if self.character["type_weapon"] == "pistol":
            return "пистолет"
        elif self.character["type_weapon"] == "automat":
            return "автомат"
        elif self.character["type_weapon"] == "arms":
            return "руки"
        else:
            return None

    def give_weapon(self):
        type_weapon = self.character["type_weapon"]
        print_type = self.translate_name_weapon()
        if print_type in (None, "руки"):
            self.game.set_message("Выбрано оружие, у которого нет обоим и пуль ", delay=2000)
            return None
        need_money = self.character['bullets_price'][type_weapon][0]
        need_bullets = need_money * self.character['bullets_price'][type_weapon][1]
        need_money = int(need_money)
        need_bullets = int(need_bullets)
        # print("GIVE BULLETS: ", need_bullets, need_money)
        if self.character["bullets"][type_weapon][0] + need_bullets > self.character["bullets"][type_weapon][1]: self.game.set_message(f"Больше нельзя получить обоим для {print_type}", delay=1000)
        elif self.character["money"][0] < need_money: self.game.set_message(f"Не хватает денег, на обоиму для {print_type}, 1 обоима = {need_money} монет ")
        else:
            self.character["money"][0] -= need_money
            self.character["bullets"][type_weapon][0] += need_bullets
            self.game.set_label("money", f"монеты: {self.character['money'][0]}")

    def set_move(self, cond):
        if list(self.character["flags"].values()) != [0] * len(self.character["flags"].values()) or cond == "idle":
            self.character["val_speed"] = self.character["speed"][cond]
            if cond in ("attack", "shoot_pistol", "shoot_automat", "hit"): self.character["old_cond"] = self.character["cond"]
            if cond == "walk": self.character["dop_old_cond"] = "walk"
            elif cond == "run": self.character["dop_old_cond"] = "run"
            elif cond == "sneak": self.character["dop_old_cond"] = "sneak"
            self.character["cond"] = cond
            # print(self.character["cond"])
            self.character["freq_sprite"] = self.character["speed_TO_freq"][cond]


    def respawn(self, coords):
        if coords[0] is not None: self.character["coords"][0] = coords[0] - self.character["coords"][2] // 2
        if coords[1] is not None: self.character["coords"][1] = coords[1] - self.character["coords"][3] // 2
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
        self.character["rect"].x = self.character["coords"][0] + self.character["coords_rect"][0]
        self.character["rect"].y = self.character["coords"][1] + self.character["coords"][3] - self.character["coords_rect"][3] - self.character["coords_rect"][1]
        self.character["rect"].w = self.character["coords_rect"][2]
        self.character["rect"].h = self.character["coords_rect"][3] # self.character["coords"][3]
        self.character["absolute_coords_rect"] = (self.character["rect"].x + self.character["rect"].w // 2, self.character["rect"].y + self.character["rect"].h // 2)
        if 1 not in self.game.flags_dinamic.values():
            self.character["coords_display"] = self.character["absolute_coords_rect"]
        # self.character["center_coords"] = (self.character["coords"][0] + self.character["coords"][2]//2, self.character["coords"][1] + self.character["coords"][3]//2)

    def update(self, draw_rects):
        # ----------- Урон
        if self.character["cond"] == "hit":
            if self.character["time_hit"] < self.character["period_hit"]:
                self.character["time_hit"] += 1
            else:
                self.set_move(self.character["old_cond"]) # self.set_move(self.character["dop_old_cond"])
                self.character["time_hit"] = 0

        # ----------- Атака
        if self.character["cond"] == "attack":
            self.attack_arms()
        elif self.character["cond"] in ("shoot_pistol", "shoot_automat"):
            self.shoot(self.character["type_weapon"])

        # -------- Перемещение
        dir_collides = self.game.collide(base_object=self.character,
                                         objects=list(self.game.room_now.objects.values())
                                                 + list(self.game.room_now.dop_objects_up.values())
                                                 + list(self.game.room_now.dop_objects_down.values()),
                                         draw_rects=draw_rects)
        if self.character["cond"] not in ("hit", "attack", "shoot_pistol", "shoot_automat"):
            self.move(dir_collides)
        # print(self.character["time_attack"], self.character["dir"], self.character["cond"])

        # ----- Подсчёт значений
        self.counting()

        # ----- Обновление спрайта персонажа
        self.set_sprite()
        self.draw()  # !!! Для оптиммизации можно добавить основной флаг, который будет отслеживать изменился ли персонаж

        # ----- Звуки
        if self.character["cond"] in ("walk", "run", "sneak", "attack", "shoot_pistol", "shoot_automat"):
            self.game.set_sound(self.character["cond"])
        else:
            self.game.set_sound(None)

        # ----- Выводящиеся данных
        if self.character["type_weapon"] == "arms":
            self.game.set_label("weapon", self.translate_name_weapon())
            self.game.set_label("both", "")
            self.game.set_label("bullets", "")
        elif self.character["type_weapon"] in ("pistol", "automat"):
            self.game.set_label("weapon", self.translate_name_weapon())
            both = self.character['bullets'][self.character["type_weapon"]][0] * self.character['bullets_price'][self.character["type_weapon"]][1] // self.character['bullets_price'][self.character["type_weapon"]][0]
            max_both = self.character['bullets'][self.character["type_weapon"]][1] * self.character['bullets_price'][self.character["type_weapon"]][1] // self.character['bullets_price'][self.character["type_weapon"]][0]
            if both not in (0, max_both):
                both += 1
            self.game.set_label("both", f"обоим: {both} / {max_both}")
            self.game.set_label("bullets", f"всего патронов: {self.character['bullets'][self.character["type_weapon"]][0]} / {self.character['bullets'][self.character["type_weapon"]][1]}")

    def attack_arms(self):
        if self.character["time_attack"] == 0:
            collide_enemys = self.game.collide(base_object=self.character,
                                               objects=dict(list(filter(
                                                   lambda x: hasattr(x[1], 'category') and "enemy" in x[1].category,
                                                   self.game.room_now.objects.items()))),
                                               type_return="objcts",
                                               type_collide="rect",
                                               draw_rects=False)
            list(map(lambda name_enemy: name_enemy[1].hit(self.character["damage"][self.character["type_weapon"]], name_enemy[0]),
                     collide_enemys.items()))
            self.character["coords"][0] += self.character["delta_coords_attack"][0]
            self.character["coords"][1] += self.character["delta_coords_attack"][1]
        if self.character["time_attack"] < self.character["period_attack"]:
            self.character["time_attack"] += 1
        else:
            self.set_move(self.character["old_cond"])

            self.character["coords"][0] -= self.character["delta_coords_attack"][0]
            self.character["coords"][1] -= self.character["delta_coords_attack"][1]
            self.character["time_attack"] = 0
            self.character["flags"]["key_space"] = 0
            if self.character["energy"][0] - 3 >= self.character["energy"][1]:
                self.character["energy"][0] -= 3
            # self.set_sprite()

    def shoot(self, type_shoot):
        if self.character["time_attack"] < self.character["period_attack"]:
            self.character["time_attack"] += 1
        else:
            name = f"bullet_{self.character['counter_bullet']}"
            self.game.room_now.objects[name] = Bullet(parent=self.parent, game=self.game,
                                                      base_style=self.base_style,
                                                      name=name, damage=self.character["damage"][self.character["type_weapon"]])
            self.character["bullets"][type_shoot][0] -= 1
            self.character["counter_bullet"] += 1
            if self.character["energy"][0] - 1 >= self.character["energy"][1]:
                self.character["energy"][0] -= 1

            self.character["shoot1_counter_bullets"][type_shoot][0] += 1
            self.character["time_attack"] = self.character["period_attack"] - 2

        if self.character["shoot1_counter_bullets"][type_shoot][0] >= self.character["shoot1_counter_bullets"][type_shoot][1]:
            self.set_move(self.character["old_cond"])
            self.character["time_attack"] = 0
            self.character["flags"]["key_space"] = 0
            self.character["shoot1_counter_bullets"][type_shoot][0] = 0
            # self.set_sprite()

    def move(self, dir_collides):
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

    def counting(self):
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

    def draw(self):
        self.game.game_layer.blit(self.character["sprite"], self.character["coords"])
        # pygame.draw.rect(self.game.game_layer, self.character["type_cond"][self.character["cond"]][self.character["dir"]], self.character["rect"])




class Map:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        self.rect_cell = {
            "size": [40, 40],
            "thickness_border": 3,
            "val_delta": 4,
            "color": {
                "start": (1, 1, 1, 50),
                "end": (255, 255, 255, 50),
                "border": (128, 128, 128),
                "0": (0, 0, 0, 50),
                "1": (0, 0, 200),
                "2": (0, 200, 0)
            }
        }
        self.map = [[0 for _ in range(self.game.coords_game_layer[2]//self.rect_cell["size"][0]+1)] for _ in range(self.game.coords_game_layer[3]//self.rect_cell["size"][1]+1)]
        self.coords_objects = []
        self.rows, self.cols = len(self.map), len(self.map[0])

        # print("\nMAP:")
        # print(*self.map, sep="\n")

    def init_graph(self):
        self.graph = {}
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)
        # print("graph: ", *self.graph.items(), sep="\n")

    def set_cell(self, x, y, val):
        self.map[y][x] = val

    def get_next_nodes(self, x, y):
        check_next_node = lambda x, y: True if 0 <= x < self.cols and 0 <= y < self.rows and not self.map[y][x] else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1] # , [-1, -1], [1, -1], [1, 1], [-1, 1]
        return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def set_object(self, coords, name=None, old_coords=None):
        if coords[1] == coords[3]: coords[3] += 1
        if coords[0] == coords[2]: coords[2] += 1
        for y in range(coords[1], coords[3]):
            for x in range(coords[0], coords[2]):
                if y < len(self.map) and x < len(self.map[y]):
                    self.map[y][x] = 1 # 50
                    self.coords_objects.append((x, y))

    def draw(self):
        x, y = 0, 0
        for i_row in range(len(self.map)):
            for i_cell in range(len(self.map[i_row])):
                color = self.rect_cell["color"][str(self.map[i_row][i_cell])]
                self.game.set_rect(layer=self.game.game_layer, coords=[x, y, self.rect_cell["size"][0], self.rect_cell["size"][1]],
                                   color_base=color, color_border=self.rect_cell["color"]["border"],
                                   thickness_border=self.rect_cell["thickness_border"])
                x += self.rect_cell["size"][0]
            y += self.rect_cell["size"][1]
            x = 0


class Game:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent

        # ------ Живые объекты
        self.coords_enemy = {}
        self.delete_enemys = {}
        self.hp_enemys = {}

        # ------ Звуки
        self.sounds = {
            "walk": 'sounds/walk.mp3',
            "run": 'sounds/run.mp3',
            "sneak": 'sounds/sneak.mp3',
            "attack": "sounds/attack.mp3",
            "shoot_pistol": "sounds/pistol.mp3",
            "shoot_automat": "sounds/automat.mp3",
        }
        # for k, v in self.sounds.items():
        #     self.sounds[k] = pygame.mixer.music.load(v)
        self.flag_sound = 1
        self.curr_sound = None

        # ------ Уровень
        self.level1 = Level1(self.parent, self, self.base_style)
        # ------ Комната
        self.list_rooms = self.level1.list_rooms
        self.type_room = "start_room" # list(self.list_rooms.keys())[0]  # Здесь указывается первая комната ("start_room")
        self.flag_change_room = 0
        self.room_now = self.list_rooms[self.type_room](self.parent, self, self.base_style)
        # ------ Слой комнаты
        self.game_layer = self.room_now.room_layer
        self.start_spawn = [self.room_now.size_room_layer[0] // 4 + 200, self.room_now.size_room_layer[1] - 100] # [500, self.room_now.size_room_layer[1] // 2]
        self.coords_game_layer = [0, 0, self.room_now.size_room_layer[0], self.room_now.size_room_layer[1]]
        self.coords_game_layer_old = self.coords_game_layer.copy()
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

        # ------ Карта
        self.init_map()
        # print("\nMAP:")
        # print(*self.map.map, sep="\n")

        # ------------ Мышка
        # self.coords_cursor = pygame.mouse.get_pos()
        # self.old_coords_cursor = self.coords_cursor
        self.val_mouse_state = "click"

        # ------ Персонаж
        self.character = Character(self.parent, self, self.base_style)
        self.character.respawn(self.start_spawn)
        self.start2_coords_dinamic_zone = self.coords_dinamic_zone.copy()

        # ------ Команды и горячие клавиши
        self.commands = {
            pygame.KEYDOWN: {
                pygame.K_ESCAPE: lambda: self.parent.display_change("menu"),
                # pygame.K_0: lambda: self.parent.display_change("final", dop_type="victory"),
                # pygame.K_9: lambda: self.parent.display_change("final", dop_type="fail")
            },
            pygame.MOUSEBUTTONDOWN: self.mouse_state,
            pygame.MOUSEBUTTONUP: self.mouse_state
        }
        self.commands = self.parent.format_commands(self.commands)
        print("GAME: ", *self.commands.items(), sep="\n")
        self.list_comands = [self.commands, self.character.commands]

        # ------ Мини игры
        self.mini_games = {
            'start_room': {
                'dino': lambda: dino_game(self.parent.display),
                'hyper_dash': lambda: curcle(self.parent.display),
                'dash_hex': lambda: dash_hex(self.parent.display),
            },
        }
        self.flag_mini_games = False

        # ------ Надписи и данные о игре, находящиеся сверху слева
        self.labels = {}
        self.init_labels()
        # ------ Кнопки на экране
        self.buttons = []
        self.init_button_menu()

    def init_map(self):
        self.map = Map(self.parent, self, self.base_style)
        for name, obj in self.room_now.objects.items():
            if "enemy" not in name: # Статический объект
                obj.set_object_map(name)
            else:
                if name in self.coords_enemy.keys(): # Динамический объект (объект, который перемещается)
                    self.room_now.objects[name].data["coords"][0] = self.coords_enemy[name][0]
                    self.room_now.objects[name].data["coords"][1] = self.coords_enemy[name][1]
                    self.room_now.objects[name].data["hp"] = self.hp_enemys[name]
                obj.init_start()
                if name not in self.coords_enemy.keys():
                    obj.check_random_spawn()
        self.map.init_graph()

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
            "text": f"hp: {self.character.character['hp'][0]} / {self.character.character['hp'][2]}",
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
                "text": f"энергия: {self.character.character['energy'][0]} / {self.character.character['energy'][2]}",
                "font": pygame.font.Font(self.base_style["font_path"], 30)
            }
            label_energy["label"] = self.parent.label_text(coords=label_energy["coords"],
                                                       text=label_energy["text"],
                                                       font=label_energy["font"],
                                                       color=self.base_style["colors"]["light"])
            self.labels["energy"] = label_energy

        label_money = {
            "coords": (5, 90),
            "text": f"монеты: {self.character.character['money'][0]}",
            "font": pygame.font.Font(self.base_style["font_path"], 30)
        }
        label_money["label"] = self.parent.label_text(coords=label_money["coords"],
                                                       text=label_money["text"],
                                                       font=label_money["font"],
                                                       color=self.base_style["colors"]["light"])
        self.labels["money"] = label_money

        label_weapon = {
            "coords": [5, self.parent.display_h - 120],
            "text": "тип оружие:",
            "font": pygame.font.Font(self.base_style["font_path"], 30)
        }
        self.labels["weapon"] = label_weapon

        label_both = {
            "coords": [5, self.parent.display_h - 80],
            "text": "обоим:",
            "font": pygame.font.Font(self.base_style["font_path"], 30)
        }
        self.labels["both"] = label_both

        label_bullets = {
            "coords": [5, self.parent.display_h - 50],
            "text": "всего патронов:",
            "font": pygame.font.Font(self.base_style["font_path"], 30)
        }
        self.labels["bullets"] = label_bullets

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

    def set_sound(self, sound):
        if self.curr_sound != sound:
            if sound == None:
                pygame.mixer.music.pause()
                # self.flag_sound = 1
            else: # elif self.flag_sound:
                pygame.mixer.music.load(self.sounds[sound])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.unpause()
                # self.flag_sound = 0
        self.curr_sound = sound

    def set_sound_player(self, type_player):
        if type_player == "pause": pygame.mixer.music.pause()
        elif type_player == "play": pygame.mixer.music.unpause()

    def room_change(self, type_room):
        self.type_room = type_room
        self.flag_change_room = 1

    def change_game(self, name_game):
        delta_energy = 3
        if not self.flag_mini_games:
            if self.character.character["energy"][0] - delta_energy < 0:
                self.set_message(f"Не хватает энергии чтобы поиграть в игры, нужно ещё {delta_energy + 1} ")
            else:
                self.flag_mini_games = True
                out_many = self.mini_games[self.type_room][name_game]()
                self.character.character["money"][0] += out_many
                self.set_label("money", f"монеты: {self.character.character['money'][0]}")
                self.character.character["energy"][0] -= delta_energy
                for obj in self.room_now.objects.values():
                    obj.data["func"] = 0
                self.flag_mini_games = False

    def draw(self):
        # ------ Иницилизация карты, пола
        self.parent.display.fill(self.base_style["colors"]["black"])
        self.parent.display.blit(self.game_layer, (self.coords_game_layer[0], self.coords_game_layer[1]))
        self.game_layer.fill((0, 0, 0))
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
            for name, obj in self.room_now.objects.items():
                if name in self.delete_enemys:
                    if "enemy" in name and self.delete_enemys[name] == False:
                        self.coords_enemy[name] = [obj.data["coords"][0], obj.data["coords"][1]]
                        self.hp_enemys[name] = obj.data["hp"]
                # if "enemy" in name and name not in self.coords_enemy.keys():
                #     self.coords_enemy[name] = [obj.data["coords"][0], obj.data["coords"][1]]
            self.room_now.delete_all()
            self.room_now = self.list_rooms[self.type_room](self.parent, self, self.base_style)
            self.room_now.enter_rooms()
            self.init_map()
            # print()
            # print("enemys", list(filter(lambda x: "enemy" in x, self.room_now.objects.keys())))
            # print("coords_enemys", list(self.coords_enemy.keys()))
            # print("delete_enemys", list(self.delete_enemys.keys()))
        # print(self.coords_game_layer[0] - self.coords_game_layer_old[0], self.coords_game_layer[1] - self.coords_game_layer_old[1])
        self.room_now.draw()

        # ------ Пули
        delete_bullet = []
        for name, bullet in dict(list(filter(lambda x: "bullet" in x[0], self.room_now.objects.items()))).items():
            bullet.update()
            if bullet.bullet_data["delete"] == 1: delete_bullet.append(bullet.bullet_data["name"])
        # print(list(dict(list(filter(lambda x: "bullet" in x[0], self.room_now.objects.items()))).keys()))
        for _ in range(len(delete_bullet)):
            if delete_bullet[0] in self.room_now.objects.keys():
                del self.room_now.objects[delete_bullet[0]]

        # ------ Вывод значений и данных о игре
        # if self.flag_message_energy == 1: self.set_message()
        for i in self.labels.values():
            if "label" in i.keys():
                self.parent.display.blit(i["label"], i["coords"])
        self.set_label("fps", f"fps: {self.parent.clock.get_fps():2.0f} / {self.parent.FPS}")
        self.set_label("hp", f"hp: {self.character.character['hp'][0]} / {self.character.character['hp'][2]}")
        if self.parent.settings_var["character_energy"] == 1:
            self.set_label("energy", f"энергия: {self.character.character['energy'][0]} / {self.character.character['energy'][2]}")

        # ------ Карта
        if self.parent.settings_var["draw_map"] == 1: self.map.draw()

        # ------ Условия выхода
        if self.character.character["hp"][0] <= 0:
            self.parent.display_change("final", dop_type="fail")

        # ------ Вывод данных в консоль
        # print("MOUSE", pygame.mouse.get_pos())
        # print(pygame.mouse._get_cursor()) # pygame.mouse.get_pos()

        # self.coords_game_layer_old = self.coords_game_layer.copy()

    def set_rect(self, layer, coords, color_base, thickness_border=None, color_border=None):
        if thickness_border == None: thickness_border = 5
        if len(coords) < 4: raise IndexError("Мало параметров coords, как минимум 4 (x, y, w, h)")
        if len(color_base) < 3: raise IndexError("Мало параметров RGB цвета color, как минимум 3")
        rect_layer = pygame.Surface((coords[2], coords[3]))
        if color_border != None:
            pygame.draw.lines(self.game_layer, color_border, True, [[coords[0], coords[1]],
                                                               [coords[0]+coords[2], coords[1]],
                                                               [coords[0]+coords[2], coords[1]+coords[3]],
                                                               [coords[0], coords[1]+coords[3]]], thickness_border)
        if len(color_base) >= 4: rect_layer.set_alpha(color_base[3])
        rect_layer.fill(color_base[:3])
        layer.blit(rect_layer, (coords[0], coords[1]))

    def set_dinamic_zone(self, type_output=0):
        if type_output == 1:
            output_flags = list(self.flags_dinamic.values())
        elif type_output == 2:
            if list(self.flags_dinamic.values())[0] == 0: # up
                pass
        self.set_rect(layer=self.parent.display,
                      coords=(self.start_coords_dinamic_zone[0],
                              self.start_coords_dinamic_zone[1],
                              self.start_coords_dinamic_zone[2] - self.start_coords_dinamic_zone[0],
                              self.start_coords_dinamic_zone[3] - self.start_coords_dinamic_zone[1]),
                      color_base=(50, 50, 50, 100))

    def set_message(self, text, delay=2500):
        label = {
            "coords": (100, 100),
            "text": text,
            "font": pygame.font.Font(self.base_style["font_path"], 40)  # self.base_style["dop_font"]
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
        pygame.draw.rect(self.parent.display, self.base_style["colors"]["base2"], coords_rect) # self.game_layer
        self.parent.display.blit(label["label"], label["coords"]) # self.game_layer
        pygame.display.flip()
        pygame.time.wait(delay)

    def hp_character_up(self, price, val, type_val):
        if self.character.character["money"][0] - price < 0: self.set_message(f"Не хватает денег, для {val} {type_val} нужно {price} монет ")
        elif self.character.character[type_val][0] + val > self.character.character[type_val][2]: self.set_message(f"Всё {type_val} восстановлено (макс. {self.character.character[type_val][2]} {type_val}) ")
        else:
            self.character.character["money"][0] -= price
            self.character.character[type_val][0] += val
            self.set_label("money", f"монеты: {self.character.character['money'][0]}")

    def render_objects(self, draw_rects=False): # dop_buttons=None,
        objects = self.room_now.objects #list(self.room_now.objects.values())
        dop_objects_down = list(self.room_now.dop_objects_down.values())
        dop_objects_up = list(self.room_now.dop_objects_up.values())

        delete_obj = []
        for name, obj in objects.items():
            if name == "DINAMIC_door_1":
                if True in self.delete_enemys.values() or self.delete_enemys == {}:
                    delete_obj.append(name)
        for _ in range(len(delete_obj)):
            del self.room_now.objects[delete_obj[0]]

        # Распределение по слоям
        for obj in objects.values():
            if self.character.character["rect"].centery > obj.data["rect"].centery:
                obj.data["type_render"] = 1
            else:
                obj.data["type_render"] = 2

        # Отрисовка
        if dop_objects_up is not None:
            for obj in dop_objects_up: # sorted(dop_objects_up, key=lambda obj: (obj.data["rect"].y, obj.data["rect"].h)):
                obj.draw()
        for name, obj in sorted(list(filter(lambda name_obj: name_obj[1].data["type_render"] == 1, objects.items())), key=lambda name_obj: name_obj[1].data["rect"].y + name_obj[1].data["rect"].h):
            obj.draw()
        self.character.update(draw_rects)
        for name, obj in sorted(list(filter(lambda name_obj: name_obj[1].data["type_render"] == 2, objects.items())), key=lambda name_obj: name_obj[1].data["rect"].y + name_obj[1].data["rect"].h):
            obj.draw()
        if dop_objects_down is not None:
            for obj in dop_objects_down: # sorted(dop_objects_down, key=lambda obj: (obj.data["rect"].y, obj.data["rect"].h)):
                obj.draw()
        if draw_rects:
            for obj in objects:
                pygame.draw.rect(self.game_layer, (255, 255, 255), obj.data["rect"])

    def collide(self, base_object, objects, draw_rects, type_collide="rect", type_return="dirs"):
        if type(objects) == dict:
            names_objects = list(objects.keys())
            objects = list(objects.values())
        dir_collides = []
        if type_return == "objcts": collide_objcts = {}

        if type_collide == "rect":
            base_rect = base_object["rect"]
        elif type_collide == "sprite":
            base_rect = base_object["sprite"].get_rect()
            base_rect.x = base_object["coords"][0]
            base_rect.y = base_object["coords"][1]
        else:
            base_rect = base_object["rect"]
        if draw_rects: pygame.draw.rect(self.game_layer, (255, 0, 0), base_rect)

        i = 0
        for obj in objects:
            if type_collide == "sprite":
                if "sprite" in obj.data:
                    obj_rect = obj.data["sprite"].get_rect()
                    obj_rect.x = obj.data["coords"][0]
                    obj_rect.y = obj.data["coords"][1]
                else:
                    obj_rect = obj.data["rect"]
            else: obj_rect = obj.data["rect"]
            if base_rect.colliderect(obj_rect):
                collision_area = base_rect.clip(obj_rect)
                if type_return == "objcts": collide_objcts[names_objects[i]] = obj
                if collision_area.width > collision_area.height:
                    if base_rect.centery < obj_rect.centery:
                        dir_collides.append("down")
                    else:
                        dir_collides.append("up")
                else:
                    if base_rect.centerx < obj_rect.centerx:
                        dir_collides.append("right")
                    else:
                        dir_collides.append("left")
            i += 1

        if dir_collides == []: dir_collides = [None]
        dir_collides = list(set(dir_collides))
        if type_return == "dirs":
            return dir_collides
        elif type_return == "objcts":
            return collide_objcts

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

    # ==== BFS
    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None} # {}
        # for start in starts:
        #     visited[start] = None

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break

            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return queue, visited
    # ========

    def mouse_state(self, state):
        self.val_mouse_state = state

    def check_event(self, event):
        for commands in self.list_comands:
            if event.type in commands.keys():
                if type(commands[event.type]) == dict:
                    if event.key in commands[event.type].keys():
                        commands[event.type][event.key]()
                else:
                    if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                        commands[event.type](event.type)
                    else:
                        commands[event.type]()

    def delete_all(self):
        # print("GAME ", *list(map(lambda x: x["text"] if "text" in x.keys() else x["texts"], self.buttons)), sep=" ")
        for j in range(len(self.buttons)): del self.buttons[0]
        # self.parent.type_music = 1
        self.parent.set_music()
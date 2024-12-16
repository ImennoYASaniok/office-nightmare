import pygame
import numpy as np

class Map:
    def __init__(self):
        self.info = {
            "#": {
                "w": 50, "h": 50,
                "sprite": (0, 0, 255)
            }
        }
        self.map = []


class Character:
    def __init__(self, parent, base_color, container_flags):
        self.container_flags = container_flags
        self.parent = parent
        self.base_color = base_color

        self.init_shell()
        self.container_flags["character"] = 0
        self.commands = { # если val - list тогда, [(f1, flag1), (f2, flag2)], где 0-ой элемент на нажатие а 1-ый на отпускание,
            pygame.KEYDOWN: {
                (pygame.K_DOWN, pygame.K_s): lambda: self.set_flag("key_down", 1), # lambda: print("character - front"),
                (pygame.K_UP, pygame.K_w): lambda: self.set_flag("key_up", 1), # lambda: print("character - back"),
                (pygame.K_LEFT, pygame.K_a): lambda: self.set_flag("key_left", 1), # lambda: print("character - left"),
                (pygame.K_RIGHT, pygame.K_d): lambda: self.set_flag("key_right", 1), # lambda: print("character - right")
                (pygame.K_RCTRL, pygame.K_LCTRL): lambda: self.set_delta_move(self.character["delta_sneak"]),
                (pygame.K_RSHIFT, pygame.K_LSHIFT): lambda: self.set_delta_move(self.character["delta_run"])
            },
            pygame.KEYUP: {
                (pygame.K_DOWN, pygame.K_s): lambda: self.set_flag("key_down", 0),
                (pygame.K_UP, pygame.K_w): lambda: self.set_flag("key_up", 0),
                (pygame.K_LEFT, pygame.K_a): lambda: self.set_flag("key_left", 0),
                (pygame.K_RIGHT, pygame.K_d): lambda: self.set_flag("key_right", 0),
                (pygame.K_RCTRL, pygame.K_LCTRL, pygame.K_RSHIFT, pygame.K_LSHIFT): lambda: self.set_delta_move(self.character["delta_move"])
            }
        }
        self.commands = self.parent.format_commands(self.commands)
        print("CHARACTER: ", self.commands)

    def set_flag(self, key, val):
        self.character["flags"][key] = val

    def set_delta_move(self, delta):
        # print(delta)
        if  self.character["delta_run"] == delta: self.character["cond"] = "run"
        elif self.character["delta_sneak"] == delta: self.character["cond"] = "sneak"
        else: self.character["cond"] = "move"
        self.character["delta"] = delta

    def udpate(self):
        flag_change = 0
        if self.character["flags"]["key_down"]:
            self.character["coords"][1] += self.character["delta"]
            self.character["dir"] = "front"
            flag_change = 1
        if self.character["flags"]["key_up"]:
            self.character["coords"][1] -= self.character["delta"]
            self.character["dir"] = "back"
            flag_change = 1
        if self.character["flags"]["key_left"]:
            self.character["coords"][0] -= self.character["delta"]
            self.character["dir"] = "left"
            flag_change = 1
        if self.character["flags"]["key_right"]:
            self.character["coords"][0] += self.character["delta"]
            self.character["dir"] = "right"
            flag_change = 1
        if flag_change == 0:
            self.character["cond"] = "stand"
            self.character["dir"] = "base"
        else:
            self.set_delta_move(self.character["delta"])
        self.draw() # !!! Для оптиммизации можно добавить основной флаг, который будет отслеживать изменился ли персонаж
        # print(*self.character["flags"].items())
        # print(self.character["dir"], type_move)

    def init_shell(self):
        self.character = {
            "type_cond": {
                "move": {
                    "front": (150, 0, 0),
                    "back": (150, 150, 0),
                    "left": (0, 150, 0),
                    "right": (70, 150, 70)
                },
                "run": {
                    "front": (255, 0, 0),
                    "back": (255, 255, 0),
                    "left": (0, 255, 0),
                    "right": (100, 255, 150)
                },
                "sneak": {
                    "front": (80, 0, 0),
                    "back": (80, 80, 0),
                    "left": (0, 80, 0),
                    "right": (40, 80, 40)
                },
                "stand": {
                    "base": (255, 255, 255)
                }
            },
            "flags": {
                "key_down": 0,  # front
                "key_up": 0,  # back
                "key_left": 0,  # left
                "key_right": 0  # right
            },
            "dir" : "base",
            "cond": "stand",
            "delta_sneak": 3,
            "delta_move": 5,
            "delta_run": 7,
            "delta": 2,
            "coords": [self.parent.display_w // 2, self.parent.display_h // 2, 50, 70]
        }
        self.character["coords"][0] -= self.character["coords"][2] / 2
        self.character["coords"][1] -= self.character["coords"][3] / 2
        self.draw()

    def draw(self):
        self.character["rect"] = pygame.Rect(self.character["coords"])
        pygame.draw.rect(self.parent.display, self.character["type_cond"][self.character["cond"]][self.character["dir"]], self.character["rect"])




# !!! При создание объектов игре мы добавляем под них флаг состояния в контейнер (np.array)
# И мы будем обновлять экран, только если хотя бы 1 объект изменился в контейнер
class Game:
    def __init__(self, parent, base_color):
        self.base_color = base_color
        self.parent = parent
        self.container_flags = {}

        self.init_label_test()
        self.init_button_menu()

        self.character = Character(self.parent, self.base_color, self.container_flags)

        self.commands = {
            pygame.KEYDOWN: {
                pygame.K_ESCAPE: lambda: self.parent.display_change("menu"),
                pygame.K_0: lambda: self.parent.display_change("final", dop_type="victory"),
                pygame.K_9: lambda: self.parent.display_change("final", dop_type="fail")
            }
        }
        self.commands = self.parent.format_commands(self.commands)
        print("GAME: ", self.commands)
        self.list_comands = [self.commands, self.character.commands]


    def init_label_test(self):
        # !!! Если нужно будет создавать много label -> сделай init_label_title общей для всех и возвращай label_title
        self.label_test = {
            "coords": [20, 20],
            "text": "здесь будет игра",
            "font": pygame.font.SysFont("Century Gothic", 40),
            "label": None
        }
        self.label_test["label"] = self.parent.label_text(coords=self.label_test["coords"],
                                                           text=self.label_test["text"],
                                                           font=self.label_test["font"])
        # self.label_test["coords"][2] = self.label_test["label"].get_width()
        # self.label_test["coords"][3] = self.label_test["label"].get_height()

    def init_button_menu(self):
        w, h = 80, 50
        self.button_ToMenu = {
            "font": pygame.font.SysFont("Century Gothic", 30),
            "coords": (self.parent.display_w-w, 0, w, h),
            "text": "...",
            "func": lambda: self.parent.display_change("menu"),
            "inv_clr":1
        }
        self.button_ToMenu["button"] = self.parent.button(coords=self.button_ToMenu["coords"],
                                                              text=self.button_ToMenu["text"],
                                                              font=self.button_ToMenu["font"],
                                                              func=self.button_ToMenu["func"],
                                                              inv_clr=self.button_ToMenu["inv_clr"])

    def reinstall(self, _type):
        if _type == "hide":
            self.button_ToMenu["button"].hide()
        elif _type == "show":
            self.parent.display.fill(self.base_color["black"])
            self.draw()
            self.button_ToMenu["button"].show()

    def draw(self):
        self.parent.display.fill(self.base_color["black"])
        self.character.udpate()
        self.parent.display.blit(self.label_test["label"], self.label_test["coords"])

    def check_event(self, event):
        for commands in self.list_comands:
            if event.type in commands.keys() and event.key in commands[event.type].keys():
                commands[event.type][event.key]()


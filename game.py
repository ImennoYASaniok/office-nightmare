import pygame
import numpy as np

class Character:
    def __init__(self, parent, base_color, container_flags):
        self.container_flags = container_flags
        self.parent = parent
        self.base_color = base_color

        self.init_shell()
        self.container_flags["character"] = 0
        self.commands = {
            (pygame.K_DOWN, pygame.K_s): lambda: self.move("down"), # lambda: print("character - front"),
            (pygame.K_UP, pygame.K_w): lambda: self.move("up"), # lambda: print("character - back"),
            (pygame.K_LEFT, pygame.K_a): lambda: self.move("left"), # lambda: print("character - left"),
            (pygame.K_RIGHT, pygame.K_d): lambda: self.move("right"), # lambda: print("character - right")
        }

    def move(self, type_move):
        print(type_move)
        if type_move == "down": self.character["coords"][1] += self.character["delta"]
        elif type_move == "up": self.character["coords"][1] -= self.character["delta"]
        elif type_move == "left": self.character["coords"][0] -= self.character["delta"]
        elif type_move == "right": self.character["coords"][0] += self.character["delta"]

    def init_shell(self):
        self.character = {
            "type_pos": {
                "front": (200, 0, 0),
                "back": (100, 100, 0),
                "left": (0, 100, 100),
                "right": (0, 0, 200)
            },
            "pos" : "front",
            "delta": 30,
            "coords": [self.parent.display_w // 2, self.parent.display_h // 2, 50, 70]
        }
        self.character["coords"][0] -= self.character["coords"][2] / 2
        self.character["coords"][1] -= self.character["coords"][3] / 2
        self.draw()

    def draw(self):
        self.character["rect"] = pygame.Rect(self.character["coords"])
        pygame.draw.rect(self.parent.display, self.character["type_pos"][self.character["pos"]], self.character["rect"])




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
        res_commands = {}
        for key, val, in self.character.commands.items():
            if type(key) in (list, tuple):
                for mini_key in key: res_commands[mini_key] = val
            else:
                res_commands[key] = val
        self.commands = res_commands


    def init_label_test(self):
        # !!! Если нужно будет создавать много label -> сделай init_label_title общей для всех и возвращай label_title
        self.label_test = {
            "coords": (20, 20),
            "text": "здесь будет игра",
            "font": pygame.font.SysFont("Century Gothic", 40),
            "label": None
        }
        self.label_test["label"] = self.parent.label_text(coords=self.label_test["coords"],
                                                           text=self.label_test["text"],
                                                           font=self.label_test["font"])

    def init_button_menu(self):
        w, h = 80, 50
        self.button_ToMenu = {
            "font": pygame.font.SysFont("Century Gothic", 30),
            "coords": (self.parent.display_w-w, 0, w, h),
            "text": "...",
            "func": lambda: self.parent.display_change("menu"),
            "inv_clr":1
        }
        self.button_ToMenu["buttons"] = self.parent.button(coords=self.button_ToMenu["coords"],
                                                              text=self.button_ToMenu["text"],
                                                              font=self.button_ToMenu["font"],
                                                              func=self.button_ToMenu["func"],
                                                              inv_clr=self.button_ToMenu["inv_clr"])

    def reinstall(self, _type):
        if _type == "hide":
            self.button_ToMenu["buttons"].hide()
        elif _type == "show":
            self.draw()
            self.button_ToMenu["buttons"].show()

    def draw(self):
        self.parent.display.fill(self.base_color["dark"])
        self.character.draw()
        self.parent.display.blit(self.label_test["label"], self.label_test["coords"])

    def check_event(self, event):
        flag_change = False
        if event.type == pygame.KEYDOWN:
            for key, val in self.commands.items():
                if event.key == key:
                    val()
                    flag_change = True
        if flag_change == True:
            self.draw()


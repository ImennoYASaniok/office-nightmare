import pygame, pygame_widgets

class Game:
    def __init__(self, parent, base_color):
        self.base_color = base_color
        self.parent = parent
        self.init_label_test()
        self.init_button_menu()

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
        self.buttons_menu = {
            "font": pygame.font.SysFont("Century Gothic", 30),
            "coords": (self.parent.display_w-w, 0, w, h),
            "text": "...",
            "func": lambda: self.parent.display_change("menu"),
            "inv_clr":1
        }
        self.buttons_menu["buttons"] = self.parent.button(coords=self.buttons_menu["coords"],
                                                              text=self.buttons_menu["text"],
                                                              font=self.buttons_menu["font"],
                                                              func=self.buttons_menu["func"],
                                                              inv_clr=self.buttons_menu["inv_clr"])

    def reinstall(self, _type):
        if _type == "hide":
            self.buttons_menu["buttons"].hide()
        elif _type == "show":
            self.init_button_menu()
            self.parent.display.blit(self.label_test["label"], self.label_test["coords"])

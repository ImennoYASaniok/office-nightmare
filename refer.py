import pygame

class Refer:
    def __init__(self, parent, base_color):
        self.base_color = base_color
        self.parent = parent
        self.init_label_title()
        self.init_button_menu()

    def init_label_title(self):
        # !!! Если нужно будет создавать много label -> сделай init_label_title общей для всех и возвращай label_title
        self.label_title = {
            "coords": (600, 20),
            "text":"Справка",
            "font": pygame.font.SysFont("Century Gothic", 50)
        }
        self.label_title["label"] = self.parent.label_text(coords=self.label_title["coords"],
                                                           text=self.label_title["text"],
                                                           font=self.label_title["font"])
        self.label_title["label"], self.label_title["coords"] = self.parent.align(self.label_title["label"], self.label_title["coords"],
                                                            inacurr=-20, type_blit=False, type_align="horizontal")

    def init_button_menu(self):
        w, h = 80, 50
        self.button_ToMenu = {
            "font": pygame.font.SysFont("Century Gothic", 30),
            "coords": (self.parent.display_w - w, 0, w, h),
            "text": "...",
            "func": lambda: self.parent.display_change("menu"),
            "inv_clr": 1
        }
        self.button_ToMenu["button"] = self.parent.button(coords=self.button_ToMenu["coords"],
                                                          text=self.button_ToMenu["text"],
                                                          font=self.button_ToMenu["font"],
                                                          func=self.button_ToMenu["func"],
                                                          inv_clr=self.button_ToMenu["inv_clr"])


    def reinstall(self, _type):
        if _type == "hide":
            pass
        elif _type == "show":
            self.parent.display.fill(self.base_color["dark"])
            self.parent.display.blit(self.label_title["label"], self.label_title["coords"])
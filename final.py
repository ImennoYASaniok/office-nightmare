import pygame

class Final:
    def __init__(self, parent, base_color):
        self.base_color = base_color
        self.parent = parent
        self.commands = {
            pygame.KEYDOWN: {
                (pygame.K_ESCAPE, pygame.K_RETURN): lambda: self.parent.display_change("menu")
            }
        }
        self.init_button_OK()
        self.types_final = {
            "type": "victory",
            "victory": {
                "text": "Молодец, ты победил!"
            },
            "fail": {
                "text": "Ты проиграл... Попробуй ещё раз!"
            }
        }
        self.label_title = self.set_label_title()


    def set_final(self, final):
        self.types_final["type"] = final
        self.label_title = self.set_label_title()
        # self.parent.align(self.label_title["label"])

    def set_label_title(self):
        label = {
            "coords": [self.parent.display_w // 2, 20],
            "text": self.types_final[self.types_final["type"]]["text"],
            "font": pygame.font.SysFont("Century Gothic", 40)
        }
        label["label"] = self.parent.label_text(coords=label["coords"],
                                                text=label["text"],
                                                font=label["font"])
        label["label"], label["coords"] = self.parent.align(label["label"], label["coords"],
                                                            inacurr=-20, type_blit=False, type_align="horizontal")
        return label

    def init_button_OK(self):
        w, h = 100, 90
        self.button_OK = {
            "font": pygame.font.SysFont("Century Gothic", 50),
            "coords": (self.parent.display_w // 2 - w, self.parent.display_h - h - 30, w, h),
            "text": "ОК",
            "func": lambda: self.parent.display_change("menu"),
            "inv_clr": 1
        }
        self.button_OK["button"] = self.parent.button(coords=self.button_OK["coords"],
                                                           text=self.button_OK["text"],
                                                           font=self.button_OK["font"],
                                                           func=self.button_OK["func"],
                                                           inv_clr=self.button_OK["inv_clr"])

    def reinstall(self, _type):
        if _type == "hide":
            print("hide final")
            self.button_OK["button"].hide()
        elif _type == "show":
            print("show final")
            self.parent.display.fill(self.base_color["dark"])
            self.button_OK["button"].show()
            self.parent.display.blit(self.label_title["label"], self.label_title["coords"])
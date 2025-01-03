import pygame

class Settings:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent
        self.labels = []
        self.buttons = []

        self.init_labels()
        self.init_buttons()

    def init_labels(self):
        # !!! Если нужно будет создавать много label -> сделай init_label_title общей для всех и возвращай label_title
        label_title = {
            "coords": (600, 20),
            "text":"Настройки",
            "font": pygame.font.Font(self.base_style["font_path"], 50)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                      text=label_title["text"],
                                                      font=label_title["font"])
        label_title["label"], label_title["coords"] = self.parent.align(label_title["label"], label_title["coords"],
                                                                        inacurr=-20, type_blit=False,
                                                                        type_align="horizontal")
        self.labels.append(label_title)

    def init_buttons(self):
        w, h = 80, 50
        button_ToMenu = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (self.parent.display_w - w, 0, w, h),
            "color": {
                "inactive": self.base_style["colors"]["base2"],
                "hover": self.base_style["colors"]["base1"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "text": "...",
            "func": lambda: self.parent.display_change("menu"),
        }
        button_ToMenu["button"] = self.parent.button(coords=button_ToMenu["coords"],
                                                     text=button_ToMenu["text"],
                                                     color=button_ToMenu["color"],
                                                     font=button_ToMenu["font"],
                                                     func=button_ToMenu["func"])
        self.buttons.append(button_ToMenu)

    def delete_all(self):
        # print("SETT", *list(map(lambda x: x["text"] if "text" in x.keys() else x["texts"], self.buttons)), sep=" ")
        for _ in range(len(self.buttons)):
            del self.buttons[0]
        del self.buttons

    def draw(self):
        self.parent.display.fill(self.base_style["colors"]["dark"])
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])
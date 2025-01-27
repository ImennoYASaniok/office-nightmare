import pygame

class Final:
    def __init__(self, parent, base_style, type_final):
        self.base_style = base_style
        self.parent = parent
        self.labels = []
        self.buttons = []

        self.commands = {
            pygame.KEYDOWN: {
                (pygame.K_ESCAPE, pygame.K_RETURN): lambda: self.parent.display_change("menu")
            }
        }
        self.commands = self.parent.format_commands(self.commands)
        self.types_final = {
            "type": type_final,
            "victory": {
                "text": "Молодец, ты победил!"
            },
            "fail": {
                "text": "Ты проиграл... Попробуй ещё раз!"
            }
        }
        # self.

        self.init_labels()
        self.init_buttons()

    def init_labels(self):
        label_title = {
            "coords": [self.parent.display_w // 2, 20],
            "text": self.types_final[self.types_final["type"]]["text"],
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
        w, h = 100, 90
        button_OK = {
            "font": pygame.font.Font(self.base_style["font_path"], 40),
            "coords": (self.parent.display_w // 2 - w, self.parent.display_h - h - 30, w, h),
            "color": {
                "inactive": self.base_style["colors"]["base2"],
                "hover": self.base_style["colors"]["base1"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "text": "ОК",
            "func": lambda: self.parent.display_change("menu"),
        }
        button_OK["button"] = self.parent.button(coords=button_OK["coords"],
                                                     text=button_OK["text"],
                                                     color=button_OK["color"],
                                                     font=button_OK["font"],
                                                     func=button_OK["func"])
        self.buttons.append(button_OK)

    def delete_all(self):
        # print("SETT", *list(map(lambda x: x["text"] if "text" in x.keys() else x["texts"], self.buttons)), sep=" ")
        for _ in range(len(self.buttons)):
            del self.buttons[0]
        del self.buttons
        self.parent.set_music()

    def draw(self):
        self.parent.display.fill(self.base_style["colors"]["dark"])
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])


    def check_event(self, event):
        if event.type in self.commands.keys():
            if type(self.commands[event.type]) == dict:
                if event.key in self.commands[event.type].keys():
                    self.commands[event.type][event.key]()
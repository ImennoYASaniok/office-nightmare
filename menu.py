import pygame

class Menu:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent
        self.labels = []
        self.buttons = []
        self.init_buttons()
        self.init_labels()

    def init_buttons(self):
        buttons = {
            "font": pygame.font.Font(self.base_style["font_path"], 40),
            "coords": (450, 200, 250, 100),
            "layout": [1, 4],
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            }
        }
        param_button_start = {"text": "играть", "func": lambda: self.parent.display_change("game")}
        param_button_sett = {"text": "настройки", "func": lambda: self.parent.display_change("settings")}
        param_button_refer = {"text": "справка", "func": lambda: self.parent.display_change("refer")}
        param_button_quit = {"text": "выход", "func": self.parent.display_quit}
        array_buttons = [param_button_start, param_button_sett, param_button_refer, param_button_quit]
        buttons["layout"][1] = len(array_buttons)
        for key in array_buttons[0].keys(): buttons[key + "s"] = list(map(lambda b: b[key], array_buttons))
        # print("\nINIT MENU GENERAL BUTTONS" + "-" * 200)
        # print(*list(map(lambda x: f"{x[0]}: {x[1]}", buttons.items())),
        #       sep="\n")  # ({len(x[1]) if type(x[1]) not in (int, pygame.font.Font, None) else None})
        # print("-" * 200 + "\n")
        buttons["buttons"] = self.parent.buttons(coords=buttons["coords"],
                                                              layout=buttons["layout"],
                                                              color=buttons["color"],
                                                              fonts=[buttons["font"]] * len(array_buttons),
                                                              texts=buttons["texts"],
                                                              funcs=buttons["funcs"])
        self.buttons.append(buttons)

        self.button_music = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (1400, 200, 80, 50),
            "text": "выкл",
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.music_off_or_on()
        }
        if self.button_music["text"] == "выкл":
            self.parent.music_play = False
        elif self.button_music["text"] == "вкл":
            self.parent.music_play = True
        self.button_music["button"] = self.parent.button(coords=self.button_music["coords"],
                                                     text=self.button_music["text"],
                                                     color=self.button_music["color"],
                                                     font=self.button_music["font"],
                                                     func=self.button_music["func"])
        self.buttons.append(self.button_music)

    def init_labels(self):
        label_title = {
            "coords": (0, 50),
            "text": "Office Nightmare",
            "font": pygame.font.Font(self.base_style["font_path"], 80)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                      text=label_title["text"],
                                                      font=label_title["font"])
        label_title["label"], label_title["coords"] = self.parent.align(label_title["label"], label_title["coords"],
                                                            type_blit=False, type_align="horizontal")
        self.labels.append(label_title)

        label_music = {
            "coords": (1250, 200+5),
            "text": "музыка",
            "font": pygame.font.Font(self.base_style["font_path"], 40)
        }
        label_music["label"] = self.parent.label_text(coords=label_music["coords"],
                                                      text=label_music["text"],
                                                      font=label_music["font"])
        self.labels.append(label_music)


    def delete_all(self):
        # print("MENU ", *list(map(lambda x: x["text"] if "text" in x.keys() else x["texts"], self.buttons)), sep=" ")
        for _ in range(len(self.buttons)):
            del self.buttons[0]
        del self.button_music
        del self.buttons


    def draw(self):
        self.parent.display.fill(self.base_style["colors"]["dark"])
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])

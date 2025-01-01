import pygame

class Menu:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent
        self.labels = []
        self.buttons = []
        self.init_buttons_general()
        self.init_label_title()

    def init_buttons_general(self):
        button = {
            "font": pygame.font.Font(self.base_style["font_path"], 40),
                "coords": (365, 200, 290, 100),
            "layout": [1, 3],
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            }
        }
        param_button_start = {"text": "играть", "func":lambda: self.parent.display_change("game")}
        param_button_refer = {"text": "справка", "func":lambda: self.parent.display_change("refer")}
        param_button_quit = {"text": "выход", "func":self.parent.display_quit}
        array_buttons = [param_button_start, param_button_refer, param_button_quit]
        button["layout"][1] = len(array_buttons)

        for key in array_buttons[0].keys(): button[key+"s"] = list(map(lambda b: b[key], array_buttons))
        button["buttons"] = self.parent.buttons(coords=button["coords"],
                                                          layout=button["layout"],
                                                          color=button["color"],
                                                          fonts=[button["font"]] * len(array_buttons),
                                                          texts=button["texts"],
                                                          funcs=button["funcs"])
        self.buttons.append(button)

        button_musik = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (900, 720, 80, 50),
            "text": "муз",
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.music_off_or_on()
        }
        button_musik["button"] = self.parent.button(coords=button_musik["coords"],
                                                     text=button_musik["text"],
                                                     color=button_musik["color"],
                                                     font=button_musik["font"],
                                                     func=button_musik["func"])
        self.buttons.append(button_musik)

    def init_label_title(self):
        label_title = {
            "coords": (350, 80),
            "text": " Ultimate",
            "font": pygame.font.Font(self.base_style["font_path"], 80)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                      text=label_title["text"],
                                                      font=label_title["font"])
        label_title["label"], label_title["coords"] = self.parent.align(label_title["label"], label_title["coords"],
                                                            type_blit=False, type_align="horizontal")
        self.labels.append(label_title)


    def delete_all(self):
        del self.buttons


    def draw(self):
        self.parent.display.fill(self.base_style["colors"]["dark"])
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])

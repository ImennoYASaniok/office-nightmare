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
        self.buttons = {
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
        self.buttons["layout"][1] = len(array_buttons)

        for key in array_buttons[0].keys(): self.buttons[key+"s"] = list(map(lambda b: b[key], array_buttons))
        self.buttons["buttons"] = self.parent.buttons(coords=self.buttons["coords"],
                                                          layout=self.buttons["layout"],
                                                          color=self.buttons["color"],
                                                          fonts=[self.buttons["font"]] * len(array_buttons),
                                                          texts=self.buttons["texts"],
                                                          funcs=self.buttons["funcs"])

    def init_label_title(self):
        label_title = {
            "coords": (350, 80),
            "text": "Office Nightmare",
            "font": pygame.font.Font(self.base_style["font_path"], 80)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                      text=label_title["text"],
                                                      font=label_title["font"])
        # label_title["text"] = self.parent.add_distance_between_letters(label_title["text"], 2)
        print(label_title["text"])
        self.labels.append(label_title)


    def delete_all(self):
        del self.buttons


    def draw(self):
        self.parent.display.fill(self.base_style["colors"]["dark"])
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])
import pygame

class Menu:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent

        self.commands = {
            pygame.KEYDOWN: {
                pygame.K_ESCAPE: self.parent.display_quit,
            }
        }

        with open("files/base_refer.txt", "r", encoding="utf-8") as file_data:
            self.base_refer = list(file_data.readlines())

        name = "menu"
        self.back_images = list(map(lambda x: pygame.image.load(f"sprites/{name}_logo/{name}_logo_{x}.jpg").convert(), range(2 + 1)))
        self.delta_size_image = 100
        self.back_images = list(map(lambda x: pygame.transform.scale(x, [x.get_rect().w + self.delta_size_image, x.get_rect().h + self.delta_size_image]), self.back_images))
        # self.back_images = list(map(lambda x: pygame.transform.scale(x, self.parent.resize_image([x.get_rect().w, x.get_rect().h])), self.back_images))
        self.for_back_image = {
            "var": 0,
            "end": len(self.back_images),
            "count": 0,
            "freq": 15,
        }

        self.labels = []
        self.buttons = []
        self.init_buttons()
        self.init_labels()

    def init_buttons(self):
        buttons = {
            "font": pygame.font.Font(self.base_style["font_path"], 40),
            "coords": (250, 200, 250, 100),
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

        x, y = 540, 200
        size_text = 30
        delta_y = size_text
        i = 0
        for s in self.base_refer:
            if s not in ("", "\n", None):
                label_i = {
                    "coords": (x, y),
                    "text": s,
                    "font": pygame.font.Font(self.base_style["font_path"], size_text),
                }
                if i + 3 >= len(self.base_refer):
                    label_i["color"] = self.base_style["colors"]["base1"]
                else:
                    label_i["color"] = self.base_style["colors"]["light"]
                label_i["label"] = self.parent.label_text(coords=label_i["coords"],
                                                              text=label_i["text"],
                                                              font=label_i["font"],
                                                              color=label_i["color"])
                self.labels.append(label_i)
            i += 1
            y += delta_y


    def delete_all(self):
        # print("MENU ", *list(map(lambda x: x["text"] if "text" in x.keys() else x["texts"], self.buttons)), sep=" ")
        for _ in range(len(self.buttons)):
            del self.buttons[0]
        del self.buttons


    def draw(self):
        self.parent.display.fill(self.base_style["colors"]["dark"])

        x_mouse, y_mouse = pygame.mouse.get_pos()
        delta_x = x_mouse // self.delta_size_image * 3
        delta_y = y_mouse // self.delta_size_image * 3
        self.parent.display.blit(self.back_images[self.for_back_image["var"]], (0-delta_x, -80-delta_y))
        if self.for_back_image["count"] >= self.for_back_image["freq"]:
            self.for_back_image["count"] = 0
            self.for_back_image["var"] += 1
        if self.for_back_image["var"] >= self.for_back_image["end"]:
            self.for_back_image["var"] = 0
        self.for_back_image["count"] += 1

        # self.parent.display.fill(self.base_style["colors"]["dark"])
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])

    def check_event(self, event):
        if event.type in self.commands.keys():
            if type(self.commands[event.type]) == dict:
                if event.key in self.commands[event.type].keys():
                    self.commands[event.type][event.key]()

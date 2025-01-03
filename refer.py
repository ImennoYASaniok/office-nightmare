import pygame

main_text = ('Добро пожаловать в игру Office NightMare',
             'здесь скоро будет справка')

class Refer:
    def __init__(self, parent, base_style):
        self.labels = []
        self.base_style = base_style
        self.parent = parent
        self.buttons = []

        self.init_label_title()
        self.init_main_text()
        self.init_button_menu()


    def init_label_title(self):
        label_title = {
            "coords": (100, 10),
            "text": "Справка",
            "font": pygame.font.Font(self.base_style["font_path"], 50)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                      text=label_title["text"],
                                                      font=label_title["font"])
        label_title["label"], label_title["coords"] = self.parent.align(label_title["label"], label_title["coords"],
                                                                        inacurr=-20, type_blit=False,
                                                                        type_align="horizontal")
        self.labels.append(label_title)

    def init_main_text(self):
        txt = [text for text in main_text]
        for i, mini_t in enumerate(txt):
            label_title = {
                "coords": (25, 80 + i * 30),
                "text": mini_t,
                "font": pygame.font.Font(self.base_style["font_path"], 30)
            }
            label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                          text=label_title["text"],
                                                          font=label_title["font"])
            # label_title["label"], label_title["coords"] = self.parent.align(label_title["label"], label_title["coords"],
            #                                                                inacurr=-20, type_blit=False)
            self.labels.append(label_title)

    def init_button_menu(self):
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
            "inv_clr": 1
        }
        button_ToMenu["button"] = self.parent.button(coords=button_ToMenu["coords"],
                                           text=button_ToMenu["text"],
                                           color=button_ToMenu["color"],
                                           font=button_ToMenu["font"],
                                           func=button_ToMenu["func"])
        self.buttons.append(button_ToMenu)

    def delete_all(self):
        # print("REFER ", *list(map(lambda x: x["text"] if "text" in x.keys() else x["texts"], self.buttons)), sep=" ")
        for i in range(len(self.buttons)): del self.buttons[i]
        for i in self.labels: del i

    def draw(self):
        self.parent.display.fill(self.base_style["colors"]["dark"])
        # for i in self.buttons: i.show()
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])

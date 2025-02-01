import pygame
from pygame_widgets.slider import Slider

class Refer:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent

        self.commands = {
            pygame.KEYDOWN: {
                pygame.K_ESCAPE: lambda: self.parent.display_change("menu"),
            }
        }

        with open("files/refer.txt", "r", encoding="utf-8") as file_data:
            self.main_text = list(file_data.readlines())

        self.labels = []
        self.buttons = []
        self.sliders = []

        name = "refer"
        self.back_images = list(map(lambda x: pygame.image.load(f"sprites/{name}_logo/{name}_logo_{x}.jpg").convert(), range(12 + 1)))
        self.back_images = list(map(lambda x: pygame.transform.scale(x, self.parent.resize_image([x.get_rect().w, x.get_rect().h])), self.back_images))
        self.delta_size_image = 100
        self.back_images = list(map(lambda x: pygame.transform.scale(x, [x.get_rect().w+self.delta_size_image, x.get_rect().h+self.delta_size_image]), self.back_images))
        # print(self.back_images.)
        self.for_back_image = {
            "var": 0,
            "end": len(self.back_images),
            "count": 0,
            "freq": 10,
        }
        self.init_label_title()
        self.init_main_text()
        self.init_button_menu()
        self.init_slider()

    def init_slider(self):
        # ------ Слайдер
        w = 30
        self.base_slider = {
            "coords": (self.parent.display_w - w - 10, 80, w, self.parent.display_h - 110),
            "color": {
                "base_part": self.base_style["colors"]["base2"],
                "handle": self.base_style["colors"]["base1"],
                "border": self.base_style["colors"]["light"]
            },
            "min": 0, "max": self.prefix_i, "step": 1, "start": self.prefix_i,
            "vertical": True,
            "thickness": 10,
        }
        self.base_slider["slider"] = self.parent.slider(coords=self.base_slider["coords"],
                                              min_slider=self.base_slider["min"], max_slider=self.base_slider["max"], step=self.base_slider["step"], start=self.base_slider["start"],
                                              color=self.base_slider["color"]["base_part"], handle_color=self.base_slider["color"]["handle"],
                                              vertical=self.base_slider["vertical"],
                                              border_color=self.base_slider["color"]["border"], border_thickness=self.base_slider["thickness"])
        self.sliders.append(self.base_slider)


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
        txt = self.main_text
        self.prefix_i = 0
        for mini_t in txt:
            if mini_t not in ["", "\n"]:
                label_title = {
                    "coords": (25, 80 + self.prefix_i),
                    "text": mini_t,
                    "font": pygame.font.Font(self.base_style["font_path"], 25)
                }
                # print([label_title["text"]])
                delta_color = -50
                label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                              text=label_title["text"],
                                                              font=label_title["font"],) # color=(249+delta_color,125+delta_color,61+delta_color)
                self.labels.append(label_title)
                self.prefix_i += 30
            else:
                self.prefix_i += 20

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
        del self.base_slider
        del self.sliders

    def draw(self):
        self.parent.display.fill(self.base_style["colors"]["dark"])

        val_slider = self.base_slider["slider"].getValue()

        x_mouse, y_mouse = pygame.mouse.get_pos()
        delta_x = x_mouse // self.delta_size_image * 3
        delta_y = y_mouse // self.delta_size_image * 3
        self.parent.display.blit(self.back_images[self.for_back_image["var"]], (-delta_x, (self.base_slider["max"]-val_slider)//self.delta_size_image*5-self.delta_size_image-delta_y)) #  delta_size
        if self.for_back_image["count"] >= self.for_back_image["freq"]:
            self.for_back_image["count"] = 0
            self.for_back_image["var"] += 1
        if self.for_back_image["var"] >= self.for_back_image["end"]:
            self.for_back_image["var"] = 0
        self.for_back_image["count"] += 1
        # print(self.for_back_image["var"], self.for_back_image["count"])

        list(map(lambda slider: slider["slider"].draw(), self.sliders))
        # for i in self.buttons: i.show()
        for i in self.labels: self.parent.display.blit(i["label"], [i["coords"][0], i["coords"][1]+val_slider-self.base_slider["max"]])

    def check_event(self, event):
        if event.type in self.commands.keys():
            if type(self.commands[event.type]) == dict:
                if event.key in self.commands[event.type].keys():
                    self.commands[event.type][event.key]()

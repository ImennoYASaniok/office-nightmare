import pygame


class Settings:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent

        self.commands = {
            pygame.KEYDOWN: {
                pygame.K_ESCAPE: lambda: self.parent.display_change("menu"),
            }
        }

        name = "settings"
        self.back_images = list(map(lambda x: pygame.image.load(f"sprites/{name}_logo/{name}_logo_{x}.jpg").convert(), range(2 + 1)))
        self.delta_size_image = 100
        self.back_images = list(map(lambda x: pygame.transform.scale(x, [x.get_rect().w + self.delta_size_image, x.get_rect().h + self.delta_size_image]),self.back_images))
        self.for_back_image = {
            "var": 0,
            "end": len(self.back_images),
            "count": 0,
            "freq": 10,
        }
        self.init_frontend()

    def init_frontend(self):
        self.labels = []
        self.buttons = []
        self.lines = []

        # !!! Если нужно будет создавать много label -> сделай init_label_title общей для всех и возвращай label_title
        # ------ Переменные
        SPACES = {"title":10, "point":30, "line":30} # Вертикальные пробелы между объектами
        INDENTS = [10, 10] # Отступ | [начало, конец]
        WIDTH_LINE = 4
        height_base = 0
        SIZE_LABEL = 35
        button_w, button_h = 80, 50

        # ------ Кнопка
        button_ToMenu = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (self.parent.display_w - button_w, 0, button_w, button_h),
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
        # ------ Надпись
        label_title = {
            "coords": (600, 20),
            "text":"Настройки",
            "font": pygame.font.Font(self.base_style["font_path"], 50)
        }
        label_title["label"] = self.parent.label_text(coords=label_title["coords"],
                                                      text=label_title["text"],
                                                      font=label_title["font"])
        label_title["label"], label_title["coords"] = self.parent.align(label_title["label"], label_title["coords"],
                                                                        inacurr=0, type_blit=False,
                                                                        type_align="horizontal")
        height_base += label_title["coords"][1]
        height_base += label_title["label"].get_height()
        self.labels.append(label_title)
        # ------ Линия
        height_base += SPACES["title"]
        line_horizontal_1 = {
            "color": self.base_style["colors"]["base1"],
            "start_pos": [0, height_base],
            "end_pos": [self.parent.display_w, height_base],
            "width": WIDTH_LINE
        }
        height_base += line_horizontal_1["width"]
        self.lines.append(line_horizontal_1)

        # ====== БЛОК ОБЩИЕ НАСТРОЙКИ
        # ------ Надпись
        height_base += SPACES["title"]
        label_general_sett = {
                "coords": [INDENTS[0], height_base],
            "text": "Общие:",
            "font": pygame.font.Font(self.base_style["font_path"], 45)
        }
        label_general_sett["label"] = self.parent.label_text(coords=label_general_sett["coords"],
                                                      text=label_general_sett["text"],
                                                      font=label_general_sett["font"])
        label_general_sett["label"], label_general_sett["coords"] = self.parent.align(label_general_sett["label"], label_general_sett["coords"],
                                                                        inacurr=0, type_blit=False,
                                                                        type_align="horizontal")
        height_base += label_general_sett["label"].get_height()
        self.labels.append(label_general_sett)
        # =-=-=- Строка
        # ------ Надпись
        height_base += SPACES["point"]
        label_music = {
            "coords": [INDENTS[0], height_base],
            "text": "музыка",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_music["label"] = self.parent.label_text(coords=label_music["coords"],
                                                      text=label_music["text"],
                                                      font=label_music["font"])
        self.labels.append(label_music)
        # ------ Кнопка
        self.button_music = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": (self.parent.display_w-button_w-INDENTS[1], height_base, button_w, button_h),
            "text": "выкл",
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.change_music()
        }
        if self.parent.settings_var["music_play"] == 0:
            self.button_music["text"] = "выкл"
        elif self.parent.settings_var["music_play"] == 1:
            self.button_music["text"] = "вкл"
        self.button_music["button"] = self.parent.button(coords=self.button_music["coords"],
                                                         text=self.button_music["text"],
                                                         color=self.button_music["color"],
                                                         font=self.button_music["font"],
                                                         func=self.button_music["func"])
        self.buttons.append(self.button_music)
        height_base += label_music["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        # ------ Надпись
        height_base += SPACES["point"]
        label_color = {
            "coords": [INDENTS[0], height_base],
            "text": "тема",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_color["label"] = self.parent.label_text(coords=label_color["coords"],
                                                      text=label_color["text"],
                                                      font=label_color["font"])
        self.labels.append(label_color)
        # ------ Кнопка
        delta_width = 50
        self.button_color = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": [self.parent.display_w - INDENTS[1] - button_w - delta_width, height_base, button_w + delta_width,
                       button_h],
            "text": "светлая",
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.change_color()
        }
        if self.parent.settings_var["color"] == 0:
            self.button_color["text"] = "светлая"
        elif self.parent.settings_var["color"] == 1:
            self.button_color["text"] = "тёмная"
        self.button_color["button"] = self.parent.button(coords=self.button_color["coords"],
                                                         text=self.button_color["text"],
                                                         color=self.button_color["color"],
                                                         font=self.button_color["font"],
                                                         func=self.button_color["func"])
        self.buttons.append(self.button_color)
        height_base += label_color["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        # ------ Надпись
        height_base += SPACES["point"]
        label_format_screen = {
            "coords": [INDENTS[0], height_base],
            "text": "полноэкранный режим",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_format_screen["label"] = self.parent.label_text(coords=label_format_screen["coords"],
                                                      text=label_format_screen["text"],
                                                      font=label_format_screen["font"])
        self.labels.append(label_format_screen)
        # ------ Кнопка
        delta_width = 50
        self.button_format_screen = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": [self.parent.display_w - INDENTS[1] - button_w - delta_width, height_base, button_w + delta_width,
                       button_h],
            "text": "выкл",
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.change_format_screen()
        }
        if self.parent.settings_var["format_screen"] == 0:
            self.button_format_screen["text"] = "выкл"
        elif self.parent.settings_var["format_screen"] == 1:
            self.button_format_screen["text"] = "вкл"
        self.button_format_screen["button"] = self.parent.button(coords=self.button_format_screen["coords"],
                                                         text=self.button_format_screen["text"],
                                                         color=self.button_format_screen["color"],
                                                         font=self.button_format_screen["font"],
                                                         func=self.button_format_screen["func"])
        self.buttons.append(self.button_format_screen)
        height_base += label_color["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        # ------ Надпись
        height_base += SPACES["point"]
        label_difficulty = {
            "coords": [INDENTS[0], height_base],
            "text": "сложность",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_difficulty["label"] = self.parent.label_text(coords=label_difficulty["coords"],
                                                              text=label_difficulty["text"],
                                                              font=label_difficulty["font"])
        self.labels.append(label_difficulty)
        # ------ Кнопка
        delta_width = 50
        self.button_difficulty = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": [self.parent.display_w - INDENTS[1] - button_w - delta_width, height_base, button_w + delta_width,
                       button_h],
            "text": "сложная",
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.change_difficulty()
        }
        if self.parent.settings_var["difficulty"] == 0:
            self.button_difficulty["text"] = "лёгкая"
        elif self.parent.settings_var["difficulty"] == 1:
            self.button_difficulty["text"] = "сложная"
        self.button_difficulty["button"] = self.parent.button(coords=self.button_difficulty["coords"],
                                                                 text=self.button_difficulty["text"],
                                                                 color=self.button_difficulty["color"],
                                                                 font=self.button_difficulty["font"],
                                                                 func=self.button_difficulty["func"])
        self.buttons.append(self.button_difficulty)
        height_base += label_color["label"].get_height()
        # =-=-=-
        # ------ Линия
        height_base += SPACES["line"]
        line_horizontal_1 = {
            "color": self.base_style["colors"]["base1"],
            "start_pos": [0, height_base],
            "end_pos": [self.parent.display_w, height_base],
            "width": WIDTH_LINE
        }
        height_base += line_horizontal_1["width"]
        self.lines.append(line_horizontal_1)

        # ====== БЛОК РЕЖИМ РАЗРАБОТЧИКА
        # ------ Надпись
        height_base += SPACES["title"]
        label_general_sett = {
            "coords": [INDENTS[0], height_base],
            "text": "Режим разработчика:",
            "font": pygame.font.Font(self.base_style["font_path"], 45)
        }
        label_general_sett["label"] = self.parent.label_text(coords=label_general_sett["coords"],
                                                             text=label_general_sett["text"],
                                                             font=label_general_sett["font"])
        label_general_sett["label"], label_general_sett["coords"] = self.parent.align(label_general_sett["label"],
                                                                                      label_general_sett["coords"],
                                                                                      inacurr=0, type_blit=False,
                                                                                      type_align="horizontal")
        height_base += label_general_sett["label"].get_height()
        self.labels.append(label_general_sett)
        # =-=-=- Строка
        # ------ Надпись
        height_base += SPACES["point"]
        label_type_dinamic_camera = {
            "coords": [INDENTS[0], height_base],
            "text": "динамическая камера",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_type_dinamic_camera["label"] = self.parent.label_text(coords=label_type_dinamic_camera["coords"],
                                                                      text=label_type_dinamic_camera["text"],
                                                                      font=label_type_dinamic_camera["font"])
        self.labels.append(label_type_dinamic_camera)
        # ------ Кнопка
        delta_width = 50
        self.button_type_dinamic_camera = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": [self.parent.display_w-INDENTS[1]-button_w-delta_width, height_base, button_w+delta_width, button_h],
            "text": "с зоной",
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.change_type_dinamic()
        }
        if self.parent.settings_var["type_dinamic"] == 0:
            self.button_type_dinamic_camera["text"] = "с зоной"
        elif self.parent.settings_var["type_dinamic"] == 1:
            self.button_type_dinamic_camera["text"] = "без зоны"
        self.button_type_dinamic_camera["button"] = self.parent.button(coords=self.button_type_dinamic_camera["coords"],
                                                                       text=self.button_type_dinamic_camera["text"],
                                                                       color=self.button_type_dinamic_camera["color"],
                                                                       font=self.button_type_dinamic_camera["font"],
                                                                       func=self.button_type_dinamic_camera["func"])
        self.buttons.append(self.button_type_dinamic_camera)
        height_base += label_type_dinamic_camera["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        # ------ Надпись
        height_base += SPACES["point"]
        label_draw_dinamic_camera = {
            "coords": [INDENTS[0], height_base],
            "text": "отрисовка динамической зоны",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_draw_dinamic_camera["label"] = self.parent.label_text(coords=label_draw_dinamic_camera["coords"],
                                                                    text=label_draw_dinamic_camera["text"],
                                                                    font=label_draw_dinamic_camera["font"])
        self.labels.append(label_draw_dinamic_camera)
        # ------ Кнопка
        delta_width = 50
        self.button_draw_dinamic_camera = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": [self.parent.display_w - INDENTS[1] - button_w - delta_width, height_base, button_w + delta_width, button_h],
            "text": "выкл",
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.change_draw_dinamic()
        }
        if self.parent.settings_var["do_draw_dinamic_zone"] == 0:
            self.button_draw_dinamic_camera["text"] = "выкл"
        elif self.parent.settings_var["do_draw_dinamic_zone"] == 1:
            self.button_draw_dinamic_camera["text"] = "вкл"
        self.button_draw_dinamic_camera["button"] = self.parent.button(coords=self.button_draw_dinamic_camera["coords"],
                                                                       text=self.button_draw_dinamic_camera["text"],
                                                                       color=self.button_draw_dinamic_camera["color"],
                                                                       font=self.button_draw_dinamic_camera["font"],
                                                                       func=self.button_draw_dinamic_camera["func"])
        self.buttons.append(self.button_draw_dinamic_camera)
        height_base += label_draw_dinamic_camera["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        # ------ Надпись
        height_base += SPACES["point"]
        label_character_energy = {
            "coords": [INDENTS[0], height_base],
            "text": "энергия у персонажа",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_character_energy["label"] = self.parent.label_text(coords=label_character_energy["coords"],
                                                                    text=label_character_energy["text"],
                                                                    font=label_character_energy["font"])
        self.labels.append(label_character_energy)
        # ------ Кнопка
        delta_width = 50
        self.button_character_energy = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": [self.parent.display_w - INDENTS[1] - button_w - delta_width, height_base, button_w + delta_width,
                       button_h],
            "text": "выкл",
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.change_character_energy()
        }
        if self.parent.settings_var["character_energy"] == 0:
            self.button_character_energy["text"] = "выкл"
        elif self.parent.settings_var["character_energy"] == 1:
            self.button_character_energy["text"] = "вкл"
        self.button_character_energy["button"] = self.parent.button(coords=self.button_character_energy["coords"],
                                                                       text=self.button_character_energy["text"],
                                                                       color=self.button_character_energy["color"],
                                                                       font=self.button_character_energy["font"],
                                                                       func=self.button_character_energy["func"])
        self.buttons.append(self.button_character_energy)
        height_base += label_character_energy["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        # ------ Надпись
        height_base += SPACES["point"]
        label_draw_map = {
            "coords": [INDENTS[0], height_base],
            "text": "отрисовка карты путей к персонажу",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_draw_map["label"] = self.parent.label_text(coords=label_draw_map["coords"],
                                                                 text=label_draw_map["text"],
                                                                 font=label_draw_map["font"])
        self.labels.append(label_draw_map)
        # ------ Кнопка
        delta_width = 50
        self.button_draw_map = {
            "font": pygame.font.Font(self.base_style["font_path"], 30),
            "coords": [self.parent.display_w - INDENTS[1] - button_w - delta_width, height_base, button_w + delta_width,
                       button_h],
            "text": "выкл",
            "color": {
                "inactive": self.base_style["colors"]["base1"],
                "hover": self.base_style["colors"]["base2"],
                "pressed": self.base_style["colors"]["light"],
                "text": self.base_style["colors"]["light"]
            },
            "func": lambda: self.parent.change_draw_map()
        }
        if self.parent.settings_var["draw_map"] == 0:
            self.button_draw_map["text"] = "выкл"
        elif self.parent.settings_var["draw_map"] == 1:
            self.button_draw_map["text"] = "вкл"
        self.button_draw_map["button"] = self.parent.button(coords=self.button_draw_map["coords"],
                                                                    text=self.button_draw_map["text"],
                                                                    color=self.button_draw_map["color"],
                                                                    font=self.button_draw_map["font"],
                                                                    func=self.button_draw_map["func"])
        self.buttons.append(self.button_draw_map)
        height_base += label_character_energy["label"].get_height()
        # =-=-=-

    def delete_all(self):
        # print("SETT", *list(map(lambda x: x["text"] if "text" in x.keys() else x["texts"], self.buttons)), sep=" ")
        for _ in range(len(self.buttons)):
            del self.buttons[0]
        del self.button_music
        del self.button_color
        del self.button_format_screen
        del self.button_difficulty
        del self.button_type_dinamic_camera
        del self.button_draw_dinamic_camera
        del self.button_character_energy
        del self.button_draw_map
        del self.buttons

    def draw(self):
        self.parent.display.fill(self.base_style["colors"]["dark"])

        x_mouse, y_mouse = pygame.mouse.get_pos()
        delta_x = x_mouse // self.delta_size_image * 3
        delta_y = y_mouse // self.delta_size_image * 3
        self.parent.display.blit(self.back_images[self.for_back_image["var"]], (0 - delta_x, -80 - delta_y))
        if self.for_back_image["count"] >= self.for_back_image["freq"]:
            self.for_back_image["count"] = 0
            self.for_back_image["var"] += 1
        if self.for_back_image["var"] >= self.for_back_image["end"]:
            self.for_back_image["var"] = 0
        self.for_back_image["count"] += 1

        # Отрисовка надписей
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])
        # Отрисовка линий
        for line in self.lines:
            pygame.draw.line(surface=self.parent.display, color=line["color"],
                             start_pos=line["start_pos"],
                             end_pos=line["end_pos"],
                             width=line["width"])

    def check_event(self, event):
        if event.type in self.commands.keys():
            if type(self.commands[event.type]) == dict:
                if event.key in self.commands[event.type].keys():
                    self.commands[event.type][event.key]()
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
        self.textboxs = {}

        # !!! Если нужно будет создавать много label -> сделай init_label_title общей для всех и возвращай label_title
        # ------ Переменные
        SPACES = {"title":10, "point":30, "line":30} # Вертикальные пробелы между объектами
        INDENTS = [10, 10] # Отступ | [начало, конец]
        WIDTH_LINE = 4
        self.height_base = 0
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
        self.height_base += label_title["coords"][1]
        self.height_base += label_title["label"].get_height()
        self.labels.append(label_title)
        # ------ Линия
        self.height_base += SPACES["title"]
        line_horizontal_1 = {
            "color": self.base_style["colors"]["base1"],
            "start_pos": [0, self.height_base],
            "end_pos": [self.parent.display_w, self.height_base],
            "width": WIDTH_LINE
        }
        self.height_base += line_horizontal_1["width"]
        self.lines.append(line_horizontal_1)

        # ====== БЛОК ОБЩИЕ НАСТРОЙКИ
        # ------ Надпись
        self.height_base += SPACES["title"]
        label_general_sett = {
                "coords": [INDENTS[0], self.height_base],
            "text": "Общие:",
            "font": pygame.font.Font(self.base_style["font_path"], 45)
        }
        label_general_sett["label"] = self.parent.label_text(coords=label_general_sett["coords"],
                                                      text=label_general_sett["text"],
                                                      font=label_general_sett["font"])
        label_general_sett["label"], label_general_sett["coords"] = self.parent.align(label_general_sett["label"], label_general_sett["coords"],
                                                                        inacurr=0, type_blit=False,
                                                                        type_align="horizontal")
        self.height_base += label_general_sett["label"].get_height()
        self.labels.append(label_general_sett)
        # =-=-=- Строка
        # ------ Надпись
        self.height_base += SPACES["point"]
        label_music = {
            "coords": [INDENTS[0], self.height_base],
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
            "coords": (self.parent.display_w-button_w-INDENTS[1], self.height_base, button_w, button_h),
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
        self.height_base += label_music["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        # ------ Надпись
        self.height_base += SPACES["point"]
        label_color = {
            "coords": [INDENTS[0], self.height_base],
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
            "coords": [self.parent.display_w - INDENTS[1] - button_w - delta_width, self.height_base, button_w + delta_width,
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
        self.height_base += label_color["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        # ------ Надпись
        self.height_base += SPACES["point"]
        label_difficulty = {
            "coords": [INDENTS[0], self.height_base],
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
            "coords": [self.parent.display_w - INDENTS[1] - button_w - delta_width, self.height_base, button_w + delta_width,
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
        self.height_base += label_color["label"].get_height()
        # =-=-=-
        # ------ Линия
        self.height_base += SPACES["line"]
        line_horizontal_1 = {
            "color": self.base_style["colors"]["base1"],
            "start_pos": [0, self.height_base],
            "end_pos": [self.parent.display_w, self.height_base],
            "width": WIDTH_LINE
        }
        self.height_base += line_horizontal_1["width"]
        self.lines.append(line_horizontal_1)

        # ====== БЛОК РЕЖИМ РАЗРАБОТЧИКА
        # ------ Надпись
        self.height_base += SPACES["title"]
        label_general_sett = {
            "coords": [INDENTS[0], self.height_base],
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
        self.height_base += label_general_sett["label"].get_height()
        self.labels.append(label_general_sett)
        # =-=-=- Строка
        delta_w = 20
        prefix_w = INDENTS[0]
        # ------ Надпись
        self.height_base += SPACES["point"]
        label_money = {
            "coords": [prefix_w, self.height_base],
            "text": f"кол-во монет (старт - {self.parent.settings_var['start_money']})",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_money["label"] = self.parent.label_text(coords=label_money["coords"],
                                                                    text=label_money["text"],
                                                                    font=label_money["font"])
        self.labels.append(label_money)
        prefix_w += label_money["label"].get_width() + delta_w
        # ------ Поле ввода
        w_textbox_money = 165
        textbox_money = {
            "coords": [prefix_w, self.height_base, w_textbox_money, SPACES["point"]+10],
            "start_text": str(self.parent.settings_var["money"]),
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL),
            "color": {
                "base": self.base_style["colors"]["base1"],
                "dop": self.base_style["colors"]["base2"],
                "back": self.base_style["colors"]["dark"],
            },
        }
        textbox_money["textbox"] = self.parent.create_textbox(
            coords=textbox_money["coords"][0:2], size=textbox_money["coords"][2:4], font=textbox_money["font"],
            base_color=textbox_money["color"]["base"], dop_color=textbox_money["color"]["dop"], back_color=textbox_money["color"]["back"],
            start_text=textbox_money["start_text"],
        )
        self.textboxs["money"] = textbox_money
        prefix_w += textbox_money["coords"][2] + delta_w
        # ------ Надпись
        label_hp = {
            "coords": [prefix_w, self.height_base],
            "text": f"| кол-во hp (старт - {self.parent.settings_var['start_hp']})",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_hp["label"] = self.parent.label_text(coords=label_hp["coords"],
                                                      text=label_hp["text"],
                                                      font=label_hp["font"])
        self.labels.append(label_hp)
        prefix_w += label_hp["label"].get_width() + delta_w
        # ------ Поле ввода
        w_textbox_money = 165
        textbox_hp = {
            "coords": [prefix_w, self.height_base, w_textbox_money, SPACES["point"] + 10],
            "start_text": str(self.parent.settings_var["hp"]),
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL),
            "color": {
                "base": self.base_style["colors"]["base1"],
                "dop": self.base_style["colors"]["base2"],
                "back": self.base_style["colors"]["dark"],
            },
        }
        textbox_hp["textbox"] = self.parent.create_textbox(
            coords=textbox_hp["coords"][0:2], size=textbox_hp["coords"][2:4], font=textbox_hp["font"],
            base_color=textbox_hp["color"]["base"], dop_color=textbox_hp["color"]["dop"],
            back_color=textbox_hp["color"]["back"],
            start_text=textbox_hp["start_text"],
        )
        self.textboxs["hp"] = textbox_hp
        prefix_w += textbox_hp["coords"][2] + delta_w

        self.height_base += label_money["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        delta_w = 20
        prefix_w = INDENTS[0]
        # ------ Надпись
        self.height_base += SPACES["point"]
        label_bullets = {
            "coords": [prefix_w, self.height_base],
            "text": "макс кол-во пуль",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_bullets["label"] = self.parent.label_text(coords=label_bullets["coords"],
                                                      text=label_bullets["text"],
                                                      font=label_bullets["font"])
        self.labels.append(label_bullets)
        prefix_w += label_bullets["label"].get_width() + delta_w
        # ------ Надпись
        label_bullets_pistol = {
            "coords": [prefix_w, self.height_base],
            "text": f"| пистолет (старт - {self.parent.settings_var['start_max_bullets_pistol']})",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_bullets_pistol["label"] = self.parent.label_text(coords=label_bullets_pistol["coords"],
                                                        text=label_bullets_pistol["text"],
                                                        font=label_bullets_pistol["font"])
        self.labels.append(label_bullets_pistol)
        prefix_w += label_bullets_pistol["label"].get_width() + delta_w
        # ------ Поле ввода
        w_textbox_bullets = 165
        textbox_bullets_pistol = {
            "coords": [prefix_w, self.height_base, w_textbox_bullets, SPACES["point"] + 10],
            "start_text": str(self.parent.settings_var["max_bullets_pistol"]),
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL),
            "color": {
                "base": self.base_style["colors"]["base1"],
                "dop": self.base_style["colors"]["base2"],
                "back": self.base_style["colors"]["dark"],
            },
        }
        textbox_bullets_pistol["textbox"] = self.parent.create_textbox(
            coords=textbox_bullets_pistol["coords"][0:2], size=textbox_bullets_pistol["coords"][2:4], font=textbox_bullets_pistol["font"],
            base_color=textbox_bullets_pistol["color"]["base"], dop_color=textbox_bullets_pistol["color"]["dop"],
            back_color=textbox_bullets_pistol["color"]["back"],
            start_text=textbox_bullets_pistol["start_text"],
        )
        self.textboxs["max_bullets_pistol"] = textbox_bullets_pistol
        prefix_w += textbox_bullets_pistol["coords"][2] + delta_w
        # ------ Надпись
        label_bullets_automat = {
            "coords": [prefix_w, self.height_base],
            "text": f"| автомат (старт - {self.parent.settings_var['start_max_bullets_automat']})",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_bullets_automat["label"] = self.parent.label_text(coords=label_bullets_automat["coords"],
                                                               text=label_bullets_automat["text"],
                                                               font=label_bullets_automat["font"])
        self.labels.append(label_bullets_automat)
        prefix_w += label_bullets_automat["label"].get_width() + delta_w
        # ------ Поле ввода
        w_textbox_bullets = 165
        textbox_bullets_automat = {
            "coords": [prefix_w, self.height_base, w_textbox_bullets, SPACES["point"] + 10],
            "start_text": str(self.parent.settings_var["max_bullets_automat"]),
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL),
            "color": {
                "base": self.base_style["colors"]["base1"],
                "dop": self.base_style["colors"]["base2"],
                "back": self.base_style["colors"]["dark"],
            },
        }
        textbox_bullets_automat["textbox"] = self.parent.create_textbox(
            coords=textbox_bullets_automat["coords"][0:2], size=textbox_bullets_automat["coords"][2:4],
            font=textbox_bullets_automat["font"],
            base_color=textbox_bullets_automat["color"]["base"], dop_color=textbox_bullets_automat["color"]["dop"],
            back_color=textbox_bullets_automat["color"]["back"],
            start_text=textbox_bullets_automat["start_text"],
        )
        self.textboxs["max_bullets_automat"] = textbox_bullets_automat
        prefix_w += textbox_bullets_automat["coords"][2] + delta_w

        self.height_base += label_bullets["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        # ------ Надпись
        self.height_base += SPACES["point"]
        label_type_dinamic_camera = {
            "coords": [INDENTS[0], self.height_base],
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
            "coords": [self.parent.display_w-INDENTS[1]-button_w-delta_width, self.height_base, button_w+delta_width, button_h],
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
        self.height_base += label_type_dinamic_camera["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        # ------ Надпись
        self.height_base += SPACES["point"]
        label_character_energy = {
            "coords": [INDENTS[0], self.height_base],
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
            "coords": [self.parent.display_w - INDENTS[1] - button_w - delta_width, self.height_base, button_w + delta_width,
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
        self.height_base += label_character_energy["label"].get_height()
        # =-=-=-
        # =-=-=- Строка
        # ------ Надпись
        self.height_base += SPACES["point"]
        label_draw_map = {
            "coords": [INDENTS[0], self.height_base],
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
            "coords": [self.parent.display_w - INDENTS[1] - button_w - delta_width, self.height_base, button_w + delta_width,
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
        self.height_base += label_character_energy["label"].get_height()
        # =-=-=-

    def delete_all(self):
        # print("SETT", *list(map(lambda x: x["text"] if "text" in x.keys() else x["texts"], self.buttons)), sep=" ")
        for _ in range(len(self.buttons)):
            del self.buttons[0]
        del self.button_music
        del self.button_color
        del self.button_difficulty
        del self.button_type_dinamic_camera
        del self.button_character_energy
        del self.button_draw_map
        del self.buttons
        del self.textboxs

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
        # Отрисовка текстовых полей
        for name, textbox in self.textboxs.items():
            textbox["textbox"].draw()
            if textbox["textbox"].getText().isdigit():
                self.parent.settings_var[name] = int(textbox["textbox"].getText())


    def check_event(self, event):
        if event.type in self.commands.keys():
            if type(self.commands[event.type]) == dict:
                if event.key in self.commands[event.type].keys():
                    self.commands[event.type][event.key]()
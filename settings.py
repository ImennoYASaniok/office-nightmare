import pygame


class Settings:
    def __init__(self, parent, base_style):
        self.base_style = base_style
        self.parent = parent
        self.labels = []
        self.buttons = []
        self.lines = []

        self.init_frontend()

    def init_frontend(self):
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
        label_type_dinamic_camera = {
            "coords": [INDENTS[0], height_base],
            "text": "энергия у персонажа",
            "font": pygame.font.Font(self.base_style["font_path"], SIZE_LABEL)
        }
        label_type_dinamic_camera["label"] = self.parent.label_text(coords=label_type_dinamic_camera["coords"],
                                                                    text=label_type_dinamic_camera["text"],
                                                                    font=label_type_dinamic_camera["font"])
        self.labels.append(label_type_dinamic_camera)
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
        height_base += label_type_dinamic_camera["label"].get_height()
        # =-=-=-


    def delete_all(self):
        # print("SETT", *list(map(lambda x: x["text"] if "text" in x.keys() else x["texts"], self.buttons)), sep=" ")
        for _ in range(len(self.buttons)):
            del self.buttons[0]
        del self.button_music
        del self.button_type_dinamic_camera
        del self.button_draw_dinamic_camera
        del self.button_character_energy
        del self.buttons

    def draw(self):
        self.parent.display.fill(self.base_style["colors"]["dark"])
        # Отрисовка надписей
        for i in self.labels: self.parent.display.blit(i["label"], i["coords"])
        # Отрисовка линий
        for line in self.lines:
            pygame.draw.line(surface=self.parent.display, color=line["color"],
                             start_pos=line["start_pos"],
                             end_pos=line["end_pos"],
                             width=line["width"])
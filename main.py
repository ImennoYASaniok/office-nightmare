import pygame
import pygame_widgets
from pygame_widgets.button import ButtonArray, Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from menu import Menu
from game import Game
from final import Final
from settings import Settings
from refer import Refer

class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        ########### ДИСПЛЕЙ
        self.FPS = 60
        self.running = 1
        self.display_w, self.display_h = 1526, 814 # pygame.display.Info().current_w - 10, pygame.display.Info().current_h - 50
        self.start_display_w, self.start_display_h = self.display_w, self.display_h
        print(self.display_w, self.display_h)
        self.list_active_surface = {'menu': Menu,
                                    'game': Game,
                                    'settings': Settings,
                                    'refer': Refer,
                                    'final': Final}
        self.type_display = "menu"
        self.style = {
            "colors": {
                "light": (255,217,106), # (187, 148, 87),
                "base1": (249,125,61), # (153, 88, 42),
                "base2": (73,181,132), # (111, 29, 27),
                "dark":  (75,39,41), # (67, 40, 24),
                "black": (0, 0, 0)
            },
            "font_path": "fonts/pixel/EpilepsySansBold.ttf",
            "dop_font": pygame.font.SysFont('Arial', 40, bold=True)
            # "fonts111/pixel/DotGothic16-Regular.ttf" - для латиницы слишком растянутый шрифт
            # fonts111/pixel/EpilepsySans.ttf - слишком сжатый текст, особенно при большом масштабе
        }
        self.display = pygame.display.set_mode((self.display_w, self.display_h))
        self.display.fill(self.style["colors"]["dark"])

        ########### МУЗЫКА
        self.musics = {'menu': 'music/menu.mp3',
                       'game': 'music/game.mp3',
                       'final_victory': 'music/final_victory.mp3',
                       'final_fail': 'music/final_fail.mp3',}
        self.type_music = 0

        ########### АКТИВНОЕ ОКНО
        self.holst = self.list_active_surface[self.type_display](self, self.style)
        self.changes_holst = 0

        ########### НАСТРОЙКИ
        self.settings_var = {
            # ---- Общие настройки
            "music_play": 0,
            # 0 - музыка играет
            # 1 - музыка не играет
            "color": 0,
            # 0 - светлая
            # 1 - тёмная
            "format_screen": 0,
            # 0 - выкл полно-экранный режим
            # 1 - вкл полно-экранный режим
            # ---- Режим разработчика
            "type_dinamic": 0,
            # 0 - динамическая камера с прямоугольной зоной
            # 1 - постоянная динамическая зона
            "do_draw_dinamic_zone": 0,
            # 0 - отрисовать
            # 1 - не отрисовывать
            "character_energy": 1,
            # 0 - нет энергии у персонажа, может бесконечно бегать по полю
            # 1 - есть энергия у персонажа
            "difficulty": 0, # 1
            # 0 - лёгкий
            # 1 - сложный
            "draw_map": 0,
            # 0 - рисовать
            # 1 - не рисовать
            "unlimited_hp": 0,
            # 0 - не бесконечное hp
            # 1 - бесконечное hp
            "unlimited_pistol": 0,
            # 0 - не бесконечные патроны на пистолете
            # 1 - бесконечные патроны на пистолете
        }

        ########### РЕЗУЛЬТАТ ИГРЫ
        self.type_final = "victory"

        ########### ОСТАЛЬНОЕ
        pygame.display.set_caption("Ultimate")
        self.clock = pygame.time.Clock()

        ########### КОНСТАНТЫ
        self.LAYERS = {
            "start_room": [1500, 1500], # [3000, 3000]
            "meeting_room": [self.display_w, self.display_h],
            "final_boss_room": [self.display_h, self.display_w]
        }

        ########### КОНСТАНТЫ ИГРЫ
        self.const = {
            "count_enemy": {
                "curr": [0, 15, 20],
                "few": [0, 10, 7],
                "many": [0, 15, 20]
            }
        }
        self.const["count_enemy"]["curr"] = self.const["count_enemy"][["few", "many"][self.settings_var["difficulty"]]]


    def buttons(self, coords, layout, texts, color, fonts, funcs):
        check_keys = {
            "inactive": self.style["colors"]["base1"],
            "hover": self.style["colors"]["base2"],
            "pressed": self.style["colors"]["light"],
            "text": self.style["colors"]["light"]
        }
        for k, v in check_keys.items():
            if k not in color.keys():
                color[k] = v
        return ButtonArray(
            self.display,
            coords[0], coords[1], coords[2]*layout[0], coords[3]*layout[1],
            layout,
            texts=texts,
            fonts=fonts,
            colour=color["text"],
            inactiveColours=[color["inactive"]]*len(texts),
            hoverColours=[color["hover"]]*len(texts),
            pressedColours=[color["pressed"]]*len(texts),
            textColours=[color["text"]]*len(texts),
            onClicks=funcs
        )

    def button(self, coords, text, color, font, func, layer=None):
        if layer is None: layer = self.display
        check_keys = {
            "inactive": self.style["colors"]["base1"],
            "hover": self.style["colors"]["base2"],
            "pressed": self.style["colors"]["light"],
            "text": self.style["colors"]["light"]
        }
        for k, v in check_keys.items():
            if k not in color.keys():
                color[k] = v
        # print(*color.items())
        return Button(
            layer,
            coords[0], coords[1], coords[2], coords[3],
            text=text,
            font=font,
            # colour=colour,
            inactiveColour=color["inactive"],
            hoverColour=color["hover"],
            pressedColour=color["pressed"],
            textColour=color["text"],
            onClick=func
        )

    def label_text(self, coords, text, font, color=False, type_blit=True):
        color = self.style["colors"]["light"] if not color else color
        f = font
        res_label = f.render(text, True, color)
        if type_blit == True: self.display.blit(res_label, coords)
        # pygame.display.update()
        return res_label

    def create_textbox(self, coords, size, border_colour=(0, 0, 0), text_colour=(0, 0, 0), r=10, bd=5):
        textbox = TextBox(
        self.display,
        x=coords[0],
        y=coords[1],
        width=size[0],
        height=size[1],
        fontSize=50,
        borderColour=border_colour,
        textColour=text_colour,
        radius=r,
        borderThickness=bd)
        return textbox

    def slider(self, coords, color, handle_color, min, max, step, border_color, border_thickness=0, start=None, vertical=False, layer=None):
        if layer is None: layer = self.display
        if start is None: start = (min + max) // 2
        return Slider(layer,
                      coords[0], coords[1], coords[2], coords[3],
                      min=min, max=max, step=step, initial=start,
                      colour=color, handleColour=handle_color,
                      vertical=vertical, handleRadius=int(coords[2 if vertical else 3] / 1.5),
                      borderColour=border_color, borderThickness=border_thickness)

    def align(self, obj, coords, inacurr=(0, 0), type_blit=False, type_align="center"):
        if type(coords) == tuple: coords = list(coords)
        inacurr_w, inacurr_h = 0, 0
        if type(inacurr) == int: inacurr_w = inacurr
        if type(inacurr) == tuple: inacurr = list(inacurr)
        if type(inacurr) == list:
            if len(inacurr) == 1: inacurr_w = inacurr[0]
            elif len(inacurr) == 2: inacurr_w, inacurr_h = inacurr

        if type_align == "horizontal":
            coords[0] = (self.display.get_width() - obj.get_width()) // 2 + inacurr_w
        elif type_align == "vertical":
            coords[1] = (self.display.get_height() - obj.get_height()) // 2 + inacurr_h
        elif type_align == "center":
            coords[0] = (self.display.get_width() - obj.get_width()) // 2 + inacurr_w
            coords[1] = (self.display.get_height() - obj.get_height()) // 2 + inacurr_h
        else:
            raise TypeError("Align type must be 'horizontal' or 'vertical' or 'center'")
        if type_blit == True:
            if type(obj) == pygame.surface.Surface:
                self.display.blit(obj, coords)
        return obj, coords

    def resize_image(self, size, type_side="width"):
        print(size)
        if type_side == "width":
            return (self.display_w, int(size[0] * (self.display_h / size[1])))
        elif type_side == "height":
            return (int(size[0] * (self.display_h / size[1])), self.display_w)

    def format_commands(self, commands):
        res_commands = {}
        for type_key, type_val in commands.items():
            if type(type_val) in (tuple, list, dict):
                res_commands[type_key] = {}
                for key, val in type_val.items():
                    if type(key) in (list, tuple):
                        for mini_key in key: res_commands[type_key][mini_key] = val
                    else:
                        res_commands[type_key][key] = val
            else:
                res_commands[type_key] = type_val
        return res_commands

    def display_quit(self):
        self.running = 0

    def display_change(self, type_display, dop_type=None):
        self.changes_holst = 1
        if dop_type != None: 
            if type_display == "final":
                self.type_final = dop_type
                print("CHANGE FINAL", self.type_final)
        self.type_display = type_display

    def view_logo(self):
        logo = pygame.image.load('sprites/logo.png')
        logo = pygame.transform.scale(logo, (logo.get_width() // (logo.get_height()/self.display_h), self.display_h))
        self.display.fill((0, 0, 0))
        self.display.blit(logo, ((self.display_w-logo.get_width()) // 2, 0))
        pygame.display.flip()
        pygame.time.wait(1000)

    def set_music(self):
        if self.type_display == "menu":
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.load(self.musics['menu'])
            pygame.mixer.music.play(-1)
        elif self.type_display == "final":
            pygame.mixer.music.set_volume(0.3)
            if self.type_final == "victory":
                pygame.mixer.music.load(self.musics['final_victory'])
            elif self.type_final == "fail":
                pygame.mixer.music.load(self.musics['final_fail'])
            pygame.mixer.music.play()
            pygame.mixer.music.unpause()


    def show(self):
        self.view_logo()
        pygame.mixer.music.load(self.musics['menu'])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        while self.running:
            if self.changes_holst:
                if self.type_display == 'game':
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.pause()
                self.holst.delete_all()
                if self.type_display == "final":
                    self.holst = self.list_active_surface[self.type_display](self, self.style, self.type_final)
                else:
                    self.holst = self.list_active_surface[self.type_display](self, self.style)
                self.changes_holst = 0

            self.events = pygame.event.get()

            if self.type_display not in ('game', 'final'):
                if self.settings_var["music_play"]:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

            self.holst.draw()

            for event in self.events:
                if event.type == pygame.QUIT: self.running = False
                self.holst.check_event(event)
            self.clock.tick(self.FPS)
            pygame_widgets.update(self.events)
            pygame.display.update()

    def change_music(self):
        self.settings_var["music_play"] = not self.settings_var["music_play"]
        self.holst.button_music["button"].setText(["выкл", "вкл"][self.settings_var["music_play"]])

    def change_type_dinamic(self):
        self.settings_var["type_dinamic"] = not self.settings_var["type_dinamic"]
        self.holst.button_type_dinamic_camera["button"].setText(["с зоной", "без зоны"][self.settings_var["type_dinamic"]])

    def change_draw_dinamic(self):
        self.settings_var["do_draw_dinamic_zone"] = not self.settings_var["do_draw_dinamic_zone"]
        self.holst.button_draw_dinamic_camera["button"].setText(["выкл", "вкл"][self.settings_var["do_draw_dinamic_zone"]])

    def change_character_energy(self):
        self.settings_var["character_energy"] = not self.settings_var["character_energy"]
        self.holst.button_character_energy["button"].setText(["выкл", "вкл"][self.settings_var["character_energy"]])

    def change_draw_map(self):
        self.settings_var["draw_map"] = not self.settings_var["draw_map"]
        self.holst.button_draw_map["button"].setText(["выкл", "вкл"][self.settings_var["draw_map"]])

    def change_unlimited_hp(self):
        self.settings_var["unlimited_hp"] = not self.settings_var["unlimited_hp"]
        self.holst.button_unlimited_hp["button"].setText(["выкл", "вкл"][self.settings_var["unlimited_hp"]])

    def change_color(self):
        self.settings_var["color"] = not self.settings_var["color"]
        if self.settings_var["color"] == 0:
            self.style["colors"] = {
                "light": (255,217,106), # (187, 148, 87),
                "base1": (249,125,61), # (153, 88, 42),
                "base2": (73,181,132), # (111, 29, 27),
                "dark":  (75,39,41), # (67, 40, 24),
                "black": (0, 0, 0)
            }
        else:
            self.style["colors"] = {
                "light": (249, 125, 61),  # (187, 148, 87),
                "base1": (255,217,106),  # (153, 88, 42),
                "base2": (73, 181, 132),  # (111, 29, 27),
                "dark": (75, 39, 41),  # (67, 40, 24),
                "black": (0, 0, 0)
            }
        self.holst.init_frontend()
        self.holst.button_color["button"].setText(["светлая", "тёмная"][self.settings_var["color"]])

    def change_format_screen(self):
        self.settings_var["format_screen"] = not self.settings_var["format_screen"]
        if self.settings_var["format_screen"] == 0:
            self.display_w, self.display_h = self.start_display_w, self.start_display_h
            self.display = pygame.display.set_mode((self.display_w, self.display_h))
        else:
            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.display_w, self.display_h = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.holst.delete_all()
        self.holst.init_frontend()
        self.holst.button_format_screen["button"].setText(["выкл", "вкл"][self.settings_var["format_screen"]])

if __name__ == "__main__":
    menu = Main()
    menu.show()
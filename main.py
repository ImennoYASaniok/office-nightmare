import pygame
import pygame_widgets
from pygame_widgets.button import ButtonArray, Button
from pygame_widgets.textbox import TextBox
import numpy as np

from menu import Menu
from game import Game
from final import Final
from settings import Settings
from refer import Refer

# 35% моего ЦП при запуске игры съедает виджеты библиотеки pygame_widgets, в дальнейшем это может стать проблемой оптимизации
class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.display_w, self.display_h = pygame.display.Info().current_w-10,pygame.display.Info().current_h-50
        self.FPS = 60

        self.user = None


        self.running = 1
        #self.type_display, self.flag_type_display = "menu", 1 # 0 - None | 1 - menu | 2 - game | 3 - final
        self.type_display = "menu"
        self.style = {
            "colors": {
                "light": (187, 148, 87),
                "base1": (153, 88, 42),
                "base2": (111, 29, 27),
                "dark": (67, 40, 24),
                "black": (0, 0, 0)
            },
            "font_path": "fonts/pixel/EpilepsySans.ttf",
            # норм шрифта:
            # fonts/pixel/EpilepsySansBold.ttf - немного слипаются буквы, но норм
            #
            # так себе:
            # fonts/pixel/DotGothic16-Regular.ttf - для латиницы слишком растянутый шрифт
            # fonts/pixel/EpilepsySans.ttf - слишком сжатый текст, особенно при большом масштабе
        }

        self.display = pygame.display.set_mode((self.display_w, self.display_h))

        self.display.fill(self.style["colors"]["dark"])
        pygame.display.set_caption("Ultimate")
        self.clock = pygame.time.Clock()

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
            self.display,  # Surface to place button array on
            coords[0], coords[1], coords[2]*layout[0], coords[3]*layout[1],
            layout,
            # border=100,  # Distance between buttons and edge of array
            texts=texts,
            fonts=fonts,
            # colour=color["colour"],
            inactiveColours=[color["inactive"]]*len(texts),  # Colour of button when not being interacted with
            hoverColours=[color["hover"]]*len(texts),  # Colour of button when being hovered over
            pressedColours=[color["pressed"]]*len(texts),  # Colour of button when being clicked
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
        return Button(
            layer,  # Surface to place button array on
            coords[0], coords[1], coords[2], coords[3],
            # border=100,  # Distance between buttons and edge of array
            text=text,
            font=font,
            # colour=colour,
            inactiveColour=color["inactive"],
            hoverColour=color["hover"],  # Colour of button when being hovered over
            pressedColour=color["pressed"],  # Colour of button when being clicked
            textColour=color["hover"],
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

    def align(self, coords, obj, inacurr=(0, 0), type_blit=False, type_align="center"):
        if type(coords) == tuple: coords = list(coords)
        inacurr_w, inacurr_h = 0, 0
        if type(inacurr) == int: inacurr_w = inacurr
        if type(inacurr) == tuple: inacurr = list(inacurr)
        if type(inacurr) == list:
            if len(inacurr) == 1: inacurr_w = inacurr[0]
            elif len(inacurr) == 2: inacurr_w, inacurr_h = inacurr
        # print(type(obj))
        # if type(obj) == pygame.surface.Surface:
        print(obj)
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
        return coords, obj

    def format_commands(self, commands):
        res_commands = {}
        for type_key, type_val in commands.items():
            res_commands[type_key] = {}
            for key, val in type_val.items():
                if type(key) in (list, tuple):
                    for mini_key in key: res_commands[type_key][mini_key] = val
                else:
                    res_commands[type_key][key] = val
        return res_commands

    def display_quit(self):
        self.running = 0

    def display_change(self, type_display, dop_type=None):
        self.changes_holst = 1
        #if type_display == "final": self.final.set_final(dop_type)
        self.type_display = type_display

    def update_widgets(self):
        # print("EVENT:", self.events)
        pygame_widgets.update(self.events)

    def view_logo(self):
        pass
        # logo = pygame.image.load(None)
        # self.display.fill((255, 255, 255))
        # self.display.blit(logo, (0, 0))
        # pygame.display.flip()
        # pygame.time.wait(1000)

    def show(self):
        self.view_logo()
        self.list_active_surface = {'menu': Menu,
                                    'game': Game,
                                    'sett': Settings,
                                    'refer': Refer}
        self.holst = self.list_active_surface[self.type_display](self, self.style)
        self.changes_holst = 0
        while self.running:
            self.events = pygame.event.get()
            if self.changes_holst:
                self.holst.delete_all()
                self.holst = self.list_active_surface[self.type_display](self, self.style)
                self.changes_holst = 0
            self.holst.draw()
            for event in self.events:
                if event.type == pygame.QUIT: self.running = False
                if self.type_display == "game":
                    self.holst.check_event(event)
            self.clock.tick(self.FPS)
            self.update_widgets()
            pygame.display.update()

if __name__ == "__main__":
    menu = Main()
    menu.show()
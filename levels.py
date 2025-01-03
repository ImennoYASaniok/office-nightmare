import pygame
from pygame.locals import Rect



TYPE_BUTTONS = {
    "color": {
            "inactive": (0, 0, 0, 0), # (0, 0, 0)
            "hover": (200, 208, 200, 200), # (0, 32, 214)
            "pressed": (200, 208, 200),
            "text": (200, 208, 200)
    }
}



class Map:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style
        self.info = {
            "#": {
                "w": 50, "h": 50,
                "sprite": (0, 0, 255)
            }
        }
        self.map = []



class Object:
    def __init__(self, parent, game, base_style, coords, size, image=None, size_rect=(0, 20), type_collide="rect"): #absolute_coords_rect=(0, 0)
        self.base_style = base_style
        self.parent = parent
        self.game = game
        self.image = image

        size_rect = list(size_rect)

        self.data = {
            "color": self.base_style["colors"]["light"],
            "coords": [coords[0], coords[1], size[0], size[1]],  # 50, 70
            "size_rect": size_rect,
            # "absolute_coords_rect": absolute_coords_rect,
            "type_render": 1, # тип слоя, на котором будет отрисовка
            # "type_collide": type_collide
            # "mask" - коллизия по маске
            # "rect" - коллизия по прямоугольнику
        }
        if self.image == None:
            self.data["rect"] = Rect(coords[0], coords[1], size[0], size[1])
        else:
            self.data["sprite"] = pygame.image.load(self.image).convert_alpha()
            self.data["sprite"] = pygame.transform.scale(self.data["sprite"],
                                                         (self.data["coords"][2], self.data["coords"][3]))
            self.data["mask"] = pygame.mask.from_surface(self.data["sprite"])
            self.data["rect"] = self.data["sprite"].get_rect()
        for i in range(len(size_rect)):
            if self.data["size_rect"][i] == 0:
                self.data["size_rect"][i] = size[i]
            elif self.data["size_rect"][i] < 0:
                self.data["size_rect"][i] = size[i] - abs(size_rect[i])
            else:
                self.data["size_rect"][i] = size_rect[i]
        # if self.data["absolute_coords_rect"][0] <= 0:
        #     self.data["absolute_coords_rect"][0] = self.data["coords"][0] + self.size[0]
        # else:
        #     self.data["absolute_coords_rect"][0] = self.data["absolute_coords_rect"][0]
        self.set_sprite()

    def set_sprite(self):
        self.data["rect"].x = self.data["coords"][0] # + self.data["absolute_coords_rect"][0]
        self.data["rect"].y = self.data["coords"][1] + self.data["coords"][3] - self.data["size_rect"][1] # - self.data["absolute_coords_rect"][1]
        self.data["rect"].w = self.data["size_rect"][0] # self.data["coords"][2]
        self.data["rect"].h = self.data["size_rect"][1] # self.character["coords"][3]

    def update_sprite(self, image):
        if self.image != None:
            self.image = image
            self.data["sprite"] = pygame.image.load(self.image).convert_alpha()
            self.data["sprite"] = pygame.transform.scale(self.data["sprite"],(self.data["coords"][2], self.data["coords"][3]))
            self.set_sprite()

    def draw(self):
        if self.image != None:
            self.parent.display.blit(self.data["sprite"], self.data["coords"])



class Hitbox_Button:
    def __init__(self, parent, game, object, layer, func, coords, size, colors):
        self.parent = parent
        self.game = game
        self.object = object
        self.layer = layer
        self.func = func
        self.size = size
        self.coords = coords
        self.colors = colors
        if "hover" not in self.colors.keys(): self.colors["hover"] = self.colors["inactive"]
        elif "pressed" not in self.colors.keys(): self.colors["pressed"] = self.colors["inactive"]
        self.data = {
            "coords": (self.object.data["coords"][0]+self.coords[0], self.object.data["coords"][1]+self.coords[1], self.size[0], self.size[1]),
            "color": {
                "inactive": self.colors["inactive"],
                "hover":  self.colors["hover"],
                "pressed": self.colors["pressed"],
                "text": self.colors["inactive"]
            },
            "func": self.func,
            # "type_render": 1
        }
        self.create(layer)

    def create(self, layer):
        self.layer = layer
        self.data["button"] = self.parent.button(coords=self.data["coords"],
                                             text="",
                                             color=self.data["color"],
                                             font=pygame.font.SysFont(None, 30),
                                             func=self.data["func"],
                                            layer=layer
                                            )
    def delete(self):
        del self.data["button"]



class Level1:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        self.list_rooms = {'start_room': Start_room}



class Start_room:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        plant_1 = Object(self.parent, self.game, self.base_style, [200, 100],
                         (100, 100), 'sprites/plants/plant_1.png')
        plant_2 = Object(self.parent, self.game, self.base_style, [200, 150],
                         (100, 100), 'sprites/plants/plant_1.png')

        self.objects = {"plant_1": plant_1, "plant_2": plant_2}
        self.list_objects = list(self.objects.values())
        # ------------------
        self.dop_objects = {}
        self.list_dop_objects = list(self.dop_objects.values())
        # ------------------
        button_plant_1 = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["plant_1"],
                                       layer=self.parent.display,
                                       func=lambda: print("plant 1"),
                                       coords=(0, 0),
                                       size=(100, 100),
                                       colors=TYPE_BUTTONS["color"])
        button_plant_2 = Hitbox_Button(parent=self.parent, game=self.game, object=self.objects["plant_2"],
                                       layer=self.parent.display,
                                       func=lambda: print("plant 2"),
                                       coords=(0, 0),
                                       size=(100, 100),
                                       colors=TYPE_BUTTONS["color"])
        self.buttons = [button_plant_1, button_plant_2]

    def enter_rooms(self):
        # self.game.floor.blit(self.texture_floor, (0, 0))
        self.game.data_layers = [0] * len(self.buttons)
        self.game.old_data_layers = [0] * len(self.buttons)

    def draw(self):
        self.game.render_objects(self.list_objects, buttons=self.buttons, dop_objects=self.list_dop_objects)
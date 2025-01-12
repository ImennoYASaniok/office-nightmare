import pygame
from pygame.locals import Rect

THICKNESS_WALL = 30
HEIGHT_WALL = 200
DELTA_SIZE_NEAR_OBJECTS = 3
WIDTH_DOOR = 250
# (Пока что двери нет, а имеется ввиду просто проход)
# Размеры двери смотрятся вот так: (------- <- это типо дверь)
#
# Спереди:                                              Cбоку:
#
# WIDTH_DOOR                                   |
#    |                                         | <- WIDTH_DOOR
# ------- <-HEIGHT_DOOR (=THICKNESS_WALL)      |
#                                             /
#                                          HEIGHT_DOOR (=THICKNESS_WALL)

TYPE_BUTTONS = {
    "color": {
            "inactive": (0, 200, 0, 100), # (0, 0, 0, 0)
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

    def draw(self): # layer
        if self.image != None:
            self.game.game_layer.blit(self.data["sprite"], self.data["coords"]) # self.parent.display



class Hitbox_Button:
    def __init__(self, parent, game, object, func, coords, size, colors, layer=None, name=None):
        self.parent = parent
        # self.game = game
        self.name = name
        if "hover" not in colors.keys(): colors["hover"] = colors["inactive"]
        elif "pressed" not in colors.keys(): colors["pressed"] = colors["inactive"]
        coords = list(coords)
        if object != None:
            coords[0] += object.data["coords"][0]
            coords[1] += object.data["coords"][1]
        self.data = {
            "coords": (coords[0], coords[1], size[0], size[1]),
            "color": {
                "inactive": colors["inactive"],
                "hover":  colors["hover"],
                "pressed": colors["pressed"],
                "text": colors["inactive"]
            },
            "func": func,
            # "type_render": 1
        }
        if layer is not None:
            self.create(layer)

    def create(self, layer):
        self.data["button"] = self.parent.button(coords=self.data["coords"],
                                             text="",
                                             color=self.data["color"],
                                             font=pygame.font.SysFont(None, 30),
                                             func=self.data["func"],
                                            layer=layer
                                            )

    def listen(self, events):
        self.data["button"].listen(events)

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

        self.size_room_layer = [1500, 1500] # [3000, 3000]
        self.room_layer = pygame.Surface(self.size_room_layer)

        size_hall = [400, 400]
        delta_hall = [0, 0]
        # ------ Пол
        self.floor = pygame.image.load('sprites/floor/floor_start_room.png')
        self.room_layer.blit(self.floor, (0, 0))
        self.floor_empty_zone = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                       coords=[self.size_room_layer[0] - size_hall[0] + THICKNESS_WALL, size_hall[1] + HEIGHT_WALL],
                                       size=(size_hall[0] - THICKNESS_WALL, self.size_room_layer[1] - size_hall[1] - HEIGHT_WALL),
                                       image=f'sprites/floor_empty_zone.png',
                                       size_rect=(0, 0))
        # ------ Остальные объекты
        wall_up = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, 0],
                           size=(self.size_room_layer[0], HEIGHT_WALL),
                           image=f'sprites/walls/wall_red_front.png',
                           size_rect=(0, 0))
        wall_down_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, self.size_room_layer[1]],
                           size=(self.size_room_layer[0], THICKNESS_WALL),
                           image=None, size_rect=(0, 0))
        wall_down_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[self.size_room_layer[0] - size_hall[0] + THICKNESS_WALL, size_hall[1]],
                           size=(size_hall[0] - THICKNESS_WALL, HEIGHT_WALL),
                           image=f'sprites/walls/wall_red_frontdop.png',
                           size_rect=(0, -HEIGHT_WALL + 30))
        wall_left = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, 0],
                           size=(THICKNESS_WALL, self.size_room_layer[1] - HEIGHT_WALL),
                           image=f'sprites/walls/wall_red_top.png',
                           size_rect=(0, 0))
        wall_left_front = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                 coords=[0, self.size_room_layer[1]-HEIGHT_WALL],
                                 size=(THICKNESS_WALL, HEIGHT_WALL),
                                 image=f'sprites/walls/wall_red_front.png',
                                 size_rect=(0, 0))
        wall_right_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[self.size_room_layer[0]-size_hall[0], size_hall[1]],
                              size=(THICKNESS_WALL, self.size_room_layer[1] - size_hall[1] - HEIGHT_WALL),
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, -HEIGHT_WALL+30-DELTA_SIZE_NEAR_OBJECTS))
        wall_right_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                    coords=[self.size_room_layer[0]-size_hall[0], self.size_room_layer[1] - HEIGHT_WALL],
                                    size=(THICKNESS_WALL, HEIGHT_WALL),
                                    image=f'sprites/walls/wall_red_front.png',
                                    size_rect=(0, 0))
        wall_right_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[self.size_room_layer[1] - THICKNESS_WALL, THICKNESS_WALL - DELTA_SIZE_NEAR_OBJECTS],
                              size=(THICKNESS_WALL,  (size_hall[1]-WIDTH_DOOR)//2+delta_hall[1]), #  + THICKNESS_WALL
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, -HEIGHT_WALL + 30 - DELTA_SIZE_NEAR_OBJECTS))
        wall_right_front_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                    coords=[self.size_room_layer[1] - THICKNESS_WALL, THICKNESS_WALL+wall_right_2.data["coords"][3] - DELTA_SIZE_NEAR_OBJECTS],
                                    size=(THICKNESS_WALL, HEIGHT_WALL),
                                    image=f'sprites/walls/wall_red_front.png',
                                    size_rect=(0, 0))
        delta_wall_right_3_x = 30
        wall_right_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[self.size_room_layer[1] - THICKNESS_WALL, THICKNESS_WALL+wall_right_2.data["coords"][3]+WIDTH_DOOR - DELTA_SIZE_NEAR_OBJECTS - delta_wall_right_3_x],
                              size=(THICKNESS_WALL, (size_hall[1]-WIDTH_DOOR)//2+delta_hall[1]+HEIGHT_WALL), # +100+delta_wall_right_3_x
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, -HEIGHT_WALL+30))
        # ------ Добавление всех объектов
        self.objects = {
            "floor_empty_zone": self.floor_empty_zone,
            "wall_up": wall_up, "wall_down_1": wall_down_1, "wall_down_2":wall_down_2,
            "wall_left":wall_left, "wall_left_front":wall_left_front,
            "wall_right":wall_right_1, "wall_right_front":wall_right_front_1,
            "wall_right_2": wall_right_2,  "wall_right_front_2": wall_right_front_2, "wall_right_3": wall_right_3
        }
        self.list_objects = list(self.objects.values())
        # ------------------
        self.dop_objects = {}
        self.list_dop_objects = list(self.dop_objects.values())
        self.buttons = []

    def enter_rooms(self):
        # self.game.floor.blit(self.texture_floor, (0, 0))
        self.game.data_layers = [0] * len(self.buttons)
        self.game.old_data_layers = [0] * len(self.buttons)

    def draw(self):
        self.game.render_objects(self.list_objects, dop_objects=self.list_dop_objects) # buttons=self.buttons
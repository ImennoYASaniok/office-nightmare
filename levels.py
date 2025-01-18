import pygame

# from pygame.examples.cursors import image
from pygame.locals import Rect
from collections import deque

THICKNESS_WALL = 30
HEIGHT_WALL = 200
THICKNESS_PARTITION = 10
HEIGHT_PARTITION = 120
DELTA_SIZE_NEAR_OBJECTS = 3
WIDTH_DOOR = 250
SPRITES = {
    "comp_size": (200, 125),
    "sofa_size": (200, 100),
    "avtomat_size": (120, 200), # (100, 150)
    "avtomat_y_up": 50,
    'chair': (80, 132),
    'clock': (40, 40)
}
BUTTONS = {
    "comp_cord": (77, -5), "comp_size": (83, 47), # (63, 28)
    "avtomat_cord": (10, 23), "avtomat_size": (96, 182),
    "avtomat_green_cord": (15, 33), "avtomat_green_size": (93, 162),
    "tv_ps_cord": (-5, -5), "tv_ps_size": (310, 135),
    "tv_vr_cord": (-5, -5), "tv_vr_size": (110, 60),
    "reception_table_cord": (2, -5), "reception_table_size": (190, 150),
    "color": {
            "inactive": (0, 0, 0, 0), # (0, 0, 0)
            "hover": (200, 208, 200, 200), # (0, 32, 214)
            "pressed": (200, 208, 200),
            "text": (200, 208, 200)
    }
}
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



class Object:
    def __init__(self, parent, game, base_style, coords, size, func=None, image=None, size_rect=(0, 20), type_collide="rect"): #absolute_coords_rect=(0, 0)
        self.base_style = base_style
        self.parent = parent
        self.game = game
        self.image = image
        self.func = func

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
            "flag_func": 0
            # 0 - не нужно выполнять
            # 1 - нужно выполнять
        }
        if self.image == None:
            self.data["rect"] = Rect(coords[0], coords[1], size[0], size[1])
        else:
            self.data["sprite"] = pygame.image.load(self.image).convert_alpha()
            self.data["sprite"] = pygame.transform.scale(self.data["sprite"], (self.data["coords"][2], self.data["coords"][3]))
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

        # Обозначение границ на карте
    def set_object_map(self, name):
        # if self.image != None:
        #     self.game.map.set_object([self.data["coords"][0]//self.game.map.rect_cell["size"][0],
        #                           self.data["coords"][1]//self.game.map.rect_cell["size"][1],
        #                           (self.data["coords"][0]+self.data["coords"][2])//self.game.map.rect_cell["size"][0]+1,
        #                           (self.data["coords"][1]+self.data["coords"][3])//self.game.map.rect_cell["size"][1]+1])
        self.game.map.set_object([self.data["rect"].x//self.game.map.rect_cell["size"][0],
                                  self.data["rect"].y//self.game.map.rect_cell["size"][1],
                                  (self.data["rect"].x+self.data["rect"].w)//self.game.map.rect_cell["size"][0], # +1
                                  (self.data["rect"].y+self.data["rect"].h)//self.game.map.rect_cell["size"][1]], # +1
                                 name, [self.data["rect"].x, self.data["rect"].y, self.data["rect"].x+self.data["rect"].w, self.data["rect"].y+self.data["rect"].h])

    def set_sprite(self, coords=None):
        if coords == None:
            self.data["rect"].x = self.data["coords"][0] # + self.data["absolute_coords_rect"][0]
            self.data["rect"].y = self.data["coords"][1] + self.data["coords"][3] - self.data["size_rect"][1] # - self.data["absolute_coords_rect"][1]
            self.data["rect"].w = self.data["size_rect"][0] # self.data["coords"][2]
            self.data["rect"].h = self.data["size_rect"][1] # self.character["coords"][3]
        else:
            self.data["rect"].x = coords[0]  # + self.data["absolute_coords_rect"][0]
            self.data["rect"].y = coords[1] + coords[3] - self.data["size_rect"][1]  # - self.data["absolute_coords_rect"][1]
            self.data["rect"].w = self.data["size_rect"][0]  # self.data["coords"][2]
            self.data["rect"].h = self.data["size_rect"][1]  # self.character["coords"][3]
        # self.data["mask"] = pygame.mask.from_surface(self.data["sprite"])

    def update_sprite(self, image):
        if self.image != None:
            self.image = image
            self.data["sprite"] = pygame.image.load(self.image).convert_alpha()
            self.data["sprite"] = pygame.transform.scale(self.data["sprite"],(self.data["coords"][2], self.data["coords"][3]))
            self.set_sprite()

    def draw(self): # layer
        if self.image != None:
            self.game.game_layer.blit(self.data["sprite"], self.data["coords"]) # self.parent.display

    def check_click(self):
        if self.func != None:
            mouse_pos = pygame.mouse.get_pos()
            rect = Rect(self.game.coords_game_layer[0]+self.data["coords"][0], self.game.coords_game_layer[1]+self.data["coords"][1], self.data["coords"][2], self.data["coords"][3])
            # print(rect.x, rect.y, mouse_pos)
            if rect.collidepoint(mouse_pos):
                # Наведение
                self.game.set_rect(layer=self.parent.display, coords=[rect.x, rect.y, rect.w, rect.h], color_base=BUTTONS["color"]["hover"])
            if rect.collidepoint(mouse_pos) and self.game.val_mouse_state == pygame.MOUSEBUTTONDOWN and self.data["flag_func"] == 1:
                # Нажатие
                self.game.set_rect(layer=self.parent.display, coords=[rect.x, rect.y, rect.w, rect.h], color_base=BUTTONS["color"]["pressed"])
                self.func()
                self.data["flag_func"] = 0
            elif self.game.val_mouse_state == pygame.MOUSEBUTTONUP:
                # Выкл нажатие
                self.data["flag_func"] = 1




# class Hitbox_Button:
#     def __init__(self, parent, game, object, func, coords, size, colors, layer=None, name=None):
#         self.parent = parent
#         # self.game = game
#         self.name = name
#         if "hover" not in colors.keys(): colors["hover"] = colors["inactive"]
#         elif "pressed" not in colors.keys(): colors["pressed"] = colors["inactive"]
#         coords = list(coords)
#         if object != None:
#             coords[0] += object.data["coords"][0]
#             coords[1] += object.data["coords"][1]
#         self.data = {
#             "coords": (coords[0], coords[1], size[0], size[1]),
#             "color": {
#                 "inactive": colors["inactive"],
#                 "hover":  colors["hover"],
#                 "pressed": colors["pressed"],
#                 "text": colors["inactive"]
#             },
#             "func": func,
#             # "type_render": 1
#         }
#         if layer is not None:
#             self.create(layer)
#
#     def create(self, layer):
#         self.data["button"] = self.parent.button(coords=self.data["coords"],
#                                              text="",
#                                              color=self.data["color"],
#                                              font=pygame.font.SysFont(None, 30),
#                                              func=self.data["func"],
#                                             layer=layer
#                                             )
#
#     def listen(self, events):
#         self.data["button"].listen(events)
#
#     def delete(self):
#         del self.data["button"]

class Enemy(Object):
    def __init__(self, parent, game, base_style, coords, size, func=None, image=None, size_rect=(0, 20), type_collide="rect"):
        super().__init__(parent, game, base_style, coords, size, func, image, size_rect, type_collide)
        self.way = []
        self.old_way = []
        self.data["speed"] = 3
        self.data["dir"] = "down"
        self.data["cond"] = "idle"

    def init_start(self):
        self.start = self.set_start()

    def set_start(self):
        # return ((self.data["coords"][0] + self.data["coords"][2] // 2) // self.game.map.rect_cell["size"][0],
        #         (self.data["coords"][1] + self.data["coords"][3] // 2) // self.game.map.rect_cell["size"][1])
        return ((self.data["rect"].x+self.data["rect"].w//2) // self.game.map.rect_cell["size"][0],
                (self.data["rect"].y+self.data["rect"].h//2) // self.game.map.rect_cell["size"][1])

    def search_way(self):
        for cell in self.way:
            self.game.map.set_cell(cell[0], cell[1], 0)
        goal = ((self.game.character.character["rect"].x+self.game.character.character["rect"].w//2) // self.game.map.rect_cell["size"][0],
                (self.game.character.character["rect"].y+self.game.character.character["rect"].h//2) // self.game.map.rect_cell["size"][1])
        self.queue, self.visited = self.game.bfs(start=self.start,
                                                  goal=goal,
                                                  graph=self.game.map.graph)
        self.way = []
        path_segment = goal
        # print(path_segment)
        while path_segment and path_segment in self.visited:
            self.way.append(path_segment)
            path_segment = self.visited[path_segment]
        self.way.reverse()
        self.way.append(self.start)
        if len(self.way) <= 1:
            self.way = self.old_way.copy()
        for cell in self.way:
            self.game.map.set_cell(cell[0], cell[1], 2)
        self.old_way = self.way.copy()
        # print(self.way[0], self.way[1])

    def move(self): # Попробовать: если лево - точка перемещения слева, если право, точка перемещения справа
        old_coords = self.data["coords"].copy()
        # dirs = []
        if self.way[0][0] < self.way[1][0]:
            self.data["cond"] = "walk"
            self.data["dir"] = "right"
            self.data["coords"][0] += self.data["speed"]
        elif self.way[0][0] > self.way[1][0]:
            self.data["cond"] = "walk"
            self.data["dir"] = "left"
            self.data["coords"][0] -= self.data["speed"]
        if self.way[0][1] > self.way[1][1]:
            self.data["cond"] = "walk"
            self.data["dir"] = "up"
            self.data["coords"][1] -= self.data["speed"]
        elif self.way[0][1] < self.way[1][1]:
            self.data["cond"] = "walk"
            self.data["dir"] = "down"
            self.data["coords"][1] += self.data["speed"]
        if self.data["cond"] != "idle":
            self.set_sprite()
        self.start = self.set_start()

        if self.start in self.game.map.coords_objects:
            self.data["coords"] = old_coords.copy()
            self.set_sprite()
            self.start = self.set_start()




class Level1:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        self.list_rooms = {'start_room': Start_room,
                           "meeting_room": Meeting_room}



class Start_room:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        self.size_room_layer = self.parent.LAYERS["start_room"]
        self.room_layer = pygame.Surface(self.size_room_layer)

        size_hall = [400, 400]
        delta_hall = [0, 0]
        # ------ Пол
        self.floor = pygame.image.load('sprites/floor/floor_start_room.png')
        self.floor_empty_zone = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                       coords=[self.size_room_layer[0] - size_hall[0] + THICKNESS_WALL, size_hall[1] + HEIGHT_WALL],
                                       size=(size_hall[0] - THICKNESS_WALL, self.size_room_layer[1] - size_hall[1] - HEIGHT_WALL),
                                       image=f'sprites/floor_empty_zone.png',
                                       size_rect=(0, 0))
        # ------ Стены
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
                              coords=[self.size_room_layer[1] - THICKNESS_WALL, THICKNESS_WALL + wall_right_2.data["coords"][ 3] + WIDTH_DOOR - DELTA_SIZE_NEAR_OBJECTS - delta_wall_right_3_x],
                              size=(THICKNESS_WALL, (size_hall[1] - WIDTH_DOOR) // 2 + delta_hall[1] + HEIGHT_WALL),
                              # +100+delta_wall_right_3_x
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, -HEIGHT_WALL + 30))
        # ------ Перегородки
        coords_partition_side_1 = [400, 0]
        partition_side_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                        coords=[THICKNESS_WALL + coords_partition_side_1[0], self.size_room_layer[1] - HEIGHT_PARTITION - coords_partition_side_1[1]],
                                        size=(THICKNESS_PARTITION, HEIGHT_PARTITION),
                                        image='sprites/walls/partition_front.png',
                                        size_rect=(0, 0))
        partition_side_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                  coords=[THICKNESS_WALL + coords_partition_side_1[0], self.size_room_layer[1] - HEIGHT_PARTITION - coords_partition_side_1[1] -partition_side_front_1.data["coords"][3]],
                                  size=(THICKNESS_PARTITION, 150),
                                  image='sprites/walls/partition_top.png',
                                  size_rect=(0, -HEIGHT_PARTITION + 30))
        partition_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                   coords=[THICKNESS_WALL, self.size_room_layer[1] - HEIGHT_PARTITION - partition_side_front_1.data["coords"][3] - 200],
                                   size=(coords_partition_side_1[0] + THICKNESS_PARTITION, HEIGHT_PARTITION),
                                   image='sprites/walls/partition_front.png',
                                   size_rect=(0, -HEIGHT_PARTITION + 30))
        w_partition_front_2 = 350
        y_partition_front_2 = 550
        partition_front_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                   coords=[self.size_room_layer[0] - size_hall[0] - w_partition_front_2, self.size_room_layer[1] - y_partition_front_2],
                                   size=(w_partition_front_2, HEIGHT_PARTITION),
                                   image='sprites/walls/partition_front.png',
                                   size_rect=(0, -HEIGHT_PARTITION + 30))
        partition_side_front_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                  coords=[partition_front_2.data["coords"][0], self.size_room_layer[1] - 100 - HEIGHT_PARTITION],
                                  size=(THICKNESS_PARTITION, HEIGHT_PARTITION),
                                  image='sprites/walls/partition_front.png',
                                  size_rect=(0, 0))
        partition_side_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                  coords=[partition_front_2.data["coords"][0], partition_front_2.data["coords"][1] + THICKNESS_PARTITION - DELTA_SIZE_NEAR_OBJECTS],
                                  size=(THICKNESS_PARTITION, partition_side_front_2.data["coords"][1] - partition_front_2.data["coords"][1]),
                                  image='sprites/walls/partition_top.png',
                                  size_rect=(0, -HEIGHT_PARTITION + 30))
        w_partition_front_3 = 350
        h_partition_side_3 = 250
        partition_front_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                   coords=[THICKNESS_WALL, self.size_room_layer[1] - 1000],
                                   size=(w_partition_front_3, HEIGHT_PARTITION),
                                   image='sprites/walls/partition_front.png',
                                   size_rect=(0, -HEIGHT_PARTITION + 30))
        partition_side_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                  coords=[partition_front_3.data["coords"][0]+partition_front_3.data["coords"][2], partition_front_3.data["coords"][1]],
                                  size=(THICKNESS_PARTITION, h_partition_side_3),
                                  image='sprites/walls/partition_top.png',
                                  size_rect=(0, -HEIGHT_PARTITION + 30))
        partition_side_front_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                        coords=[partition_side_3.data["coords"][0], partition_side_3.data["coords"][1] + partition_side_3.data["coords"][3]],
                                        size=(THICKNESS_PARTITION, HEIGHT_PARTITION),
                                        image='sprites/walls/partition_front.png',
                                        size_rect=(0, 0))
        # ------ Другие объекты
        self.computer_sprites = ['sprites/comp/gaming_comp_1.png', 'sprites/comp/gaming_comp_2.png',
                                 'sprites/comp/gaming_comp_3.png', 'sprites/comp/gaming_comp_4.png',
                                 'sprites/comp/gaming_comp_5.png', 'sprites/comp/gaming_comp_6.png',
                                 'sprites/comp/gaming_comp_7.png', 'sprites/comp/gaming_comp_8.png',
                                 'sprites/comp/gaming_comp_9.png']
        # ------ Комп 1
        coords_computer_1 = [100, 300]
        coords_computer_1 = [THICKNESS_WALL+coords_computer_1[0], self.size_room_layer[1]-SPRITES["comp_size"][1]-coords_computer_1[1]]
        computer_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                            coords=coords_computer_1,
                            size=SPRITES["comp_size"],
                            # +100+delta_wall_right_3_x
                            image=self.computer_sprites[0],
                            func=lambda: print("click computer"),
                            size_rect=(0, -100))
        self.sprite_computer_for_1 = [0, 0.1, 8]
        self.sprite_computer_isprite_1 = self.sprite_computer_for_1[0]
        self.sprite_computer_isprite_1_OLD = self.sprite_computer_isprite_1
        # ------ Стул 1
        coords_chair_1 = [80, 20]
        chair_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                            coords=[coords_computer_1[0]+coords_chair_1[0], coords_computer_1[1]+coords_chair_1[1]],
                            size=SPRITES["chair"],
                            # +100+delta_wall_right_3_x
                            image="sprites/chair/chair_1.png",
                            size_rect=(0, -100))
        # ------ Комп 2
        coords_computer_2 = [100, 400]
        coords_computer_2 = [self.size_room_layer[0] - size_hall[0] - SPRITES["comp_size"][0] - coords_computer_2[0], self.size_room_layer[1] - SPRITES["comp_size"][1] - coords_computer_2[1]]
        computer_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                            coords=coords_computer_2,
                            size=SPRITES["comp_size"],
                            # +100+delta_wall_right_3_x
                            image=self.computer_sprites[0],
                            size_rect=(0, -100))
        self.sprite_computer_for_2 = [5, 0.1, 8]
        self.sprite_computer_isprite_2 = self.sprite_computer_for_2[0]
        self.sprite_computer_isprite_2_OLD = self.sprite_computer_isprite_2
        # ------ Стул 2
        coords_chair_2 = [40, 20]
        chair_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                         coords=[coords_computer_2[0] + coords_chair_2[0], coords_computer_2[1] + coords_chair_2[1]],
                         size=SPRITES["chair"],
                         # +100+delta_wall_right_3_x
                         image="sprites/chair/chair_1.png",
                         size_rect=(0, -100))
        # ------ Комп 3
        coords_computer_3 = [0, 500]
        coords_computer_3 = [THICKNESS_WALL + coords_computer_3[0], THICKNESS_WALL + coords_computer_3[1]]
        computer_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                            coords=coords_computer_3,
                            size=SPRITES["comp_size"],
                            # +100+delta_wall_right_3_x
                            image=self.computer_sprites[0],
                            size_rect=(0, -100))
        self.sprite_computer_for_3 = [2, 0.1, 8]
        self.sprite_computer_isprite_3 = self.sprite_computer_for_3[0]
        self.sprite_computer_isprite_3_OLD = self.sprite_computer_isprite_3
        # ------ Стул 3
        coords_chair_3 = [40, 20]
        chair_3 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                         coords=[coords_computer_3[0] + coords_chair_3[0], coords_computer_3[1] + coords_chair_3[1]],
                         size=SPRITES["chair"],
                         # +100+delta_wall_right_3_x
                         image="sprites/chair/chair_1.png",
                         size_rect=(0, -100))
        # ------ Живые объекты
        enemy = Enemy(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[200, self.size_room_layer[1]-200],
                              size=(100, 140),
                              image='sprites/character/base_choice/idle/idle_front_0.png',
                              size_rect=(82, 20))
        self.objects = {
            "floor_empty_zone": self.floor_empty_zone,
            # Стены:
            "wall_up": wall_up, "wall_down_1": wall_down_1, "wall_down_2":wall_down_2,
            "wall_left":wall_left, "wall_left_front":wall_left_front,
            "wall_right":wall_right_1, "wall_right_front":wall_right_front_1,
            "wall_right_2": wall_right_2,  "wall_right_front_2": wall_right_front_2, "wall_right_3": wall_right_3,
            # Перегородки:
            "partition_side_1": partition_side_1, "partition_side_front_1": partition_side_front_1, "partition_front_1": partition_front_1,
            "partition_front_2": partition_front_2, "partition_side_front_2": partition_side_front_2, "partition_side_2": partition_side_2,
            "partition_front_3": partition_front_3, "partition_side_front_3": partition_side_front_3, "partition_side_3": partition_side_3,
            # Статичные предметы:
            "computer_1": computer_1, "computer_2": computer_2, "computer_3": computer_3,
            "chair_1": chair_1, "chair_2": chair_2, "chair_3": chair_3,
            # Живые объекты:
            "enemy": enemy,
        }
        self.list_objects = list(self.objects.values())
        # ------------------
        self.dop_objects = {}
        self.list_dop_objects = list(self.dop_objects.values())
        # ------------------
        doors_right_x = THICKNESS_WALL + self.objects["wall_left_front"].data["coords"][2] + HEIGHT_WALL
        self.doors = {"right": (self.size_room_layer[0], [doors_right_x, doors_right_x + WIDTH_DOOR])}
        # ------ Кнопки
        self.buttons = []

    def enter_rooms(self):
        self.game.game_layer = self.room_layer
        self.game.coords_game_layer[2] = self.size_room_layer[0]
        self.game.coords_game_layer[3] = self.size_room_layer[1]
        self.game.data_layers = [0] * len(self.buttons)
        self.game.old_data_layers = [0] * len(self.buttons)

    def delete_all(self):
        pass

    def draw(self):
        self.animate_sprite()
        for name, obj in self.objects.items():
            if "enemy" in name:
                obj.search_way()
                obj.move()
        self.game.render_objects(self.list_objects, dop_objects=self.list_dop_objects) # , draw_rects=True
        # print(self.doors["right"][1][0], self.game.character.character["absolute_coords_rect"][1], self.doors["right"][1][1])
        if self.game.character.character["absolute_coords_rect"][0] >= self.doors["right"][0] and self.doors["right"][1][0] < self.game.character.character["absolute_coords_rect"][1] < self.doors["right"][1][1]:
            print("start_room -> meeting_room")
            self.game.character.respawn([self.game.character.character["coords"][2], self.parent.display_h // 2])
            self.game.room_change("meeting_room")

    def animate_sprite(self):
        self.sprite_computer_for_1 = self.game.animate_sprite(self.sprite_computer_for_1, reverse=True)
        self.sprite_computer_isprite_1 = int(self.sprite_computer_for_1[0])
        if self.sprite_computer_isprite_1 != self.sprite_computer_isprite_1_OLD:
            self.objects["computer_1"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_1])
        self.sprite_computer_isprite_1_OLD = self.sprite_computer_isprite_1

        self.sprite_computer_for_2 = self.game.animate_sprite(self.sprite_computer_for_2, reverse=True)
        self.sprite_computer_isprite_2 = int(self.sprite_computer_for_2[0])
        if self.sprite_computer_isprite_2 != self.sprite_computer_isprite_2_OLD:
            self.objects["computer_2"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_2])
        self.sprite_computer_isprite_2_OLD = self.sprite_computer_isprite_2

        self.sprite_computer_for_3 = self.game.animate_sprite(self.sprite_computer_for_3, reverse=True)
        self.sprite_computer_isprite_3 = int(self.sprite_computer_for_3[0])
        if self.sprite_computer_isprite_3 != self.sprite_computer_isprite_3_OLD:
            self.objects["computer_3"].update_sprite(self.computer_sprites[self.sprite_computer_isprite_3])
        self.sprite_computer_isprite_3_OLD = self.sprite_computer_isprite_3




class Meeting_room:
    def __init__(self, parent, game, base_style):
        self.parent = parent
        self.game = game
        self.base_style = base_style

        self.size_room_layer = self.parent.LAYERS["meeting_room"]  # [3000, 3000]
        self.room_layer = pygame.Surface(self.size_room_layer)
        self.floor = pygame.image.load('sprites/floor/floor_meeting_room.png')
        self.room_layer.blit(self.floor, (0, 0))
        # ------ Стены
        wall_up = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, 0],
                           size=(self.size_room_layer[0], HEIGHT_WALL),
                           image=f'sprites/walls/wall_red_front.png',
                           size_rect=(0, 0))
        wall_down = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                           coords=[0, self.size_room_layer[1]],
                           size=(self.size_room_layer[0], THICKNESS_WALL),
                           image=None, size_rect=(0, 0))
        wall_left_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[0, THICKNESS_WALL - DELTA_SIZE_NEAR_OBJECTS],
                              size=(THICKNESS_WALL, (self.parent.display_h - WIDTH_DOOR - HEIGHT_WALL) // 2),
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, 0))
        wall_left_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                    coords=[0, THICKNESS_WALL + wall_left_1.data["coords"][3] - DELTA_SIZE_NEAR_OBJECTS],
                                    size=(THICKNESS_WALL, HEIGHT_WALL),
                                    image=f'sprites/walls/wall_red_front.png',
                                    size_rect=(0, 0))
        delta_wall_left_2_x = 30
        wall_left_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                              coords=[0, THICKNESS_WALL + wall_left_1.data["coords"][3] + WIDTH_DOOR - DELTA_SIZE_NEAR_OBJECTS - delta_wall_left_2_x],
                              size=(THICKNESS_WALL, (self.parent.display_h - WIDTH_DOOR) // 2),
                              # +100+delta_wall_right_3_x
                              image=f'sprites/walls/wall_red_top.png',
                              size_rect=(0, -HEIGHT_WALL + 30))
        wall_left_front_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                             coords=[0, self.size_room_layer[1] - HEIGHT_WALL],
                             size=(THICKNESS_WALL, HEIGHT_WALL),
                             # +100+delta_wall_right_3_x
                             image=f'sprites/walls/wall_red_front.png',
                             size_rect=(0, 0))
        wall_right_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                             coords=[self.size_room_layer[0]-THICKNESS_WALL, THICKNESS_WALL - DELTA_SIZE_NEAR_OBJECTS],
                             size=(THICKNESS_WALL, (self.parent.display_h - WIDTH_DOOR - HEIGHT_WALL) // 2),
                             image=f'sprites/walls/wall_red_top.png',
                             size_rect=(0, 0))
        wall_right_front_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                   coords=[self.size_room_layer[0]-THICKNESS_WALL, THICKNESS_WALL + wall_left_1.data["coords"][3] - DELTA_SIZE_NEAR_OBJECTS],
                                   size=(THICKNESS_WALL, HEIGHT_WALL),
                                   image=f'sprites/walls/wall_red_front.png',
                                   size_rect=(0, 0))
        delta_wall_right_2_x = 30
        wall_right_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                             coords=[self.size_room_layer[0]-THICKNESS_WALL, THICKNESS_WALL + wall_right_1.data["coords"][3] + WIDTH_DOOR - DELTA_SIZE_NEAR_OBJECTS - delta_wall_right_2_x],
                             size=(THICKNESS_WALL, (self.parent.display_h - WIDTH_DOOR) // 2),
                             # +100+delta_wall_right_3_x
                             image=f'sprites/walls/wall_red_top.png',
                             size_rect=(0, -HEIGHT_WALL + 30))
        wall_right_front_2 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
                                   coords=[self.size_room_layer[0]-THICKNESS_WALL, self.size_room_layer[1] - HEIGHT_WALL],
                                   size=(THICKNESS_WALL, HEIGHT_WALL),
                                   # +100+delta_wall_right_3_x
                                   image=f'sprites/walls/wall_red_front.png',
                                   size_rect=(0, 0))
        # coords_partition_1 = [400, 0]
        # partition_side_1 = Object(parent=self.parent, game=self.game, base_style=self.base_style,
        #                            coords=[THICKNESS_WALL + coords_partition_1[0],
        #                                    self.size_room_layer[1] - HEIGHT_PARTITION - coords_partition_1[1]],
        #                            size=(THICKNESS_PARTITION, HEIGHT_PARTITION),
        #                            image='sprites/walls/partition_front.png',
        #                            size_rect=(0, 0))
        self.objects = {
            "wall_up": wall_up, "wall_down": wall_down,
            "wall_left_1":wall_left_1, "wall_left_front_1": wall_left_front_1, "wall_left_2": wall_left_2, "wall_left_front_2": wall_left_front_2,
            "wall_right_1":wall_right_1, "wall_right_front_1": wall_right_front_1, "wall_right_2": wall_right_2, "wall_right_front_2": wall_right_front_2,
        }
        self.list_objects = list(self.objects.values())
        # ------------------
        self.dop_objects = {}
        self.list_dop_objects = list(self.dop_objects.values())
        # ------------------
        self.doors = {"left": (0, [(self.size_room_layer[1]-WIDTH_DOOR) // 2, (self.size_room_layer[1]+WIDTH_DOOR) // 2 + HEIGHT_WALL])}

        # ------ Кнопки
        self.buttons = []

    def enter_rooms(self):
        # self.game.floor.blit(self.texture_floor, (0, 0))
        self.game.game_layer = self.room_layer
        self.game.coords_game_layer[2] = self.size_room_layer[0]
        self.game.coords_game_layer[3] = self.size_room_layer[1]
        self.game.data_layers = [0] * len(self.buttons)
        self.game.old_data_layers = [0] * len(self.buttons)

    def delete_all(self):
        pass

    def draw(self):
        self.animate_sprite()
        self.game.render_objects(self.list_objects, dop_objects=self.list_dop_objects) # buttons=self.buttons
        # print(self.doors["left"][1][0], self.game.character.character["absolute_coords_rect"][1], self.doors["left"][1][1])
        if self.game.character.character["absolute_coords_rect"][0] <= self.doors["left"][0] and self.doors["left"][1][0] < self.game.character.character["absolute_coords_rect"][1] < self.doors["left"][1][1]:
            print("meeting_room -> start_room")
            self.game.character.respawn([self.parent.LAYERS["start_room"][0]-self.game.character.character["coords"][2], self.doors["left"][1][0]])
            self.game.room_change("start_room")

    def animate_sprite(self):
        pass
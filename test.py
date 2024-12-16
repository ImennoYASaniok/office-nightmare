# import pygame
#
# import pygame_widgets
# from pygame_widgets.button import ButtonArray
#
# # Set up Pygame
# pygame.init()
# win = pygame.display.set_mode((600, 600))
#
#
# colors = {"base": (255, 0, 0), "hover": (0, 0, 255), "press": (0, 255, 0)}
# # Creates an array of buttons
# buttonArray = ButtonArray(
#     # Mandatory Parameters
#     win,  # Surface to place button array on
#     50,  # X-coordinate
#     50,  # Y-coordinate
#     500,  # Width
#     500,  # Height
#     (1, 4),  # Shape: 2 buttons wide, 2 buttons tall
#     #border=100,  # Distance between buttons and edge of array
#     texts=('1', '2', '3', '4', '5', '6'),  # Sets the texts of each button (counts left to right then top to bottom)
#     # colour=colors["base"],
#     inactiveColours=[colors["base"]]*6,  # Colour of button when not being interacted with
#     hoverColours=[colors["hover"]]*6,  # Colour of button when being hovered over
#     pressedColours=[colors["press"]]*6,  # Colour of button when being clicked
#     onClicks=(lambda: print('1'), lambda: print('2'), lambda: print('3'), lambda: print('4'), lambda: print('5'), lambda: print('6'))
# )
#
# run = True
# while run:
#     events = pygame.event.get()
#     for event in events:
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             run = False
#             quit()
#
#     pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
#     pygame.display.update()



# def button(self, coords, layout, colors, font, func):
#     self.base_buttons = ButtonArray(
#         # Mandatory Parameters
#         self.parent.display,  # Surface to place button array on
#         coords[0],  # X-coordinate of top left corner
#         coords[1],  # Y-coordinate of top left corner
#         coords[2] - coords[0],
#         coords[3] - coords[1],  # Height
#         layout,  # Shape: 2 buttons wide, 2 buttons tall
#         # border=100,  # Distance between buttons and edge of array
#         texts=('1', '2', '3', '4'),  # Sets the texts of each button (counts left to right then top to bottom)
#         inactiveColour=colors["base"],  # Colour of button when not being interacted with
#         hoverColour=colors["hover"],  # Colour of button when being hovered over
#         pressedColour=colors["press"],  # Colour of button when being clicked
#         # When clicked, print number
#         onClicks=(lambda: print('1'), lambda: print('2'), lambda: print('3'), lambda: print('4'))
#     )
#
#
#     self.button = Button(
#         # Mandatory Parameters
#         self.parent.display,  # Surface to place button on
#         coords[0],  # X-coordinate of top left corner
#         coords[1],  # Y-coordinate of top left corner
#         coords[2]-coords[0],
#         coords[3]-coords[1],
#         text=font["text"],  # Text to display
#         fontSize=font["size"],  # Size of font
#         #margin=20,  # Minimum distance between text/image and edge of button
#         inactiveColour=colors["base"],  # Colour of button when not being interacted with
#         hoverColour=colors["hover"],  # Colour of button when being hovered over
#         pressedColour=colors["press"],  # Colour of button when being clicked
#         onClick=func  # Function to call when clicked on
#     )

# label text
# import pygame
#
# class Main:
#     def __init__(self):
#         pygame.init()
#         pygame.mixer.init()
#         self.display = pygame.display.set_mode((800, 800))
#         self.clock = pygame.time.Clock()
#         self.clock.tick(30)
#
#         self.running = True
#         # self.surf = pygame.Surface((300, 300))
#         # self.surf.fill((255, 255, 255))
#         # self.rect = pygame.Rect(20, 20, 20, 20)
#         # self.display.blit(self.surf, self.rect)
#         pygame.draw.rect(
#             self.display, (255, 255, 255), (50, 50, 100, 100),
#         )
#
#     def show(self):
#         while self.running:
#             events = pygame.event.get()
#
#             for event in events:
#                 if event.type == pygame.QUIT: self.running = False
#             pygame.display.update()
#
# if __name__ == "__main__":
#     menu = Main()
#     menu.show()

# import pygame
# import sys
#
# GREEN = (200, 255, 200)
# WHITE = (255, 255, 255)
#
# sc = pygame.display.set_mode((300, 300))
#
# surf = pygame.Surface((100, 100))
# surf.fill(WHITE)
#
# rect = surf.get_rect()  # создается экземпляр Rect
#
# print(surf.get_width())  # 100
# print(rect.width)  # 100
# print(rect.x, rect.y)  # 0 0
#
# while 1:
#     for i in pygame.event.get():
#         if i.type == pygame.QUIT:
#             sys.exit()
#
#     sc.fill(GREEN)
#     sc.blit(surf, rect)
#     pygame.display.update()
#
#     rect.x += 1
#
#     pygame.time.delay(20)







# Проверка нажатий
# import pygame
#
# class Main:
#     def __init__(self):
#         pygame.init()
#         pygame.mixer.init()
#         self.display = pygame.display.set_mode((800, 800))
#         self.clock = pygame.time.Clock()
#         self.clock.tick(30)
#
#         self.running = True
#         # self.surf = pygame.Surface((300, 300))
#         # self.surf.fill((255, 255, 255))
#         # self.rect = pygame.Rect(20, 20, 20, 20)
#         # self.display.blit(self.surf, self.rect)
#         pygame.draw.rect(
#             self.display, (255, 255, 255), (50, 50, 100, 100),
#         )
#         self.type_key = 0
#
#
#     def show(self):
#         while self.running:
#             events = pygame.event.get()
#
#             for event in events:
#                 if event.type == pygame.QUIT: self.running = False
#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_w: self.type_key = 1
#                 elif event.type == pygame.KEYUP:
#                     if event.key == pygame.K_w: self.type_key = 0
#             if self.type_key == 1:
#                 print("press")
#             else:
#                 print("not press")
#             pygame.display.update()
#
# if __name__ == "__main__":
#     menu = Main()
#     menu.show()















import pygame as pg
import sys
import random as rnd

pg.init()
win = pg.display.set_mode((500, 500))
background = pg.image.load("background.png").convert()
##  Рекомендую использовать .convert(), иначе будет сильно лагать

class cam:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 500, 500)

    def move(self, vector):
        self.rect[0] += vector[0]
        self.rect[1] += vector[1]

class Player:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 10, 10)

    def move(self, vector):
        self.rect[0] += vector[0]
        self.rect[1] += vector[1]

    def draw(self):
        ##  Игрок на самом окне не двигается, двигается мир вокруг него
        pg.draw.rect(win, (0, 0, 0), (240, 240, 10, 10))

player = Player(0, 0)
camera = cam(0, 0)

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    vector = [0, 0]

    kpressed = pg.key.get_pressed()
    if kpressed[pg.K_UP]:
        vector[1] -= 3
    elif kpressed[pg.K_DOWN]:
        vector[1] += 3

    if kpressed[pg.K_LEFT]:
        vector[0] -= 3
    elif kpressed[pg.K_RIGHT]:
        vector[0] += 3

    ##  Если игрок ходил
    if vector != [0, 0]:
        player.move(vector)
        camera.move(vector)

    win.fill((255, 255, 255))
    win.blit(background, (-camera.rect[0], -camera.rect[1]))
    player.draw()

    pg.display.flip() ##    = pg.display.update()
    pg.time.wait(30)
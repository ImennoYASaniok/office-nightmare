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















# import pygame
#
# # --- constants --- (UPPER_CASE names)
#
# BLACK = (0, 0, 0)
# RED   = (255, 0, 0)
# GREEN = (0, 255, 0)
#
# # --- classes --- (CamelCase names)
#
# class Sheldon(pygame.sprite.Sprite):
#
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#
#         self.image = pygame.Surface((230, 310))
#         self.image.fill(RED)
#
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#
#     def check_click(self, mouse):
#         if self.rect.collidepoint(mouse):
#             print("hit RED")
#
# class Rake(pygame.sprite.Sprite):
#
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#
#         self.image = pygame.Surface((230, 310))
#         self.image.fill(GREEN)
#
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#
#     def check_click(self, mouse):
#         if self.rect.collidepoint(mouse):
#             print("hit GREEN")
#
# # --- main --- (lower_case names)
#
# # - init -
#
# pygame.init()
# window = pygame.display.set_mode((800,600))
#
# # - objects -
#
# sheldon = Sheldon(10, 10)
# #sheldon.rect.topleft = (10, 10)
#
# rake = Rake(400, 250)
# #rake.rect.topleft = (400, 250)
#
# all_sprites = pygame.sprite.Group()
# all_sprites.add(sheldon, rake)
#
# # - mainloop -
#
# running = True
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT or \
#            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#             running = False
#
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             for s in all_sprites:
#                 s.check_click(event.pos)
#
#     window.fill(BLACK)
#     all_sprites.update()
#     all_sprites.draw(window)
#     pygame.display.update()
#
# # - end -
#
# pygame.quit()














import pygame
import sys

pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Преследование врагом")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Настройки персонажа
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
player_speed = 5
player_radius = 15

# Настройки врага
enemy_pos = pygame.Vector2(100, 100)
enemy_speed = 3
enemy_radius = 15
enemy_detection_radius = 200  # Радиус обнаружения врага

clock = pygame.time.Clock()

while True:
    clock.tick(60)  # Ограничение FPS до 60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Движение персонажа
    keys = pygame.key.get_pressed()
    movement = pygame.Vector2(0, 0)
    if keys[pygame.K_w]:
        movement.y -= player_speed
    if keys[pygame.K_s]:
        movement.y += player_speed
    if keys[pygame.K_a]:
        movement.x -= player_speed
    if keys[pygame.K_d]:
        movement.x += player_speed
    if movement.length() > 0:
        movement = movement.normalize() * player_speed
        player_pos += movement

    # Расчет расстояния между персонажем и врагом
    distance = player_pos.distance_to(enemy_pos)
    if distance < enemy_detection_radius:
        # Враг преследует персонажа
        direction = (player_pos - enemy_pos).normalize()
        enemy_pos += direction * enemy_speed

    # Отрисовка
    WIN.fill(WHITE)
    # Радиус обнаружения
    pygame.draw.circle(WIN, (200, 200, 200), (int(enemy_pos.x), int(enemy_pos.y)), enemy_detection_radius, 1)
    # Враг
    pygame.draw.circle(WIN, RED, (int(enemy_pos.x), int(enemy_pos.y)), enemy_radius)
    # Персонаж
    pygame.draw.circle(WIN, BLUE, (int(player_pos.x), int(player_pos.y)), player_radius)

    pygame.display.flip()
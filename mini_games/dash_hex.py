import math
import random
import pygame
import pygame_widgets
from pygame_widgets.button import Button as buttonsss

def dash_hex(display):
	win = pygame.Surface((WIDTH, HEIGHT))
	clock = pygame.time.Clock()
	FPS = 90
	RED = (255, 0, 0)
	GREEN = (0, 177, 64)
	BLUE = (0, 0, 255)
	ORANGE = (252, 76, 2)
	YELLOW = (254, 221, 0)
	PURPLE = (155, 38, 182)
	AQUA = (0, 103, 127)
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	GRAY = (239, 237, 238)
	GRAY2 = (200, 200, 203)
	GRAY3 = (180, 180, 180)

	COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE]
	cindex = 0
	ccolor = COLORS[cindex]

	# Fonts
	score_font = "mini_games/mini_fonts/Aladin-Regular.ttf"
	msg_font = "mini_games/mini_fonts/DalelandsUncialBold-82zA.ttf"

	game_msg = Message(90, HEIGHT // 2 + 20, 30, "GAME", msg_font, BLACK, win)
	over_msg = Message(WIDTH // 2 + 60, HEIGHT // 2 + 20, 30, "OVER!", msg_font, RED, win)

	cscore_msg = Message(WIDTH // 2, 50, 20, "SCORE", msg_font, GRAY3, win)
	cscore_msg2 = Message(WIDTH // 2, 75, 24, "0", msg_font, BLACK, win)
	best_msg = Message(WIDTH // 2, 140, 20, "BEST", msg_font, GRAY3, win)
	bestscore_msg = Message(WIDTH // 2, 170, 24, "0", msg_font, BLACK, win)

	hex_msg = Message(WIDTH // 2, HEIGHT // 2 - 30, 40, "HEX", msg_font, GRAY3, win)
	dash_msg = Message(WIDTH // 2, HEIGHT // 2 + 20, 40, "DASH", msg_font, GRAY3, win)

	score_msg = Message(WIDTH // 2, HEIGHT // 2, 60, "0", score_font, GRAY2, win)

	# Buttons
	close_img = pygame.image.load('mini_games/mini_assets/closeBtn_123.png')
	replay_img = pygame.image.load('mini_games/mini_assets/replay_123.png')
	sound_off_img = pygame.image.load("mini_games/mini_assets/soundOffBtn_123.png")
	sound_on_img = pygame.image.load("mini_games/mini_assets/soundOnBtn_123.png")

	close_btn = Button(close_img, (24, 24), WIDTH // 4 - 18, HEIGHT // 2 + 120)
	replay_btn = Button(replay_img, (36, 36), WIDTH // 2 - 18, HEIGHT // 2 + 115)
	sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT // 2 + 120)

	# Positons
	left = 100
	top = 150
	right = WIDTH - left
	bottom = HEIGHT - top
	mid = HEIGHT // 2

	# Groups & Objects
	line_group = pygame.sprite.Group()
	ball_group = pygame.sprite.Group()
	particle_group = pygame.sprite.Group()

	topr = Line((left, top), (WIDTH - left, top))
	l1 = Line((left - 15, top + 10), (30, mid - 10))
	l2 = Line((30, mid + 10), (left - 15, bottom - 10))
	r1 = Line((right + 15, top + 10), (WIDTH - 30, mid - 10))
	r2 = Line((WIDTH - 30, mid + 10), (right + 15, bottom - 10))
	bottom = Line((left, HEIGHT - top), (WIDTH - left, HEIGHT - top))

	line_group.add(topr)
	line_group.add(r1)
	line_group.add(r2)
	line_group.add(bottom)
	line_group.add(l2)
	line_group.add(l1)

	player = Player(WIDTH // 2, HEIGHT // 2)

	# Score Bar
	bar_index = random.randint(0, 5)
	l = line_group.sprites()[bar_index]
	bar = Line((l.x1, l.y1), (l.x2, l.y2))

	clicked = False
	score = 0
	high = 0
	counter = 0

	sound_on = True
	gameover = False
	home_page = True
	game_page = False
	score_page = False

	color = COLORS[random.randint(0, 4)]

	running = True
	a = []
	sss = []
	dddd = []

	button = buttonsss(
		display,  # Surface to place button on
		288,
		0,  # Y-coordinate of top left corner
		100,  # Width
		50,
		colour=(255, 0, 0),
		text='X',  # Heigh
		onClick=lambda: stopping(sss), )
	a.append(button)
	print(a)


	def stopping(ss):
		ss.append(1)


	while running:
		if counter % 100 == 0:
			ball = Ball(win)
			ball_group.add(ball)
			counter = 0
		counter += 1
		if sss:
			running = False

		win.fill(GRAY)
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if not clicked and game_page:
					clicked = True
					player.di *= -1
					player.update_index()
					rect = line_group.sprites()[player.index]

				if home_page:
					home_page = False
					game_page = True

			if event.type == pygame.MOUSEBUTTONUP:
				clicked = False

		if home_page:
			line_group.update(win, color)
			hex_msg.update()
			dash_msg.update()

		if score_page:
			running = False

		# drawing Objects
		if game_page:
			score_msg.update(score, shadow=True)
			line_group.update(win)
			particle_group.update()
			bar.update(win, ccolor)
			line = line_group.sprites()[player.index]
			player.update(line, ccolor, win)
			ball_group.update(win)

			# Collison Detection
			if player.rect.collidepoint(bar.get_center()):
				bar_index = random.randint(0, 5)
				l = line_group.sprites()[bar_index]
				bar = Line((l.x1, l.y1), (l.x2, l.y2))
				score += 1
				if score & score > high:
					high = score
				if score % 3 == 0:
					cindex = (cindex + 1) % 5
					ccolor = COLORS[cindex]

			for ball in ball_group:
				if player.alive and ball.rect.colliderect(player.rect):
					x, y = player.rect.centerx, player.rect.centery
					for i in range(20):
						particle = Particle(x, y, ccolor, win)
						particle_group.add(particle)
					player.alive = False
					ball.kill()
					if not gameover:
						gameover = True

			if gameover and len(particle_group) == 0:
				game_page = False
				score_page = True
		pygame_widgets.update(pygame.event.get())
		display.blit(win, (0, 0))
		clock.tick(FPS)
		pygame.display.update()
	return score

class Line(pygame.sprite.Sprite):
	def __init__(self, start, end):
		super(Line, self).__init__()

		self.x1 = start[0]
		self.y1 = start[1]
		self.x2 = end[0]
		self.y2 = end[1]

		self.active = False
		self.counter = 0

	def get_center(self):
		return self.rect.centerx, self.rect.centery

	def update(self, win, color=None):
		if not color:
			if self.active:
				color = (252, 76, 2)
				self.counter += 1
				if self.counter % 30 == 0:
					self.active = False
					self.counter = 0
			else:
				color = (0, 0, 0)

		self.rect = pygame.draw.line(win, color, (self.x1, self.y1), (self.x2, self.y2), 5)


class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Player, self).__init__()
		self.x = x
		self.y = y
		self.index = 0
		self.di = 1
		self.alive

	def update_index(self):
		self.index = (self.index + self.di) % 6
		if self.index == -1:
			self.index = 5

	def update(self, line, color, win):
		if self.alive:
			rect = line.rect
			self.rect = pygame.draw.circle(win, color, (self.x, self.y), 5)
			pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), 2)

			dx = rect.centerx - self.x
			dy = rect.centery - self.y
			angle = math.atan2(dy, dx)
			thetax = math.cos(angle)
			thetay = math.sin(angle)

			self.x += thetax
			self.y += thetay

			if self.rect.collidepoint((rect.centerx, rect.centery)):
				self.update_index()
				line.active = True


class Ball(pygame.sprite.Sprite):
	def __init__(self, win):
		super(Ball, self).__init__()

		self.positions = [
			([30, HEIGHT // 2], [WIDTH - 30, HEIGHT // 2]),
			([WIDTH - 30, HEIGHT // 2], [30, HEIGHT // 2]),
			([left - 7, top + 5], [right + 7, bottom - 5]),
			([right + 7, bottom - 5], [left - 7, top + 5]),
			([right + 7, top + 5], [left - 7, bottom - 5]),
			([left - 7, bottom - 5], [right + 7, top + 5])
		]

		self.pos = random.randint(0, len(self.positions) - 1)
		self.position = self.positions[self.pos]
		self.start = self.position[0]
		self.end = self.position[1]
		self.rect = pygame.draw.circle(win, (0, 0, 0), self.start, 5)

	def update(self, win):
		dx = self.end[0] - self.start[0]
		dy = self.end[1] - self.start[1]
		angle = math.atan2(dy, dx)
		thetax = math.cos(angle)
		thetay = math.sin(angle)

		self.start[0] += thetax
		self.start[1] += thetay

		if self.rect.collidepoint(self.end):
			self.kill()

		self.rect = pygame.draw.circle(win, (0, 0, 0), self.start, 5)


class Particle(pygame.sprite.Sprite):
	def __init__(self, x, y, color, win):
		super(Particle, self).__init__()
		self.x = x
		self.y = y
		self.color = color
		self.win = win
		self.size = random.randint(4, 7)
		xr = (-3, 3)
		yr = (-3, 3)
		f = 2
		self.life = 40
		self.x_vel = random.randrange(xr[0], xr[1]) * f
		self.y_vel = random.randrange(yr[0], yr[1]) * f
		self.lifetime = 0

	def update(self):
		self.size -= 0.1
		self.lifetime += 1
		if self.lifetime <= self.life:
			self.x += self.x_vel
			self.y += self.y_vel
			s = int(self.size)
			pygame.draw.rect(self.win, self.color, (self.x, self.y, s, s))
		else:
			self.kill()


class Message:
	def __init__(self, x, y, size, text, font, color, win):
		self.win = win
		self.color = color
		self.x, self.y = x, y
		if not font:
			self.font = pygame.font.SysFont("Verdana", size)
			anti_alias = True
		else:
			self.font = pygame.font.Font(font, size)
			anti_alias = False
		self.image = self.font.render(text, anti_alias, color)
		self.rect = self.image.get_rect(center=(x, y))
		if self.color == (200, 200, 200):
			self.shadow_color = (255, 255, 255)
		else:
			self.shadow_color = (54, 69, 79)
		self.shadow = self.font.render(text, anti_alias, self.shadow_color)
		self.shadow_rect = self.image.get_rect(center=(x + 2, y + 2))

	def update(self, text=None, color=None, shadow=True):
		if text:
			if not color:
				color = self.color
			self.image = self.font.render(f"{text}", False, color)
			self.rect = self.image.get_rect(center=(self.x, self.y))
			self.shadow = self.font.render(f"{text}", False, self.shadow_color)
			self.shadow_rect = self.image.get_rect(center=(self.x + 2, self.y + 2))
		if shadow:
			self.win.blit(self.shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)


class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()

		self.scale = scale
		self.image = pygame.transform.scale(img, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action

SCREEN = WIDTH, HEIGHT = 288, 512
left = 100
top = 150
right = WIDTH - left
bottom = HEIGHT - top
mid = HEIGHT // 2

import pygame, sys
from pygame.locals import *

pygame.init()
winSize = (800, 512)
win = pygame.display.set_mode(winSize)
pygame.display.set_caption('Ninja')
clock = pygame.time.Clock()

class World():
	def __init__(self, bg):
		self.bg = pygame.image.load(bg)

	def loadMap(self, path):
		f = open(path, 'r')
		map = f.read()
		f.close
		map = map.split('\n')

		self.map = []
		for row in map:
			self.map.append(list(row))

	def getRect(self):
		rectList = []
		for y, row in enumerate(self.map):
			for x, tile in enumerate(row):
				if tile != '0':
					rectList.append(pygame.Rect(x * 32, y * 32, 32, 32))

		self.rect = rectList

class Player():
	def __init__(self, x, y):
		self.x = 32 * x
		self.y = 32 * y
		self.WIDTH = 32
		self.HEIGHT = 32
		self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

		self.standing = True
		self.down = False
		self.left = False
		self.right = True

		self.movingLeft = False
		self.movingRight = False

		self.walkCounter = 0
		self.standingCounter = 0

		self.xstep = 8
		self.yMomentum = 0
		self.movement = [0, 0]
		self.airCounter = 0

		self.faceLeft = [pygame.image.load('data/images/ninja/ninja_left_standing1.png'), pygame.image.load('data/images/ninja/ninja_left_standing2.png'), pygame.image.load('data/images/ninja/ninja_left_standing3.png'), pygame.image.load('data/images/ninja/ninja_left_standing4.png'), pygame.image.load('data/images/ninja/ninja_left_standing5.png'), pygame.image.load('data/images/ninja/ninja_left_standing6.png'), pygame.image.load('data/images/ninja/ninja_left_standing7.png'), pygame.image.load('data/images/ninja/ninja_left_standing8.png')]
		self.faceRight = [pygame.image.load('data/images/ninja/ninja_right_standing1.png'), pygame.image.load('data/images/ninja/ninja_right_standing2.png'), pygame.image.load('data/images/ninja/ninja_right_standing3.png'), pygame.image.load('data/images/ninja/ninja_right_standing4.png'), pygame.image.load('data/images/ninja/ninja_right_standing5.png'), pygame.image.load('data/images/ninja/ninja_right_standing6.png'), pygame.image.load('data/images/ninja/ninja_right_standing7.png'), pygame.image.load('data/images/ninja/ninja_right_standing8.png')]
		self.leftRun = [pygame.image.load('data/images/ninja/ninja_left_run1.png'), pygame.image.load('data/images/ninja/ninja_left_run2.png'), pygame.image.load('data/images/ninja/ninja_left_run3.png'), pygame.image.load('data/images/ninja/ninja_left_run4.png'), pygame.image.load('data/images/ninja/ninja_left_run5.png'), pygame.image.load('data/images/ninja/ninja_left_run6.png'), pygame.image.load('data/images/ninja/ninja_left_run7.png'), pygame.image.load('data/images/ninja/ninja_left_run8.png')]
		self.rightRun = [pygame.image.load('data/images/ninja/ninja_right_run1.png'), pygame.image.load('data/images/ninja/ninja_right_run2.png'), pygame.image.load('data/images/ninja/ninja_right_run3.png'), pygame.image.load('data/images/ninja/ninja_right_run4.png'), pygame.image.load('data/images/ninja/ninja_right_run5.png'), pygame.image.load('data/images/ninja/ninja_right_run6.png'), pygame.image.load('data/images/ninja/ninja_right_run7.png'), pygame.image.load('data/images/ninja/ninja_right_run8.png')]
		self.leftDown = pygame.image.load('data/images/ninja/ninja_left_down1.png')
		self.rightDown = pygame.image.load('data/images/ninja/ninja_right_down1.png')

	def spikeCollision(self, spikes):
		for spike in spikes:
			if self.rect.colliderect(spike.rect):
				self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

	def draw(self):
		if self.standingCounter + 1 >= 16:
			self.standingCounter = 0
		if self.walkCounter + 1 >= 16:
			self.walkCounter = 0
		if self.standing and not (self.movingLeft) and not (self.movingRight):
			if self.left:
				win.blit(self.faceLeft[self.standingCounter // 2], (self.rect.x - scroll[0], self.rect.y - scroll[1]))
				self.standingCounter += 1
			if self.right:
				win.blit(self.faceRight[self.standingCounter // 2], (self.rect.x - scroll[0], self.rect.y - scroll[1]))
				self.standingCounter += 1
		else:
			if self.movingLeft:
				win.blit(self.leftRun[self.walkCounter // 2], (self.rect.x - scroll[0], self.rect.y - scroll[1]))
				self.walkCounter += 1
			elif self.movingRight:
				win.blit(self.rightRun[self.walkCounter // 2], (self.rect.x - scroll[0], self.rect.y - scroll[1]))
				self.walkCounter += 1

class spike():
	def __init__(self, x, y):
		self.x = 32 * x
		self.y = 32 * y
		self.rect = pygame.Rect(self.x, self.y + 16, 32, 16)
		self.image = pygame.image.load('data/images/world/spike.png')

	def draw(self):
		win.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))



def checkCollision(rect, tiles):
	collisionTiles = []
	for tile in tiles:
		if rect.colliderect(tile):
			collisionTiles.append(tile)
	return collisionTiles

def move(rect, movement, tiles):
	collisionType = {'left': False, 'right': False, 'top': False, 'bottom': False}
	rect.x += movement[0]
	collisionTiles = checkCollision(rect, tiles)
	for tile in collisionTiles:
		if movement[0] > 0:
			rect.right = tile.left
			collisionType['right'] = True
		elif movement[0] < 0:
			rect.left = tile.right
			collisionType['left'] = True
	rect.y += movement[1]
	collisionTiles = checkCollision(rect, tiles)
	for tile in collisionTiles:
		if movement[1] > 0:
			rect.bottom = tile.top
			collisionType['bottom'] = True
		elif movement[1] < 0:
			rect.top = tile.bottom
			collisionType['top'] = True
	return rect, collisionType

def drawWindow():
	win.fill((79, 51, 56))
	win.blit(world.bg, (0 - scroll[0], 0 - scroll[1]))

	for spike in spikes:
		spike.draw()

	ninja.draw()

	pygame.display.update()

world = World('data/images/world/world.png')
world.loadMap('data/worlds/world.txt')

ninja = Player(2, 3)

spikes = [spike(7, 4), spike(14, 5), spike(15, 5), spike(19, 4), spike(26, 3), spike(27, 4), spike(30, 11), spike(29, 11), spike(28, 11), spike(26, 11), spike(25, 11), spike(24, 11), spike(22, 11), spike(21, 11), spike(20, 11), spike(18, 11), spike(17, 11), spike(16, 11), spike(9, 10), spike(8, 10), spike(7, 10), spike(9, 16), spike(10, 16), spike(11, 16), spike(20, 15), spike(21, 15), spike(36, 23), spike(29, 23), spike(28, 23), spike(24, 23), spike(23, 23), spike(19, 23), spike(18, 23), spike(9, 23), spike(8, 23), spike(7, 23), spike(6, 23)]

scroll = [0, 0]


run = True
while run:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				run = False
				sys.exit()
			if event.key == pygame.K_LEFT:
				ninja.movingLeft = True
				ninja.left = True
				ninja.right = False
				ninja.standing = False
			if event.key == pygame.K_RIGHT:
				ninja.movingRight = True
				ninja.left = False
				ninja.right = True
				ninja.standing = False
			if event.key == pygame.K_UP:
				if ninja.airCounter < 3:
					ninja.yMomentum = -13
		else:
			ninja.standing = True
			ninja.walkCounter = 0
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				ninja.movingLeft = False
			if event.key == pygame.K_RIGHT:
				ninja.movingRight = False

	world.getRect()

	collisionTiles = checkCollision(ninja.rect, world.rect)

	ninja.movement = [0, 0]
	if ninja.movingLeft:
		ninja.movement[0] -= 8
	if ninja.movingRight:
		ninja.movement[0] += 8
	ninja.movement[1] += ninja.yMomentum
	ninja.yMomentum += 2
	if ninja.yMomentum > 30:
		ninja.yMomentum = 30

	ninja.rect, collisionType = move(ninja.rect, ninja.movement, world.rect)
	if collisionType['bottom']:
		ninja.yMomentum = 0
		ninja.airCounter = 0
	else:
		ninja.airCounter += 1

	scroll[0] += (ninja.rect.x - scroll[0] - (winSize[0] - ninja.WIDTH) // 2) / 20
	scroll[1] += (ninja.rect.y - scroll[1] - (winSize[1] - ninja.HEIGHT) // 2) / 20

	ninja.spikeCollision(spikes)

	drawWindow()
pygame.quit()
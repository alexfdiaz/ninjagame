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

		self.grass1 = pygame.image.load('data/images/world/grass_tile1.png')
		self.grass2 = pygame.image.load('data/images/world/grass_tile2.png')
		self.grass3 = pygame.image.load('data/images/world/grass_tile3.png')
		self.grass4 = pygame.image.load('data/images/world/grass_tile4.png')
		self.grass5 = pygame.image.load('data/images/world/grass_tile5.png')
		self.dirt1 = pygame.image.load('data/images/world/dirt_tile1.png')
		self.dirt2 = pygame.image.load('data/images/world/dirt_tile2.png')
		self.dirt3 = pygame.image.load('data/images/world/dirt_tile3.png')

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
		self.x = x
		self.y = y
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


scroll = [0, 0]


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
	#win.blit(world.bg, (0, 0))
	win.fill((38, 188, 248))

	for y, row in enumerate(world.map):
		for x, tile in enumerate(row):
			if tile == '1':
				win.blit(world.grass1, (x * 32 - scroll[0], y * 32 - scroll[1]))
			elif tile == '2':
				win.blit(world.grass2, (x * 32 - scroll[0], y * 32 - scroll[1]))
			elif tile == '3':
				win.blit(world.grass3, (x * 32 - scroll[0], y * 32 - scroll[1]))
			elif tile == '4':
				win.blit(world.grass4, (x * 32 - scroll[0], y * 32 - scroll[1]))
			elif tile == '5':
				win.blit(world.grass5, (x * 32 - scroll[0], y * 32 - scroll[1]))
			elif tile == '6':
				win.blit(world.dirt1, (x * 32 - scroll[0], y * 32 - scroll[1]))
			elif tile == '7':
				win.blit(world.dirt2, (x * 32 - scroll[0], y * 32 - scroll[1]))
			elif tile == '8':
				win.blit(world.dirt3, (x * 32 - scroll[0], y * 32 - scroll[1]))

	ninja.draw()

	pygame.display.update()

world = World('data/images/world/background.png')
world.loadMap('data/worlds/world.txt')
ninja = Player(32 * 12, 32 * 11)
gravity = 0.8


run = True
while run:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			sys.exit()
		if event.type == pygame.KEYDOWN:
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

	drawWindow()
pygame.quit()
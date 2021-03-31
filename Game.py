import pygame as pg
import sys, random
from pygame.locals import *

#Initiating pygame
pg.init()

#Set surface as Fullscreen Display
surface = pg.display.set_mode((0,0),pg.FULLSCREEN)
monitor_info = pg.display.Info()
w = monitor_info.current_w
h = monitor_info.current_h
		
#Clock and Framerate
clock = pg.time.Clock()
FPS = 60


#Color List for quick reference
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
LIME = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
SILVER = (192,192,192)
GRAY = (128,128,128)
MAROON = (128,0,0)
OLIVE = (128,128,0)
GREEN = (0,128,0)
PURPLE = (128,0,128)
TEAL = (0,128,128)
NAVY = (0,0,128)

#Global colors relating to Menu themes
text_color = RED
back_color = BLACK

#-----------Class Definitions-----------#
class Button:
	def __init__(self, xPos, yPos, width, height, color, surface):
		self.xPos = xPos
		self.yPos = yPos
		self.width = width
		self.height = height
		self.rectangle = (xPos, yPos, width, height)
		self.color = color
		self.surface = surface
	def draw(self):
		pg.draw.rect(self.surface, self.color, self.rectangle)

	#Called upon Clicks
	def wasClicked(self, clickPos):
		if clickPos[0] > self.xPos and clickPos[0] < self.xPos + self.width:
			if clickPos[1] > self.yPos and clickPos[1] < self.yPos + self.height:
				return True
		return False
	
class GameTile:
	#Constants
	MISS = 0
	HIT = 1
	BLANK = -1

	#Members
	def __init__(self, xPos, yPos, width, height, playerNumber, surface):
		self.xPos = xPos
		self.yPos = yPos
		self.width = width
		self.height = height
		self.status = self.BLANK
		self.surface = surface
		self.hasBeenClicked = False
		self.color = back_color
		self.isClickableOverride = False
		self.rectangle = (xPos, yPos, width, height)
		self.ship = None
		self.playerNumber = playerNumber
		#Sound Effects
		self.explosion_sound = pg.mixer.Sound("sounds\Explosion.wav")
		self.splash_sound = pg.mixer.Sound("sounds\Splash.wav")

	def wasClicked(self, clickPos):
		if self.isClickable():
			if clickPos[0] > self.xPos and clickPos[0] < self.xPos + self.width:
				if clickPos[1] > self.yPos and clickPos[1] < self.yPos + self.height:
					self.hasBeenClicked = True
					if self.ship != None:
						self.setStatus(self.HIT)
						#Hit Sound
						pg.mixer.Sound.play(self.explosion_sound)
						self.ship.hit()
						self.shipDestroyedAnimation()
					else:
						self.setStatus(self.MISS)
						#Miss Sound
						pg.mixer.Sound.play(self.splash_sound)
					return True
		return False

	def isClickable(self):
		if self.isClickableOverride:
			return False
		return not self.hasBeenClicked

	def setStatus(self, status):
		self.status = status

	def setClickable(self, setting):
		self.isClickableOverride = setting

	def draw(self, playerTurn):
		self.color = back_color
		if self.ship != None and (playerTurn == True or self.status == self.HIT or self.status == self.MISS):
			if self.playerNumber == 2:
				value = self.getShip().getLength()
				self.color = (100 + value * 30, 100 + value * 30, 100 + value * 30 )
				if back_color == WHITE:
					self.color = (0 + value * 30, 0 + value * 30, 0 + value * 30)
			if self.playerNumber == 1:
				value = self.getShip().getLength()
				self.color = (100 + value * 30, 100 + value * 30, 100 + value * 30 )
				if back_color == WHITE:
					self.color = (0 + value * 30, 0 + value * 30, 0 + value * 30)
		elif self.playerNumber == 2:
			self.color = back_color
				
		pg.draw.rect(self.surface, self.color, self.rectangle)

		if not self.isClickable():
			if self.status == self.HIT:
				pg.draw.line(self.surface, text_color, (self.xPos, self.yPos), (24 + self.xPos, 24 + self.yPos))
				pg.draw.line(self.surface, text_color, (24 + self.xPos, self.yPos), (self.xPos, 24 + self.yPos))
			elif self.status == self.MISS:
				pg.draw.circle(self.surface, text_color, (12 + self.xPos,12 + self.yPos), 12, 1)

	def setShip(self, ship):
		self.ship = ship

	def shipDestroyedAnimation(self):
		if self.ship.checkDestroyed():
			font = pg.font.SysFont("none", 24)
			if self.playerNumber == 1:
				text = font.render("Player 2 ship destroyed!", True, text_color)
				taunts = ["'You're a natural'", "'Easiest kill of my life!'", "'Roger, looks like we got a code E-Z.'", 
					"'Are you even trying?'", "'Oops, did I do that?'", "'Was that ship made of paper?'"]
				text2 = font.render(taunts[random.randint(0, 5)], True, text_color)
			if self. playerNumber == 2:
				text = font.render("Player 1 ship destroyed!", True, text_color)
				taunts = ["'That was easy.'", "'Supreme Leader South will love that'", "'RIP Jack Sparrow'", "'FRESH MEAT!'", 
					"'This predicament will be over in no time'", "'We live in a society'" ]
				text2 = font.render(taunts[random.randint(0, 5)], True, text_color)
			loopFinished = False
			while loopFinished == False:
				for event in pg.event.get():
					if event.type == pg.QUIT:
						pg.quit()
						sys.exit()
					if event.type == pg.MOUSEBUTTONDOWN:
							loopFinished = True
				self.surface.fill(BLACK)
				self.surface.blit(text, (w /2 - text.get_width() / 2, 50))
				self.surface.blit(text2, (w /2 - text.get_width() / 2, h / 2))
				pg.display.update()

	def getShip(self):
		return self.ship
		
class Player:
	#Constants
	LEFT = 0
	UP = 1
	RIGHT = 2
	DOWN = 3
	
	def __init__(self, setting, playerNumber, surface, grid_size):
		self.myTurn = setting
		self.playerNumber = playerNumber
		self.surface = surface
		self.buttonTiles = []
		self.ships = [Ship(5), Ship(4), Ship(3), Ship(3), Ship(2)]
		for i in range(grid_size):
			temp = []
			for j in range(grid_size):
				if self.playerNumber == 1:
					temp.append(GameTile(24*i, int(h/3) + 24*j, 24, 24, 1, self.surface))
				else:
					temp.append(GameTile(w-24 - 24*i, int(h/3) + 24*j, 24, 24, 1, self.surface))

			self.buttonTiles.append(temp)
		self.distributeShips(grid_size)
			
	def drawTiles(self):
		for row in self.buttonTiles:
			for tile in row:
				tile.draw(self.myTurn)
				
	def flipTurn(self):
		self.myTurn = not self.myTurn

	def getButtonTiles(self):
		return self.buttonTiles

	def distributeShips(self, grid_size):
		for ship in self.ships:
			done = False
			while not done:
				row = random.randint(0, grid_size-1)
				column = random.randint(0, grid_size-1)
				direction = random.randint(self.LEFT, self.DOWN)
				if self.checkIfSectionEmpty(row, column, direction, ship):
					self.placeShip(row, column, direction, ship)
					done = True

	def getTurn(self):
		return self.myTurn

	def checkIfSectionEmpty(self, row, column, direction, ship):
		if self.buttonTiles[row][column].getShip() == None:
			if direction == self.LEFT:
				if column - ship.getLength() < 0:
					return False
				else:
					for i in range(column, column - ship.getLength(), -1):
						if self.buttonTiles[row][i].getShip() != None:
							return False
					return True
				
			elif direction == self.UP:
				if row - ship.getLength() < 0:
					return False
				else:
					for i in range(row, row - ship.getLength(), -1):
						if self.buttonTiles[i][column].getShip() != None:
							return False
					return True
				
			elif direction == self.RIGHT:
				if column + ship.getLength() > 5:
					return False
				else:
					for i in range(column, column + ship.getLength()):
						if self.buttonTiles[row][i].getShip() != None:
							return False
					return True
				
			elif direction == self.DOWN:
				if row + ship.getLength() > 5:
					return False
				else:
					for i in range(row, row + ship.getLength()):
						if self.buttonTiles[i][column].getShip() != None:
							return False
					return True
		else:
			return False

	def placeShip(self, row, column, direction, ship):
		if direction == self.LEFT:
			for i in range(column, column - ship.getLength(), -1):
				self.buttonTiles[row][i].setShip(ship)
				
		if direction == self.UP:
			for i in range(row, row - ship.getLength(), -1):
				self.buttonTiles[i][column].setShip(ship)
				
		if direction == self.RIGHT:
			for i in range(column, column + ship.getLength(), 1):
				self.buttonTiles[row][i].setShip(ship)
				
		if direction == self.DOWN:
			for i in range(row, row + ship.getLength(), 1):
				self.buttonTiles[i][column].setShip(ship)
	def getPlayerNumber(self):
		return self.playerNumber

	def allShipsDestroyed(self):
		for ship in self.ships:
			for value in ship.getHitList():
				if value == False:
					return False
		return True
				
class Ship:
	def __init__(self, length):
		self.length = length
		self.hitList = [False] * self.length

	def hit(self):
		shipRemoved = False
		iterator = 0
		while shipRemoved == False:
			if self.hitList[iterator] == False:
				self.hitList[iterator] = True
				shipRemoved = True
			iterator += 1

	def getLength(self):
		return self.length

	def checkDestroyed(self):
		for i in self.hitList:
			if i == False:
				return False
		return True

	def getHitList(self):
		return self.hitList

#--------------------------
# Grid creation
#--------------------------
#def drawGrid(surface,grid_size):

#	center_offset_left = (w/2) - 48 - grid_size
#	center_offset_right = (w/2) + 48 + grid_size

#	#First grid
#	#Vertical Lines
#	for i in range(0, 24*grid_size+1, 24):
#		pg.draw.line(surface, text_color, (i, h/3), (i, (h/3)+24*grid_size))
#	# Horizontal Lines
#	for i in range(int(h/3), int(h/3)+24*grid_size+1, 24):
#		pg.draw.line(surface, text_color, (0, i), (24*grid_size, i))

#	#Second grid
#	#Vertical Lines
#	for i in range(w-24*grid_size, w, 24):
#		pg.draw.line(surface, text_color, (i, (h/3)), (i, (h/3)+24*grid_size))
#	# Horizontal Lines
#	for i in range(int(h/3), int(h/3)+24*grid_size+1, 24):
#		pg.draw.line(surface, text_color, (w, i), (w-24*grid_size, i))

#	pg.draw.line(surface, text_color, (w-1, h/3), (w-1, (h/3)+(24*grid_size)))

def drawGrid(surface,grid_size):

	center_offset_left = int((w/2) - (24*5 + 24*grid_size))
	center_offset_right = int((w/2) + 24*5)

	#First grid
	#Vertical Lines
	for i in range(0, 24*grid_size+1, 24):
		pg.draw.line(surface, text_color, (i + center_offset_left, h/3), (i + center_offset_left, (h/3)+24*grid_size))
	# Horizontal Lines
	for i in range(int(h/3), int(h/3)+24*grid_size+1, 24):
		pg.draw.line(surface, text_color, (0 + center_offset_left, i), (center_offset_left + 24*grid_size, i))

	#Second grid
	#Vertical Lines
	#for i in range(int(w-24*grid_size), int(w), 24):
	#	pg.draw.line(surface, text_color, (i + center_offset_right, (h/3)), (i + center_offset_right, (h/3)+24*grid_size))
	for i in range(center_offset_right, center_offset_right + 24*grid_size + 24, 24):
		pg.draw.line(surface, text_color, (i, (h/3)), (i, (h/3)+24*grid_size))
	# Horizontal Lines
	for i in range(int(h/3), int(h/3)+24*grid_size+1, 24):
		pg.draw.line(surface, text_color, (center_offset_right, i), (center_offset_right + 24*grid_size, i))

#--------------------------
# Music For In Game Play
#--------------------------
def gameplay_music_engine(volume_level):
	pg.init()
	pg.mixer.music.stop()
	pg.mixer.music.load('sounds\MusicGunnerFight.ogg')
	pg.mixer.music.set_volume(volume_level)
	pg.mixer.music.play(-1)

#--------------------------
# Gameplay Controller
#--------------------------
def RunGame(grid_size, volume_level, color_text, color_background):
	global text_color
	global back_color

	pg.init()

	text_color = color_text
	back_color = color_background

	player1 = Player(True, 1, surface, grid_size)
	player2 = Player(False, 2, surface, grid_size)

	upNext = 2
	limboMode = False 

	font = pg.font.SysFont("none", 24)
	text2 = font.render("Click to begin turn", True, text_color)
	exitButton = Button(w /2 -62.5, h - h/4 - 25, 125, 50, text_color, surface)

	#Sounds begin playing after initialization of drawings
	gameplay_music_engine(volume_level)
	game_over_sound = pg.mixer.Sound("sounds\SmallApplause.wav")

	while True:
		#Checking for game events'
		tileClicked = False
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					done = True
					pg.mixer.music.stop()
					#Return 0 for main menu
					return 0
				
			if event.type == pg.MOUSEBUTTONDOWN:
				if player2.getTurn() == True:
					for row in player1.getButtonTiles():
						for tile in row:
							feels = tile.wasClicked(pg.mouse.get_pos())
							if feels == True:
								tileClicked = True
					if exitButton.wasClicked(pg.mouse.get_pos()):
						#Return 0 for main menu
						return 0

				if player1.getTurn() == True:		
					for row in player2.getButtonTiles():
						for tile in row:
							feels = tile.wasClicked(pg.mouse.get_pos())
							if feels == True:
								tileClicked = True
					if exitButton.wasClicked(pg.mouse.get_pos()):
						#Return 0 for main menu
						return 0
								
				if limboMode == True:
					if upNext == 2:
						player2.flipTurn()
						upNext = 1
						limboMode = False
					else:
						player1.flipTurn()
						upNext = 2
						limboMode = False
			
							
			if tileClicked == True:
				if player1.getTurn() == True:
					player1.flipTurn()
					limboMode = True
				elif player2.getTurn() == True:
					player2.flipTurn()
					limboMode = True

		surface.fill(back_color)
		player1.drawTiles()
		player2.drawTiles()
		exit_text = font.render("Exit to Menu", True, back_color)
		exitButton.draw()
		surface.blit(exit_text, (w/2 - exit_text.get_width() / 2, h - h/4 - 5))
		if not limboMode:
			if upNext == 1:
				text = font.render("Player 2's turn!", True, text_color)
			else:
				text = font.render("Player 1's turn!", True, text_color)
			surface.blit(text,(w /2 - text.get_width() / 2, 50))
		else:
			text = font.render("Player " + str(upNext) + " is up next! Click to continue", True, text_color)
			surface.blit(text,(w /2 - text.get_width() / 2, 50))
		drawGrid(surface, grid_size)
		pg.display.update()

		if player1.allShipsDestroyed():
			pg.mixer.Sound.play(game_over_sound)
			return 2
			
		if player2.allShipsDestroyed():
			pg.mixer.Sound.play(game_over_sound)
			return 1
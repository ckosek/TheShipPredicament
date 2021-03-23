import pygame as pg
import sys, random
from pygame.locals import *

#Initiating pygame
pg.init()

#Set surface as Fullscreen Display
surface = pg.display.set_mode((0,0),pg.FULLSCREEN)
monitor_info = pg.display.Info()
		
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
		self.color = WHITE
		self.isClickableOverride = False
		self.rectangle = (xPos, yPos, width, height)
		self.ship = None
		self.playerNumber = playerNumber

	def wasClicked(self, clickPos):
		if self.isClickable():
			if clickPos[0] > self.xPos and clickPos[0] < self.xPos + self.width:
				if clickPos[1] > self.yPos and clickPos[1] < self.yPos + self.height:
					self.hasBeenClicked = True
					if self.ship != None:
						self.setStatus(self.HIT)
						self.ship.hit()
						self.shipDestroyedAnimation()
					else:
						self.setStatus(self.MISS)
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
		self.color = WHITE
		if self.ship != None and (playerTurn == True or self.status == self.HIT or self.status == self.MISS):
			if self.playerNumber == 2:
				value = self.getShip().getLength()
				self.color = (100 + value * 30, 100 + value * 30, 100 + value * 30 )
			if self.playerNumber == 1:
				value = self.getShip().getLength()
				self.color = (0, 100 + value * 30, 0 )
		elif self.playerNumber == 2:
			self.color = (0,191,255)
				
		pg.draw.rect(self.surface, self.color, self.rectangle)

		if not self.isClickable():
			if self.status == self.HIT:
				pg.draw.line(self.surface, RED, (self.xPos, self.yPos), (24 + self.xPos, 24 + self.yPos))
				pg.draw.line(self.surface, RED, (24 + self.xPos, self.yPos), (self.xPos, 24 + self.yPos))
			elif self.status == self.MISS:
				pg.draw.circle(self.surface, RED, (12 + self.xPos,12 + self.yPos), 12, 1)

	def setShip(self, ship):
		self.ship = ship

	def shipDestroyedAnimation(self):
		if self.ship.checkDestroyed():
			font = pg.font.SysFont("none", 24)
			if self.playerNumber == 1:
				text = font.render("Player 2 ship destroyed!", True, WHITE)
				taunts = ["'You're a natural'", "'Easiest kill of my life!'", "'Roger, looks like we got a code E-Z.'", "'Are you even trying?'", "'Oops, did I do that?'", "'Was that ship made of paper?'"]
				text2 = font.render(taunts[random.randint(0, 5)], True, WHITE)
			if self. playerNumber == 2:
				text = font.render("Player 1 ship destroyed!", True, WHITE)
				taunts = ["'That was easy.'", "'Supreme Leader South will love that'", "'RIP Jack Sparrow'", "'FRESH MEAT!'", "'This predicament will be over in no time'", "'We live in a society'" ]
				text2 = font.render(taunts[random.randint(0, 5)], True, WHITE)
			loopFinished = False
			while loopFinished == False:
				for event in pg.event.get():
					if event.type == pg.QUIT:
						pg.quit()
						sys.exit()
					if event.type == pg.MOUSEBUTTONDOWN:
							loopFinished = True
				self.surface.fill(BLACK)
				self.surface.blit(text, (monitor_info.current_w /2 - text.get_width() / 2, 50))
				self.surface.blit(text2, (monitor_info.current_w /2 - text.get_width() / 2, monitor_info.current_h / 2))
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
					temp.append(GameTile(250 + 24*i, 300 + 24*j, 24, 24, 1, self.surface))
				else:
					temp.append(GameTile(1000 + 24*i, 300 + 24*j, 24, 24, 2, self.surface))
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
def drawGrid(surface,grid_size):
	#First grid
	#Vertical Lines
	for i in range(250, 250+24*grid_size+1, 24):
		pg.draw.line(surface, BLACK, (i, 300), (i, 300+24*grid_size))
	# Horizontal Lines
	for i in range(300, 300+24*grid_size+1, 24):
		pg.draw.line(surface, BLACK, (250, i), (250+24*grid_size, i))

	#Second grid
	#Vertical Lines
	for i in range(1000, 1000+24*grid_size+1, 24):
		pg.draw.line(surface, BLACK, (i, 300), (i, 300+24*grid_size))
	# Horizontal Lines
	for i in range(300, 300+24*grid_size+1, 24):
		pg.draw.line(surface, BLACK, (1000, i), (1000+24*grid_size, i))

def gameplay_sound_engine():
	pg.init()
	pg.mixer.music.stop()
	pg.mixer.music.load('sounds\MusicGunnerFight.ogg')
	pg.mixer.music.play(-1)

def RunGame(grid_size):

	player1 = Player(True, 1, surface, grid_size)
	player2 = Player(False, 2, surface, grid_size)

	upNext = 2
	limboMode = False 

	font = pg.font.SysFont("none", 24)
	text2 = font.render("Click to begin turn", True,WHITE)


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
					#main_menu() call is where this will be sent
					return
				
			if event.type == pg.MOUSEBUTTONDOWN:
				if player2.getTurn() == True:
					for row in player1.getButtonTiles():
						for tile in row:
							feels = tile.wasClicked(pg.mouse.get_pos())
							if feels == True:
								tileClicked = True

				if player1.getTurn() == True:		
					for row in player2.getButtonTiles():
						for tile in row:
							feels = tile.wasClicked(pg.mouse.get_pos())
							if feels == True:
								tileClicked = True
								
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

		surface.fill(BLACK)
		player1.drawTiles()
		player2.drawTiles()
		if not limboMode:
			if upNext == 1:
				text = font.render("Player 2's turn!", True, WHITE)
			else:
				text = font.render("Player 1's turn!", True, WHITE)
			surface.blit(text,(monitor_info.current_w /2 - text.get_width() / 2, 50))
		else:
			text = font.render("Player " + str(upNext) + " is up next! Click to continue", True, WHITE)
			surface.blit(text,(monitor_info.current_w /2 - text.get_width() / 2, 50))
		drawGrid(surface, grid_size)
		pg.display.update()

		if player1.allShipsDestroyed():
			loopFinished = False
			font = pg.font.SysFont("none", 24)
			text = font.render("Player 1 has won!", True,WHITE)
			while loopFinished == False:
				for event in pg.event.get():
					if event.type == pg.QUIT:
						pg.quit()
						sys.exit()
					if event.type == pg.MOUSEBUTTONDOWN:
						loopFinished = True
				surface.fill(BLACK)
				surface.blit(text, (monitor_info.current_w /2 - text.get_width() / 2, 50))
				pg.display.update()
			upNext = 2
			limboMode = False
			player1 = Player(True, 1, surface, grid_size)
			player2 = Player(False, 2, surface, grid_size)
			
		if player2.allShipsDestroyed():
			loopFinished = False
			font = pg.font.SysFont("none", 24)
			text = font.render("Player 2 has won!", True,WHITE)
			while loopFinished == False:
				for event in pg.event.get():
					if event.type == pg.QUIT:
						pg.quit()
						sys.exit()
					if event.type == pg.MOUSEBUTTONDOWN:
						loopFinished = True
				surface.fill(BLACK)
				surface.blit(text, (monitor_info.current_w /2 - text.get_width() / 2, 50))
				pg.display.update()
			upNext = 2
			limboMode = False
			player1 = Player(True, 1, surface, grid_size)
			player2 = Player(False, 2, surface, grid_size)
			

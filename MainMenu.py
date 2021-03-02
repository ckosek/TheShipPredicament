import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import pygame as pg
import pygame_menu as pm
from pygame_menu import sound

#---------------------
#Constants and Globals
#---------------------

#Set surface as Fullscreen Display
surface = pg.display.set_mode((0,0),pg.FULLSCREEN)

#Used for debugging
#Note: Do not actually resize the window, this may cause window errors
#surface = pg.display.set_mode((700,700),pg.RESIZABLE)

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

#Color set for Text
color = RED
color_default = 0

#Color set for Background
back_color = BLACK
back_color_default = 0

#Volume set for sounds
volume_level = 0.2
volume_default = 2

#Player set for play menu
players = 1
player_default = 0
player_str = 'Players: 1 :'

#Difficulty set for play menu
difficulty = 1
difficulty_default = 0
difficulty_str = 'Difficulty: Easy :'

#Grid size set for play menu
grid_size = 10
grid_default = 0
grid_str = 'Grid Size: 10 x 10 :'

#---------------------
#Methods/Functions
#---------------------

#Method: Sets color for text based on input
def set_color(name, value):
	global color
	global color_default

	if value == 1:
		color = RED #RED
		color_default = value-1
		options_menu()
	if value == 2:
		color = BLUE #BLUE
		color_default = value-1
		options_menu()
	if value == 3:
		color = GREEN #GREEN
		color_default = value-1
		options_menu()
	else:
		color = RED #RED BACKUP
		color_default = 0
		options_menu()

#Method: sets color of background based on input
def set_background(name, value):
	global back_color
	global back_color_default

	if value == 1:
		back_color = BLACK #BLACK
		back_color_default = value-1
		options_menu()
	if value == 2:
		back_color = WHITE #WHITE
		back_color_default = value-1
		options_menu()
	if value == 3:
		back_color = GRAY #GRAY
		back_color_default = value-1
		options_menu()
	else:
		back_color = BLACK #BLACK BACKUP
		back_color_default = 0
		options_menu()

#Method: Creates the theme used for all menus
def set_theme():
	eight_bit_font = pm.font.FONT_8BIT
	title_theme = pm.widgets.MENUBAR_STYLE_NONE
	font_size = 37
	select_box_color = WHITE
	if back_color == WHITE:
		select_box_color = BLACK
		
	current_theme = pm.themes.Theme(background_color=back_color, widget_font=eight_bit_font, title_bar_style=title_theme, 
							menubar_close_button=True, title_font=eight_bit_font, title_font_color=color, 
							title_font_size=font_size, selection_color=select_box_color)
	return current_theme

#Method: Creates the sound engine used with menus and gameplay
def create_sound_engine():
	engine = sound.Sound()
	engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, sound.SOUND_EXAMPLE_CLICK_MOUSE)
	engine.set_sound(sound.SOUND_TYPE_CLOSE_MENU, sound.SOUND_EXAMPLE_CLOSE_MENU)
	engine.set_sound(sound.SOUND_TYPE_ERROR, sound.SOUND_EXAMPLE_ERROR)
	engine.set_sound(sound.SOUND_TYPE_EVENT, sound.SOUND_EXAMPLE_EVENT)
	engine.set_sound(sound.SOUND_TYPE_EVENT_ERROR, sound.SOUND_EXAMPLE_EVENT_ERROR)
	engine.set_sound(sound.SOUND_TYPE_KEY_ADDITION, sound.SOUND_EXAMPLE_KEY_ADD)
	engine.set_sound(sound.SOUND_TYPE_KEY_DELETION, sound.SOUND_EXAMPLE_KEY_DELETE)
	engine.set_sound(sound.SOUND_TYPE_OPEN_MENU, sound.SOUND_EXAMPLE_OPEN_MENU)
	engine.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION, sound.SOUND_EXAMPLE_WIDGET_SELECTION)
	return engine


#Method: Begins background music play, stops upon exiting the game
def background_music_loop():
	global volume_level
	pg.init()
	pg.mixer.music.load('MusicGameplay.ogg')
	pg.mixer.music.set_volume(volume_level)
	pg.mixer.music.play(-1) #loops forevever while game is up

#Method: Sets the volume level and default for the sound engine
#Note: volume levels are only set between 0.0 and 1.0
def set_volume_level(name, value):
	global volume_level
	global volume_default
	volume_level = value * 0.1
	volume_default = value
	pg.init()
	pg.mixer.music.stop()
	background_music_loop()
	options_menu()

#Method: Sets the items to be used by the options menu volume selector
def set_volume_items():
	volume_int_list = []
	volume_str_list = []
	volume_int_list = [i for i in range(0,11)]
	for a in volume_int_list:
		a = str(a)
		volume_str_list.append(a)
	volume_items = list(zip(volume_str_list, volume_int_list))
	return volume_items

#Method: Sets the difficulty level for Single Player games
def set_difficulty(name, value):
	global difficulty
	global difficulty_default
	global difficulty_str
	
	if value == 1:
		difficulty = value #EASY
		difficulty_default = value - 1
		difficulty_str = 'Difficulty: Easy :'
		play_menu()
	if value == 2:
		difficulty = value #MEDIUM
		difficulty_default = value - 1
		difficulty_str = 'Difficulty: Medium :'
		play_menu()
	if value == 3:
		difficulty = value #HARD
		difficulty_default = value - 1
		difficulty_str = 'Difficulty: Hard :'
		play_menu()
	else:
		difficulty = 1 #EASY DEFAULT
		difficulty_default = 0
		difficulty_str = 'Difficulty: Easy :'
		play_menu()

#Method: Sets the number of players, 1 or 2
def set_players(name, value):
	global players
	global player_default
	global player_str

	if value == 1:
		players = value #ONE PLAYER
		player_default = value - 1
		player_str = 'Players: 1 :'
		play_menu()
	if value == 2:
		players = value #TWO PLAYERS
		player_default = value - 1
		player_str = 'Players: 2 :'
		play_menu()
	else:
		players = 1 #ONE PLAYER DEFAULT
		difficulty_default = 0
		player_str = 'Players: 1 :'
		play_menu()

#Method: Sets the grid size to use during play
def set_grid_size(name, value):
	global grid_size
	global grid_default
	global grid_str

	if value == 10:
		grid_size = value # 10x10
		grid_default = 0
		grid_str = 'Grid Size: 10 x 10 :'
		play_menu()
	if value == 15:
		grid_size = value # 15x15
		grid_default = 1
		grid_str = 'Grid Size: 15 x 15 :'
		play_menu()
	if value == 20:
		grid_size = value # 20x20
		grid_default = 2
		grid_str = 'Grid Size: 20 x 20 :'
		play_menu()
	else:
		grid_size = 10 # 10x10 DEFAULT
		grid_default = 0
		grid_str = 'Grid Size: 10 x 10 :'
		play_menu()

#Method: Begins the game after options are set
def start_the_game():
	# Do the job here !
	pass

#--------------------------
# Main Menu
#--------------------------
def main_menu():
	pg.init()
	global surface
	global color
	global back_color

	mytheme = set_theme()
	sound_engine = create_sound_engine()

	menu = pm.Menu(700, 700, 'The Ship Predicament', theme=mytheme)

	menu.add_button('Play', play_menu, font_color=color)
	menu.add_button('Options', options_menu, font_color=color)
	menu.add_button('Exit', pm.events.EXIT, font_color=color)
	menu.set_sound(sound_engine)

	menu.mainloop(surface)

#--------------------------
# Options Menu
#--------------------------
def options_menu():
	pg.init()
	global surface
	global color
	global back_color
	global volume_default

	mytheme = set_theme()
	sound_engine = create_sound_engine()
	volume_items = set_volume_items()
	
	options_sub = pm.Menu(700, 700, 'Options', theme=mytheme)

	options_sub.add_label('Press Enter To')
	options_sub.add_label('Apply Selected Item')
	options_sub.add_vertical_margin(30)
	options_sub.add_selector('Music Volume ', volume_items, default=volume_default, onreturn=set_volume_level, font_color=color)
	options_sub.add_selector('Text Color ', [('Red', 1), ('Blue', 2), ('Green', 3)], default=color_default, onreturn=set_color, font_color=color)
	options_sub.add_selector('Background ', [('Black', 1), ('White', 2), ('Gray', 3)], default=back_color_default, onreturn=set_background, font_color=color)
	options_sub.add_vertical_margin(50)
	options_sub.add_button('[ Main Menu ]', main_menu, font_color=color)
	options_sub.set_sound(sound_engine)
	
	options_sub.mainloop(surface)

#-------------------------------------------
# Play Menu and Final Settings Confirmation
#-------------------------------------------
def play_menu():
	pg.init()
	global surface
	global color
	global back_color

	mytheme = set_theme()
	sound_engine = create_sound_engine()

	play_setting_sub = pm.Menu(700, 700, 'Confirm Settings', theme=mytheme)

	play_setting_sub.add_label(player_str)
	play_setting_sub.add_label(difficulty_str)
	play_setting_sub.add_label(grid_str)
	play_setting_sub.add_vertical_margin(30)
	play_setting_sub.add_button('[ Confirm ]', start_the_game, font_color=color)
	play_setting_sub.add_button('[ Back ]', pm.events.BACK, font_color=color)
	play_setting_sub.set_sound(sound_engine)

	play_sub = pm.Menu(700, 700, 'Game Setup', theme=mytheme)

	play_sub.add_label('Press Enter To')
	play_sub.add_label('Apply Selected Item')
	play_sub.add_vertical_margin(30)
	play_sub.add_selector('Players ', [('1 Player', 1), ('2 Player', 2)], default=player_default, onreturn=set_players, font_color=color)
	play_sub.add_selector('Difficulty ', [('Easy', 1), ('Medium', 2), ('Hard', 3)], default=difficulty_default, onreturn=set_difficulty, font_color=color)
	play_sub.add_selector('Grid Size ', [('10 x 10', 10), ('15 x 15', 15), ('20 x 20', 20)], default=grid_default, onreturn=set_grid_size, font_color=color)
	play_sub.add_button('[ Go ]', play_setting_sub, font_color=color)
	play_sub.add_vertical_margin(50)
	play_sub.add_button('[ Main Menu ]', main_menu, font_color=color)
	play_sub.set_sound(sound_engine)

	play_sub.mainloop(surface)

#--------------------------
# Main Statement
#--------------------------
if __name__ == '__main__':
	background_music_loop()
	main_menu()
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import pygame as pg
import pygame_menu as pm

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

#Method: Sets color for text based on input
def set_color(name, value):
	global color
	global color_default
	# Changes color to options value selection
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
		options_menu()

#Method: sets color of background based on input
def set_background(name, value):
	global back_color
	global back_color_default
	# Changes color to options value selection for menu background
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
		options_menu()

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

def set_volume(name, value):
	#Set up volume level
	pass

def set_difficulty(value, difficulty):
	# Do the job here !
	pass

def start_the_game():
	# Do the job here !
	pass

def main_menu():
	pg.init()
	surface = pg.display.set_mode((0,0),pg.FULLSCREEN)
	global color
	global back_color

	mytheme = set_theme()

	menu = pm.Menu(700, 700, 'The Ship Predicament', theme=mytheme)

	#menu.add_image('C:\\Users\Alex McDonald\Desktop\CSE 550\warships-uss-new-jersey-bb-62-battleship-hd-wallpaper-preview.jpg')
	menu.add_selector('Difficulty ', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=set_difficulty, font_color=color)
	menu.add_button('Play', start_the_game, font_color=color)
	menu.add_button('Options', options_menu, font_color=color)
	menu.add_button('Exit', pm.events.EXIT, font_color=color)

	menu.mainloop(surface)


def options_menu():
	pg.init()
	surface = pg.display.set_mode((0,0),pg.FULLSCREEN)
	global color
	global back_color

	mytheme = set_theme()

	volume_int_list = []
	volume_str_list = []
	volume_int_list = [i for i in range(0,101)]
	for a in volume_int_list:
		a = str(a)
		volume_str_list.append(a)
	volume_items = list(zip(volume_str_list, volume_int_list))
	
	menu = pm.Menu(700, 700, 'Options', theme=mytheme)

	menu.add_label('Press Enter To')
	menu.add_label('Apply Selected Item')
	menu.add_vertical_margin(30)
	menu.add_selector('Volume ', volume_items, onchange=set_volume, font_color=color)
	menu.add_selector('Text Color ', [('Red', 1), ('Blue', 2), ('Green', 3)], default=color_default, onreturn=set_color, font_color=color)
	menu.add_selector('Background ', [('Black', 1), ('White', 2), ('Gray', 3)], default=back_color_default, onreturn=set_background, font_color=color)
	menu.add_vertical_margin(50)
	menu.add_button('[ Main Menu ]', main_menu, font_color=color)

	menu.mainloop(surface)

if __name__ == '__main__':
	main_menu()


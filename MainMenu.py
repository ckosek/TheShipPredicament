import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import pygame as pg
import pygame_menu as pm

color = (255,50,50)

def set_color(name, value):
	global color
	if value == 1:
		color = (255,50,50)
		options_menu()
	if value == 2:
		color = (0,0,255)
		options_menu()
	if value == 3:
		color = (0,255,0)
		options_menu()
	else:
		color = (255,50,50)
		options_menu()

def main_menu():
	pg.init()
	surface = pg.display.set_mode((0,0),pg.FULLSCREEN)
	global color
	def set_difficulty(value, difficulty):
		# Do the job here !
		pass

	def start_the_game():
		# Do the job here !
		pass


	eight_bit_font = pm.font.FONT_8BIT
	title_theme = pm.widgets.MENUBAR_STYLE_NONE
	mytheme = pm.themes.Theme(background_color=(0,0,0), widget_font=eight_bit_font, title_bar_style=title_theme, 
							menubar_close_button=True, title_font=eight_bit_font, title_font_color=color)

	menu = pm.Menu(700, 700, 'The Ship Predicament', theme=mytheme)
	#menu = pm.Menu(500, 500, 'The Ship Predicament', theme=pm.themes.THEME_DARK)

	#menu.add_text_input('Name :', default='John Doe')
	menu.add_selector('Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=set_difficulty, font_color=color)
	menu.add_button('Play', start_the_game, font_color=color)
	menu.add_button('Options', options_menu, font_color=color)
	menu.add_button('Quit', pm.events.EXIT, font_color=color)

	menu.mainloop(surface)


def options_menu():
	pg.init()
	surface = pg.display.set_mode((0,0),pg.FULLSCREEN)
	global color

	eight_bit_font = pm.font.FONT_8BIT
	title_theme = pm.widgets.MENUBAR_STYLE_NONE
	mytheme = pm.themes.Theme(background_color=(0,0,0), widget_font=eight_bit_font, title_bar_style=title_theme, 
							menubar_close_button=True, title_font=eight_bit_font, title_font_color=color)

	menu = pm.Menu(700, 700, 'Options', theme=mytheme)
	#menu = pm.Menu(500, 500, 'The Ship Predicament', theme=pm.themes.THEME_DARK)

	#menu.add_text_input('Name :', default='John Doe')
	menu.add_selector('Text Color :', [('Red', 1), ('Blue', 2), ('Green', 3)], onreturn=set_color, font_color=color)
	menu.add_button('Back to Main Menu', main_menu, font_color=color)

	menu.mainloop(surface)

if __name__ == '__main__':
	main_menu()


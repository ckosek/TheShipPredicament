import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import Menus

#--------------------------
# Main Statement
#--------------------------
if __name__ == '__main__':
	Menus.background_music_loop()
	Menus.main_menu()
#!/usr/bin/env python3

import os
import sys
import urbandictionary as ud
from tkinter import *
from svg2can import Svg2Can
from hangman import Hangman
from hangman_text_view import HangmanTextView
from hangman_text_controller import HangmanTextController
from hangman_tkinter_view import HangmanTkinterView
from hangman_tkinter_controller import HangmanTkinterController


if __name__ == '__main__':

	h = Hangman()
	is_gui = len(sys.argv) <= 1 or (len(sys.argv) > 1 and sys.argv[1] != 'cli')
	
	if (is_gui):
		window = Tk()
	
		hv = HangmanTkinterView(h, window)
		hc = HangmanTkinterController(h, hv)
		hv.controller = hc
		window.mainloop()
	else:
		hv = HangmanTextView(h)
		hc = HangmanTextController(h, hv)
		hc.run_game_loop()
	
	


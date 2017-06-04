#!/usr/bin/python3

import urbandictionary as ud
from tkinter import *
from svg2can import Svg2Can
from hangman import Hangman
from hangman_tkinter_view import HangmanTkinterView
from hangman_tkinter_controller import HangmanTkinterController


if __name__ == '__main__':

	h = Hangman()
	#hv = HangmanTextView(h)
	#hc = HangmanTextController(h, hv)
	window = Tk()
	
	hv = HangmanTkinterView(h, window)
	hc = HangmanTkinterController(h, hv)
	hv.controller = hc
	window.mainloop()
	
	
	#hc.run_game_loop()
	
	


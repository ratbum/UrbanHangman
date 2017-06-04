#!/usr/bin/python3

import urbandictionary as ud
from tkinter import *
from svg2can import Svg2Can

from hangman import Hangman
from hangman_tkinter_view import HangmanTkinterView

class HangmanTkinterController:
	
	def __init__(self, hangman, view):
		self._hangman = hangman
		self._view = view
		view.start_button.bind("<Button-1>", self.run_game)
		view.draw_all()
		view.mainframe.bind("<KeyPress>", self.key_press)
		view.mainframe.focus_set()
		view.mainframe.pack()
		
	def key_press(self, event):
		self._hangman.letter_guess(event.char)
		self._view.draw_all()
		
	
	def run_game(self, event):
		self._hangman.reset()
		self._hangman.generate_random_word()
		self._view.draw_all()



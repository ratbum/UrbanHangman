#!/usr/bin/python3

import urbandictionary as ud
from tkinter import *
from svg2can import Svg2Can

from hangman import Hangman

class HangmanTkinterView:
	def __init__(self, hangman, root):
		self._hangman = hangman
		self._root = root
		self.create_layout()
		self.draw_all()
	
	def draw_hangman_stage(self, stage_index):
		
		if (stage_index < 0 or stage_index > Hangman.MAX_DEATH_POINTS):
			raise IndexError('No such image', 'Must be a number between 0 and Hangman.MAX_DEATH_POINTS')
		self._hangman_image.delete('all')
		if (stage_index == 0):
			# clearing the canvas is sufficient to draw stage 0
			return
		svg2can = Svg2Can()
		svg2can.draw_svg_from_file_on_canvas(self._hangman_image, '/Users/thomaslee/Documents/hangmen/hangman-{0:02d}.svg'.format(stage_index))
	
	def draw_all(self):
		self.draw_hangman_stage(self._hangman.death_points)
		self._word_string_var.set(self.word_as_guessed)
		self.mainframe.pack()
	
	def create_layout(self):
		self.mainframe = Frame(self._root)
		self.start_button = Button(self.mainframe, text='Start')
		self._word_string_var = StringVar()
		self._word_label = Label(self.mainframe, textvariable=self._word_string_var)
		self._hangman_image = Canvas(self.mainframe, width=160, height=248)
		self.draw_hangman_stage(0)
		self._hangman_image.pack()
		self._word_label.pack(expand=1, fill=X)
		self.start_button.pack()
		self.mainframe.pack()
		
	@property
	def letters_incorrect(self):
		return ', '.join(self._hangman._guessed_letters_incorrect)
		
	@property
	def word_as_guessed(self):
		word_as_guessed = self._hangman.word_as_guessed
		word_as_guessed[:] = [c if c != None else '_' for c in word_as_guessed]
		return ' '.join(word_as_guessed)
		
	@property
	def gallows(self):
		return HangmanTextView.TEXTUAL_HANGING_STATES[self._hangman.death_points]
		
	@property
	def game_state(self):
		return self.letters_incorrect + '\n' + self.gallows + '\n' + self.word_as_guessed
		
	def victory(self):
		return 'VICTORY!'
		
	def defeat(self):
		return 'DEFEAT!'

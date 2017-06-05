import os
import urbandictionary as ud
from tkinter import *
from svg2can import Svg2Can

from hangman import Hangman

class HangmanTkinterView:
	def __init__(self, hangman, root):
		self._hangman = hangman
		self._root = root
		self._word_string_var = StringVar()
		self._message_string_var = StringVar()
		self._definition_string_var = StringVar()
		self.create_layout()
		self.draw_all()
		
	def set_message(self, message):
		self._message_string_var.set(message)
		
	def show_definition(self):
		self._definition_string_var.set('{}\n\n{}'.format(self._hangman.word, self._hangman.word_definition))
	
	def clear_definition(self):
		self._definition_string_var.set('')
	
	
	def draw_hangman_stage(self, stage_index):
		
		if (stage_index < 0 or stage_index > Hangman.MAX_DEATH_POINTS):
			raise IndexError('No such image', 'Must be a number between 0 and Hangman.MAX_DEATH_POINTS')
		self._hangman_image.delete('all')
		if (stage_index == 0):
			# clearing the canvas is sufficient to draw stage 0
			return
		
		location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
		
		svg2can = Svg2Can()
		svg2can.draw_svg_from_file_on_canvas(self._hangman_image, os.path.join(location, './hangmen/hangman-{0:02d}.svg'.format(stage_index)))
	
	def draw_all(self):
		self.draw_hangman_stage(self._hangman.death_points)
		self._word_string_var.set(self.word_as_guessed)
		self.mainframe.pack()
	
	def create_layout(self):
		self.mainframe = Frame(self._root, width=1000, height=248)
		
		top_frame = Frame(self.mainframe, bg='red')
		message_label = Label(top_frame, textvariable=self._message_string_var, anchor=W, justify=LEFT)
		message_label.pack(fill=X)
		top_frame.pack(fill=X, padx=5, pady=5)
		
		left_frame = Frame(self.mainframe, width=200, height=248)
		right_frame = Frame(self.mainframe, width=160, height=248, highlightbackground="black", highlightcolor="black", highlightthickness=1, bg='white')
		bottom_frame = Frame(self.mainframe, width=500, height=40)
		
		self.start_button = Button(left_frame, text='Start', width=10)
		word_label = Label(left_frame, textvariable=self._word_string_var)
		self._hangman_image = Canvas(right_frame, width=160, height=248, bg='white')
		message_label = Label(bottom_frame, textvariable=self._definition_string_var, anchor=W, justify=LEFT, wraplength=400)
		
		self._hangman_image.pack()
		message_label.pack(side=LEFT, fill=X)
		word_label.pack(fill=X, side=TOP)
		self.start_button.pack(side=BOTTOM, fill=X)
		
		bottom_frame.pack(side=BOTTOM, fill=X)
		left_frame.pack(fill=Y, side=LEFT, padx=(5, 10), pady=5)
		right_frame.pack(side=RIGHT)
		self.mainframe.pack(padx=10, pady=(0, 10))		
		
		
	@property
	def letters_incorrect(self):
		return ', '.join(self._hangman._guessed_letters_incorrect)
		
	@property
	def word_as_guessed(self):
		word_as_guessed = self._hangman.word_as_guessed
		word_as_guessed[:] = [c if c != None else '_' for c in word_as_guessed]
		return ' '.join(word_as_guessed)
		
	@property
	def game_state(self):
		return self.letters_incorrect + '\n' + self.gallows + '\n' + self.word_as_guessed


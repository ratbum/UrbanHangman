import urbandictionary as ud
from tkinter import *
from svg2can import Svg2Can


class Hangman:
	MAX_DEATH_POINTS = 10
	
	def __init__(self):
		self.reset()
		self._word = ''

	def generate_random_word(self):
		udword = ud.random()[0]
		self._word = udword.word
		self._word_lower_case = self._word.lower()
		self._word_definition = udword.definition
		if ' ' in self._word:
			self._guessed_letters_correct.append(' ')
		if '-' in self._word:
			self._guessed_letters_correct.append('-')
		
	def reset(self):
		self._word = ''
		self._word_lower_case = ''
		self._word_definitition = ''
		self._guessed_letters_correct = []
		self._guessed_letters_incorrect = []

	@property
	def word(self):
		return self._word
	
	@property
	def word_definition(self):
		return self._word_definition
	
	@property
	def death_points(self):
		return len(self._guessed_letters_incorrect)
	
	def letter_guess(self, c):
		if not c.isalpha() or len(c) != 1:
			raise Exception('Expected letter', 'letter_guess accepts only single characters')
		
		c = c.lower()
		
		if c in self._guessed_letters_correct or c in self._guessed_letters_incorrect:
			raise Exception('Already guessed', 'letter_guess doesn\'t accept repeats')
		
		if c in self._word_lower_case:
			self._guessed_letters_correct.append(c)
			return True
		else:
			self._guessed_letters_incorrect.append(c)
			return False
	
	@property
	def is_victory(self):
		return None not in self.word_as_guessed
	
	@property
	def is_defeat(self):
		return self.death_points == Hangman.MAX_DEATH_POINTS
	
	@property
	def is_game_ongoing(self):
		is_started = self._word != ''
		is_ended = (self.is_victory or self.is_defeat)
		return is_started and not is_ended
	
	@property
	def word_as_guessed(self):
		ret_val = []
		for i, c in enumerate(self._word_lower_case):
			if c.lower() in self._guessed_letters_correct:
				ret_val.append(self._word[i])
			else:
				ret_val.append(None)
		return ret_val


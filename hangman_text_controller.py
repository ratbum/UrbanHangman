#!/usr/bin/python3

from hangman import Hangman
from hangman_text_view import HangmanTextView

	
class HangmanTextController:
	
	def __init__(self, hangman, view):
		self._hangman = hangman
		self._view = view
	
	def run_game_loop(self):
		self._hangman.generate_random_word()
		l = ''
		while(h.is_game_ongoing()):
			print('---\n' + hv.game_state + '\n---')
			l = input('Guess a letter:')
			try:
				h.letter_guess(l)
			except Exception as e:
				print(e.args[0])
		
	
		print(hv.game_state)
	
		if h.is_victory():
			print(hv.victory())
		if h.is_defeat():
			print(hv.defeat())
	
		print(h.word)
		print(h.word_definition)
	


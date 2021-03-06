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
		self._view.set_message('Click \'Start\' to run the game.')
		
	def key_press(self, event):
		if(self._hangman.is_game_ongoing):
			try:
				self._hangman.letter_guess(event.char)
				if not self._hangman.is_game_ongoing:
					self.end_game()
			except Exception as e:
				self._view.set_message(e.args[0])
			self._view.draw_all()
		else:
			if self._hangman.is_game_ended:
				self.end_game()

	def end_game(self):
		self._view.show_definition()
		
		performance_comment = 'Well done.' if self._hangman.is_victory else 'Sorry.'
		
		self._view.set_message(performance_comment + '\nClick \'Start\' for a new word.')
		
	def run_game(self, event):
		self._hangman.reset()
		self._hangman.generate_random_word()
		self._view.draw_all()
		self._view.set_message('')
		self._view.clear_definition()



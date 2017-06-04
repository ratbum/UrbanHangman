from hangman import Hangman
from hangman_text_view import HangmanTextView

	
class HangmanTextController:
	
	def __init__(self, hangman, view):
		self._hangman = hangman
		self._view = view
	
	def run_game_loop(self):
		self._hangman.generate_random_word()
		l = ''
		while(self._hangman.is_game_ongoing):
			print('---\n' + self._view.game_state + '\n---')
			l = input('Guess a letter:')
			try:
				self._hangman.letter_guess(l)
			except Exception as e:
				print(e.args[0])
		
	
		print(self._view.game_state)
	
		if self._hangman.is_victory:
			print(self._view.victory())
		if self._hangman.is_defeat:
			print(self._view.defeat())
	
		print(self._hangman.word)
		print(self._hangman.word_definition)
	


#!/usr/bin/python3

from hangman import Hangman


class HangmanTextView:
	def __init__(self, hangman):
		self._hangman = hangman
		
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

HangmanTextView.TEXTUAL_HANGING_STATES = [
'''
       
       
       
       
       
''',
'''
       
       
       
       
===    
''',
'''
       
 |     
 |     
 |     
===    
''',
'''
 +     
 |     
 |     
 |     
===    
''',
'''
 +---+ 
 |     
 |     
 |     
===    
''',
'''
 +---+ 
 |   o 
 |     
 |     
===    
''',
'''
 +---+ 
 |   o 
 |   | 
 |     
===    
''',
'''
 +---+ 
 |   o 
 |  /| 
 |     
===    
''',
'''
 +---+ 
 |   o 
 |  /|\\
 |     
===    
''',
'''
 +---+ 
 |   o 
 |  /|\\
 |  /  
===    
''',
'''
 +---+ 
 |   o 
 |  /|\\
 |  / \\
===    
''']


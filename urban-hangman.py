import urbandictionary as ud


class Hangman:
	MAX_DEATH_POINTS = 10
	
	def __init__(self):
		self._word = ''
		self._word_lower_case = ''
		self._word_definitition = ''
		self._guessed_letters_correct = []
		self._guessed_letters_incorrect = []
		self.generate_random_word()

	def generate_random_word(self):
		udword = ud.random()[0]
		self._word = udword.word
		self._word_lower_case = self._word.lower()
		self._word_definition = udword.definition
		if ' ' in self._word:
			self._guessed_letters_correct.append(' ')
	
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
		
		if c in self._guessed_letters_correct or c in self._guessed_letters_incorrect:
			raise Exception('Already guessed', 'letter_guess doesn\'t accept repeats')
		
		c = c.lower()
		if c in self._word_lower_case:
			self._guessed_letters_correct.append(c)
			if self.is_victory():
				return self.victory()
			return True
		else:
			self._guessed_letters_incorrect.append(c)
			if self.is_defeat():
				return self.defeat()
			return False
	
	def is_victory(self):
		return None not in self.word_as_guessed
	
	
	def is_game_ongoing(self):
		return not (self.is_victory() or self.is_defeat())
	
	
	@property
	def word_as_guessed(self):
		ret_val = []
		for i, c in enumerate(self._word_lower_case):
			if c.lower() in self._guessed_letters_correct:
				ret_val.append(self._word[i])
			else:
				ret_val.append(None)
		return ret_val
	
	
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
		
	def is_defeat(self):
		return self.death_points == Hangman.MAX_DEATH_POINTS
	
class HangmanTextController:
	
	def __init__(self, hangman, view):
		self._hangman = hangman
		self._view = view
	
	def run_game_loop(self):
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


if __name__ == '__main__':

	h = Hangman()
	hv = HangmanTextView(h)
	hc = HangmanTextController(h, hv)
	
	hc.run_game_loop()
	
	


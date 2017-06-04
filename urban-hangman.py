#!/usr/bin/python3

import urbandictionary as ud
from tkinter import *
from svg2can import Svg2Can


class Hangman:
	MAX_DEATH_POINTS = 10
	
	def __init__(self):
		self.reset()

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
	
	def is_victory(self):
		return None not in self.word_as_guessed
	
	def is_defeat(self):
			return self.death_points == Hangman.MAX_DEATH_POINTS
	
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
		
	def defeat(self):
		return 'DEFEAT!'
	
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
		

class HangmanTkinterController:
	
	def __init__(self, hangman, view):
		print('hello')
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
	#hv = HangmanTextView(h)
	#hc = HangmanTextController(h, hv)
	print('h')
	window = Tk()
	
	hv = HangmanTkinterView(h, window)
	print('he')
	hc = HangmanTkinterController(h, hv)
	hv.controller = hc
	window.mainloop()
	
	
	#hc.run_game_loop()
	
	


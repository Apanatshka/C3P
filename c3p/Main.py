#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.2 code
#
# Copyright (c) 2012 Jeff Smits
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# C3P - C-compatible code preprocessor
# This commandline tool reads a file and expands macro's. 
#
# This file is a utility file and doesn't contain the whole tool. 
import re
if __name__ == "__main__" or __name__ == "Main":
	from Command import Command
	import namespaces
else:
	from .Command import Command
	from . import namespaces

class Main:
	"""Command parser and wrapper for the main loop and helper functions. """
	
	def __init__(self, file, dest, shebang = False, command_prefix = "#",
			var_prefix = "", quiet = False, verbose = False):
		#save the input arguments
		self.file = file
		self.dest = dest
		self.shebang = shebang
		self.command_prefix = command_prefix
		self.var_prefix = var_prefix
		self.quiet = quiet
		self.verbose = verbose and not quiet
		
		#set some more things
		self.options = {
			"empty_line": True,
		}
		self.conditions = []
		self.else_found = []
		
		#this function holds the loop through the input file
		self.main_loop()
	
	def command_split(self, line):
		"""Split line on before_text, command and after_text. When no command is
		 found, the command and after_text parts are empty strings. """
		todo        = line
		before_text = ""
		command     = ""
		after_text  = ""
		
		#split on the command_prefix
		split = todo.split(self.command_prefix, 1)
		#while you've found a command_prefix
		while len(split) != 1:
			[temp_text, todo] = split
			before_text += temp_text
			
			#see if a valid command is after the prefix
			try:
				(command, after_text) = self.get_command(todo)
				break
			except ValueError: pass
			
			#if no command found, add the prefix to the before text
			before_text += self.command_prefix
			#and retry finding the prefix in the rest of the string
			split = todo.split(self.command_prefix, 1)
		#if nothing was found, add the last stuff to the before_text again
		if len(split) == 1:
			before_text += split[0]
		
		return (before_text, command, after_text)
	
	def get_command(self, string):
		"""Extract command according to rules defined by command-line flags. """
		#TODO: add option to reject whitespace before command
		matches = re.match(r"\s*(\w+)\s([\s\S]*)", string)
		if matches == None:
			matches = re.match(r"\s*(\w+)$", string)
			if matches == None:
				raise ValueError("Not a valid command string")
			else:
				matches = (matches, "")
		else:
			matches = matches.group(1,2)
		return matches
	
	def last_condition(self):
		try:
			return self.conditions[-1]
		except IndexError:
			return True
	
	def main_loop(self):
		"""The loop through the lines of the input on which it does stuff. """
		
		input = self.file
		output = self.dest
		
		#different namespaces may be used in a later version of the tool to be
		# able to easily undefine a group of macro's
		namespace = namespaces.NormalNameSpace()
		
		#this linenumber is used in error messages
		self.inputLineNo = 0
		#this linenumber might later be available as a macro
		self.outputLineNo = 0
		
		if self.shebang:
			self.inputLineNo += 1
			line = input.readLine()
		
		for line in input:
			self.inputLineNo += 1
			#when a command is not found, command and after are empty strings
			(before, command, after) = self.command_split(line)
			
			#check if the text is just followed or actually processed
			lc = self.last_condition()
			if lc:
				#only output a line when there was more than whitespace before the
				# command prefix, or when the empty_line option is True. 
				if (before.strip() != "" 
						or (self.options["empty_line"] and command == "")):
					output.write(self.replace_object_macro(namespace, before))
					self.outputLineNo += 1
			
			#check if the command here is to be ignored
			if (command != "" and Command.command_allowed(command, lc)):
				try:
					Command.get_command_func(command)(namespace, after, 
						self.last_condition, self.conditions, self.else_found)
				except ValueError as e:
					self.error(e.args[0])
				except IndexError as e:
					self.error(e.args[0])
	
	def replace_object_macro(self, namespace, input):
		"""The replacement of defined object macro's to their values"""
		#split into potentially replaceable parts and non-replaceable parts
		words = re.split(r"(\W+)", input)
		output = ""
		for word in words:
			try:
				#try to find a variable named word
				replacement = namespace.get(word)
			except AssertionError:
				#no variable? then don't replace
				output += word
			else:
				#variable found? replace :D
				output += str(replacement)
		return output
	
	def error(self, msg):
		import os.path
		import sys
		if not self.quiet:
			print("c3p \"{}\":{}: error. {}".format(
					os.path.abspath(self.file.name), self.lineNo, msg
				), file=sys.stderr)
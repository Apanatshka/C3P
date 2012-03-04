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
# This commandline tools reads a file and expands macro's. 
#
# Known encoding issue: Please note that Python cannot handle a BOM in a UTF-8
# encoded file without special care, which I did not add. 
import re

class C3P:
	"""C3P class wrapper"""
	#Don't know on what to base this number yet. 
	#The plan for now is major = milestone, minor = revision. 
	version = "1.0"
	
	def __init__(self):
		"""Constructor. 
		Doesn't do much. Creates the argument parser and parses. Sets some things
		 which should be configurable by the user in a later version. 
		After that it just calls the next function to do the rest. """
		#get parser
		argparser = self.get_argparser()
		#parse arguments
		args = self.args = argparser.parse_args()
		
		self.options = {
			"empty_line": False,
		}
		
		self.var_prefix = ""
		
		self.conditions = []
		self.else_found = []
		
		#this function holds the loop through the input file
		self.main_loop()
	
	def get_argparser(self):
		"""Definition/creation of the argument parser for the command-line
		 arguments of the tool. """
		import argparse
		
		parser = self.parser = argparse.ArgumentParser(description="this"
			" commandline tools reads a file and expands macro's ", prog="c3p",
			usage="%(prog)s -d DEST [-s] [-c CP] [-q | -v] file", add_help=False)
		
		required_args = parser.add_argument_group(title="required arguments")
		
		required_args.add_argument("-d", "--destination", metavar="DEST", 
			required=True, type=argparse.FileType("w"), help="file to write to", 
			dest="dest")
		required_args.add_argument("file", type=argparse.FileType("r"), 
			help="file to read")
		
		optional_args = parser.add_argument_group(title="optional arguments")
		
		optional_args.add_argument("-s", "--shebang", action="store_true",
			help="remove the first line so you can use a shebang for this tool",
			dest="shebang")
		optional_args.add_argument("-c", "--command-prefix", default="#",
			metavar="CP", help="set the command prefix to CP",
			dest="command_prefix")
		qv = optional_args.add_mutually_exclusive_group()
		qv.add_argument("-q", "--quiet", action="store_true",
			help="keep from outputting errors", dest="quiet")
		qv.add_argument("-v", "--verbose", action="store_true",
			help="output lots of stuff", dest="verbose")
		
		other_args = parser.add_argument_group(title="additional arguments")
		
		other_args.add_argument("-h", "--help", action="help",
			help="show this help message and exit")
		other_args.add_argument("--version", action="version", 
			version="%(prog)s "+self.version)
		
		return parser
	
	def is_command(self, command):
		"""Check if the command is registered"""
		return command in self.func_map.keys()
	
	def get_command_func(self, command):
		"""Just a map from string to function"""
		if self.is_command(command):
			return self.func_map[command]
		else:
			raise ValueError("Command not found")
	
	def command_allowed(self, command):
		maplist = self.allow_maps
		if self.last_condition():
			return command in maplist[0] or command in maplist[1]
		else:
			return command in maplist[0]
	
	def command_split(self, line):
		"""Split line on before_text, command and after_text. When no command is
		 found, the command and after_text parts are empty strings. """
		todo        = line
		before_text = ""
		command     = ""
		after_text  = ""
		
		#split on the command_prefix
		split = todo.split(self.args.command_prefix, 1)
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
			before_text += self.args.command_prefix
			#and retry finding the prefix in the rest of the string
			split = todo.split(self.args.command_prefix, 1)
		#if nothing was found, add the last stuff to the before_text again
		if len(split) == 1:
			before_text += split[0]
		
		return (before_text, command, after_text)
	
	def get_command(self, string):
		"""Extract command according to rules defined by command-line flags. """
		#TODO: add option not to reject whitespace before command
		matches = re.match(r"\s*(\w+)\s([\s\S]*)", string)
		if matches == None:
			raise ValueError("Not a valid command string")
		else:
			return matches.group(1,2)
	
	def last_condition(self):
		try:
			return self.conditions[-1]
		except IndexError:
			return True
	
	def main_loop(self):
		"""The loop through the lines of the input on which it does stuff. """
		import namespaces
		
		input = self.args.file
		output = self.args.dest
		
		#different namespaces may be used in a later version of the tool to be
		# able to easily undefine a group of macro's
		namespace = namespaces.NormalNameSpace()
		
		#the linenumber is used in error messages
		self.lineNo = 0
		
		if self.args.shebang:
			self.lineNo += 1
			line = input.readLine()
		
		for line in input:
			self.lineNo += 1
			#when a command is not found, command and after are empty strings
			(before, command, after) = self.command_split(line)
			
			#only output a line when there was more than whitespace before the
			# command prefix, or when the empty_line option is True. 
			if self.last_condition():
				if (before.strip() != "" 
						or (self.options["empty_line"] and command == "")):
					output.write(self.replace_object_macro(namespace, before))
			if command != "" and self.command_allowed(command):
				self.get_command_func(command)(self, namespace, after)
	
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
				output += replacement
		return output
	
	def command_define(self, namespace, string):
		"""The define command"""
		#get an identifier for the definition
		matches = re.match(r"\s*(\w+)(.*)", string)
		if matches == None:
			self.error("Unable to find valid identifier for `define` command in "
				+repr(string.strip()))
			return
		
		(name, value) = matches.group(1,2)
		#stripping whitespace off the value may be unwanted...
		value = value.strip()
		
		#try to make a number of the value, otherwise keep the string
		try:
			value = int(value)
		except ValueError: 
			try:
				value = float(value)
			except ValueError: pass
		
		namespace.set_var(name, value)
	
	def command_undefine(self, namespace, string):
		"""The undef command"""
		#get the identifier
		matches = re.match(r"\s*(\w+)", string)
		if matches == None:
			self.error("Unable to find valid identifier for `undefine` command in "
				+repr(string.strip()))
			return
		
		name = matches.group(1)
		namespace.unset(name)
	
	def command_ifdef(self, namespace, string):
		self.conditions.append(namespace.exists(string.strip()) 
			and self.last_condition())
		self.else_found.append(False)
	
	def command_ifndef(self, namespace, string):
		self.conditions.append(not namespace.exists(string.strip()) 
			and self.last_condition())
		self.else_found.append(False)
	
	def command_else(self, namespace, string):
		try:
			if not self.else_found.pop():
				self.conditions.append(not self.conditions.pop()
					and self.last_condition())
			else:
				self.error("An `else` was already found earlier. ")
			self.else_found.append(True)
		except IndexError:
			self.error("No `if` found to match the `else`. ")
	
	def command_endif(self, namespace, string):
		try:
			self.conditions.pop()
			self.else_found.pop()
		except IndexError:
			self.error("No `if` found to match the `endif`. ")
	
	func_map = {
		"define": command_define,
#		"def":    command_define,
		"undef":  command_undefine,
		"ifdef":  command_ifdef,
		"ifndef": command_ifndef,
		"else":   command_else,
		"endif":  command_endif,
	}
	
	allow_maps = [
		{"ifdef", "ifndef", "else", "endif"}, #0 == always
		{"define", "undef"}, #1 == while inside an if with condition == True
	]
	
	def error(self, msg):
		import os.path
		import sys
		if not self.args.quiet:
			print("c3p \"{}\":{}: error. {}".format(
					os.path.abspath(self.args.file.name), 
					self.lineNo, msg),
				file=sys.stderr)

if __name__ == "__main__":
	C3P()
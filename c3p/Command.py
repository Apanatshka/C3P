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

if __name__ == "__main__":
	import commands
elif __name__ == "Command":
	import commands
else:
	from . import commands

class Command:
	"""Wrapper to call other commands. """
	func_map = {
		"define": commands._define,
#		"def":    commands._define,
		"undef":  commands._undefine,
		"ifdef":  commands._ifdef,
		"ifndef": commands._ifndef,
		"else":   commands._else,
		"endif":  commands._endif,
	}
	allow_maps = [
		{"ifdef", "ifndef", "else", "endif"}, #0: always
		{"define", "undef"}, #1: while inside an if with condition True
	]
	
	def is_command(com):
		"""Check if the command is registered"""
		return com in Command.func_map.keys()
	
	def get_command_func(com):
		"""Just a map from string to function"""
		if Command.is_command(com):
			return Command.func_map[com]
		else:
			raise ValueError("Command not found")
	
	def command_allowed(com, last_condition):
		maplist = Command.allow_maps
		if last_condition:
			return com in maplist[0] or com in maplist[1]
		else:
			return com in maplist[0]
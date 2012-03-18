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

def _define(namespace, string, last_condition, conditions, else_found):
	"""The define command"""
	#get an identifier for the definition
	matches = re.match(r"\s*(\w+)(.*)", string)
	if matches == None:
		raise ValueError("Unable to find valid identifier for `define` command in "
			+repr(string.strip()))
	
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

def _undefine(namespace, string, last_condition, conditions, else_found):
	"""The undef command"""
	#get the identifier
	matches = re.match(r"\s*(\w+)", string)
	if matches == None:
		raise ValueError("Unable to find valid identifier for `undefine` command in "
			+repr(string.strip()))
	
	name = matches.group(1)
	namespace.unset(name)

def _ifdef(namespace, string, last_condition, conditions, else_found):
	"""The ifdef construct"""
	conditions.append(namespace.exists(string.strip()) 
		and last_condition())
	else_found.append(False)

def _ifndef(namespace, string, last_condition, conditions, else_found):
	"""The ifndef construct"""
	conditions.append(not namespace.exists(string.strip()) 
		and last_condition())
	else_found.append(False)

def _else(namespace, string, last_condition, conditions, else_found):
	"""The else construct"""
	try:
		if not else_found.pop():
			conditions.append(not conditions.pop()
				and last_condition())
		else:
			raise ValueError("An `else` was already found earlier. ")
	except IndexError:
		raise IndexError("No `if` found to match the `else`. ")
	except ValueError:
		raise
	finally:
		else_found.append(True)

def _endif(namespace, string, last_condition, conditions, else_found):
	"""The endif construct"""
	try:
		conditions.pop()
		else_found.pop()
	except IndexError:
		raise IndexError("No `if` found to match the `endif`. ")
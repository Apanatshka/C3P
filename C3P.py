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
# encoded file. 
import re

class C3P:
	"""C3P class wrapper"""
	version = "0.1"
	
	def __init__(self):
		parser = self.get_parser()
		args = self.args = parser.parse_args()
		
		self.command_prefix = "#"
		self.var_prefix = ""
		
		self.do_stuff()
	
	def get_parser(self):
		import argparse
		parser = self.parser = argparse.ArgumentParser(description="this"
			" commandline tools reads a file and expands macro's ", prog="c3p",
			usage="%(prog)s -f FILE [optional arguments] dest", add_help=False)
		
		optional_args = parser.add_argument_group(title="optional arguments")
		
		#optional_args.add_argument("-s", "--shebang", type=Boolean, default=False)
		
		required_args = parser.add_argument_group(title="required arguments")
		
		required_args.add_argument("-f", "--file", type=argparse.FileType("r"),
			required=True, help="file to read", metavar="FILE", dest="file")
		
		required_args.add_argument("dest", type=argparse.FileType("w"), 
			help="file to write to")
		
		
		other_args = parser.add_argument_group(title="additional arguments")
		
		other_args.add_argument("-h", "--help", action="help",
			help="show this help message and exit")
		
		other_args.add_argument("--version", action="version", 
			version="%(prog)s "+self.version)
		
		return parser
	
	def get_command_func(self, command):
		func_map = {
			"define": self.define,
			"def": self.define,
			"undef": self.undefine,
		}
		if command in func_map.keys():
			return func_map[command]
	
	def do_stuff(self):
		import namespaces
		
		input = self.args.file
		output = self.args.dest
		
		namespace = namespaces.NormalNameSpace()
		
		for line in input:
			split = line.split(self.command_prefix, 1)
			if len(split) == 1:
				output.write(self.replace_stuff(namespace, line))
				continue
			[before, after] = split
			if re.match(r"\w+", after) == None:
				before = line
			if before.strip() != "":
				output.write(self.replace_stuff(namespace, before))
			if re.match(r"\w+", after) != None:
				matches = re.match(r"(^\w+)(.*)", after)
				if matches != None:
					func = self.get_command_func(matches.group(1))
					if func != None:
						func(namespace, matches.group(2))
	
	def replace_stuff(self, namespace, input):
		words = re.split(r"(\W+)", input)
		output = ""
		for word in words:
			try:
				replacement = namespace.get(word)
			except AssertionError:
				output += word
			else:
				output += replacement
		return output
	
	def define(self, namespace, string):
		matches = re.match(r"\s*(\w+)(.*)", string)
		if matches == None:
			pass#ERROR! + return
		(name, value) = matches.group(1,2)
		value = value.strip()
		try:
			value = int(value)
		except ValueError: pass
		namespace.set_var(name, value)
	
	def undefine(self, namespace, string):
		matches = re.match(r"\s*(\w+)(.*)", string)
		if matches == None:
			pass#ERROR! + return
		name = matches.group(1)
		namespace.unset(name)

if __name__ == "__main__":
	C3P()
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

class Argparser:
	def get_args():
		#get parser
		argparser = Argparser.get_argparser()
		#parse arguments
		return argparser.parse_args()
		#TODO: change the destination type from argparse.FileType("w") to a check
		# if exists and a prompt to overwrite. 
		#Also add a non-interactive mode where the tool fails in stead of prompts?
	
	def get_argparser():
		"""Definition/creation of the argument parser for the command-line
		 arguments of the tool. """
		import argparse
		
		parser = argparse.ArgumentParser(description="this"
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
		
		return parser
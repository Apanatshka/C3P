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
# Also it does not run standalone. 
#
# These are acceptance tests, recycled from some static I/O tests

import unittest
from io import StringIO
from os import linesep
from os.path import dirname
#import from cp3 package
from .. import *

class Acc_test(unittest.TestCase):
	def error(self, m, msg):
		self.errors.append(msg)
		
	def setUp(self):
		self.errors = []
		#mock the error method of the Main class
		self.m = Main
		self.m.error = lambda x,y: self.error(x,y)
		self.dir = dirname(__file__)+r"\\"
	
	def test_define1(self):
		test_name = "define1"
		r = StringIO()
		with open(self.dir+"acc_tests_io/"+test_name+"_input.txt") as file:
			self.m(**{'dest': r, 'file': file}).main_loop()
		result = r.getvalue()
		r.close()
		with open(self.dir+"acc_tests_io/"+test_name+"_output.txt") as o:
			output = o.read()
		self.assertEqual(result.replace(linesep, '\n'), output)
		self.assertEqual(0, len(self.errors))
	
	def test_undef1(self):
		test_name = "undef1"
		r = StringIO()
		with open(self.dir+"acc_tests_io/"+test_name+"_input.txt") as file:
			self.m(**{'dest': r, 'file': file}).main_loop()
		result = r.getvalue()
		r.close()
		with open(self.dir+"acc_tests_io/"+test_name+"_output.txt") as o:
			output = o.read()
		self.assertEqual(result.replace(linesep, '\n'), output)
		self.assertEqual(0, len(self.errors))
	
	def test_ifdef(self):
		test_name = "ifdef"
		r = StringIO()
		with open(self.dir+"acc_tests_io/"+test_name+"_input.txt") as file:
			self.m(**{'dest': r, 'file': file}).main_loop()
		result = r.getvalue()
		r.close()
		with open(self.dir+"acc_tests_io/"+test_name+"_output.txt") as o:
			output = o.read()
		self.assertEqual(result.replace(linesep, '\n'), output)
		self.assertEqual(0, len(self.errors))
	
	def test_else(self):
		test_name = "else"
		r = StringIO()
		with open(self.dir+"acc_tests_io/"+test_name+"_input.txt") as file:
			self.m(**{'dest': r, 'file': file}).main_loop()
		result = r.getvalue()
		r.close()
		with open(self.dir+"acc_tests_io/"+test_name+"_output.txt") as o:
			output = o.read()
		self.assertEqual(result.replace(linesep, '\n'), output)
		self.assertEqual(0, len(self.errors))
	
	def test_whitespace(self):
		test_name = "whitespace"
		r = StringIO()
		with open(self.dir+"acc_tests_io/"+test_name+"_input.txt") as file:
			self.m(**{'dest': r, 'file': file}).main_loop()
		result = r.getvalue()
		r.close()
		with open(self.dir+"acc_tests_io/"+test_name+"_output.txt") as o:
			output = o.read()
		self.assertEqual(result.replace(linesep, '\n'), output)
		self.assertEqual(0, len(self.errors))
	
	def test_invalid_define(self):
		test_name = "invalid_define"
		r = StringIO()
		with open(self.dir+"acc_tests_io/"+test_name+"_input.txt") as file:
			self.m(**{'dest': r, 'file': file}).main_loop()
		result = r.getvalue()
		r.close()
		with open(self.dir+"acc_tests_io/"+test_name+"_output.txt") as o:
			output = o.read()
		self.assertEqual(result.replace(linesep, '\n'), output)
		self.assertEqual(1, len(self.errors))
		self.assertIn("identifier", self.errors[0])
		self.assertIn("define", self.errors[0])
	
	def test_double_else(self):
		test_name = "double_else"
		r = StringIO()
		with open(self.dir+"acc_tests_io/"+test_name+"_input.txt") as file:
			self.m(**{'dest': r, 'file': file}).main_loop()
		result = r.getvalue()
		r.close()
		with open(self.dir+"acc_tests_io/"+test_name+"_output.txt") as o:
			output = o.read()
		self.assertEqual(result.replace(linesep, '\n'), output)
		self.assertEqual(1, len(self.errors))
		self.assertIn("else", self.errors[0])
		self.assertIn("already found", self.errors[0])
	
	def test_unmatched(self):
		test_name = "unmatched"
		r = StringIO()
		with open(self.dir+"acc_tests_io/"+test_name+"_input.txt") as file:
			self.m(**{'dest': r, 'file': file}).main_loop()
		result = r.getvalue()
		r.close()
		with open(self.dir+"acc_tests_io/"+test_name+"_output.txt") as o:
			output = o.read()
		self.assertEqual(result.replace(linesep, '\n'), output)
		self.assertEqual(2, len(self.errors))
		self.assertIn("if", self.errors[0])
		self.assertIn("found", self.errors[0])
		self.assertIn("match", self.errors[0])
		self.assertIn("else", self.errors[0])
		self.assertIn("if", self.errors[1])
		self.assertIn("found", self.errors[1])
		self.assertIn("match", self.errors[1])
		self.assertIn("endif", self.errors[1])

def load_tests(loader, tests, pattern):
	suite = unittest.TestSuite()
	tests = loader.loadTestsFromTestCase(Acc_test)
	suite.addTests(tests)
	return suite
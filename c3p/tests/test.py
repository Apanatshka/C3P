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

import unittest
from io import StringIO
from os import linesep
from os.path import dirname
#import from cp3 package
from .. import *

class test(unittest.TestCase):
	def error(self, m, msg):
		self.errors.append(msg)
		
	def setUp(self):
		self.errors = []
		#mock the error method of the Main class
		self.m = Main
		self.m.error = lambda x,y: self.error(x,y)
		self.dir = dirname(__file__)+r"\\"
	
	def test_define1(self):
		r = StringIO()
		with open(self.dir+"define1_input.txt") as file:
			self.m(**{'dest': r, 'file': file})
		result = r.getvalue()
		r.close()
		with open(self.dir+"define1_output.txt") as o:
			output = o.read()
		self.assertEqual(result.replace(linesep, '\n'), output)
		self.assertEqual(len(self.errors), 0)

def load_tests(loader, tests, pattern):
	suite = unittest.TestSuite()
	for test_class in (test,):
		tests = loader.loadTestsFromTestCase(test_class)
		suite.addTests(tests)
	return suite
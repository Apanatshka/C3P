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
from .. import Main
from .. import namespaces

class Main_unit_test(unittest.TestCase):
	def setUp(self):
		self.m = Main(dest=None, file=None)
	
	def test_get_command_wrong_input(self):
		f = self.m.get_command
		self.assertRaises(ValueError, f, "#hello")
		self.assertRaises(ValueError, f, "?shello")
		self.assertRaises(ValueError, f, "blargh? lala")
	
	def test_get_command_right_input(self):
		f = self.m.get_command
		self.assertEqual(("define", ""), f("define"))
		self.assertEqual(("com_mand", "hello"), f("com_mand hello"))
		self.assertEqual(("com_mand", " hello"), f("com_mand  hello"))
		self.assertEqual(("com_mand", "hello"), f("com_mand\thello"))
		self.assertEqual(("com_mand", " hello"), f("com_mand\t hello"))
	
	def test_command_split(self):
		f = self.m.command_split
		self.assertEqual(("#?hello", "", ""), f("#?hello"))
		self.assertEqual(("#?", "hello", ""), f("#?#hello"))
		self.assertEqual(("#?", "hello", ""), f("#?#hello "))
		self.assertEqual(("#?", "hello", " world"), f("#?#hello  world"))
		self.assertEqual(("#?", "hello", "world"), f("#?#hello\tworld"))
	
	def test_last_condition(self):
		f = self.m.last_condition
		#True on the stack
		self.m.conditions.append(True)
		self.assertTrue(f())
		#False on the stack
		self.m.conditions.append(False)
		self.assertFalse(f())
		#Empty stack
		self.m.conditions = []
		self.assertTrue(f())
	
	def test_replace_object_macro(self):
		f = self.m.replace_object_macro
		namespace = namespaces.NormalNameSpace()
		#Empty namespace
		self.assertEqual("Hello world!", f(namespace, "Hello world!"))
		
		#Word in the namespace
		namespace.set_var("Hello", "Hi")
		self.assertEqual("Hi world!", f(namespace, "Hello world!"))
		

def load_tests(loader, tests, pattern):
	suite = unittest.TestSuite()
	tests = loader.loadTestsFromTestCase(Main_unit_test)
	suite.addTests(tests)
	return suite
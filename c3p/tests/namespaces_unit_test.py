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
from ..namespaces import *

class Namespaces_unit_test(unittest.TestCase):
	def setUp(self):
		self.nn = NormalNameSpace()
		#self.cn = ChildNameSpace()
		#self.mn = MaskNameSpace()
	
	def test_set_var(self):
		f = self.nn.set_var
		m = self.nn.map
		self.assertEqual({}, m)
		f("hello", "world")
		self.assertEqual({"hello": (True, "world")}, m)
	
	def test_set_const(self):
		f = self.nn.set_const
		m = self.nn.map
		self.assertEqual({}, m)
		f("hello", "world")
		self.assertEqual({"hello": (False, "world")}, m)
	
	def test_exists(self):
		f = self.nn.exists
		f1 = self.nn.set_var
		f2 = self.nn.set_const
		m = self.nn.map
		f1("hello", "world")
		f2("hi", "world")
		self.assertTrue(f("hello"))
		self.assertTrue(f("hi"))
		self.assertFalse(f("hey"))
	
	def test_get(self):
		f = self.nn.get
		f1 = self.nn.set_var
		f2 = self.nn.set_const
		m = self.nn.map
		f1("hello", "world1")
		f2("hi", "world2")
		self.assertEqual("world1", f("hello"))
		self.assertEqual("world2", f("hi"))
	
	def test_unset(self):
		f = self.nn.exists
		f1 = self.nn.set_var
		f2 = self.nn.set_const
		f3 = self.nn.unset
		m = self.nn.map
		f1("hello", "world")
		f2("hi", "world")
		self.assertTrue(f("hello"))
		self.assertTrue(f("hi"))
		self.assertFalse(f("hey"))
		f3("hello")
		f3("hi")
		self.assertFalse(f("hello"))
		self.assertFalse(f("hi"))
		self.assertFalse(f("hey"))

def load_tests(loader, tests, pattern):
	suite = unittest.TestSuite()
	tests = loader.loadTestsFromTestCase(Main_unit_test)
	suite.addTests(tests)
	return suite
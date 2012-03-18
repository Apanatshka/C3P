#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.2 code
#
# Copyright (c) 2012 Jeff Smits
#
# This file is part of C3P. 
#
# C3P is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# C3P is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with C3P.  If not, see <http://www.gnu.org/licenses/>.
#
# Code description of different namespaces or scopes of variables

class NameSpace: #abstract class
	is_variable = 0
	value = 1
	
	def __init__(self, parent = None): #inheritable function for __init__
		assert id(parent) != id(self)
		self.map = {}
		self.parent = parent
	
	def set_var(self, identifier, value):
		map = self.map
		if identifier not in map.keys() or map[identifier][NameSpace.is_variable]:
			map[identifier] = (True, value)
	
	def set_const(self, identifier, value):
		map = self.map
		assert identifier not in map.keys()
		map[identifier] = (False, value)
	
	def exists(self, identifier):
		return identifier in self.map.keys()
	
	def get(self, identifier): #abstract function
		raise NotImplementedError
	
	def unset(self, identifier):
		map = self.map
		if identifier in map.keys():
			del map[identifier]
	
	def __repr__(self):
		parent = self.parent
		if parent != None:
			return "NameSpace("+repr(parent)+")"
		else:
			return "NameSpace()"
	
	def __str__(self):
		parent = self.parent
		map = self.map
		if parent != None:
			return "NameSpace(map="+str(map)+", parent="+repr(parent)+")"
		else:
			return "NameSpace(map="+str(map)+")"

#ignores the parent
class NormalNameSpace(NameSpace):
	def get(self, identifier):
		map = self.map
		assert identifier in map.keys()
		return map[identifier][NameSpace.value]
	
	def __repr__(self):
		return "Normal"+super().__repr__()
	
	def __str__(self):
		return "Normal"+super().__str__()

#copies parent so it's values will not change
class ChildNameSpace(NameSpace):
	def __init__(self, parent):
		assert parent != None
		self = super().__init__(parent)
		self.map = parent.map.copy()
	
	get = NormalNameSpace.get
	
	def __repr__(self):
		return "Child"+super().__repr__()
	
	def __str__(self):
		return "Child"+super().__str__()

#overlays it's namespace and may change/unset parent values
class MaskNameSpace(NameSpace):
	def __init__(self, parent):
		assert parent != None
		super().__init__(parent)
	
	def set_var(self, identifier, value):
		if identifier in map.keys():
			map = self.map
		elif parent.exists(identifier):
			parent.set_var(identifier, value)
		else:
			map = self.map
		if identifier not in map.keys() or map[identifier][NameSpace.is_variable]:
			map[identifier] = (True, value)
	
	def set_const(self, identifier, value):
		if identifier in map.keys():
			map = self.map
		elif parent.exists(identifier):
			parent.set_const(identifier, value)
		else:
			map = self.map
		assert identifier not in map.keys()
		map[identifier] = (False, value)
	
	def exists(self, identifier):
		ret = identifier in map.keys()
		if ret:
			return ret
		else:
			return parent.exists(identifier)
	
	def get(self, identifier):
		map = self.map
		if identifier in map.keys():
			return map[identifier]
		elif parent.exists(identifier):
			return parent.get(self, identifier)
		else:
			raise AssertionError
	
	def unset(self, identifier):
		map = self.map
		if identifier in map.keys():
			del map[identifier]
		else:
			self.parent.unset(identifier)
	
	def __repr__(self):
		return "Mask"+super().__repr__()
	
	def __str__(self):
		return "Mask"+super().__str__()
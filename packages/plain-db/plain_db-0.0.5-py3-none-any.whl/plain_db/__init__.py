#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'plain_db'
import os

def getFile(fn):
	result = {}
	if not os.path.exists(fn):
		return result
	with open(fn) as f:
		for line in f.readlines():
			line = line.strip()
			if not line:
				continue
			key = ' '.join(line.split()[:-1])
			value = int(line.split()[-1])
			result[key] = value
	return result

class DB(object):
	def __init__(self, name): # first version, int value only
		self.fn = 'db/' + name
		self.items = getFile(self.fn)

	def update(self, key, value):
		if key not in self.items:
			self.items[key] = value
			self.appendSave(key, value)
			return
		self.items[key] = value
		self.save()

	def inc(self, key, value):
		oldValue = self.items.get(key, 0)
		self.update(key, oldValue + value)

	def get(self, key, default=None):
		return self.items.get(key) or default

	def appendSave(self, key, value):
		if len(self.items) == 1:
			prefix = '\n'
		else:
			prefix = ''
		with open(self.fn, 'a') as f:
			f.write(prefix + str(key) + ' ' + str(value))

	def save(self):
		lines = [key + ' ' + str(self.items[key]) for key in self.items]
		lines.sort()
		towrite = '\n'.join(lines)
		if not towrite:
			return
		os.system('mkdir db > /dev/null 2>&1')
		with open(self.fn + 'tmp', 'w') as f:
			f.write(towrite)
		os.system('mv %stmp %s' % (self.fn, self.fn))

def load(fn):
	return DB(fn)

class NoValueDB(object):
	def __init__(self, name):
		self._db = DB(name)

	def add(self, key):
		if self._db.get(key) == 1:
			return False
		self._db.update(key, 1)
		return True

def loadKeyOnlyDB(fn):
	return NoValueDB(fn)

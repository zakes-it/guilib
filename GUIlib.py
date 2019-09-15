#! /usr/bin/python

import subprocess
import sys
import os
import json
import warnings
from threading import Timer

class GUIPrompt(object):
	def __init__(self, title, button='OK', timeout=None):
		self.path = os.path.abspath(os.path.dirname(__file__))
		self.title = title
		self.button = button
		self.timeout = timeout
		self._pid = None
	
	def script(self, fname):
		'''return full path to fname python script'''
		return os.path.join(self.path, fname)

	def kill(self):
		try:
			self._pid.kill()
		except:
			warnings.warn('No killable process found')
		self._pid = None
	
	def run(self, args, data=None):
		'''run args in a subprocess, sending data through stdin on an optional
		timer'''
		self._pid = subprocess.Popen(
			args, 
			stdin=subprocess.PIPE, 
			stdout=subprocess.PIPE, 
			stderr=subprocess.PIPE)
		# setup timer to close window if there has been no input
		timer = Timer(self.timeout, self._pid.kill)
		try:
			timer.start()
			stdout, stderr = self._pid.communicate(data)
			if stderr:
				print(stderr)
			return stdout
		finally:
			timer.cancel()
			# kill the child window process if the parent script has crashed or
			# been terminated (ie. CTRL-C)
			self.kill()

	def notify(self, prompt, button=None):
		button = button if button else self.button
		args = [ 
			sys.executable, self.script('notify.py'), 
			'--title', self.title, 
			'--prompt', prompt, 
			'--button', button ]
		result = self.run(args)
		return result

	def spinner(self, prompt):
		args = [
			sys.executable, self.script('spinner.py'), 
			'--title', self.title, 
			'--prompt', prompt ]
		if self.timeout:
			args.append('--timeout')
			args.append(str(self.timeout))
			_ = self.run(args)
		else:
			self._pid = subprocess.Popen(args)

	def two_button(self, prompt, button1, button2):
		args = [
			sys.executable, self.script('two_button.py'), 
			'--title', self.title, 
			'--prompt', prompt, 
			'--button1', button1, 
			'--button2', button2 ]
		result = self.run(args)
		return result

	def line(self, prompt, default='', button=None):
		button = button if button else self.button
		args = [ 
			sys.executable, self.script('singleline.py'), 
			'--title', self.title, 
			'--prompt', prompt, 
			'--default', default, 
			'--button', button ]
		result = self.run(args)
		return result

	def open(self, prompt, default='', button=None):
		button = button if button else self.button
		args = [
			sys.executable, self.script('picker.py'),
			'--title', self.title,
			'--prompt', prompt,
			'--default', default,
			'--button', button,
			'--open'
		]
		result = self.run(args)
		return result

	def save(self, prompt, default='', button=None):
		button = button if button else self.button
		args = [
			sys.executable, self.script('picker.py'),
			'--title', self.title,
			'--prompt', prompt,
			'--default', default,
			'--button', button,
			'--save'
		]
		result = self.run(args)
		return result

	def multiline(self, prompt, default='', button=None):
		button = button if button else self.button
		args = [ 
			sys.executable, self.script('multiline.py'), 
			'--title', self.title, 
			'--prompt', prompt, 
			'--default', default, 
			'--button', button ]
		result = self.run(args)
		return result
	
	def credentials(self, prompt, button=None):
		button = button if button else self.button
		args = [ 
			sys.executable, self.script('credentials.py'), 
			'--title', self.title, 
			'--prompt', prompt, 
			'--button', button ]
		result = self.run(args)
		return json.loads(result)
	
	def list_select(self, prompt, list, button=None):
		button = button if button else self.button
		args = [ 
			sys.executable, self.script('listselect.py'), 
			'--title', self.title, 
			'--prompt', prompt, 
			'--list', json.dumps(list),
			'--button', button]
		result = self.run(args)
		return result

	def table_select(self, prompt, table, button=None, multiple=False):
		button = button if button else self.button
		args = [ 
			sys.executable, self.script('tableselect.py'), 
			'--title', self.title, 
			'--prompt', prompt, 
			'--button', button]
		if multiple:
			args.append('--multiple')
		data = json.dumps(table)
		result = self.run(args, data)
		return json.loads(result)
#! /usr/bin/python

import subprocess
import sys
import os
import json
import warnings
from threading import Timer


class GUITimeout(Exception):
	pass


class GUIProccessError(Exception):
	pass


class GUIPrompt(object):
	def __init__(self, title, button='OK', timeout=None):
		self.path = os.path.abspath(os.path.dirname(__file__))
		self.title = title
		self.button = button
		self.timeout = timeout
		self._pid = None
		self._timer_ended = False
	
	def script(self, fname):
		'''return full path to fname python script'''
		return os.path.join(self.path, fname)

	def _end_timer(self):
		self._timer_ended = True
		self.kill()
	
	def _kill_on_timeout(self):
		self._timer_ended = False
		err = 'Prompt timeout expired after {} seconds'.format(self.timeout)
		raise GUITimeout(err)

	def kill(self):
		try:
			self._pid.kill()
		except:
			warnings.warn('No killable process found')
		self._pid = None
		self._timedout = False

	def run(self, args, data=None):
		'''run args in a subprocess, sending data through stdin on an optional
		timer'''
		self._pid = subprocess.Popen(
			args, 
			stdin=subprocess.PIPE, 
			stdout=subprocess.PIPE, 
			stderr=subprocess.PIPE)
		timer = Timer(self.timeout, self._end_timer)
		timer.start()
		try:
			stdout, stderr = self._pid.communicate(data)
			if stderr:
				print(stderr)
			if self._pid and self._pid.returncode != 0:
				err = 'Prompt terminated unexpectedly with exit code {}'.format(
					self._pid.returncode)
				raise GUIProccessError(err)
			return stdout
		finally:
			timer.cancel()
			if self._timer_ended:
				self._kill_on_timeout()
			else:
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
			try:
				_ = self.run(args)
			except GUITimeout:
				pass
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
		if sys.version_info > (3, 0):
			data = data.encode()
		result = self.run(args, data)
		return json.loads(result)
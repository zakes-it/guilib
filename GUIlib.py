#! /usr/bin/python

import subprocess
import sys
import os
import json

PATH =  os.path.abspath(os.path.dirname(__file__))

def notify(title, prompt, button):
	script = os.path.join(PATH, 'notify.py')
	args = [ 
		sys.executable, script, 
		'--title', title, 
		'--prompt', prompt, 
		'--button', button ]
	pid = subprocess.Popen(
		args, 
		stdin=subprocess.PIPE, 
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE)
	stdout, stderr = pid.communicate()
	return

def two_button(title, prompt, button1, button2):
	script = os.path.join(PATH, 'two_button.py')
	args = [
		sys.executable, script, 
		'--title', title, 
		'--prompt', prompt, 
		'--button1', button1, 
		'--button2', button2 ]
	pid = subprocess.Popen(
		args, 
		stdin=subprocess.PIPE, 
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE)
	stdout, stderr = pid.communicate()
	return stdout

def get_singleline(title, prompt, default, button):
	script = os.path.join(PATH, 'singleline.py')
	args = [ 
		sys.executable, script, 
		'--title', title, 
		'--prompt', prompt, 
		'--default', default, 
		'--button', button ]
	pid = subprocess.Popen(
		args, 
		stdin=subprocess.PIPE, 
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE)
	stdout, stderr = pid.communicate()
	return stdout

def get_multiline(title, prompt, default, button):
	script = os.path.join(PATH, 'multiline.py')
	args = [ 
		sys.executable, script, 
		'--title', title, 
		'--prompt', prompt, 
		'--default', default, 
		'--button', button ]
	pid = subprocess.Popen(
		args, 
		stdin=subprocess.PIPE, 
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE)
	stdout, stderr = pid.communicate()
	return stdout
	
def get_credentials(title, prompt, button):
	script = os.path.join(PATH, 'credentials.py')
	args = [ 
		sys.executable, script, 
		'--title', title, 
		'--prompt', prompt, 
		'--button', button ]
	pid = subprocess.Popen(
		args, 
		stdin=subprocess.PIPE, 
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE)
	stdout, stderr = pid.communicate()
	return json.loads(stdout)
	
def get_listselection(title, prompt, list, button):
	script = os.path.join(PATH, 'listselect.py')
	args = [ 
		sys.executable, script, 
		'--title', title, 
		'--prompt', prompt, 
		'--list', json.dumps(list),
		'--button', button]
	pid = subprocess.Popen(
		args, 
		stdin=subprocess.PIPE, 
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE)
	stdout, stderr = pid.communicate()
	return stdout
	
def get_tableselection(title, prompt, table, button, multiple=False):
	script = os.path.join(PATH, 'tableselect.py')
	args = [ 
		sys.executable, script, 
		'--title', title, 
		'--prompt', prompt, 
		'--button', button]
	if multiple:
		args.append('--multiple')
	pid = subprocess.Popen(
		args, 
		stdin=subprocess.PIPE, 
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE)
	stdout, stderr = pid.communicate(json.dumps(table))
	print stderr
	return json.loads(stdout)
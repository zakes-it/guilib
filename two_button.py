#! /usr/bin/python

from nibbler import *
import argparse
import os
import sys


def submit_button1():
	text = n.views['button1'].title()
	try:
		sys.stdout.write(text)
		sys.stdout.flush()
	except:
		pass
	n.quit()


def submit_button2():
	text = n.views['button2'].title()
	try:
		sys.stdout.write(text)
		sys.stdout.flush()
	except:
		pass
	n.quit()


def get_args():
	parser = argparse.ArgumentParser(description=('Displays a prompt window '
		'with two buttons and writes the text tile of the clicked button to '
		'stdout'))
	parser.add_argument('--title', help='Window title')
	parser.add_argument('--prompt', help='Window informative text')
	parser.add_argument('--button1', help='Title of first button')
	parser.add_argument('--button2', help='Title of second button')
	args = parser.parse_args()
	return args


def init_window():
	n.win.becomeMainWindow()
	n.win.center()
	n.win.setCanBecomeVisibleWithoutLogin_(True)
	n.win.orderFrontRegardless()


def set_window(args):
	n.attach(submit_button1, 'button1')
	n.attach(submit_button2, 'button2')
	if args.title:
		n.win.setTitle_(args.title)
	if args.prompt:
		n.views['label'].setString_(args.prompt)
	if args.button1:
		n.views['button1'].setTitle_(args.button1)
	if args.button2:
		n.views['button2'].setTitle_(args.button2)


def main():
	args = get_args()
	init_window()
	set_window(args)
	n.run()


if __name__ == '__main__':
	PATH =  os.path.abspath(os.path.dirname(__file__))
	try:
		# Because of how this loads, this should be an absolute path if you don't
		# want to run this from the same directory as the script
		nib = os.path.join(PATH, 'nibs', 'TwoButton.nib')
		n = Nibbler(nib)
	except IOError:
		print("Unable to load nib!")
		exit(20)
	main()

from nibbler import *
import argparse
import os
import sys


def get_args():
	parser = argparse.ArgumentParser(description=('Displays a window with a '
		'multiline text box and writes the box contents as a string to stdout '
		'on submission'))
	parser.add_argument('--title', help='Window title')
	parser.add_argument('--prompt', help='Window informative text')
	parser.add_argument('--default', help='Default text for the text box')
	parser.add_argument('--button', help='Submission button title')
	args = parser.parse_args()
	return args


def submit_button():
	text = n.views['entry'].string()
	try:
		sys.stdout.write(text)
		sys.stdout.flush()
	except:
		pass
	n.quit()


def init_window():
	n.win.becomeMainWindow()
	n.win.center()
	n.win.setCanBecomeVisibleWithoutLogin_(True)
	n.win.orderFrontRegardless()


def set_window(args):
	n.attach(submit_button, 'button')
	if args.title:
		n.win.setTitle_(args.title)
	if args.prompt:
		n.views['label'].setString_(args.prompt)
	if args.default:
		n.views['entry'].setString_(args.default)
	if args.button:
		n.views['button'].setTitle_(args.button)


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
		nib = os.path.join(PATH, 'nibs', 'MultiLine.nib')
		n = Nibbler(nib)
	except IOError:
		print("Unable to load nib!")
		exit(20)
	main()

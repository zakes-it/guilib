from nibbler import *
import argparse
import os
import sys

PATH =  os.path.abspath(os.path.dirname(__file__))

def submit_button():
	text = n.views['entry'].stringValue()
	sys.stdout.write(text)
	sys.stdout.flush()
	n.quit()

def init_window():
	n.win.becomeMainWindow()
	n.win.center()
	n.win.setCanBecomeVisibleWithoutLogin_(True)
	n.win.orderFrontRegardless()

def set_window(args):
	n.attach(submit_button, 'button')
	n.attach(submit_button, 'entry')
	n.views['entry'].cell().setSendsActionOnEndEditing_(False)
	if args.title:
		n.win.setTitle_(args.title)
	if args.prompt:
		n.views['label'].setString_(args.prompt)
	if args.default:
		n.views['entry'].setStringValue_(args.default)
	if args.button:
		n.views['button'].setTitle_(args.button)

def main():
	parser = argparse.ArgumentParser(('Displays a window with a single line '
		'text box and writes the box contents as a string to stdout on '
		'submission'))
	parser.add_argument('--title', help='Window title')
	parser.add_argument('--prompt', help='Window informative text')
	parser.add_argument('--default', help='Default text for the text box')
	parser.add_argument('--button', help='Submission button title')
	args = parser.parse_args()
	init_window()
	set_window(args)
	n.run()

if __name__ == '__main__':
	try:
		# Because of how this loads, this should be an absolute path if you don't
		# want to run this from the same directory as the script
		nib = os.path.join(PATH, 'nibs', 'SingleLine.nib')
		n = Nibbler(nib)
	except IOError:
		print("Unable to load nib!")
		exit(20)
	main()

from nibbler import *
import argparse
import os
import sys
from AppKit import NSTimer

PATH =  os.path.abspath(os.path.dirname(__file__))

class genericWindowController(NSObject):
	"""This class represents the window controller."""

	def windowDidBecomeMain_(self, sender):
		"""Respond to the window focus event."""
		if hasattr(self, 'e'):
			self.e()

	def automaticTimerResponder_(self, timer):
		"""Respond to the automatic timer."""
		n.quit()

def init_window():
	n.win.becomeMainWindow()
	n.win.center()
	n.win.setCanBecomeVisibleWithoutLogin_(True)
	n.win.orderFrontRegardless()

def set_window(args):
	if args.title:
		n.win.setTitle_(args.title)
	if args.prompt:
		n.views['label'].setString_(args.prompt)
	ctrlr = genericWindowController.alloc().init()
	n.win.setDelegate_(ctrlr)
	if args.timeout:
			NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
				int(args.timeout),  # seconds before timer fires
				ctrlr,  # controller to be used
				'automaticTimerResponder:',  # function to be called on controller
				None,  # always None
				False  # repeat the timer
			)
	n.views['spinner'].setUsesThreadedAnimation_(True)
	n.views['spinner'].startAnimation_(None)

def main():
	parser = argparse.ArgumentParser(description=('Displays an informative '
		'window with circular progress indicator which closes after the '
		'specified time or is manually killed'))
	parser.add_argument('--title', help='Window title')
	parser.add_argument('--prompt', help='Window informative text')
	parser.add_argument('--timeout', help='Time in seconds to show window')
	args = parser.parse_args()
	init_window()
	set_window(args)
	n.run()

if __name__ == '__main__':
	try:
		# Because of how this loads, this should be an absolute path if you don't
		# want to run this from the same directory as the script
		nib = os.path.join(PATH, 'nibs', 'Spinner.nib')
		n = Nibbler(nib)
	except IOError:
		print("Unable to load nib!")
		exit(20)
	main()

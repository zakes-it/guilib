from nibbler import *
import argparse
import os
import sys
from AppKit import NSFilenamesPboardType, NSDragOperationNone, NSDragOperationCopy, \
	NSOpenPanel, NSSavePanel, NSURL


class genericWindowController(NSObject):
	def draggingEntered_(self,sender):
		pboard = sender.draggingPasteboard()
		types = pboard.types()
		opType = NSDragOperationNone
		if NSFilenamesPboardType in types:
			opType = NSDragOperationCopy
		return opType
		
	def performDragOperation_(self,sender):
		pboard = sender.draggingPasteboard()
		successful = False
		if NSFilenamesPboardType in pboard.types():
			txt = pboard.propertyListForType_(NSFilenamesPboardType)[0]
			set_entry_fld(txt)
			successful = True
		return successful


def get_args():
	parser = argparse.ArgumentParser(('Displays a window with a single line '
		'text box and writes the box contents as a string to stdout on '
		'submission'))
	parser.add_argument('--title', help='Window title')
	parser.add_argument('--prompt', help='Window informative text')
	parser.add_argument('--default', help='Default text for the text box')
	parser.add_argument('--button', help='Submission button title')
	grp = parser.add_mutually_exclusive_group(required=True)
	grp.add_argument('--open', '-o', action='store_true', help='Show a open dialog')
	grp.add_argument('--save', '-s', action='store_true', help='show a save dialog')
	args = parser.parse_args()
	return args


def set_entry_fld(entry):
	n.views['entry'].setStringValue_(str(entry))


def pnl_complete(result):
	furl = pnl.URLs()[0]
	n.views['entry'].setStringValue_(furl.path())


def browse_button():
	global pnl
	if args.save:
		pnl = NSSavePanel.alloc().init()
	elif args.open:
		pnl = NSOpenPanel.alloc().init()
	pnl.setCanChooseDirectories_(True)
	pnl.setCanChooseFiles_(True)
	fpath = n.views['entry'].stringValue()
	if fpath:
		if os.path.isfile(fpath):
			fpath = os.path.dirname(fpath)
		url = NSURL.fileURLWithPath_(fpath)
		pnl.setDirectoryURL_(url)
	pnl.beginSheetModalForWindow_completionHandler_(n.win, pnl_complete)


def submit_button():
	text = n.views['entry'].stringValue()
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


def set_window():
	ctrlr = genericWindowController.alloc().init()
	n.win.setDelegate_(ctrlr)
	n.win.registerForDraggedTypes_([NSFilenamesPboardType])
	n.attach(submit_button, 'button')
	n.attach(submit_button, 'entry')
	n.attach(browse_button, 'browse')
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
	global args
	args = get_args()
	init_window()
	set_window()
	n.run()


if __name__ == '__main__':
	PATH =  os.path.abspath(os.path.dirname(__file__))
	args = None
	pnl = None
	try:
		# Because of how this loads, this should be an absolute path if you don't
		# want to run this from the same directory as the script
		nib = os.path.join(PATH, 'nibs', 'Picker.nib')
		n = Nibbler(nib)
	except IOError:
		print("Unable to load nib!")
		exit(20)
	main()

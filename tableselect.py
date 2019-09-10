#! /usr/bin/python

from nibbler import *
import argparse
import os
import sys
import json
from AppKit import NSArrayController, NSTableColumn, NSValueBinding, \
	NSContentBinding, NSSelectionIndexesBinding, NSSortDescriptorsBinding, \
	NSLineBreakByTruncatingTail, NSPredicateFormatBindingOption, \
	NSConditionallySetsEditableBindingOption
from Foundation import NSDictionary, NSTextField, NSTableCellView, NSNotFound
	

PATH =  os.path.abspath(os.path.dirname(__file__))

class MyTableDelegate(NSObject):
	def tableView_viewForTableColumn_row_(self, view, col, row):
		col_id = col.identifier()
		result = view.makeViewWithIdentifier_owner_(col_id, self)
		if result:
			return result
		else:
			result = NSTableCellView.alloc().init()
			txt = NSTextField.alloc().init()
			result.setIdentifier_(col_id)
			result.addSubview_(txt)
			txt.bind_toObject_withKeyPath_options_('value', result, 
				'objectValue.{}'.format(col_id), 
				{NSConditionallySetsEditableBindingOption: False})
			result.widthAnchor().constraintEqualToAnchor_(
				txt.widthAnchor()).setActive_(True)
			result.heightAnchor().constraintEqualToAnchor_(
				txt.heightAnchor()).setActive_(True)
			txt.setTranslatesAutoresizingMaskIntoConstraints_(False)
			txt.setEditable_(False)
			txt.setBordered_(False)
			txt.setDrawsBackground_(False)
			txt.setLineBreakMode_(NSLineBreakByTruncatingTail)
		return result
		
	def tableView_heightOfRow_(self, view, row):
		row_contents = myController.arrangedObjects()[row].values()
		linecnt = list()
		for x in row_contents:
			if type(x) in (str, unicode):
				linecnt.append(len(x.splitlines()))
			else:
				linecnt.append(1)
		max_lines = max(linecnt)
		line_height = 16
		return line_height * max_lines

def submit_button():
	# get selection(s)
	selection = n.views['table'].selectedRowIndexes()
	selected = []
	i = selection.firstIndex()
	while i != NSNotFound:
		selected.append(dict(myController.arrangedObjects()[i]))
		i = selection.indexGreaterThanIndex_(i)
	sys.stdout.write(json.dumps(selected))
	sys.stdout.flush()
	n.quit()

def init_window():
	n.win.becomeMainWindow()
	n.win.center()
	n.win.setCanBecomeVisibleWithoutLogin_(True)
	n.win.orderFrontRegardless()

def format_predicate(data):
	s = '(self."{}" contains[cd] $value)'
	formated = ' || '.join([s.format(key) for key in data[0].keys()])
	return formated

def main():
	global myController
	parser = argparse.ArgumentParser(description=('Displays window contining '
		'the input table with headers and a search filter box similar to '
		'Powershell Out-GridView. Writes the selected item(s) to stdout as a '
		'JSON formatted array of dictionaries on submission'))
	parser.add_argument('--title', help='Window title')
	parser.add_argument('--prompt', help='Window informative text')
	parser.add_argument('--table', help='JSON formatted array of dictionaries')
	parser.add_argument('--button', help='Submission button title')
	parser.add_argument('--multiple', action='store_true', 
		help='Allow selection of multiple items')
	args = parser.parse_args()
	if not args.table:
		args.table = sys.stdin.read()
	init_window()
	n.attach(submit_button, 'button')
	if args.title:
		n.win.setTitle_(args.title)
	if args.prompt:
		n.views['label'].setString_(args.prompt)
	if args.multiple:
		n.views['table'].setAllowsMultipleSelection_(True)
	if args.button:
		n.views['button'].setTitle_(args.button)
	data = json.loads(args.table)
	predicate_format = format_predicate(data)
	data = [ NSDictionary.dictionaryWithDictionary_(x) for x in data ]
	myController = NSArrayController.alloc().initWithContent_(data)
	# bind table to array controller
	n.views['table'].bind_toObject_withKeyPath_options_(
			NSContentBinding, myController, 'arrangedObjects', None)
	n.views['table'].bind_toObject_withKeyPath_options_(
			NSSelectionIndexesBinding, myController, 'selectionIndexes', None)
	n.views['table'].bind_toObject_withKeyPath_options_(
			NSSortDescriptorsBinding, myController, 'sortDescriptors', None)
	# bind search to array controller
	n.views['search'].bind_toObject_withKeyPath_options_(
		'predicate', myController, 'filterPredicate', 
		{NSPredicateFormatBindingOption: predicate_format})
	delegate = MyTableDelegate.alloc().init()
	n.views['table'].setDelegate_(delegate)
	# remove default column that comes with .nib
	col1 = n.views['table'].tableColumnWithIdentifier_('col1')
	n.views['table'].removeTableColumn_(col1)
	# add columns to the table for every key in data sourceta
	for key in data[0].keys():
		col = NSTableColumn.alloc().initWithIdentifier_(key)
		col.setTitle_(key)
		# col.bind_toObject_withKeyPath_options_(
		# 	NSValueBinding, myController, 'arrangedObjects', None)
		n.views['table'].addTableColumn_(col)
	n.views['table'].reloadData()
	n.views['table'].sizeToFit()
	n.hidden = True
	n.run()

if __name__ == '__main__':
	try:
		# Because of how this loads, this should be an absolute path if you don't
		# want to run this from the same directory as the script
		nib = os.path.join(PATH, 'nibs', 'TableSelect.nib')
		n = Nibbler(nib)
	except IOError:
		print "Unable to load nib!"
		exit(20)
	main()

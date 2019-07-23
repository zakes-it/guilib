# guilib
A Python library of basic GUI prompts for macOS computers. Allows user interraction with utility scripts through simple dialog prompts.

## Getting Started
1. Download this repo:
```
git clone https://github.com/zakes-it/guilib.git
cd guilib
```
2. Read the help prompt for a dialog script:
```
/usr/bin/python notify.py -h
```
3. Run a dialog:
```
/usr/bin/python notify.py --title 'Test Dialog' --prompt 'Hello World!' --button 'OK'
```

## Python 3
You'll need pyobjc to use GUIlib with python 3. You can set up a virtual environment to test things out with pipenv:
```
cd guilib
pipenv install pyobjc --python 3
pipenv run python notify.py
```

## Using the module
In addition to running guilib scripts from the command line, it can be imported for use in your python projects.
1. Copy the module to your project directory.
2. Import the module in your script:
```
#! /usr/bin/python

from guilib import GUIlib
```
3. Call a dialog as a module method:
```
GUIlib.notify(
    title='Test Dialog',
    prompt='Hello World!',
    button='OK')
```
### Examples
Display an error message:
```
err = "Can't open pod bay doors"
GUIlib.notify(
    title='Test Dialog',
    prompt='There was an error: {}'.format(err)
    button='OK')
```
Get the result of two simple choices:
```
selection = GUIlib.two_button(
    title='Test Dialog',
    prompt='Do you want to play a game?',
    button1='No',
    button2='Yes')
if selection == 'Yes':
    ...
```
Get a single line of text:
```
username = GUIlib.get_singleline(
    title='Test Dialog',
    prompt='What is your name?',
    default='Smith',
    button='OK')
```
Get text spanning multiple lines:
```
exampleaddr = '''Cecilia Chapman
711-2880 Nulla St.
Mankato Mississippi 96522
(257) 563-7401'''
address = GUIlib.get_multiline(
    title='Test Dialog',
    prompt='Please confirm your address:',
    default=exampleaddr,
    button='OK')
```
Get a set of credentials:
```
creds = GUIlib.get_credentials(
    title='Test Dialog',
    prompt='Please enter your credentials for test server',
    button='OK')
r = requests.get('https://testserver.local', auth=(creds['username'],creds['password']))
```
Get one selection from multiple choices:
```
choices = ('macOS', 'Windows', 'Linux', 'Other')
best_os = GUIlib.get_listselection(
    title='Test Dialog',
    prompt='Which operating system is best?',
    list=choices,
    button='OK')
print('{} is the best operating system'.format(best_os))
```
Select one or more values from a table of data:
```
data = [
    {'numbers': 1, 'fruit': 'apple', 'pets': 'kitten'},
    {'numbers': 2, 'fruit': 'pear', 'pets': 'puppy'},
    {'numbers': 3, 'fruit': 'pineapple', 'pets': 'turtle'}]
selection = GUIlib.get_tableselection(
    title='Test Dialog',
    prompt='Choose one or more from the list:',
    table=data,
    button='OK')
```
## Tips
### Convert a CSV for tableselect
Use the following example to convert a CSV file with headers for use with tableselect:
```
import csv
with open('CSVSample.csv') as csvfile:
    data = [{k: v for k, v in row.items()} for row in csv.DictReader(csvfile, skipinitialspace=True)]

selection = GUIlib.get_tableselection('Hello World', 'Select item', data, 'ok', multiple=True)
```

## Requirements
The macOS builtin system Python `/usr/bin/python` should be used as nibbler relies on its integration with the PyObjC bridge.

Xcode is required if you would like to modify the existing guilib nib files or create new dialogs of your own.

## Known Issues
* Running scripts from some paths like mounted network shares may result in an "Unable to load nib!" error
* tableselect search filter only works on string values and does not filter integers

## Acknowledgements
guilib would not be possible without Michael Lynn and their fantastic work on nibbler https://github.com/pudquick/nibbler
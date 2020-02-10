# guilib
A Python library of basic GUI prompts for macOS computers. Allows user interraction with utility scripts through simple 
dialog prompts.

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
When run from the command line
 - singleline.py, multiline.py, picker.py, two_button.py and listselect.py will output basic text strings
- credentials.py and tableselect.py output JSON formatted strings
- notify.py and spinner.py do not return any output

## Python 3
You'll need pyobjc to use GUIlib with Python 3. You can set up a virtual environment to test things out with pipenv:
```
cd guilib
pipenv install pyobjc --python 3
pipenv run python notify.py
```

## Using the module
In addition to running guilib scripts from the command line, GUIlib can be imported for use in your python projects.
When using the GUIlib module, the 'credentials' and 'table_select' methods automatically convert responses from JSON to
native python data types.
1. Copy the module to your project directory.
2. Import the module in your script
```
import guilib
```
3. Create an instance of the GUIPrompt class:
```
prompter = guilib.GUIPrompt(title="Example Prompt", button="OK", timeout=None)
```
- title: Sets the window title for all dialogs. Required
- button: Sets the submission button text for all dialogs with a single button (notify, line, multiline, credentials, 
two_button, list_select, table_select, open, save). Defaults to 'OK'
- timeout: Sets the timeout value in seconds for dialog windows. Defaults to None

3. Call a dialog as a module method:
```
prompter.notify(
    prompt='Hello World!')
```
## Examples
### Notifications
#### notify()
Notification dialog that blocks script progress until the console user acknowledges the message by clicking the dialog 
button.

Display an error message:
```
err = "Can't open pod bay doors"
prompter.notify(
    prompt='There was an error: {}'.format(err))
```
#### spinner()
Notification dialog with a circular progress spinner that can be closed after a timeout or closed manually.

Display a blocking circular progress indicator for n seconds:
```
prompter.timeout = 10
prompter.spinner(
    prompt="Waiting 10 seconds...")
```
Display a non-blocking circular progress indicator:
```
import socket
import time

def is_connected(host, port):
    try:
        socket.create_connection((host, port))
        return True
    except OSError:
        pass
    return False

prompter.timeout = None
prompter.spinner(
    prompt="Waiting for connection to {}...".format(host))
while not is_connected('www.google.com', 80):
    time.sleep(3)
prompter.kill()
```
### Text entry
Get single or multiple lines of text. Use the 'default' flag to pre-populate the text entry box.
#### line()
A single line of text entry that sends the text box contents by clicking the dialog button or pressing the 'Return' key.
Get a single line of text:
```
username = prompter.line(
    prompt='What is your name?',
    default='Smith')
```
#### multiline()
Multi-line text editor dialog that sends once the dialog button is clicked.


Get text spanning multiple lines:
```
exampleaddr = '''Cecilia Chapman
711-2880 Nulla St.
Mankato Mississippi 96522
(257) 563-7401'''
address = prompter.multiline(
    prompt='Please confirm your address:',
    default=exampleaddr)
```
### Credentials
### credentials()
Username and password dialog that returns results as a dictionary with 'username' and 'password' keys. The password 
field is displayed as a secure text field and entries can be sent by clicking the dialog button or the 'Return' key.

Get a set of credentials:
```
creds = prompter.credentials(
    prompt='Please enter your credentials for test server')
r = requests.get('https://testserver.local', auth=(creds['username'],creds['password']))
```
### Choice selection
#### two_button()
Displays a dialog with two buttons and returns the text name of the button that was clicked.

```
selection = prompter.two_button(
    prompt='Do you want to play a game?',
    button1='No',
    button2='Yes')
if selection == 'Yes':
    ...
```
#### list_select()
Displays a dropdown list and returns the text name of the selected item from the list. Only one item can be selected if
you wish to allow the selection of multiple items, use the 'table_select()' method with only a single column of data.
```
choices = ('macOS', 'Windows', 'Linux', 'Other')
best_os = prompter.list_select(
    prompt='Which operating system is best?',
    list=choices)
print('{} is the best operating system'.format(best_os))
```
#### table_select()
Displays a table of data with a search filter. The table must be formatted as an array of dictionaries with a key for 
every column header and a dictionary for every row in the table. The result will be returned as an array of 
dictionaries. The 'multiple' argument can be used to allow multiple rows to be selected. If multiple selections are not
allowed, the return value will still be an array with only a single dictionary.

```
data = [
    {'number': 1, 'fruit': 'apple', 'pet': 'kitten'},
    {'number': 2, 'fruit': 'pear', 'pet': 'puppy'},
    {'number': 3, 'fruit': 'pineapple', 'pet': 'turtle'}]
selection = prompter.table_select(
    prompt='Choose one or more from the list:',
    table=data,
    multiple=True)
```
### File/Directory picker
The open and save dialogs present a single line text box with a 'Browse' button. Clicking the button at the bottom of 
the dialog will return the text from the box. Use the 'default' variable to provide a default file or directory path.
Paths may be entered by:
- Typing the path into the text box
- Dragging a file or folder onto the dialog window
- Clicking the 'Browse' button and selecting a file or directory from the open/save modal

Responses are not validated so you must provide the code to verify that
the file/directory exists, is writable, is not a protected system file, etc. 
#### open()
```
open_path = prompter.open(
    prompt='Select file to open')
```
#### save()
```
default_file = '/tmp/mylog.log'
save_path = prompter.save(
    prompt='Select a file to log output',
    default=default_file)
```
## Tips
### Convert a CSV for tableselect
Use the following example to convert a CSV file with headers for use with tableselect:
```
import csv
with open('CSVSample.csv') as csvfile:
    data = [{k: v for k, v in row.items()} for row in csv.DictReader(csvfile, skipinitialspace=True)]

selection = prompter.table_select(prompt='Select item', table=data, multiple=True)
```

## Requirements
GUIlib and nibbler require a PyObjc bridge to call Apple objective-c code from Python. The macOS builtin system Python 
`/usr/bin/python` includes PyObjc in the default site packages but may be depreciated in future versions of macOS. See
the Python 3 notes for an example of using GUIlib with your own Python framework.

Xcode is required if you would like to modify the existing GUIlib nib files or create new dialogs of your own.

## Known Issues
* Running scripts from some paths like mounted network shares may result in an "Unable to load nib!" error
* table_select search filter only works on string values and does not filter integers

## Acknowledgements
GUIlib would not be possible without Michael Lynn and their fantastic work on nibbler 
https://github.com/pudquick/nibbler
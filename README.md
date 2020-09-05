# PasswordsHandler
Software which organises all passwords in a safe and easy to access way.

Preparations:
1. Make a json file containing your data of the format: {First: {Value1: val1, Value2: val2,...}, Second: {Value1: val1, Value2: val2,...},...}. For example {"github": {"mail": "mail@example.com", "username": "John Smith", "password": "123456"}, "gmail": {"mail": "mail@example.com", "password": "234567"}}
* IMPORTANT
  name the password field "password" if exists (not "Password", "pass", etc.) to enable copy password flag option.
2. In file Psswrd-TUI.py, change the value of global variable "data_path" to the path of your data file.
3. Create a batch file named "pass" with the following content, and add to you path:
@ECHO OFF
python "Full path to Psswrd-TUI.py here" %*

For first encryption of the file use "pass encode". You will be asked for a key WHICH CAN'T BE RESTORED, so don't forget it.
The commant "pass decode" will decode the all file and should only be used to insert new fields or edit new ones, to get the information about <name> use "pass <name>".
For more information about the syntax use "pass help".

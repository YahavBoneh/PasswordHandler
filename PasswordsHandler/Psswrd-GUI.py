from tkinter import *
from Psswrd import *
import pyperclip

data_path = "C:\\Users\\yahav\\AppData\\Roaming\\Custom\\PasswordsHandler\\data.json"

root = Tk()
root.title("PasswordHandler GUI version 1.0 release")

Label(root, text="Identifier: ").grid(row=0, column=0, sticky="W")
identifier = Entry(root)
identifier.grid(row=0, column=1)

Label(root, text="Key: ").grid(row=1, column=0, sticky="W")
key = Entry(root)
key.grid(row=1, column=1)

hide_password_flag = IntVar()
Checkbutton(root, text="Hide password", variable=hide_password_flag).grid(row=2, column=0, sticky="W")

hide_all_flag = IntVar()
Checkbutton(root, text="Hide all", variable=hide_all_flag).grid(row=3, column=0, sticky="W")

copy_password_flag = IntVar()
Checkbutton(root, text="Copy password", variable=copy_password_flag).grid(row=4, column=0, sticky="W")

Label(root, text=" "*20).grid(row=0, column=2)  # Spacing.

decode = Button(root, text="Decode")
decode.grid(row=0, column=4, sticky="W")

encode = Button(root, text="Encode")
encode.grid(row=1, column=4, sticky="W")

information = Message(root)
information.grid(row=6, column=0, sticky="W")


def print_info(d, name, hide_password=False, hide_all=False, copy_password=False):
    """
    Prints all the required info about <name>.

    :param d: a dictionary consists of all the information.
    :type d: python dictionary.

    :param name: a data specifier name.
    :type name: string.

    :param hide_password: additional flag, if True then the password shall not be shown.
    :type hide_password: bool.

    :param hide_all: additional flag, if True then nothing shall not be shown.
    :type hide_all: bool.

    :param copy_password: additional flag, if True then the password shall be copied to clipboard.
    :type copy_password: bool.

    :raises: PsswrdNoSuchName: if <name> is not found in the dictionary.
    """
    max_len = 0
    try:
        d1 = d[name]
    except:  # If 'name' specifier is not in the dictionary.
        raise PsswrdNoSuchName

    if copy_password:
        if "password" in d1:
            pyperclip.copy(d1["password"])
    if hide_all:
        return

    for k in d1:
        max_len = max(max_len, len(k))

    message = name.upper().center(len(name) + 10, '-')

    for k in d1:
        if hide_password and k == "password":
            continue
        message += "\n" + k.ljust(max_len + 5) + d1[k]

    information.config(text=message)


error_channel = Label(root)
error_channel.grid(row=5, column=1, sticky="W")


def info():
    error_channel.config(text="")
    p = Psswrd(data_path, identifier.get(), False, False, copy_password_flag.get(), hide_password_flag.get(), hide_all_flag.get(), key.get, print_info)
    try:
        p.info()
    except BaseException as e:
        error_channel.config(text="Error: " + str(e), fg="red")


get_info = Button(root, text="Get info", command=info)
get_info.grid(row=5, column=0, sticky="W")

root.mainloop()

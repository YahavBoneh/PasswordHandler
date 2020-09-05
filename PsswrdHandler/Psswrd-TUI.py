from Psswrd import *
import sys
import getpass


try:
    import pyperclip
except ImportError:
    try:
        PsswrdNoModule.no_module('pyperclip')
        import pyperclip
    except PsswrdNoModule.PsswrdNoModuleCouldNotInstall as e:
        print(str(e))
        sys.exit()


try:
    from colorama import Fore, init
    init()
except ImportError:
    try:
        PsswrdNoModule.no_module('colorama')
        from colorama import Fore, init
        init()
    except PsswrdNoModule.PsswrdNoModuleCouldNotInstall as e:
        print(str(e))
        sys.exit()


data_path = r"C:\Users\yahav\Google Drive\Custom\PsswrdHandler\data.json"  # Path to the json file with the data here.

help_message = """
You are using PASSWORDS HANDLER TUI version 1.0-release.

pass help               Provides information on how to use the program.
pass decode             Decodes the data file. You will be asked for the key.
pass encode             Encodes the data file. You will be asked for the key.
pass <name>             Prints all the saved information about name. You will be asked for the key.

Additional flags:
-hp                     Hide password.
-ha                     Hide all.
-c                      Copy password.

If you forgot your password that's a bummer.
"""

MIN_LENGTH = 2  # Psswrd-TUI.py name/help/decode/encode.
MAX_LENGTH = 4  # Psswrd-TUI.py name -ha/-hp -c.


class PsswrdTUISyntaxError(BaseException):
    """
    Exception for syntax error.
    """
    def __init__(self):
        self.message = "Incorrect syntax. The syntax is \"pass <code> <command> <-hp/-ha to hide password/all> <-c to copy password>\".\nType \"pass help\" for help."

    def __str__(self):
        return self.message


def process_args(args):
    """
    Returns user's arguments in a specific order.

    :param args: user's args.
    :type args: python list.

    :raises PsswrdSyntaxError: in case of wrong syntax.
    """
    if not (MIN_LENGTH <= len(args) <= MAX_LENGTH):
        raise PsswrdTUISyntaxError

    return args[1], "decode" in args, "encode" in args, "-c" in args, "-hp" in args, "-ha" in args


def get_key():
    return str(getpass.getpass("Key......."))


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

    print(name.upper().center(len(name) + 10, '-'))

    for k in d1:
        if hide_password and k == "password":
            continue
        print(k.ljust(max_len + 5) + d1[k])


def make_yellow(s):
    return Fore.YELLOW + s


if __name__ == "__main__":
    try:
        args = process_args(sys.argv)
        if args[0] == "help":
            print(help_message)
            sys.exit()
        p = Psswrd(data_file_path=data_path, command=args[0], decode=args[1], encode=args[2], copy_password=args[3],
                   hide_password=args[4], hide_all=args[5], f_get_key=get_key, f_show_info=print_info)
    except PsswrdTUISyntaxError as e:
        print(make_yellow(str(e)))
        sys.exit()
    except SystemExit:
        sys.exit()

    try:
        p.info()
    except BaseException as e:
        print(make_yellow(str(e)))

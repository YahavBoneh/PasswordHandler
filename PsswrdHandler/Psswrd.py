#! python3

import sys
import os
import json
import subprocess
import PsswrdNoModule

try:
    from cryptography.fernet import Fernet
except ImportError:
    PsswrdNoModule.no_module('cryptography')  # Can raise PsswrdNoModuleCouldNotInstall
    from cryptography.fernet import Fernet


values = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-"  # All values which can be used for the key.
values_len = len(values)


class PsswrdEncrypted(BaseException):
    """
    Exception for the case the user tries to encrypt an encrypted file.
    """
    def __init__(self):
        self.message = "File is already encrypted."

    def __str__(self):
        return self.message


class PsswrdNoSuchName(BaseException):
    """
    Exception for the case the user asks for details about unrecognised specifier.
    """
    def __init__(self):
        self.message = "Given identifier was not found in the database."

    def __str__(self):
        return self.message


class PsswrdInvalidKey(BaseException):
    """
    Exception for the case the key consists invalid characters.
    """
    def __init__(self):
        self.message = "The given key consists of invalid characters."

    def __str__(self):
        return self.message


class PsswrdIncorrectKey(BaseException):
    """
    Exception for the case the given key is incorrect.
    """
    def __init__(self):
        self.message = "Given key is incorrect."

    def __str__(self):
        return self.message


def dict_to_json(d, j):
    """
    Saves dict info to a json file.

    :param d: dictionary.
    :type d: python dictionary.

    :param j: path to a json file.
    :type j: string.

    :raise: if there is a problem with writing to j or d is not iterable.
    """
    for k in d:
        k = str(k)
    with open(j, "w") as f:
        json.dump(d, f)


def json_to_dict(j):
    """
    Returns python dictionary with the data in a json file.

    :param j: path to a json file.
    :type j: string.

    :raise: if there is a problem with reading from j

    :rtype: python dictionary.
    """
    with open(j, "r") as f:
        return json.loads(f.read())


def generate_key(n):
    """
    Returns a key which can be used by Fernet.

    :param n: user's key.
    :type n: int.

    @:rtype: string.
    """

    key = ''
    for i in range(43):  # Idk that encryption is weird but that is the requested length minus 1 (to add '=' at the end).
        key += values[(n * i + i) % values_len]  # Random way of transforming the original key to a key of the requested type.
    key += '='  # The key has to end with '='.
    key = key.encode('utf-8')
    return key


def encrypt(j, n):
    """
    Encrypts a json file with the key (generating by) n.

    :param j: path to a json file.
    :type j: string.

    :param n: key.
    :type n: int.

    :raises PsswrdIncorrectKey: if the key is incorrect.
    """
    try:
        key = generate_key(n)
        with open(j, 'rb') as f:
            data = f.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        with open(j, 'wb') as f:
            f.write(encrypted)
    except:
        raise PsswrdIncorrectKey


def decrypt(j, n):
    """
    Decrypts a json file with the key (generating by) n.

    :param j: path to a json file.
    :type j: string.

    :param n: key.
    :type n: int.

    :raises PsswrdIncorrectKey: if key is incorrect.
    """
    try:
        key = generate_key(n)
        with open(j, 'rb') as f:
            data = f.read()
        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)
        with open(j, 'wb') as f:
            f.write(decrypted)
    except:
        raise PsswrdIncorrectKey


class Psswrd:
    """
    This class deals with the user's input and execute what has to be done.
    """

    def __init__(self, data_file_path, command, decode, encode, copy_password, hide_password, hide_all, f_get_key, f_show_info):
        """
        Creates new Psswrd instance.

        :param data_file_path: path to the json file containing all data.
        :type data_file_path: string.

        :param command: user's command (e.g encrypt/decrypt or a data specifier).
        :type command: string.

        :param decode: optional command, if True then the purpose of the operation is to decode the file.
        :type decode: bool.

        :param encode: optional command, if True then the purpose of the operation is to encode the file.
        :type encode: bool

        :param copy_password: additional flag, if True then the password shall be copied to clipboard.
        :type copy_password: bool.

        :param hide_password: additional flag, if True then the password shall not be shown.
        :type hide_password: bool

        :param hide_all: additional flag, if True then nothing shall not be shown.
        :type hide_all: bool

        :param f_get_key: function to get the key with.
            * not parameters*

            :rtype: string.
        :type f_get_key: function.

        :param f_show_info: function to show the information about the specifier with.
            :parameter d: a dictionary consists of all the information.
            :type d: python dictionary.

            :parameter name: a data specifier name.
            :type name: string.

            :parameter hide_password: additional flag, if True then the password shall not be shown.
            :type hide_password: bool.

            :parameter hide_all: additional flag, if True then nothing shall not be shown.
            :type hide_all: bool.

            :parameter copy_password: additional flag, if True then the password shall be copied to clipboard.
            :type copy_password: bool.

            :raises: PsswrdNoSuchName: if <name> is not found in the dictionary.

        :type f_show_info: function.
        """
        self.data_file_path = data_file_path
        self.command = command
        self.decode = decode
        self.encode = encode
        self.copy_password_flag = copy_password
        self.hide_password_flag = hide_password
        self.hide_all_flag = hide_all
        self.f_get_key = f_get_key
        self.f_show_info = f_show_info
        self.key = 0  # Key is initialized to zero because we won't necessarily need to ask for it.

    def __is_decoded(self):
        """
        Check if the json file is already decrypted.

        rtype: bool.
        """
        try:
            d = json_to_dict(self.data_file_path)
            return True
        except:
            return False

    def __get_key(self):
        """
        Returns the union of the ascii values of user's input.

        :raises PsswrdInvalidKey: in case the user inserted invalid characters as key.

        :rtype: int.
        """
        try:
            # temp = str(getpass.getpass("Key......."))
            # temp = "".join([str(ord(i)) for i in temp])  # Converts every character to int and attach them.
            # self.key = int(temp)
            temp = str(self.f_get_key())
            self.key = int("".join([str(ord(i)) for i in temp]))  # Converts every character to int and attach them.
        except:
            raise PsswrdInvalidKey

    def __decode(self):
        """
        Return a dictionary from an encrypted json file.

        :raises PsswrdIncorrectKey: if the key is incorrect (i.e the file can't be decrypted with the given key).

        :rtype: python dictionary.
        """
        try:
            decrypt(self.data_file_path, self.key)
        except PsswrdIncorrectKey:  # Key is incorrect if an exception has been raised by decrypt.
            raise
        try:
            d = json_to_dict(self.data_file_path)
        except PsswrdIncorrectKey:  # Key is incorrect if an exception has been raised by json_to_dict.
            encrypt(self.data_file_path, self.key)  # If we got here the file has been incorrectly decrypted so the process should be reversed.
            raise
        return d

    def __encode(self):
        """
        Encrypt the json file.

        :raises PsswrdEncrypted: if the file is already encrypted, meant to make sure the file is not double encrypted.
        """
        try:
            d = json_to_dict(self.data_file_path)
        except:  # If an exception is raised then the file is already encrypted.
            raise PsswrdEncrypted
        encrypt(self.data_file_path, self.key)

    def info(self):
        """
        Gives the user the requested information if possible.

        :except: PsswrdEncrypted: if the user try to encrypt an encrypted file.

        :except PsswrdInvalidKey: if the key consists of invalid characters.

        :except PsswrdIncorrectKey: if the key is incorrect.

        :except PsswrdNoSuchName: if the identifier name is unrecognisable.
        """
        if self.__is_decoded() and self.decode:
            os.system(self.data_file_path)  # Decoding the whole file means a change has to be done, so the file is automatically opened.
            return

        if (not self.__is_decoded()) and self.encode:  # If the file is already encrypted and we only need to encrypt the file we won't need the key.
            raise PsswrdEncrypted

        self.__get_key()

        if self.encode:  # If the only purpose is to encode the file.
            self.__encode()
            return
        d = self.__decode()  # We decode the file even if it is not the only purpose because we will need the data anyway.

        if self.decode:  # In case decoding the file is the sole purpose of the operation.
            os.system(self.data_file_path)  # Decoding the whole file means a change has to be done, so the file is automatically opened.
            return

        try:
            self.f_show_info(d, self.command, self.hide_password_flag, self.hide_all_flag, self.copy_password_flag)
        except PsswrdNoSuchName:
            self.__encode()
            raise
        self.__encode()

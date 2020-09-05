import subprocess


class PsswrdNoModuleCouldNotInstall(BaseException):
    """
    Exception for the case the missing module couldn't be downloaded.
    """
    def __init__(self, module_name):
        self.message = f"Module {module_name} could not be imported nor automatically installed, please install it."

    def __str__(self):
        return self.message


def no_module(module):
    """
        Trying to install a module if necessary.

        :param module: name of missing module.
        :type module: string.

        :raises PsswrdNoModuleCouldNotInstall: if module could not be installed.
        """
    try:
        subprocess.check_output(f"pip install {module}", stderr=subprocess.STDOUT)  # Runs the command and hides the output.
    except subprocess.CalledProcessError:
        raise PsswrdNoModuleCouldNotInstall(module)

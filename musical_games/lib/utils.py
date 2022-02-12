import os
import subprocess
import six

__author__ = 'Robbert Harms'
__date__ = "2015-09-23"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def run_command(command, shell=False):
    """Run a shell command.

    Args:
        command (str or list): the shell command to run
        shell (bool): the subprocess flag for shell

    Raises:
        RuntimeError: if the command returned with exit code -1

    Returns:
        str: the stdout of the command
    """
    if isinstance(command, six.string_types):
        command = command.split(' ')

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    stdout, stderr = process.communicate()
    rc = process.returncode
    if rc == 1:
        raise RuntimeError('Error in command. Error message: ' + str(stderr))
    return stdout


def bash_function_exists(function_name):
    """Check if the bash function with the given name exists.

    Runs the command 'which <function_name>' to check if the function exists.

    Args:
        function_name (str): the function name to check for existence

    Returns:
        boolean: if the command exists
    """
    try:
        run_command('which {}'.format(function_name))
        return True
    except RuntimeError:
        return False


def ensure_dir_exists(file_path):
    """Ensures that the dir to the given file exists.

    Normally used when writing output to a file to make sure the directories exist.

    Args:
        file_path (str): the path to a file.
    """
    if not os.path.isdir(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))


def remove_file_if_exists(file_path):
    """Remove the given file if it exists.

    Args:
        file_path (str): the path to a file.
    """
    if os.path.isfile(file_path):
        os.remove(file_path)

__author__ = 'Robbert Harms'
__date__ = "2015-09-23"
__maintainer__ = "Robbert Harms"
__email__ = "robbert@xkls.nl"

import shutil
import subprocess


def run_command(command: list[str], shell: bool = False) -> bytes:
    """Run a shell command.

    Args:
        command: the shell command to run
        shell: the subprocess flag for shell

    Raises:
        RuntimeError: if the command returned with exit code -1

    Returns:
        bytes: the output from the command
    """
    if isinstance(command, str):
        command = command.split(' ')

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    stdout, stderr = process.communicate()
    rc = process.returncode
    if rc == 1:
        raise RuntimeError('Error in command. Error message: ' + str(stderr))
    return stdout


def bash_function_exists(function_name: str) -> bool:
    """Check if the bash function with the given name exists.

    Args:
        function_name: the function name to check for existence

    Returns:
        True if the command exists
    """
    return shutil.which(function_name) is not None

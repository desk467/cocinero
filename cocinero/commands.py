from typing import List, Callable
import subprocess


def exec_command(commands: List[str], parser_func: Callable):
    '''
    `exec_command` runs a command passed with its args and transform its outputs
    by using a `parser_func` passed.

    '''
    process = subprocess.Popen(
        commands,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output, err = process.communicate()

    return parser_func(output, err)

from typing import List, Callable
import subprocess


def exec_command(commands: List[str], parser_func: Callable):
    '''
    `exec_command` executa um comando passado, junto com seus argumentos
    transforma a saída em um objeto, usando a `parser_func` passada
    e retorna.

    '''
    process = subprocess.Popen(
        commands,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output, err = process.communicate()

    return parser_func(output, err)

'''
replace.py

Este plugin altera uma string dentro de um ou mais arquivos


'''
__author__ = 'Ricardo Gomes'

import os


def replace(*args, **kwargs):
    repo_tmp_path = kwargs.get('repo_tmp_path')
    from_string = kwargs.get('from')
    to_string = kwargs.get('to')
    paths = kwargs.get('paths')

    for path in paths:
        absolute_path = os.path.join(repo_tmp_path, path)
        with open(absolute_path, 'r') as file:
            new_content = file.read().replace(from_string, to_string)

        with open(absolute_path, 'w') as file:
            file.write(new_content)

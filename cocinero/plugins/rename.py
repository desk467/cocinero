'''
rename.py

Este plugin renomeia um ou mais arquivos


'''
__author__ = 'Ricardo Gomes'

import os


def rename(*args, **kwargs):
    from_string = kwargs.get('from')
    to_string = kwargs.get('to')
    paths = kwargs.get('paths')
    repo_tmp_path = kwargs.get('repo_tmp_path')

    for path in paths:
        absolute_path = os.path.join(repo_tmp_path, path)
        new_file = path.replace(from_string, to_string)

        new_absolute_path = os.path.join(repo_tmp_path, new_file)
        os.rename(absolute_path, new_absolute_path)

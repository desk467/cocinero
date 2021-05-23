'''
rename.py

This plugin renames one or more files


'''
__author__ = 'Ricardo Gomes'

import os


def rename(step, repository):
    '''
    `rename` rename a list of files from repository
    '''
    from_string = step.args.get('from')
    to_string = step.args.get('to')

    try:
        for path_to_rename in step.args.get('paths'):
            absolute_path = os.path.join(repository.directory, path_to_rename)
            new_filename = path_to_rename.replace(from_string, to_string)

            new_absolute_path = os.path.join(
                repository.directory, new_filename)

            os.rename(absolute_path, new_absolute_path)

        return True
    except:
        return False

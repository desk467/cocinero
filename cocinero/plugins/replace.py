'''
replace.py

This plugin replaces a string from a file

'''
__author__ = 'Ricardo Gomes'

import os


def replace(step, repository):
    '''
    `replace` change content of a file, finding a string to replace
    '''
    from_string = step.args.get('from')
    to_string = step.args.get('to')

    try:
        for filepath_to_replace in step.args.get('paths'):
            absolute_path = os.path.join(
                repository.directory, filepath_to_replace)
            with open(absolute_path, 'r') as file_to_change:
                new_content = file_to_change.read().replace(from_string, to_string)

            with open(absolute_path, 'w') as file_to_change:
                file_to_change.write(new_content)

        return True
    except:
        return False

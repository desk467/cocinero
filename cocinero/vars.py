import os


def get_cocinero_vars():
    '''
    `get_cocinero_vars` returns all environment variables that
    are defined on CLI initialization.
    '''
    return {
        'project_name': os.environ.get('COCINERO_PROJECT_NAME'),
        'version': os.environ.get('COCINERO_VERSION'),
    }

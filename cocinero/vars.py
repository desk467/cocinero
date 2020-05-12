import os


def get_cocinero_vars():
    '''
    `get_cocinero_vars` retorna todas as variáveis de ambiente que foram
    definidas na inicialização do CLI.
    '''
    return {
        'project_name': os.environ.get('COCINERO_PROJECT_NAME'),
        'version': os.environ.get('COCINERO_VERSION'),
    }

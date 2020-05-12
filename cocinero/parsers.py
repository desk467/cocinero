def parse_successful_command(output, err: str):
    '''
    `parse_successful_command` verifica se um comando executou retornando 0.

    Em sistemas Unix-based, um comando que retorna zero significa que executou
    de forma bem sucedida.
    '''
    return output is b''


def parse_git_clone_output(output, err: str):
    '''
    `parse_git_clone_output` recebe um output e um err vindos de uma execução
    de um `git clone`, analisa e retorna um objeto mais facilmente manipulável.

    @todo: Melhorar parsing
    '''
    return parse_successful_command(output, err)


def parse_git_commit_output(output, err: str):
    '''
    `parse_git_commit_output` recebe um output e um err vindos de uma execução
    de um `git commit`, analisa e retorna um booleano indicando se aquele comando
    executou com sucesso.

    @todo: Melhorar parsing
    '''
    return parse_successful_command(output, err)

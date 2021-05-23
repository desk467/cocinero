def parse_successful_command(output, err: str):
    '''
    `parse_successful_command` checks if a command returned
    successfully (by returning zero staus code).
    '''
    return output == b''


def parse_git_clone_output(output, err: str):
    '''
    `parse_git_clone_output` receives an output and an err string codes
    from a `git clone` execution, parses it and returns if command was
    executed successfully.

    @todo: Improve parsing
    '''
    return parse_successful_command(output, err)


def parse_git_commit_output(output, err: str):
    '''
    `parse_git_commit_output`  receives an output and an err string codes
    from a `git commit` execution, parses it and returns if command was
    executed successfully.

    @todo: Improve parsing
    '''
    return parse_successful_command(output, err)

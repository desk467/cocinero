import os
import uuid
import subprocess
import shutil
from cocinero.commands import exec_command
from cocinero.parsers import parse_git_clone_output, parse_git_commit_output
import tempfile

from dataclasses import dataclass


class CloneException(Exception):
    '''
    Uma `CloneException` é lançada quando o comando
    `git clone` falha por algum motivo.
    '''

    def __init__(self, repository_url):
        super(self).__init__('Falha ao executar o clone')
        self.repository_url = repository_url


@dataclass
class Repository:
    '''
    `Repository` define uma classe POJO para os repositórios
    manipulados pelo cocinero.
    '''
    url: str
    project_name: str
    directory: str

    def commit_changes(self):
        '''
        `commit_changes` aplica as alterações geradas pelos
        steps definidos no recipe neste repositório.
        '''
        is_successfully_executed = exec_command(
            ['git', 'commit', '-am', '"chore: Cooking repo with cocinero"'], parse_git_commit_output)

        return is_successfully_executed

    def remove_recipe(self):
        '''
        `remove_recipe` apaga a recipe do repositório.
        '''
        os.remove(os.path.join(self.directory, 'cocinero-recipe.yml'))

    def move_to_cwd(self):
        '''
        `move_to_cwd` move este repositório para a pasta
        onde o usuário está executando o CLI.
        '''
        shutil.move(
            src=os.path.join(self.directory),
            dst=os.path.join(os.getcwd(), self.project_name),
        )


def clone_repository(repository_url: str, project_name: str):
    '''
    `clone_repository` clona um repositório considerando
    a `repository_url` passada.
    '''
    repo_destination_name = str(uuid.uuid4())
    repo_destination_dir = os.path.join(
        tempfile.gettempdir(), repo_destination_name)

    is_successfully_executed = exec_command(['git', 'clone', repository_url,
                                             repo_destination_dir], parser_func=parse_git_clone_output)

    if not is_successfully_executed:
        raise CloneException(repository_url)

    return Repository(
        url=repository_url,
        directory=repo_destination_dir,
        project_name=project_name
    )

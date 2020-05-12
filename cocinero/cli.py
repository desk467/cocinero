import click
import os
import sys
from cocinero.repository import clone_repository
from cocinero.recipe import parse_recipe, is_requirement_satisfied, execute_step
from cocinero.vars import get_cocinero_vars
from rich.console import Console


@click.group()
def cli():
    pass


@click.command()
@click.argument('repository_url')
@click.argument('project_name', default='my_awesome_project')
def cook(repository_url, project_name):
    '''
    Gera um novo projeto a partir de um template
    '''

    os.environ['COCINERO_REPOSITORY_URL'] = repository_url
    os.environ['COCINERO_PROJECT_NAME'] = project_name

    console = Console()

    console.print(
        f":egg: cocinero {get_cocinero_vars().get('version')}\n", style='bold green')

    console.print('-> Clonando repositório')

    repository = clone_repository(repository_url, project_name)

    console.print('-> Carregando recipe')
    recipe = parse_recipe(repository)

    console.print('\n-> Verificando requisitos')
    for requirement in recipe.requirements:
        if is_requirement_satisfied(requirement):
            console.print(
                f'  - Requisito [bold]{requirement.name}[/bold] satisfeito')
        else:
            console.print(
                f'  - Requisito [bold]{requirement.name}[/bold] NÃO SATISFEITO. Abortar.',
                style='red'
            )
            sys.exit(-1)

    console.print('\n-> Executando passos')
    for index, step in enumerate(recipe.steps):
        console.print(f'  - [bold]Passo {index+1}:[/bold] {step.name}')
        execute_step(step, repository)

    console.print('\n-> Apagando recipe')
    repository.remove_recipe()

    console.print('\n-> Commitando mudanças no repositório')
    repository.commit_changes()

    repository.move_to_cwd()

    console.print('\n:sparkles: Pronto. :sparkles:')


cli.add_command(cook)

if __name__ == "__main__":
    cli()

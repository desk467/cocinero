import uuid
import click
import subprocess
import yaml
import shutil
import os

import plugins


@click.group()
def cli():
    pass


@click.command()
@click.argument('repo')
@click.argument('project_name', default='my_awesome_project')
def cook(repo, project_name):
    '''
    Gera um novo projeto a partir de um template
    '''

    # Clone
    repo_destination_name = f'repo-{uuid.uuid4()}'
    command = f'git clone {repo} /tmp/{repo_destination_name}'

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # Parse recipe
    repo_tmp_path = f'/tmp/{repo_destination_name}'
    with open(f'{repo_tmp_path}/cocinero-recipe.yml', 'r') as recipe_file:
        recipe = yaml.load(recipe_file, Loader=yaml.BaseLoader).get('recipe')

        requirements, steps = recipe.get(
            'requirements', []), recipe.get('steps', [])

        for requirement in requirements:
            print(requirement)

        for step in steps:
            plugin_name = [key for key in step.keys() if key != 'name'][0]
            plugin_attrs = {key: val for key,
                            val in step.items() if key == plugin_name}.get(plugin_name)

            plugin_func = getattr(plugins, plugin_name)

            if type(plugin_attrs) == dict:
                plugin_func(project_name=project_name,
                            repo_tmp_path=repo_tmp_path, **plugin_attrs)
            else:
                plugin_func(project_name=project_name,
                            repo_tmp_path=repo_tmp_path, plugin_attr=plugin_attrs)
    # Move
    shutil.move(repo_tmp_path, os.path.join(os.getcwd(), project_name))


cli.add_command(cook)

if __name__ == "__main__":
    cli()

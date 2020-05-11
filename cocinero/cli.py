import click
import os

import plugins
import repo
import parser
from requirements import check_requirement


@click.group()
def cli():
    pass


@click.command()
@click.argument('repo_url')
@click.argument('project_name', default='my_awesome_project')
def cook(repo_url, project_name):
    '''
    Gera um novo projeto a partir de um template
    '''

    repo_tmp_path = repo.clone(repo_url)

    # Parse recipe
    with open(f'{repo_tmp_path}/cocinero-recipe.yml', 'r') as recipe_file:
        recipe = parser.parse_recipe(recipe_file, project_name)

        requirements, steps = recipe.get(
            'requirements', []), recipe.get('steps', [])

        for requirement in requirements:
            check_requirement(requirement)

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
    # Commit
    repo.commit_changes(repo_tmp_path, project_name)

    # Move
    repo.move_repo(repo_tmp_path, os.path.join(os.getcwd(), project_name))


cli.add_command(cook)

if __name__ == "__main__":
    cli()

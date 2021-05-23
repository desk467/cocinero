from typing import List
from dataclasses import dataclass

import os
import yaml
import jinja2

from distutils.spawn import find_executable

from cocinero.repository import Repository
from cocinero.vars import get_cocinero_vars
from cocinero import plugins


@dataclass
class Requirement:
    '''
    `Requirement` defines a requirement that must be installed
    on the user's device so that he can execute a recipe.
    '''

    name: str


@dataclass
class Step:
    '''
    `Step` defines a step that will be execute in a recipe.
    '''
    name: str
    plugin_name: str
    args: dict


@dataclass
class Recipe:
    '''
    `Recipe` is a class that defines a list of requirements
    and a list of steps that will be executed to create a new
    repository.
    '''
    requirements: List[Requirement]
    steps: List[Step]


def load_recipe_content_from(repository: Repository) -> str:
    '''
    `load_recipe_content_from` open cocinero-recipe.yml file,
    returning its content.
    '''
    recipe_file = open(os.path.join(
        repository.directory, 'cocinero-recipe.yml'))

    recipe_content = recipe_file.read()

    recipe_file.close()

    return recipe_content


def compile_recipe_content(recipe_content: str) -> str:
    '''
    `compile_recipe_content` parses `recipe_content` using Jinja2.
    '''
    template = jinja2.Template(recipe_content)
    cocinero_vars = get_cocinero_vars()

    return template.render(**cocinero_vars)


def parse_steps(steps: List[dict]) -> List[Step]:
    '''
    `parse_steps` creates a list of steps from an array of steps.
    '''
    mounted_steps: List[Step] = []

    for step in steps:
        mounted_step: dict = {
            'name': step.get('name'),
            'args': {}
        }

        for key_name, key_val in step.items():
            if key_name != 'name':
                mounted_step['plugin_name'] = key_name
                mounted_step['args'] = key_val

        mounted_steps.append(
            Step(
                name=mounted_step['name'],
                plugin_name=mounted_step['plugin_name'],
                args=mounted_step['args']
            )
        )

    return mounted_steps


def parse_recipe(repository: Repository) -> Recipe:
    '''
    `parse_recipe` receives a `repository`, compile its recipe and returns it
    '''
    recipe_content = load_recipe_content_from(repository=repository)
    recipe_content = compile_recipe_content(recipe_content=recipe_content)

    recipe_yml = yaml.load(
        recipe_content, Loader=yaml.BaseLoader).get('recipe')

    requirements = [Requirement(requirement_name)
                    for requirement_name in recipe_yml.get('requirements', [])]

    steps = parse_steps(recipe_yml.get('steps'))

    return Recipe(requirements, steps)


def is_requirement_satisfied(requirement: Requirement) -> bool:
    '''
    `is_requirement_satisfied` checks if a requirement is satisfied
    on user's machine
    '''
    requirement_installed = find_executable(requirement.name) is not None

    return requirement_installed


def execute_step(step: Step, repository: Repository) -> bool:
    '''
    `execute_step` executes a step defined in cocinero recipe
    that is defined in the repository.
    '''

    step_func = getattr(plugins, step.plugin_name)

    is_successfully_executed = step_func(step, repository)

    return is_successfully_executed

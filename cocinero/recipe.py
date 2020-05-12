from typing import List
from dataclasses import dataclass

import os
import json
import yaml
import jinja2

from distutils.spawn import find_executable

from cocinero.commands import exec_command
from cocinero.repository import Repository
from cocinero.vars import get_cocinero_vars
from cocinero import plugins


@dataclass
class Requirement:
    '''
    `Requirement` define um requisito necessário
    instalado no dispositivo do usuário para que uma recipe
    possa ser feita.
    '''

    name: str


@dataclass
class Step:
    '''
    `Step` define um passo que será executado no `recipe`
    para gerar o projeto do usuário corretamente.
    '''
    name: str
    plugin_name: str
    args: dict


@dataclass
class Recipe:
    '''
    `Recipe` é uma receita para a geração de um template.
    Contém `requirements` e `steps`
    '''
    requirements: List[Requirement]
    steps: List[Step]


def load_recipe_content_from(repository: Repository) -> str:
    '''
    `load_recipe_content_from` abre o arquivo de recipe e retorna seu conteúdo.
    '''
    recipe_file = open(os.path.join(
        repository.directory, 'cocinero-recipe.yml'))

    recipe_content = recipe_file.read()

    recipe_file.close()

    return recipe_content


def compile_recipe_content(recipe_content: str) -> str:
    '''
    `compile_recipe_content` compila o arquivo de recipe utilizando o Jinja2.
    '''
    template = jinja2.Template(recipe_content)
    cocinero_vars = get_cocinero_vars()

    return template.render(**cocinero_vars)


def parse_steps(steps: List[dict]) -> List[Step]:
    '''
    `parse_steps` monta uma lista de Step a partir de um
    array de dicionários com a forma de um step.
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
    `parse_recipe` recebe um `repository`, recupera sua recipe e retorna um objeto
    do tipo `Recipe`.
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
    `is_requirement_satisfied` verifica se um requisito está instalado
    na máquina do usuário.
    '''
    requirement_installed = find_executable(requirement.name) is not None

    return requirement_installed


def execute_step(step: Step, repository: Repository) -> bool:
    '''
    `execute_step` executa um passo definido no recipe do repositório template.
    '''

    step_func = getattr(plugins, step.plugin_name)

    is_successfully_executed = step_func(step, repository)

    return is_successfully_executed

import json
import yaml


def parse_recipe(recipe_file, project_name):
    recipe_yml = yaml.load(recipe_file, Loader=yaml.BaseLoader).get('recipe')
    recipe_json = json.dumps(recipe_yml)

    recipe_json = recipe_json.replace('$name', project_name)

    return json.loads(recipe_json)

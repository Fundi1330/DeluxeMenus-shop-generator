from yaml import dump, load, Loader, Dumper
from os.path import isfile, join, splitext, dirname, realpath, exists
from os import listdir
from typing import Any, IO

from abc import ABC, abstractmethod


class BaseConverter(ABC):
    def __init__(self) -> None:
        self.dmenu_config_files = []

        self.ROOT_DIR = dirname(dirname(realpath(__file__)))

        with open(f'{self.ROOT_DIR}/config.yml', 'r') as conf:
            self.config = load(conf.read(), Loader)

        
        self.INPUT_DIR = join(self.ROOT_DIR, self.config['input_dir'])
        self.RESULT_DIR = join(self.ROOT_DIR, self.config['result_dir'])
        self.DIRECTORIES = self.config['directories']
        self.ORAXEN_ITEM_MATERIALS = self.config['materials']

    def format_displayname(self, displayname: str) -> str:
        return displayname[displayname.index('>') + 1:]

    @abstractmethod
    def items_to_buy_pages(self, file: dict):
        pass

    @abstractmethod
    def items_to_list_of_items(self, file: dict, dirname: str):
        pass

    def items_to_dmenu(self, file: IO[Any], dirname: str):
        file_as_yaml: dict = load(file.read(), Loader)
        self.items_to_list_of_items(file_as_yaml, dirname)
        self.items_to_buy_pages(file_as_yaml)
        self.generate_dmenu_config()

    def generate_dmenu_config(self):
        result = {
            'debug': 'HIGHEST',
            'check_updates': True,
            'gui_menus': {}
        }
        for file in self.dmenu_config_files:
            file_dict = {
                'file': f'are_you_sure/{file}'
            }
            result['gui_menus'][splitext(file)[0]] = file_dict
        result_yaml = dump(result, Dumper=Dumper, allow_unicode=True, default_style=False, default_flow_style=False, sort_keys=False)
        config_path = f'{self.ROOT_DIR}/output/config.yml'
        config_yaml = None
        if exists(config_path):
            with open(config_path, 'r') as dmenu_config:
                config_yaml = load(dmenu_config.read(), Loader)
        with open(config_path, 'w', encoding='utf-8') as dmenu_config:
            if config_yaml != None:
                config_yaml['gui_menus'].update(result['gui_menus'])
                result_yaml = dump(config_yaml, Dumper=Dumper)
            dmenu_config.write(result_yaml)

    def load_oraxen_recipes(self) -> dict:
        with open(join(self.INPUT_DIR, 'recipes.yml'), 'r') as recipes:
            recipes_dict = load(recipes.read(), Loader)
        
        result = {}
        for r_id, r_data in recipes_dict.items():
            ing_dict = {}
            result[r_id] = {}
            for ing, ing_val in r_data['ingredients'].items():
                if 'oraxen_item' in ing_val.keys():
                    ing_dict[ing] = ing_val['oraxen_item']
                else:
                    ing_dict[ing] = ing_val['minecraft_type']
                for row in r_data['shape']:
                    if not ing_dict[ing] in result[r_id].keys(): result[r_id][ing_dict[ing]] = 0
                    result[r_id][ing_dict[ing]] += row.count(ing)

        return result

    def convert(self):
        self.recipes = self.load_oraxen_recipes()
        for d in self.DIRECTORIES:
            dir_path = f'{self.INPUT_DIR}{d}/'
            for f in listdir(dir_path):
                file_path = join(dir_path, f)
                if isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        self.items_to_dmenu(file, d)


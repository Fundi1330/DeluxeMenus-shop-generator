from yaml import dump, load, Loader, Dumper
from os.path import isfile, join, splitext, dirname, realpath
from os import listdir
from typing import Any, IO
from .base_converter import BaseConverter

class VanillaForItemsConverter(BaseConverter):
    def __init__(self) -> None:
        super().__init__()
        self.DIRECTORIES = self.config['directories']['vanilla']['items']
        self.INPUT_DIR = f'{self.INPUT_DIR}vanilla/items/'
        self.RESULT_DIR = f'{self.RESULT_DIR}vanilla/items/'

    def items_to_buy_pages(self, file: dict):
        for item_id, item_data in file.items():
            result = {
                "menu_title": "&8Підтвердіть покупку",
                "size": 9,
                "items": {
                    "Yes": {
                        "material": "GREEN_WOOL",
                        "slot": 2,
                        "display_name": "&a&lТак! &fЯ хочу купити!",
                        "lore": [
                            "",
                            " &fПідтвердіть покупку",
                            " &fпредмету, натиснувши тут!",
                            "",
                            "&a⊳ Натисніть, щоб купити!"
                        ],
                        "right_click_commands": [
                            f"[console] minecraft:give %player_name% {item_id.lower()} 1",
                            f"[message] &eВи купили &e1x &f{item_id}.",
                            "[close]"
                        ],
                        "left_click_commands": [
                            f"[console] minecraft:give %player_name% {item_id.lower()} 1",
                            f"[message] &eВи купили &e1x &f{item_id}.",
                            "[close]"
                        ],
                        "right_click_requirement": {
                            "requirements": {
                                "empty_slot": {
                                    "type": "string equals ignorecase",
                                    "input": "%player_has_empty_slot%",
                                    "output": "yes",
                                    "deny_commands": [
                                        "[message] &eУ вас недостатньо місця, щоб купити цей предмет!",
                                        "[close]"
                                    ]
                                }
                            }
                        },
                        "left_click_requirement": {
                            "requirements": {
                                "empty_slot": {
                                    "type": "string equals ignorecase",
                                    "input": "%player_has_empty_slot%",
                                    "output": "yes",
                                    "deny_commands": [
                                        "[message] &eУ вас недостатньо місця, щоб купити цей предмет!",
                                        "[close]"
                                    ]
                                }
                            }
                        }
                    },
                    item_id: {
                        "material": item_id,
                        "slot": 4,
                        "display_name": f"{item_data['displayname']}"
                    },
                    "No": {
                        "material": "BARRIER",
                        "slot": 6,
                        "display_name": "&c&lТак! &fЯ не хочу купувати!",
                        "right_click_commands": [
                            "[message] &eВи відмінили покупку!",
                            "[close]"
                        ],
                        "left_click_commands": [
                            "[message] &eВи відмінили покупку!",
                            "[close]"
                        ]
                    },
                    'FilledGlass1': {
                        'material': 'RED_STAINED_GLASS_PANE',
                        'slots': ['0-1', '3', '5', '7-8'],
                        'display_name': '&r'
                    }
                    
                }
            }

            for ing, count in self.recipes[item_id].items():
                requirement = {
                    "type": "has item",
                    "material": ing,
                    "amount": count,
                    "deny_commands": [
                        f"[message] &cВи не маєте достатньо {ing}, щоб купити це! Всього вам потрібно {count}",
                        "[close]"
                    ]
                }
                result['items']['Yes']['left_click_commands'].append(
                    f'[console] minecraft:clear %player_name% minecraft:{ing.lower()} {count}'
                )
                result['items']['Yes']['right_click_commands'].append(
                    f'[console] minecraft:clear %player_name% minecraft:{ing.lower()} {count}'
                )
                result['items']['Yes']['left_click_requirement']['requirements'][f'has_{ing}'] = requirement
                result['items']['Yes']['right_click_requirement']['requirements'][f'has_{ing}'] = requirement

            result_yaml = dump(result, Dumper=Dumper, allow_unicode=True, default_style=False, default_flow_style=False, sort_keys=False)
            with open(f'{self.RESULT_DIR}are_you_sure/are_you_sure_{item_id}.yml', 'w+', encoding='utf-8') as f:
                self.dmenu_config_files.append(f'are_you_sure_{item_id}.yml')
                f.write(result_yaml)

    def items_to_list_of_items(self, file: dict, dirname: str):
        result = {
            'menu_title': '&8Категорія обладунків',
            'update_interval': 1,
            'size': 54,
            'items': {},
        }
        slot = 0
        for item_id, item_data in file.items():
            item_dict = {
                'material': item_id,
                'hide_attributes': False,
                'slot': slot ,
                'display_name': f"{item_data['displayname']}",
                'lore': [
                    f' &7● &fПотрібно: &e{', '.join([f'{ing} x{count}' for ing, count in self.recipes[item_id].items()])}',
                    ' &7● &fКількість: &ex1',
                    '',
                    '&e⊳ Натисніть, щоб купити!',
                ],
                'left_click_commands': [f'[openguimenu] are_you_sure_{item_id}'],
                'right_click_commands': [f'[openguimenu] are_you_sure_{item_id}']

            }
            if slot < 53:
                slot += 1
            result['items'][item_id] = item_dict
        result_yaml = dump(result, Dumper=Dumper, allow_unicode=True, default_style=False, default_flow_style=False, sort_keys=False)
        with open(f'{self.RESULT_DIR}{dirname}.yml', 'w+', encoding='utf-8') as f:
            self.dmenu_config_files.append(f'{dirname}.yml')
            f.write(result_yaml)

    def convert(self):
        super().convert()
        print('All vanilla items for items were converted succesfully')


class VanillaForMoneyConverter(BaseConverter):
    def __init__(self) -> None:
        super().__init__()
        self.DIRECTORIES = self.config['directories']['vanilla']['money']
        self.INPUT_DIR = f'{self.INPUT_DIR}vanilla/money/'
        self.RESULT_DIR = f'{self.RESULT_DIR}vanilla/money/'

    def items_to_buy_pages(self, file: dict):
        for item_id, item_data in file.items():
            result = {
                "menu_title": "&8Підтвердіть покупку",
                "size": 9,
                "items": {
                    "Yes": {
                        "material": "GREEN_WOOL",
                        "slot": 2,
                        "display_name": "&a&lТак! &fЯ хочу купити!",
                        "lore": [
                            "",
                            " &fПідтвердіть покупку",
                            " &fпредмету, натиснувши тут!",
                            "",
                            "&a⊳ Натисніть, щоб купити!"
                        ],
                        "right_click_commands": [
                            f"[console] o give %player_name% {item_id} {self.recipes[item_id]['amount']}",
                            f"[console] eco take %player_name% {self.recipes[item_id]['price']}",
                            f"[message] &eВи купили &e1x &f{item_id}.",
                            "[close]"
                        ],
                        "left_click_commands": [
                            f"[console] o give %player_name% {item_id} {self.recipes[item_id]['amount']}",
                            f"[console] eco take %player_name% {self.recipes[item_id]['price']}",
                            f"[message] &eВи купили &e1x &f{item_id}.",
                            "[close]"
                        ],
                        "right_click_requirement": {
                            "requirements": {
                                "has_money": {
                                    "type": "has money",
                                    "amount": self.recipes[item_id]['price'],
                                    "deny_commands": [
                                        '[message] &e&lКупець &7⊳ &cВи не маєте достатньо грошей, щоб купити це!',
                                        '[close]'
                                    ]
                                },
                                "empty_slot": {
                                    "type": "string equals ignorecase",
                                    "input": "%player_has_empty_slot%",
                                    "output": "yes",
                                    "deny_commands": [
                                        "[message] &eУ вас недостатньо місця, щоб купити цей предмет!",
                                        "[close]"
                                    ]
                                }
                            }
                        },
                        "left_click_requirement": {
                            "requirements": {
                                "has_money": {
                                    "type": "has money",
                                    "amount": self.recipes[item_id]['price'],
                                    "deny_commands": [
                                        '[message] &e&lКупець &7⊳ &cВи не маєте достатньо грошей, щоб купити це!',
                                        '[close]'
                                    ]
                                },
                                "empty_slot": {
                                    "type": "string equals ignorecase",
                                    "input": "%player_has_empty_slot%",
                                    "output": "yes",
                                    "deny_commands": [
                                        "[message] &eУ вас недостатньо місця, щоб купити цей предмет!",
                                        "[close]"
                                    ]
                                }
                            }
                        }
                    },
                    item_id: {
                        "material": item_id,
                        "slot": 4,
                        "display_name": f"{self.format_displayname(item_data['displayname'])}"
                    },
                    "No": {
                        "material": "BARRIER",
                        "slot": 6,
                        "display_name": "&c&lТак! &fЯ не хочу купувати!",
                        "right_click_commands": [
                            "[message] &eВи відмінили покупку!",
                            "[close]"
                        ],
                        "left_click_commands": [
                            "[message] &eВи відмінили покупку!",
                            "[close]"
                        ]
                    },
                    'FilledGlass1': {
                        'material': 'RED_STAINED_GLASS_PANE',
                        'slots': ['0-1', '3', '5', '7-8'],
                        'display_name': '&r'
                    }
                    
                }
            }

            result_yaml = dump(result, Dumper=Dumper, allow_unicode=True, default_style=False, default_flow_style=False, sort_keys=False)
            with open(f'{self.RESULT_DIR}are_you_sure/are_you_sure_{item_id}.yml', 'w+', encoding='utf-8') as f:
                self.dmenu_config_files.append(f'are_you_sure_{item_id}.yml')
                f.write(result_yaml)

    def items_to_list_of_items(self, file: dict, dirname: str):
        result = {
            'menu_title': '&8Категорія обладунків',
            'update_interval': 1,
            'size': 54,
            'items': {},
        }
        slot = 0
        for item_id, item_data in file.items():
            item_dict = {
                'material': item_id,
                'hide_attributes': False,
                'slot': slot ,
                'display_name': f"{self.format_displayname(item_data['displayname'])}",
                'lore': [
                    f' &7● &fЦіна: {self.recipes[item_id]['price']}$',
                    f' &7● &fКількість: &ex{self.recipes[item_id]['amount']}',
                    '',
                    '&e⊳ Натисніть, щоб купити!',
                ],
                'left_click_commands': [f'[openguimenu] are_you_sure_{item_id}'],
                'right_click_commands': [f'[openguimenu] are_you_sure_{item_id}']

            }
            if slot < 53:
                slot += 1
            result['items'][item_id] = item_dict
        result_yaml = dump(result, Dumper=Dumper, allow_unicode=True, default_style=False, default_flow_style=False, sort_keys=False)
        with open(f'{self.RESULT_DIR}{dirname}.yml', 'w+', encoding='utf-8') as f:
            self.dmenu_config_files.append(f'{dirname}.yml')
            f.write(result_yaml)

    def load_oraxen_recipes(self) -> dict:
        with open(join(self.INPUT_DIR, 'recipes.yml'), 'r') as recipes:
            recipes_dict = load(recipes.read(), Loader)
        
        result = {}
        for r_id, r_data in recipes_dict.items():
            recipe_dict = {
                'price': r_data['price'],
                'amount': r_data['amount']
            }
            result[r_id] = recipe_dict

        return result

    def convert(self):
        super().convert()
        print('All vanilla items for money were converted to dmenu for prices succesfully')
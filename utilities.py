import json
import os


def get_configs():
    file_full_path = f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/kitsune/configs/kitsune.json'
    with open(file_full_path) as config_file:
        return json.load(config_file)

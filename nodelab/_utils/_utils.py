import os

import yaml


def read_yaml(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def write_yaml(data, file_path):
    with open(file_path, "w") as file:
        yaml.safe_dump(data, file, default_flow_style=False, sort_keys=False)


def delete_file(file_path):
    if os.path.exists:
        os.remove(file_path)


def get_file_mod_time(filepath):
    return os.path.getmtime(filepath)

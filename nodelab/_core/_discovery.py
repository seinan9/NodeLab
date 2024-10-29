import ast
import os

from .._utils._configuration import CACHE_FILE
from .._utils._utils import get_file_mod_time, read_yaml, write_yaml


def scan_directory_for_nodes(dir):
    try:
        cache = read_yaml(CACHE_FILE)
    except FileNotFoundError:
        cache = {}

    node_file_map = cache.get("node_file_map", {})
    last_modified = cache.get("last_modified", {})
    current_mod_times = {}
    is_cache_valid = True

    for root, _, files in os.walk(dir):
        for filename in files:
            if filename.endswith(".py"):
                filepath = os.path.join(root, filename)
                file_mod_time = get_file_mod_time(filepath)
                current_mod_times[filepath] = file_mod_time

                if (
                    filepath not in last_modified
                    or last_modified[filepath] != file_mod_time
                ):
                    is_cache_valid = False
                    with open(filepath, "r") as file:
                        node_tree = ast.parse(file.read(), filename=filepath)
                        node_file_map.update(find_nodes_in_ast(node_tree, filepath))

    if not is_cache_valid:
        cache_data = {
            "node_file_map": node_file_map,
            "last_modified": current_mod_times,
        }
        write_yaml(cache_data, CACHE_FILE)

    return node_file_map


def find_nodes_in_ast(node_tree, filepath):
    node_file_map = {}
    for node in ast.walk(node_tree):
        if isinstance(node, ast.ClassDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name) and decorator.id == "node":
                    node_file_map[node.name] = filepath

    return node_file_map

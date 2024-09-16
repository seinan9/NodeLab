import ast
import os

def scan_directory_for_nodes(dir):

    node_file_map = {}

    for root, _, files in os.walk(dir):
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)

                with open(filepath, 'r') as file:
                    node_tree = ast.parse(file.read(), filename=filepath)

                    for node in ast.walk(node_tree):
                        if isinstance(node, ast.ClassDef):
                            for decorator in node.decorator_list:
                                if isinstance(decorator, ast.Name) and decorator.id == 'node':
                                    node_file_map[node.name] = filepath
    
    return node_file_map

from ._core._discovery import clear_cache, scan_directory_for_nodes

project_directory = None


def configure(directory):
    global project_directory
    project_directory = directory


def scan():
    nodes = scan_directory_for_nodes(project_directory)
    return nodes


def delete_cache():
    clear_cache()

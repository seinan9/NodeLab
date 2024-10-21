from ._core._discovery import scan_directory_for_nodes
from ._utils._configuration import CACHE_FILE, configure, project_directory
from ._utils._utils import delete_file


def configure(directory):
    return configure(directory)


def scan():
    nodes = scan_directory_for_nodes(project_directory)
    return nodes


def clear_cache():
    delete_file(CACHE_FILE)

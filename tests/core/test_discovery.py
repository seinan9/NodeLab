import os
import tempfile

import pytest

from nodelab._core import _discovery
from nodelab._utils._utils import write_yaml


@pytest.fixture
def temp_directory_with_nodes():
    temp_dir = tempfile.mkdtemp()

    files = {
        "file1.py": """
from nodelab.core.node import node

@node
class MyNode:
    pass
""",
        "file2.py": """
class NotANode:
    pass
""",
        "subdir/file3.py": """
from nodelab.core.node import node

@node
class AnotherNode:
    pass
""",
    }

    # Create files in the temporary directory
    for filename, content in files.items():
        file_path = os.path.join(temp_dir, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(content)

    expected = {
        "MyNode": os.path.join(temp_dir, "file1.py"),
        "AnotherNode": os.path.join(temp_dir, "subdir", "file3.py"),
    }

    yield temp_dir, expected

    # Clean up the temporary directory
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_dir)


def test_scan_directory_for_nodes_no_cache(temp_directory_with_nodes):
    temp_dir, expected = temp_directory_with_nodes
    result = _discovery.scan_directory_for_nodes(temp_dir)
    assert result == expected


def create_cache(cache_file, node_file_map, last_modified):
    cache_data = {"node_file_map": node_file_map, "last_modified": last_modified}
    write_yaml(cache_data, cache_file)


def test_scan_directory_for_nodes_valid_cache(temp_directory_with_nodes):
    temp_dir, expected = temp_directory_with_nodes
    for file in []



def test_scan_directory_for_nodes_invalid_cache():
    pass


def test_find_nodes_in_ast():
    pass

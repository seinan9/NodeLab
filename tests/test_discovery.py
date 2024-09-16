import os
import shutil
import sys
import tempfile

import pytest

from nodelab.core.discovery import scan_directory_for_nodes

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


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

    yield temp_dir

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)


def test_scan_directory_for_nodes(temp_directory_with_nodes):
    """
    Tests the scan_directory_for_nodes function.
    """
    result = scan_directory_for_nodes(temp_directory_with_nodes)

    expected = {
        "MyNode": os.path.join(temp_directory_with_nodes, "file1.py"),
        "AnotherNode": os.path.join(temp_directory_with_nodes, "subdir", "file3.py"),
    }

    assert result == expected

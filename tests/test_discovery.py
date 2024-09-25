import os
import shutil
import sys
import tempfile

import pytest

from nodelab.core.discovery import (
    CACHE_FILE,
    load_cache,
    save_cache,
    scan_directory_for_nodes,
)


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


@pytest.fixture
def setup_cache():
    """Fixture to set up and clean up cache before and after tests."""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    yield
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)


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


def test_load_cache_empty(setup_cache):
    """Test loading an empty cache."""
    cache = load_cache()
    assert cache == {}


def test_save_cache(setup_cache):
    """Test saving data to cache."""
    test_data = {"node_file_map": {"TestNode": "test_file.py"}, "last_modified": {}}
    save_cache(test_data)
    cache = load_cache()
    assert cache == test_data


def test_cache_update(temp_directory_with_nodes, setup_cache):
    """
    Test that the cache updates when files are modified.
    """
    # Initial scan to populate cache
    scan_directory_for_nodes(temp_directory_with_nodes)

    # Modify a file
    with open(os.path.join(temp_directory_with_nodes, "file1.py"), "a") as file:
        file.write(
            """
@node
class AdditionalNode:
    pass
"""
        )

    # Scan again and check that cache is updated
    result = scan_directory_for_nodes(temp_directory_with_nodes)
    assert "AdditionalNode" in result
    assert result["AdditionalNode"] == os.path.join(
        temp_directory_with_nodes, "file1.py"
    )

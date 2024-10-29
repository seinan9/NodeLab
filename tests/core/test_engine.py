import importlib.util
import os
import tempfile

import pytest

from nodelab._core import _discovery, _engine


def test_get_file_to_import_exact_match():
    # Example workflow with exact match
    workflow = {"NodeA": {"param1": 10}, "NodeB": {"param1": 20}}

    # Example node_file_map with exact nodes
    node_file_map = {"NodeA": "/path/to/node_a.py", "NodeB": "/path/to/node_b.py"}

    expected_files = {"/path/to/node_a.py": ["NodeA"], "/path/to/node_b.py": ["NodeB"]}

    result = _engine.get_file_to_import(workflow, node_file_map)

    # Assert that the result contains the expected files
    assert result == expected_files


def create_temp_file_with_name(file_name, content):
    temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
    with open(temp_file_path, "w") as temp_file:
        temp_file.write(content)
    return temp_file_path


# TODO: Fix test
def test_bulk_import_files_single_file():

    file_name = "sample_module.py"
    content = """
class SampleNode:
    def run(self):
        return "Hello from SampleNode!"
"""

    temp_file_path = create_temp_file_with_name(file_name, content)

    files_to_import = {temp_file_path: ["SampleNode"]}

    _engine.bulk_import_files(files_to_import)

    assert "SampleNode" in vars(_engine)

    os.remove(temp_file_path)


class MockNode:
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def run(self):
        return f"Processed with {self.param1} and {self.param2}"


def test_execute_workflow_basic():
    vars(_engine)["MockNode"] = MockNode
    workflow = {"MockNode": {"param1": "value1", "param2": "value2"}}
    results = _engine.execute_workflow(workflow)
    assert results["MockNode"] == "Processed with value1 and value2"

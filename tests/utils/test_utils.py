import os
import tempfile

import pytest
import yaml

from nodelab._utils import _utils


@pytest.fixture
def sample_data():
    yield {"node": "MyNode", "params": {"learning_rate": 0.01}}


@pytest.fixture
def temp_yaml_file(sample_data):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".yaml")
    with open(temp_file.name, "w") as file:
        yaml.dump(sample_data, file)
    temp_file.close()

    yield temp_file.name

    os.remove(temp_file.name)


def test_load_yaml(sample_data, temp_yaml_file):
    workflow = _utils.read_yaml(temp_yaml_file)
    assert sample_data == workflow


@pytest.fixture
def temp_yaml_path():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".yaml")
    temp_file.close()

    yield temp_file.name

    os.remove(temp_file.name)


def test_write_yaml(sample_data, temp_yaml_path):
    _utils.write_yaml(sample_data, temp_yaml_path)
    with open(temp_yaml_path, "r") as file:
        loaded_data = yaml.safe_load(file)
    assert sample_data == loaded_data


@pytest.fixture
def temp_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()

    yield temp_file.name


def test_delete_file(temp_file):
    _utils.delete_file(temp_file)
    assert os.path.exists(temp_file) is False


def test_get_file_mod_time(temp_file):
    file_mod_time = os.path.getmtime(temp_file)
    assert file_mod_time == _utils.get_file_mod_time(temp_file)

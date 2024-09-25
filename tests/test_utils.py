import os
import tempfile

import pytest
import yaml

from nodelab.utils import utils


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

    workflow = utils.read_yaml(temp_yaml_file)

    assert sample_data == workflow


@pytest.fixture
def temp_yaml_path():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".yaml")
    temp_file.close()
    yield temp_file.name
    os.remove(temp_file.name)


def test_write_yaml(sample_data, temp_yaml_path):
    utils.write_yaml(sample_data, temp_yaml_path)

    with open(temp_yaml_path, "r") as file:
        loaded_data = yaml.safe_load(file)

    assert sample_data == loaded_data

from nodelab._utils import _configuration


def test_configure():
    project_directory = "/path/to/directory"
    _configuration.configure(project_directory)
    assert project_directory == _configuration.project_directory

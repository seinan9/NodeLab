import os

DEFAULT_PROJECT_DIRECTORY = os.getcwd()
CACHE_FILE = "cache.yaml"

project_directory = DEFAULT_PROJECT_DIRECTORY


def configure(project_dir):
    global project_directory
    project_directory = project_dir

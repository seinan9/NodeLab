from setuptools import setup

setup(
    name="nodelab",
    version="1.0.0",
    py_modules=["nodelab"],
    install_requires=["pyyaml"],
    entry_points={
        "console_scripts": ["nodelab = nodelab.main:main"],
    },
)

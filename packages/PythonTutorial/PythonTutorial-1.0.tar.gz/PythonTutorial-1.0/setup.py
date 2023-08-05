import setuptools
from pathlib import Path


setuptools.setup(
    name="PythonTutorial",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(include=["TestPackage"])
)

# Install setuptools wheel twine => pip install setuptools wheel twine
# In Folder Of Project Create setup.py file
# Write Code

"""
setuptools.setup(
    name="<project-name>",
    version=1.0,
    long_description="<description>"
)

"""

# Add dist folder => python setup.py sdist bdist_wheel
# Upload Files => twine upload dist/*
# Enter UserName And Password

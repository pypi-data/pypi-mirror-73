import os
from os import path
from setuptools import find_packages, setup

project = "hub_dataflow"
version = "0.9.1"

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

with open(os.path.join(this_directory, "requirements.txt"), "r") as f:
    requirements = f.readlines()

setup(
    name=project,
    version=version,
    description="Snark Hub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Snark AI Inc.",
    author_email="support@snark.ai",
    url="https://github.com/snarkai/dataflow",
    packages=find_packages(include=["dataflow.cloud*", "dataflow.collections*", "dataflow.creds*", "dataflow.dataset_generators"], exclude=["dataflow.dataset_generators.intelinair*", "dataflow.dataset_generators.tests*"]),
    py_modules=[
        "dataflow.config",
        "dataflow.hub_api",
        "dataflow.logger",
        "dataflow.utils",
    ],
    include_package_data=True,
    zip_safe=False,
    keywords="snark-hub",
    python_requires=">=3",
    install_requires=requirements,
    dependency_links=[],
    entry_points={},
)

from setuptools import setup
import os
import re

project_name = "TearDrop"
version_file = os.environ["VERSION_FILE"]


def long_description():
    with open('README.md') as fp:
        return fp.read()


def get_requirements():
    with open("requirements.txt") as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


def get_metadata():
    with open(version_file) as file:
        file_content = file.read()

    token_pattern = re.compile(r"^__(?P<key>\w+)?__\s*=\s*(?P<quote>(?:'{3}|\"{3}|'|\"))(?P<value>.*?)(?P=quote)", re.M)

    groups = {}

    for match in token_pattern.finditer(file_content):
        group = match.groupdict()
        groups[group["key"]] = group["value"]

    return groups


metadata = get_metadata()

setup(
    name=project_name,
    version=metadata['version'],
    description="Python algorithms used to perform machine learning.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="Dec0Ded",
    author_email="4323565-dec0ded@users.noreply.gitlab.com",
    license="LGPL-3.0-ONLY",
    url="https://gitlab.com/dec0ded/teardrop",
    packages=['teardrop'],
    python_requires="> 3.7.4",
    install_requires=get_requirements(),
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
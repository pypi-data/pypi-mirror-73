from setuptools import setup, find_packages
import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    'mahotas',
    'matplotlib',
    'numpy',
    'scikit-learn'
]

setup(
    name="segutils",
    version=get_version(os.path.join('segutils', '__init__.py')),
    author="Guy Azran",
    author_email="guyazran@gmail.com",
    description="Common utilities for image processing, segmentation, and detection",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/tacos-galore/segutils",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
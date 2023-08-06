from setuptools import setup, find_packages

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
    version="0.0.5",
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
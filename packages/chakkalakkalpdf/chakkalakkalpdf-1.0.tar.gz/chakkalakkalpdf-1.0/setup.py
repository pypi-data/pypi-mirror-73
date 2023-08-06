import setuptools
from pathlib import Path

setuptools.setup(
    name="chakkalakkalpdf",
    version=1.0,
    long_desciption=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)

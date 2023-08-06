import setuptools
from pathlib import Path

setuptools.setup(
    name="ponnappanpdf",
    version=2.0,
    long_desription=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)

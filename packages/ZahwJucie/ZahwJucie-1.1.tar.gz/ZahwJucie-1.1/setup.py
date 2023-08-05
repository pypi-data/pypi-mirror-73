import setuptools
import pathlib

setuptools.setup(
    name="ZahwJucie",
    version="1.1",
    long_description=pathlib.Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"]),
)

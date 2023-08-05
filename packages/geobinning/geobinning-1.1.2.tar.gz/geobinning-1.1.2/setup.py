import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="geobinning",
    version="1.1.2",
    description="A package to bin coordinate data in geojson shapes.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://kapastor.github.io/",
    author="Kyle Pastor",
    author_email="kyleanthonypastor@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["geobinning"],
    include_package_data=True,
    install_requires=["matplotlib"],
    entry_points={
    },
)

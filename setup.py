"""Setup for Terraplanfeed."""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="terraplanfeed",
    version="0.1.1",
    description="Parse Terraform plan in json format and give feedback.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bcochofel/terraplanfeed",
    author="Bruno Cochofel",
    author_email="bruno.cochofel@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["terraplanfeed", "Python", "terraform", "terraform plan"],
    package_dir={"terraplanfeed": "terraplanfeed"},
    packages=find_packages(where="terraplanfeed"),
    python_requires=">=3.6, <4",
    install_requires=["Click", "Black"],
    entry_points={"console_scripts": ["terraplanfeed=terraplanfeed.main:main"]},
)

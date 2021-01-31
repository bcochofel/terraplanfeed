"""Setup for Terraplanfeed."""

from setuptools import setup, find_packages
import pathlib
import terraplanfeed

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="terraplanfeed",
    version=terraplanfeed.__version__,
    description="Parse Terraform plan in json format and give feedback.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bcochofel/terraplanfeed",
    author="Bruno Cochofel",
    author_email="bruno.cochofel@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Build Tools",
    ],
    keywords=["terraplanfeed", "Python", "terraform", "terraform plan"],
    package_dir={"terraplanfeed": "terraplanfeed"},
    packages=find_packages(where="terraplanfeed"),
    python_requires=">=3.7, <4",
    install_requires=["Click", "Requests"],
    entry_points={
        "console_scripts": ["terraplanfeed=terraplanfeed.__main__:main"]
    },
)

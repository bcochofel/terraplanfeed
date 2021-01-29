# terraplanfeed

[![pre-commit badge][pre-commit-badge]][pre-commit] [![Conventional commits badge][conventional-commits-badge]][conventional-commits] [![Keep a Changelog v1.1.0 badge][keep-a-changelog-badge]][keep-a-changelog] [![MIT License Badge][license-badge]][license]

This tool parses Terraform plan files in JSON format and gives feedback about the changes.

# Description

This tool aims to parse Terraform plan files (in JSON format) and gives feedback to several types of outputs.

Outputs can be:
* stdout
* Github pull request comment
* Azure DevOps pull request comment

To create the Terraform plan file:

```bash
terraform init
terraform plan -out=plan.out
terraform show -no-color -json plan.out > plan.json
```

# Run and test locally

```bash
python3 -m pip install --editable .
```

# pre-commit hooks

Read the [pre-commit hooks](docs/pre-commit-hooks.md) document for more info.

# git-chglog

Read the [git-chglog](docs/git-chlog.md) document for more info.

# References

* [Making a Python package](https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html)
* [Documenting Python code](https://realpython.com/documenting-python-code/)
* [Python Docstrings Google](https://google.github.io/styleguide/pyguide.html)
* [Python Click](https://click.palletsprojects.com)
* [Terraform JSON output format](https://www.terraform.io/docs/internals/json-format.html)

[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[conventional-commits-badge]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-green.svg
[conventional-commits]: https://conventionalcommits.org
[keep-a-changelog-badge]: https://img.shields.io/badge/changelog-Keep%20a%20Changelog%20v1.1.0-%23E05735
[keep-a-changelog]: https://keepachangelog.com/en/1.0.0/
[license]: ./LICENSE
[license-badge]: https://img.shields.io/badge/license-MIT-green.svg
[changelog]: ./CHANGELOG.md
[changelog-badge]: https://img.shields.io/badge/changelog-Keep%20a%20Changelog%20v1.1.0-%23E05735

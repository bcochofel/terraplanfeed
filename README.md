# terraplanfeed

[![pre-commit badge][pre-commit-badge]][pre-commit] [![Conventional commits badge][conventional-commits-badge]][conventional-commits] [![Keep a Changelog v1.1.0 badge][keep-a-changelog-badge]][keep-a-changelog] [![MIT License Badge][license-badge]][license]

This tool parses Terraform plan files in JSON format and gives feedback about the changes or state drift

## Description

This tool aims to parse Terraform plan files (in JSON format) and gives feedback to several types of outputs.

Outputs can be:

* stdout: stdout
* azuredevops: Azure DevOps pull request comment
* github: Github pull request comment (not yet implemented)

To create the Terraform plan file:

```bash
terraform init
terraform plan -out=plan.out
terraform show -no-color -json plan.out > plan.json
```

## Usage

To write to stdout you just need to pass a JSON file:

```bash
❯ terraplanfeed ../tfplan/example.json

Summary of changes:
===================

(✨): <known after apply> (module.failover_rg.azurerm_resource_group.rg)
(✨): <known after apply> (module.failover_rg.module.naming.random_string.first_letter)
(✨): <known after apply> (module.failover_rg.module.naming.random_string.main)
(✨): <known after apply> (module.rg.azurerm_resource_group.rg)
(✨): <known after apply> (module.rg.module.naming.random_string.first_letter)
(✨): <known after apply> (module.rg.module.naming.random_string.main)
(✨): <known after apply> (module.sql.azurerm_storage_account.audit1)
(✨): <known after apply> (module.sql.azurerm_storage_account.audit2[0])
(✨): <known after apply> (module.sql.module.naming.random_string.first_letter)
(✨): <known after apply> (module.sql.module.naming.random_string.main)
(✨): <known after apply> (module.sql.module.naming_failover.random_string.first_letter)
(✨): <known after apply> (module.sql.module.naming_failover.random_string.main)

```

To monitor state drift rather than changes

```bash
❯ terraplanfeed --drift ../tfplan/example.json
```

To enable detailed exit codes (0 - no changes, 1 - errored, 2 - changes found)

```bash
❯ terraplanfeed --detailed-exitcode ../tfplan/example.jso
```

To output to Azure DevOps

```bash
❯ terraplanfeed ../tfplan/example.json -o azuredevops

```

To use this on Azure DevOps you need the following environment variables:

* SYSTEM_TEAMFOUNDATIONSERVERURI
* SYSTEM_TEAMPROJECT
* BUILD_REPOSITORY_ID
* SYSTEM_PULLREQUEST_PULLREQUESTID
* SYSTEM_ACCESSTOKEN

these environment variables are present when you run Azure DevOps pipelines.

**Note:** The `SYSTEM_PULLREQUEST_PULLREQUESTID` is only present when you run
pipeline in a pull request.

If any of these environment variables are not present, output defaults to stdout

## Run and test locally

```bash
python3 -m pip install --editable .
```

## Build and upload to PyPI

To build and upload to Test PyPI repository:

```bash
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
python3 -m pip install --user --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```

To upload to PyPI repository:

```bash
python3 -m twine upload dist/*
```

## pre-commit hooks

Read the [pre-commit hooks](docs/pre-commit-hooks.md) document for more info.

## git-chglog

Read the [git-chglog](docs/git-chlog.md) document for more info.

## References

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

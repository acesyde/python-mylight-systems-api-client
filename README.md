# Python: MyLight Systems

[![GitHub Release][releases-shield]][releases]
[![Python Versions][python-versions-shield]][pypi]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE.md)

[![Build Status][build-shield]][build]
[![Code Coverage][codecov-shield]][codecov]

Asynchronous Python client for MyLight Systems.

## About

This package allows you to fetch data from MyLight Systems.

This source code is based on the [airgradient-python](https://github.com/acesyde/python-mylight-systems-api-client) package.

## Installation

```bash
pip install mylightsystems-api-client
```

## Changelog & Releases

This repository keeps a change log using [GitHub's releases][releases]
functionality. The format of the log is based on
[Keep a Changelog][keepchangelog].

Releases are based on [Semantic Versioning][semver], and use the format
of `MAJOR.MINOR.PATCH`. In a nutshell, the version will be incremented
based on the following:

-   `MAJOR`: Incompatible or major changes.
-   `MINOR`: Backwards-compatible new features and enhancements.
-   `PATCH`: Backwards-compatible bugfixes and package updates.

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](.github/CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

This Python project is fully managed using the [Poetry][poetry] dependency manager. But also relies on the use of NodeJS for certain checks during development.

You need at least:

-   Python 3.11+
-   [Poetry][poetry-install]

To install all packages, including all development requirements:

```bash
poetry install
```

As this repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. You can run all checks and tests
manually, using the following command:

```bash
poetry run pre-commit run --all-files
```

To run just the Python tests:

```bash
poetry run pytest
```

## Authors & contributors

The content is by [Pierre-Emmanuel Mercier][acesyde].

For a full list of all authors and contributors,
check [the contributor's page][contributors].

[build-shield]: https://github.com/acesyde/python-mylight-systems-api-client/actions/workflows/tests.yaml/badge.svg
[build]: https://github.com/acesyde/python-mylight-systems-api-client/actions
[codecov-shield]: https://codecov.io/gh/acesyde/python-mylight-systems-api-client/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/acesyde/python-mylight-systems-api-client
[commits-shield]: https://img.shields.io/github/commit-activity/y/acesyde/python-mylight-systems-api-client.svg
[commits]: https://github.com/acesyde/python-mylight-systems-api-client/commits/master
[contributors]: https://github.com/acesyde/python-mylight-systems-api-client/graphs/contributors
[acesyde]: https://github.com/acesyde
[keepchangelog]: http://keepachangelog.com/en/1.0.0/
[license-shield]: https://img.shields.io/github/license/acesyde/python-mylight-systems-api-client.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2024.svg
[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com/
[project-stage-shield]: https://img.shields.io/badge/project%20stage-stable-green.svg
[python-versions-shield]: https://img.shields.io/pypi/pyversions/mylightsystems-api-client
[releases-shield]: https://img.shields.io/github/release/acesyde/python-mylight-systems-api-client.svg
[releases]: https://github.com/acesyde/python-mylight-systems-api-client/releases
[semver]: http://semver.org/spec/v2.0.0.html
[pypi]: https://pypi.org/project/mylightsystems-api-client/

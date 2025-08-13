# TEMPLATE

TODO

This project contains all the boilerplate for initialising a new Python project
on github. It includes:

- Package management with pixi
- Automated tests with pytest
- Enforced static code linting and validation with ruff, mypy, and more
- git pre-commit linting hooks with lefthook
- Sphinx documentation framework
- Integration with github workflows, codecov.io, and readthedocs
- CI tests against multiple versions of Python, multiple OSs (Linux, Windows,
  and MacOS) and architectures (x86 and ARM).
- CI tests against nightly pre-releases of dependencies
- Explicit tests for minimum supported dependencies versions
- Stress tests for free-threading (noGIL)
- Automated versioning with setuptools-scm
- Step-by-step guide to release to pypi and conda-forge

Full documentation at http://python-project-template.readthedocs.io/

## Usage

1. Copy all the files into your project (don't forget the hidden files!)
2. Replace all TEMPLATE tags with your project name (also in file and directory
   names)
3. Search for all TODO tags and replace them as needed
4. Integrate with readthedocs, Travis, and AppVeyor and obtain successful builds
5. Replace the TEMPLATE directory with your own python files and tests.

## Credits

Forked from https://github.com/pydata/xarray

## Badges

TODO replace crusaderky/python_project_template with {github user}/{project
name}. You may want to move this section to the top of the page!

[![doc-badge](https://github.com/crusaderky/python_project_template/actions/workflows/docs.yml/badge.svg)](https://github.com/crusaderky/python_project_template/actions)
[![lint-badge](https://github.com/crusaderky/python_project_template/actions/workflows/lint.yml/badge.svg)](https://github.com/crusaderky/python_project_template/actions)
[![wheels-badge](https://github.com/crusaderky/python_project_template/actions/workflows/wheels.yml/badge.svg)](https://github.com/crusaderky/python_project_template/actions)
[![pytest-badge](https://github.com/crusaderky/python_project_template/actions/workflows/pytest.yml/badge.svg)](https://github.com/crusaderky/python_project_template/actions)
[![codecov-badge](https://codecov.io/gh/crusaderky/python_project_template/branch/main/graph/badge.svg)](https://codecov.io/gh/crusaderky/python_project_template/branch/main)

## Requirements

- Python 3.10 or higher *
- Node.js 16.0 or higher

<small>
  django-gesha supports Python >= 3.8, but type checking requires or Python >= 3.10.
</small>

## Set up test environment

### Get source code

Clone Git repository:
```sh
git clone https://github.com/ely-as/django-gesha
```

Enter directory;
```sh
cd django-gesha
```

### Python virtual environment

Create a virtual environment:
```sh
python -m venv venv
```

Activate:
```sh
source venv/bin/activate
```

Upgrade pip:
```sh
pip install --upgrade pip
```

### Install editable django-gesha

```sh
pip install -e ."[doc,test]"
```

### Node.js environment

```sh
npm install
```

## Develop

### Format Python files

Run the `format` tox environment to apply formatting:
```sh
tox -e format
```

### Type-hinting Python code

Include the following import in Python modules:

```py
from __future__ import annotations
```

This adds support for the following PEPs in the corresponding Python versions:

- [PEP 563](https://peps.python.org/pep-0563/) – Postponed Evaluation of Annotations **(<=3.9)**
- [PEP 585](https://peps.python.org/pep-0585/) – Type Hinting Generics In Standard Collections **(==3.8)**
- [PEP 604](https://peps.python.org/pep-0604/) – Allow writing union types as `X | Y` **(<=3.9)**

In addition, when declaring custom types use the
[`TYPE_CHECKING` constant](https://peps.python.org/pep-0484/#runtime-or-type-checking)
to prevent execution during runtime (otherwise this may cause issues when running
Python >= 3.9).

### Build JavaScript assets

Once-off build:
```sh
gulp
```

Watch files and build when changes occur:
```sh
gulp watch
```

## Test

### Lint and type-check Python code

```sh
tox -e lint-type
```

### Lint TypeScript code

```sh
npm run lint
```

### Run Python tests

```sh
tox -e test
```

### Run JavaScript tests

```sh
npm test
```

## Documentation

Preview changes to documentation:
```sh
mkdocs serve
```

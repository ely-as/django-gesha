## Dependencies

- [Python](https://www.python.org/) 3.10 or higher[^1]
- [Node.js](https://nodejs.org/) 16.0 or higher
- [tox](https://tox.wiki/en/latest/installation.html) 4.0 or higher

[^1]: **django-gesha** supports Python 3.8 or higher, but type-checking requires or Python 3.10 or higher.

## Create test environment

### Get source code

``` console
$ git clone https://github.com/ely-as/django-gesha # (1)!
$ cd django-gesha
```

1. If you have forked **django-gesha**, use the URL of your fork here instead.

### Create Python environment

Create a [virtual environment](https://docs.python.org/3/library/venv.html),
for example, in a directory named `venv`:

``` console
$ python -m venv venv
```

Activate the virtual environment:

=== "bash/zsh"
    ``` console
    $ source venv/bin/activate
    ```

=== "fish"
    ``` fish
    $ source venv/bin/activate.fish
    ```

=== "csh/tcsh"
    ``` tcshcon
    $ source venv/bin/activate.csh
    ```

=== "Windows cmd.exe"
    ``` doscon
    C:\> venv\Scripts\activate.bat
    ```

=== "Windows PowerShell"
    ``` pwsh-session
    PS C:\> venv\Scripts\Activate.ps1
    ```

Upgrade pip:

``` console
$ pip install --upgrade pip
```

Install editable **django-gesha** to Python environment:

``` console
$ pip install -e ."[doc,test]"
```

### Create Node.js environment

``` console
$ npm install
```

## Develop

### Python

#### Apply formatting

Run the `format` tox environment to apply formatting using black and isort rules:
``` console
$ tox -e format
```

#### Type-hinting

Include the following import at the top of Python modules to enable the latest typing
features for all Python versions supported by **django-gesha**:

``` py linenums="1"
from __future__ import annotations
```

??? info "Typing features enabled by future import"

    The following features are available by default in Python 3.10, but the future
    import is required to enable them in previous Python versions.

    | PEP                                      | Title                                         | Python   |
    | ---------------------------------------- | --------------------------------------------- | -------- |
    | [563](https://peps.python.org/pep-0563/) | Postponed Evaluation of Annotations           | 3.8, 3.9 |
    | [585](https://peps.python.org/pep-0585/) | Type Hinting Generics In Standard Collections | 3.8      |
    | [604](https://peps.python.org/pep-0604/) | Allow writing union types as `X | Y`          | 3.8, 3.9 |

??? tip "Declaring custom types"

    When declaring custom types use the
    [`TYPE_CHECKING` constant](https://peps.python.org/pep-0484/#runtime-or-type-checking)
    to prevent execution during runtime:

    ``` py title="Example using TYPE_CHECKING constant" linenums="1"
    import typing

    if typing.TYPE_CHECKING:
        CoordinateType = dict[str, float]
    ```

    Otherwise, declarations like this may cause runtime errors in Python 3.9 or lower.

### TypeScript

#### Build assets

``` console
$ gulp
```

To watch source files and continuously build when changes occur:
``` console
$ gulp watch
```

## Test

### Python

#### Lint and type-check

``` console
$ tox -e lint-type
```

#### Run tests

``` console
$ tox -e test
```

To run tests for all supported Django versions for a specific Python version:

``` console
$ tox -m py3.8 # (1)!
```

1.  See the `labels` section in
    [`tox.ini`](https://github.com/ely-as/django-gesha/blob/main/tox.ini) for available
    Python labels.

#### Run test project

``` console
$ cd test_project
$ uvicorn fake.asgi:application --reload
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### TypeScript

#### Lint

``` console
$ npm run lint
```

#### Run tests

``` console
$ npm test
```

??? note "Generating `test.html` fixture for TypeScript tests"

    The fixture `js_tests/test.html` is generated from the test Django project located
    in `test_project`. If the test project has been modified the fixture can be
    regenerated using the following command:

    === "POSIX"
        ``` console
        $ python test_project/manage.py printtestpage --pretty -o js_tests/test.html
        ```

    === "Windows"
        ``` doscon
        C:\> python test_project\manage.py printtestpage --pretty -o js_tests\test.html
        ```

## Documentation

Preview changes to documentation by running the builtin development server:

``` console
$ mkdocs serve
```

## Pull request

[Make a pull request](https://github.com/ely-as/django-gesha/pulls).

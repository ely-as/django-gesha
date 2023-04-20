## Requirements

- Python 3.8 or higher
- Node.js 16.0 or higher

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

# SCAR

Supply Chain Adaptation and Resilience

# Setup

Make sure you have Python 3.11.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).

## Installation

```
pip install -e ./scar
```

## Basic Usage
```py
import scar

# TODO: Do something here
```

## Getting Started

`scar` contains ...

## Interactive Example

```py
>>> import scar
```

## Development

To avoid extra development overhead, we expect all developers to use a unix based environment (Linux or Mac). If you use Windows, please use WSL2.

For development, we test using Docker so we can lock system deps and swap out python versions easily. However, you can also use a virtual environment if you prefer. We provide a test script and a prettify script to help with development.

## Making Changes

1) Fork the repo and clone it locally.
2) Make your modifications.
3) Use Docker or a virtual environment to run tests and make sure they pass.
4) Prettify your code.
5) **DO NOT GENERATE DOCS**.
    - We will generate the docs and update the version number when we are ready to release a new version.
6) Only commit relevant changes and add clear commit messages.
    - Atomic commits are preferred.
7) Submit a pull request.

## Docker

Make sure Docker is installed and running.

- Create a docker container and drop into a shell
    - `./run.sh`
- Run all tests (see ./utils/test.sh)
    - `./run.sh test`
- Prettify the code (see ./utils/prettify.sh)
    - `./run.sh prettify`

- Note: You can and should modify the `Dockerfile` to test different python versions.

## Virtual Environment

- Create a virtual environment
    - `python3.XX -m venv venv`
        - Replace `3.XX` with your python version (3.11 or higher)
- Activate the virtual environment
    - `source venv/bin/activate`
- Install the development requirements
    - `pip install -r requirements/dev.txt`
- Run Tests
    - `./utils/test.sh`
- Prettify Code
    - `./utils/prettify.sh`
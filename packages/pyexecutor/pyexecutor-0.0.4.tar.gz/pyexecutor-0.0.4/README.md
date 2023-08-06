# PyExecutor - A light-weight command executor to run commands and return stdout and stderr.

[![PyPI version](https://badge.fury.io/py/pyexecutor.svg)](https://badge.fury.io/py/pyexecutor)
[![PyPI license](https://img.shields.io/pypi/l/pyexecutor.svg)](https://pypi.python.org/pypi/pyexecutor/)
[![Downloads](https://pepy.tech/badge/pyexecutor)](https://pepy.tech/project/pyexecutor)
[![PyPI Downloads](https://img.shields.io/pypi/dm/pyexecutor)](https://badge.fury.io/py/pyexecutor)

> Work with both Linux and Windows, compatible with executable files like `executor`, `executor.exe` and `executor.bat`.

## Requirement

Python >= 3

> Compatible with Python 3.4 3.5 3.6 3.7 3.8

## Installation

Install with `pip`

`pip install pyexecutor`

## QuickStart

Import and run with python

```python
from pyexecutor import Executor

helm = Executor('helm')

version = helm.run('version --short')

print(version)

"""
v3.1.2+gd878d4d
"""
```

## Usage Examples

### Run with executor

Get command execution result in string

```python
from pyexecutor import Executor

kubectl = Executor('kubectl')

# Run 'kubectl version --client --short'
result = kubectl.run('version --client --short')

# Set trailer string of executor
kubectl.set_trailer('-o=json')

# Run 'kubectl version --client --short -o=json'
result = kubectl.run('version --client --short')

# Get command output in JSON object (<type 'dict'>), exception will be raised if result string is not JSON serializable.
result = kubectl.run('version --client --short', json_output=True)
```

### Run with commander

```python
from pyexecutor import Commander

commander = Commander()

# Run 'kubectl version --short --client'
result = commander.run('kubectl version --short --client')

# Get command output in string.
result.output()

# Get command output in JSON object (<type 'dict'>), exception will be raised if result string is not JSON serializable.
result.json()

# Get command error in string.
result.error()

# Get command warning in string.
result.warning()

# Error produced in command execution.
result.has_error()

# Warning produced in command execution.
result.has_warning()

# No errors or warnings produced in command execution.
result.ok()
```

### Logging

Loging in executor

```python
import logging
from pyexecutor import Executor

kubectl = Executor('kubectl', logger=logging.getLogger())
```

Logging in commander

```python
import logging
from pyexecutor import Commander

kubectl = Commander('kubectl', logger=logging.getLogger())
```
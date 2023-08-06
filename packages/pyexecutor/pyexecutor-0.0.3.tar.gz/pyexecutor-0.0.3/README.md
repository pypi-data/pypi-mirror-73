# Command executor for Python

Executor example:

```python
from pyexecutor import Executor

helm = Executor('helm')

version = helm.run('version')

print(version)
```

Commander example:

```python
from pyexecutor import Commander

commander = Commander()

version = commander.run('helm version').result()

print(version)
```
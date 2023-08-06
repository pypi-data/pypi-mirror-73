"""
Should be raised when exceptions / errors occurred during run commands with Executor
"""
class ExecutorException(Exception):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def __str__(self):
        return "Executor exception {}".format(self._message)

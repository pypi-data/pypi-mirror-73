"""
Should be raised when exceptions / errors occurred during run commands with Commander
"""
class CommanderException(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return "Commander exception {}".format(self._message)

from exceptions import ExecutorException
from pyexecutor import Commander


class Executor():

    _commander = None
    _executor = None
    _trailer = ''

    def __init__(self, executable, logger=None):
        self._commander = Commander(logger=logger)
        self._set_executor(executable)

    """
    Find proper executor
    """
    def _set_executor(self, executable):
        for executor in [executable, '{}.exe'.format(executable), '{}.bat'.format(executable)]:
            self._commander.run(executor, True)

            if self._commander.ok():
                self._executor = executor
                break

        if self._executor is None:
            raise ExecutorException('Executable file {} not found!'.format(executable))

    """
    Set command trailer
    """
    def set_trailer(self, trailer):
        self._trailer = trailer

    """
    Run commands with commander
    """
    def _run(self, cmd):
        executable_cmd = '{} {} {}'.format(self._executor, cmd, self._trailer)
        self._commander.run(executable_cmd)

        if self._commander.has_error():
            raise ExecutorException(
                    '"{}" execution failed with error "{}"'.format(
                        executable_cmd,
                        self._commander.error()
                    )
                )

        return self._commander

    """
    Run commands with pretty outputs
    """
    def run(self, cmd, json_output=False):
        if json_output:
            return self._run(cmd).json()

        return self._run(cmd).output()

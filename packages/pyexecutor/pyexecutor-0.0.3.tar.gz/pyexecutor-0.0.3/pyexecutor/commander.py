import json
import subprocess

from exceptions import CommanderException


class Commander():
    _output = None
    _error = None
    _warning = None
    _logger = None

    def __init__(self, logger=None):
        super().__init__()
        self._set_logger(logger)

    """
    Run command with sub process
    """
    def run(self, cmd, supress_error=False):
        self._log_info('Start running command {} with supress error {}'.format(cmd, supress_error))

        try:
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
            self._process(stdout, stderr)
            return self
        except Exception as e:
            self._error = str(e)
            if supress_error:
                return self
            raise e

    """
    Process the output of command execution
    """
    def _process(self, stdout, stderr):
        self._output = self._command_output(stdout)
        self._error = self._command_error(stderr)
        self._warning = self._command_warning(stderr)

        self._log_info('Finish running command with OUTPUT\n {}\n WARNING\n {}\n ERROR\n {}\n'.format(self._output, self._warning, self._error))

    """
    Get command output in string
    """
    def _command_output(self, stdout):
        return self._string(stdout)

    """
    Get command error in string
    """
    def _command_error(self, stderr):
        if stderr.lower().find(b'error') == -1:
            return None

        return self._string(stderr)

    """
    Get command warning in string
    """
    def _command_warning(self, stderr):
        if stderr.lower().find(b'warning') == -1:
            return None

        return self._string(stderr)

    """
    Convert binary string to string
    """
    def _string(self, bstring, charset='utf8'):
        return bstring.decode(charset)

    """
    Get output in string
    """
    def result(self):
        return self._output

    """
    Get output in JSON format
    """
    def json(self):
        try:
            return json.loads(self._output)
        except Exception as e:
            raise CommanderException('invalid JSON string {}'.format(self._output))

    """
    If error occurred
    """
    def error(self):
        return bool(self._error)

    """
    If warning occurred
    """
    def warning(self):
        return bool(self._warning)

    """
    If no error or no warning occurred
    """
    def noerror(self):
        return not (self.error() and self.warning())

    """
    Get error messages
    """
    def error_message(self):
        return self._error

    """
    Get warning messages
    """
    def warning_message(self):
        return self._warning

    """
    Print log info messages
    """
    def _log_info(self, message):
        if self._logger is not None:
            self._logger.info("COMMANDER: %s", message)

    """
    Print log error messages
    """
    def _log_error(self, message):
        if self._logger is not None:
            self._logger.error("COMMANDER: %s", message)

    """
    Print log warning messages
    """
    def _log_warning(self, message):
        if self._logger is not None:
            self._logger.warning("COMMANDER: %s", message)

    """
    Set the command logger
    """
    def _set_logger(self, logger):
        self._logger = logger
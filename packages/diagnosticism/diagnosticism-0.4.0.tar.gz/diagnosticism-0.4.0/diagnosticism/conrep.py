
from .program_name import get_program_name

import os
import sys

_STDERR_ISATTY = sys.stderr.isatty()
_OS_IS_POSIX = os.name.lower() == 'posix'

def _emit_to_cr_stm(message):

    sys.stderr.write(message)

def _add_eol_and_emit_to_cr_stm(message):

    _emit_to_cr_stm(message + "\n")

def _isatty():

    return _STDERR_ISATTY and _OS_IS_POSIX

def conrep(message, **kwargs):

    """DEPRECATED: use report()"""

    return report(message, **kwargs)

def report(message, show_program_name=True):

    """Emits the given message on the contingent report stream. If the optional argument show_program_name is given and is falsey, the program name will not prefix the message"""

    if show_program_name:

        pn = get_program_name()

        _emit_to_cr_stm(pn + ": " + str(message) + "\n")
    else:

        _add_eol_and_emit_to_cr_stm(message)

def abort(message, do_exit=True, show_program_name=True):

    """Emits the program prefix and the given message on the contingent report stream, and then terminates the process"""

    report(message, show_program_name=show_program_name)

    if do_exit:

        sys.exit(1)


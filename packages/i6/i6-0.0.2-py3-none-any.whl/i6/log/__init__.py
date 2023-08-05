from i6.util import util

import sys
import socket


class log():
    """
        Class for standardized logging tools.

        Example:
        ```
        i6.log('message for stdout').stdout()
        i6.log('message for stderr').stderr()

        i6.log('starts with newline', '\\n').stdout()

        # Output:
        [ 2020-06-18T23:34:01.520679Z ] - local - message for stdout
        [ 2020-06-18T23:34:01.520733Z ] - local - message for stderr

        [ 2020-06-18T23:34:01.520780Z ] - local - starts with newline
        ```
    """

    def __init__(self, message, first_char = ''):
        self.__message = f"{first_char}[ {util.now(True)} ] - {socket.gethostname()} - {message}"

    def stdout(self):
        """
            Log to stdout

            Example:
            ```
            i6.log('message for stdout').stdout()
            ```
        """

        print(self.__message)
    
    def stderr(self):
        """
            Log to stderr

            Example:
            ```
            i6.log('message for stderr').stderr()
            ```
        """

        print(self.__message, file=sys.stderr)

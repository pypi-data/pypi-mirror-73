import os
import subprocess


class shell():
    """
        Class for standardized operating system tools.

        Example:
        ```
        print(i6.shell.cwd())
        ```
    """

    def cwd():
        """
            Get Current Working Directory

            Example:
            ```
            print(i6.shell.cwd())
            ```
        """

        return os.getcwd()

    def exec(command):
        return subprocess.run(
            command,
            stdout=subprocess.PIPE,
        ).stdout.decode().replace('\n', '')

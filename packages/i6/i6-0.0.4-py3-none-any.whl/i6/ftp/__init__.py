from i6.shell import shell

import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers


class ftp():
    """
        FTP server class

        Example:
        ```
        i6.ftp().run()
        ```

        To use port 21 root premissions are required,
        else will fallback to use port 5021.
    """

    def __init__(self, port = None, bind = None, pwd = None, max_cons = None, max_cons_per_ip = None):
        if port is None:
            port = 21

        if bind is None:
            bind = '0.0.0.0'

        if pwd is None:
            pwd = shell.cwd()

        if max_cons is None:
            max_cons = 256

        if max_cons_per_ip is None:
            max_cons_per_ip = 5

        authorizer = pyftpdlib.authorizers.DummyAuthorizer()

        authorizer.add_anonymous(pwd)

        handler = pyftpdlib.handlers.FTPHandler
        handler.authorizer = authorizer

        handler.banner = ""

        try:
            self.__server = pyftpdlib.servers.FTPServer((bind, port), handler)
        except OSError:
            self.__server = pyftpdlib.servers.FTPServer((bind, 5021), handler)

        self.__server.max_cons = max_cons
        self.__server.max_cons_per_ip = max_cons_per_ip
    
    def run(self):
        """
            Run ftp server

            Example:
            ```
            i6.ftp().run()
            ```
        """

        self.__server.serve_forever()

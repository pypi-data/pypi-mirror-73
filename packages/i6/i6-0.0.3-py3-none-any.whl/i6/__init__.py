"""
    i6

    A standardized collection of python libs and tools.

    Example:
    ```
    import i6
    
    # Http request
    i6.http.get('EXAMPLE/api/endpoint/')

    # Attempt to use Dockerfile in cwd
    centos = i6.container().run()

    # Update container to git repo latest tag
    i6.git({
        'container': centos,
    }).update()

    # Start FTP server
    i6.ftp().run()

    # Connect to postgres database
    db = i6.db(
        info = False,
        debug = True,
        db_conn_string ='postgresql+psycopg2://user:password@host:5432/database'
    )
    ```

    :copyright: 2020 kruserr
    :license: MIT
"""

from i6.db import db
from i6.cli import cli
from i6.log import log
from i6.ftp import ftp
from i6.git import git
from i6.http import http
from i6.util import util
from i6.shell import shell
from i6.crypto import crypto
from i6.container import container

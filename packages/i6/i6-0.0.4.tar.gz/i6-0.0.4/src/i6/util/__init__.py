import os
import time
import datetime


class util():
    """
        Class for standardized utilities.

        Example:
        ```
        print(i6.util.now())
        i6.util.sleep(5)
        print(i6.util.now())
        ```
    """

    def check_val(obj, value, default):
        """
            If value is in dict return value, else use default

            Example:
            ```
            obj = {
                'first_name': 'john',
                'last_name': 'doe',
            }

            first_name = i6.util.check_val(obj, 'john', '')
            address = i6.util.check_val(obj, 'address', '')

            print(first_name, address)
            ```
        """

        try:
            return obj[value]
        except KeyError:
            return default

    def sleep(seconds):
        """
            Sleep for seconds

            Example:
            ```
            i6.util.sleep(5)
            ```
        """

        time.sleep(seconds)

    def now(format = False):
        """
            Get current UTC ISO timestamp

            Example:
            ```
            print(i6.util.now())
            ```
        """
        
        if format:
            return datetime.datetime.utcnow().strftime('%FT%T.%fZ')
        return datetime.datetime.utcnow()

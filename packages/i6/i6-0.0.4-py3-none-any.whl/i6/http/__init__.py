from i6.http.Result import Result

import urllib.request


class http():
    """
        Facade for urllib to work with JSON REST APIs.
        
        Example:
        ```
        result = i6.http.get('http://EXAMPLE/api/endpoint/')
        ```
    """

    def get(url, headers = None):
        """
            Example:
            ```
            result = i6.http.get('http://EXAMPLE/api/endpoint/')
            ```
        """

        if headers is not None:
            request = urllib.request.Request(url, headers=headers)
        else:
            request = urllib.request.Request(url)
        
        with urllib.request.urlopen(request) as response:
            return Result(response)

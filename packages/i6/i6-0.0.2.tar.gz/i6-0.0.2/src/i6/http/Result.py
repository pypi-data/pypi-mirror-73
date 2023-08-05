import json


class Result():
    """
        Result class to provide structured data as a result from a http request

        Example:
        ```
        print(i6.http.get('http://EXAMPLE').json)
        ```
    """

    __body = None
    __json = None

    def __init__(self, response):
        self.__body = response.read()

        try:
            self.__json = json.loads(self.__body)
        except json.decoder.JSONDecodeError:
            self.__json = dict()

    def body(self):
        """
            Raw binary data from request
        """

        return self.__body

    def json(self):
        """
            Json data from request, if empty request is not valid json
        """

        return self.__json

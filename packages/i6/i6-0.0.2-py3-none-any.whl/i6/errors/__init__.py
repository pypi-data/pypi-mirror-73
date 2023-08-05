"""
    Errors or exceptions for i6.

    Example:
    ```
    raise i6.error.ContainerIsNone()
    ```
"""

class APIError(Exception):
    """
        Base Exception for i6
    """

    def __init__(self, message = 'i6 API Error'):
        super().__init__(message)

class ContainerIsNone(APIError, ValueError):
    """
        Container is None exception
    """

    def __init__(self, message = 'container is None'):
        super().__init__(message)

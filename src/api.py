import json
import warnings
from src.exceptions import ConnectionError


class API:
    host: str
    _token: str
    _db_schema: json

    def __init__(self, host: str, token: str) -> None:
        """
        initialize object with host and token
        if host is using "http" then give a warning
        """
        self.host = host
        self._token = token

        # if host is using unsafe "http://" then give a warning
        if self.host.startswith("http://"):
            warnings.warn("HTTP is an unsafe protocol please consider using HTTPS")

        # check that api can connect to CRIPT with host and token
        try:
            # TODO send an http request to check connection with host and token
            pass
        except Exception:
            raise ConnectionError


if __name__ == "__main__":
    api = API("http://example.com", "123456789")

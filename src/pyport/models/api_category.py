from abc import ABC


class BaseResource(ABC):
    def __init__(self, client):
        self._client = client

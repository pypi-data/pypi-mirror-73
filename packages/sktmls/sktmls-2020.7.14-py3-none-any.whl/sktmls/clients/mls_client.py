import os
import base64

from typing import List
from enum import Enum


class MLSClientError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MLSENV(Enum):
    DEV = "dev"
    STG = "stg"
    PRD = "prd"

    @classmethod
    def list_items(cls) -> List["MLSENV"]:
        """
        List all supported environments
        """
        return [t for t in cls]

    @classmethod
    def list_values(cls) -> List[str]:
        """
        List all supported environment names
        """
        return [t.value for t in cls]


class MLSClient:
    def __init__(self, env: MLSENV = None, username: str = None, password: str = None):
        if env:
            assert env in MLSENV.list_items(), "Invalid environment."
            self.__env = env
        elif os.environ.get("MLS_ENV"):
            self.__env = os.environ["MLS_ENV"]
        else:
            self.__env = MLSENV.STG

        if username:
            assert type(username) == str, "Invalid type of username"
            self.__username = username
        elif os.environ.get("MLS_USERNAME"):
            self.__username = os.environ["MLS_USERNAME"]
        else:
            raise MLSClientError("'username' must be provided with parameter or environment variable (MLS_USERNAME)")

        if password:
            assert type(password) == str, "Invalid type of password"
            self.__password = password
        elif os.environ.get("MLS_PASSWORD"):
            self.__password = os.environ["MLS_PASSWORD"]
        else:
            raise MLSClientError("'password' must be provided with parameter or environment variable (MLS_PASSWORD)")

        self.__api_token = base64.b64encode(f"{self.__username}:{self.__password}".encode()).decode("utf-8")

    def get_env(self) -> MLSENV:
        return self.__env

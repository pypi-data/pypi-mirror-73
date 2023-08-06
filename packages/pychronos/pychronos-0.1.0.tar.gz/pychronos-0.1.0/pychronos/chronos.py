import logging
from urllib3.exceptions import MaxRetryError

from openapi_client.exceptions import ApiException
from openapi_client.models import Space as _Space

import pychronos
from pychronos.exceptions import api_exception_helper
from .base import PyChronosBase
from .space import Space

logger = logging.getLogger(__name__)


class Chronos(PyChronosBase):
    """ChronosDB connection"""

    def __init__(self):
        if pychronos._client_instance is None:
            raise RuntimeError("connection is not initiated; use pychronos.init() to create a connection")

    def __str__(self):
        # global _client_instance

        if pychronos._client_instance.configuration.access_token:
            return f"PyChronos connected to {pychronos._chronos_host}:{pychronos._chronos_port}"
        else:
            return "PyChronos: uninitiated; use pychronos.init() to initiate connection"

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, space_name):
        """ retrieve Space """
        obj = Space(space_name)
        obj._fetch()
        return obj

    @staticmethod
    def list_spaces():
        """
        list spaces in the database
        :return:
        """
        # check if initiated correctly
        if pychronos._client_instance is None:
            raise ConnectionError("connection not initiated")

        try:
            response = pychronos._space_api_instance.app_api_space_get_list()
        except ApiException as e:
            print(pychronos._configuration.access_token)
            api_exception_helper(e)
            # print("Exception when calling listing spaces: %s\n" % e)

        return [x.name for x in response]

    @staticmethod
    def create(name, title=None, description=None, tags=None, public: bool = None):
        """
        create a new space
        :return:
        """
        if public is None:
            visibility = None
        else:
            visibility = "public" if public else "private"

        body = _Space(name=name, title=title, description=description, tags=tags, visibility=visibility)
        try:
            obj = pychronos._space_api_instance.app_api_space_post(body)

        except ApiException as e:
            api_exception_helper(e)

        sp = Space(name)
        sp._fetch(obj)
        return sp

    def set_api_key(self, api_key):
        """Set api key"""
        pychronos._configuration.api_key['X-Auth'] = api_key

    def set_token(self, token):
        """set jwt token"""
        pychronos._configuration.access_token = token

    def login(self, username, password):
        """Login to ChronosDB"""

        # basic_auth
        pychronos._configuration.username = username
        pychronos._configuration.password = password

        try:
            response = pychronos._user_api_instance.app_api_user_login(_request_timeout=pychronos._timeout)
            # pychronos._configuration.access_token = response.jwt
            self.set_token(response.jwt)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._chronos_host} "
                f"on port {pychronos._chronos_port}"
            ) from None

        except ApiException as e:
            api_exception_helper(e)
            #
            # if e.status == 401:
            #     raise ValueError("invalid username and/or password") from None

        finally:
            pychronos._configuration.username = ""
            pychronos._configuration.password = ""

    @staticmethod
    def logout():
        """Logout"""
        try:
            pychronos._user_api_instance.app_api_user_logout()
            pychronos._configuration.access_token = ""

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._chronos_host} "
                f"on port {pychronos._chronos_port}"
            ) from None

        except ApiException as e:
            if e.status == 401:
                raise ValueError("invalid username and/or password") from None

import getpass
import os

import yaml
from urllib3.exceptions import MaxRetryError

import pychronos
from .chronos import Chronos

import openapi_client
from openapi_client.exceptions import ApiException


def init(username=None, host="https://tshub.io",
         port=443,
         base_path="/api",
         timeout=1,
         api_key=None,
         token=None):
    """
    Initiate connection to ChronosDB

    :param username:
    :param host:
    :param port:
    :param base_path:
    :param timeout: in seconds
    :param api_key:
    :param token: jwt access token
    :return: Chronos
    """

    pychronos._timeout = timeout
    pychronos._chronos_host = host
    pychronos._chronos_port = port
    pychronos._chronos_base_path = base_path

    pychronos._configuration = openapi_client.Configuration()

    if host is not None:
        pychronos._configuration.host = f"{host}:{port}" + (f"{base_path}" if base_path else "")

    # basic_auth
    # pychronos._configuration.username = username
    # pychronos._configuration.password = password

    # api_key
    # _configuration.api_key['X-Auth'] = api_key

    # bearer
    # _configuration.api_key_prefix['X-Auth'] = 'Bearer'

    # _client_instance = openapi_client.ApiClient(_configuration)
    # _user_api_instance = openapi_client.UserApi(_client_instance)

    pychronos._client_instance = openapi_client.ApiClient(pychronos._configuration)
    pychronos._space_api_instance = openapi_client.SpaceApi(pychronos._client_instance)
    pychronos._raw_space_api_instance = openapi_client.RawSpaceApi(pychronos._client_instance)
    pychronos._collection_api_instance = openapi_client.CollectionApi(pychronos._client_instance)
    pychronos._raw_collection_api_instance = openapi_client.RawCollectionApi(pychronos._client_instance)
    pychronos._timeseries_api_instance = openapi_client.TimeSeriesApi(pychronos._client_instance)
    pychronos._raw_timeseries_api_instance = openapi_client.RawTimeSeriesApi(pychronos._client_instance)
    pychronos._raw_api_instance = openapi_client.RawTimeSeriesDataApi(pychronos._client_instance)
    pychronos._raw_vintage_api_instance = openapi_client.RawVintageApi(pychronos._client_instance)
    pychronos._vintage_api_instance = openapi_client.VintageApi(pychronos._client_instance)
    pychronos._user_api_instance = openapi_client.UserApi(pychronos._client_instance)
    pychronos._raw_annot_api_instance = openapi_client.RawAnnotationsApi(pychronos._client_instance)
    pychronos._annot_api_instance = openapi_client.AnnotationsApi(pychronos._client_instance)

    obj = Chronos()

    if username is not None:
        password = getpass.getpass()
        try:
            obj.login(username=username, password=password)
        except Exception as e:
            pychronos.close()
            raise

    elif token is not None:
        # jwt
        obj.set_token(token)
    elif api_key is not None:
        obj.set_api_key(api_key)

    else:

        # # try to get info from ~/.chronos file
        # try:
        #     with open(os.path.expanduser("~/.chronos"), "r") as fp:
        #         dot_chronos = yaml.safe_load(fp)
        #
        #         if 'api_key' in dot_chronos:
        #             obj.set_api_key(api_key)
        #
        # except OSError as e:
        #
        #     pychronos.close()
        #     raise ValueError("either username/password or api_key must be provided")

        pychronos.close()
        raise ValueError("either username/password or api_key must be provided")

    pychronos.connection = obj

    return obj

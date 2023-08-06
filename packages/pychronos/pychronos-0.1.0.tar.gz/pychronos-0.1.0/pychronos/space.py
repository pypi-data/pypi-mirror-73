import logging
from datetime import datetime
from typing import Text

from urllib3.exceptions import MaxRetryError

import pychronos
from pychronos.exceptions import api_exception_helper
from .base import PyChronosBase, TIME_INF
from .collection import Collection

from openapi_client.exceptions import ApiException, ApiValueError
from openapi_client.models import Space as _Space
from openapi_client.models import Collection as _Collection

logger = logging.getLogger(__name__)


class Space(PyChronosBase):

    def __init__(self, name=None, space_id=None):
        if name is None and space_id is None:
            raise ValueError("Either 'name' or 'space_id' has to be given")

        self.__space_name__ = name
        self.__space_id__ = space_id
        self.__space_description__ = None
        self.__space_title__ = None
        self.__real_start__ = None
        self.__real_end__ = None

    def __repr__(self):
        return "Space: {}".format(self.__space_name__)

    @property
    def name(self):
        return self.__space_name__

    @name.setter
    def name(self, _name: Text):
        """ set name """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")
        self.update(name=_name)

    @property
    def title(self):
        """ get description """
        if self.__space_title__ is None:
            self._fetch()
        return self.__space_title__

    @title.setter
    def title(self, _title: Text):
        """ set title """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")
        self.update(title=_title)

    @property
    def description(self):
        """ get description """
        if self.__space_id__ is None:
            self._fetch()
        return self.__space_description__

    @description.setter
    def description(self, _description: Text):
        """ set title """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        self.update(description=_description)

    def list_collections(self):
        """ list collection names """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        try:
            response = pychronos._collection_api_instance.app_api_collection_get_list(self.__space_name__)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with "
                f"{pychronos._configuration.host} on port {pychronos._configuration.port}"
            ) from None

        except ApiException as e:
            api_exception_helper(e)

        return [x.name for x in response]

    @property
    def info(self, display=True):
        """ display space info """
        if display:
            print(f"name: {self.__space_name__}\n" +
                  f"title: {self.__space_title__}\n" +
                  f"description: {self.__space_description__}"
                  )
            return None

        return {
            'spaceId': self.__space_id__,
            'name': self.__space_name__,
            'title': self.__space_title__,
            'description': self.__space_description__
        }

    def __getitem__(self, name):
        """ retrieve collections """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        out = Collection(space_name=self.__space_name__, coll_name=name)
        out._fetch()
        return out

    def _fetch(self, obj=None):
        """ fetch data from the server """
        if obj is None:
            try:
                if self.__space_name__:
                    obj = pychronos._space_api_instance.app_api_space_get(self.__space_name__)
                elif self.__space_id__:
                    obj = pychronos._raw_space_api_instance.app_api_space_raw_get(self.__space_id__)
                else:
                    ValueError("space_name or space_id are missing")

            except MaxRetryError:
                raise ConnectionError(
                    f"Couldn't establish connection with "
                    f"{pychronos._configuration.host} on port {pychronos._configuration.port}"
                ) from None

            except ApiException as e:
                api_exception_helper(e)
                # if e.status == 401:
                #     raise ConnectionError("Login failed; login again") from None
                #
                # elif e.status == 404:
                #     raise NameError("Space, {}, not found".format(self.__space_name__)) from None
                #
                # else:
                #     raise RuntimeError(f"Error: {e}") from None

        self.__space_id__ = obj.space_id
        self.__space_title__ = obj.title
        self.__space_description__ = obj.description
        self.__real_start__ = obj.real_start
        self.__real_end__ = obj.real_end

    def history(self, real_start: datetime = None, real_end: datetime = None):
        """fetch historical collection object"""
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        if real_start and not isinstance(real_start, datetime):
            raise TypeError("real time must be datetime object")

        if real_start and not isinstance(real_start, datetime):
            raise TypeError("real time must be datetime object")

        try:
            hist = pychronos._raw_space_api_instance.app_api_space_object_history(self.__space_id__,
                                                                                  real_start=real_start,
                                                                                  real_end=real_end)

        except ApiException as e:
            api_exception_helper(e)

        out = []
        for h in hist:
            c = Space(h.name)
            c._fetch(obj=h)
            out += [c]

        return out

    def update(self, name=None, title=None, description=None, tags=None, public=None):
        """ update space properties """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        if public is None:
            visibility = None
        else:
            visibility = "public" if public else "private"

        body = _Space(name=name, title=title, description=description, tags=tags, visibility=visibility)
        try:
            obj = pychronos._raw_space_api_instance.app_api_space_raw_put(space_id=self.__space_id__, space=body)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with "
                f"{pychronos._configuration.host} on port {pychronos._configuration.port}"
            ) from None

        except ApiException as e:
            if e.status == 401:
                raise ConnectionError("Login failed; login again") from None

            elif e.status == 404:
                raise NameError("Space, {}, not found".format(self.__space_name__)) from None

            elif e.status == 409:
                raise NameError("Space, {}, already exists".format(self.__space_name__)) from None

            else:
                raise RuntimeError(f"Error: {e}") from None

        self.__space_name__ = obj.name
        self.__space_title__ = obj.title
        self.__space_description__ = obj.description
        self.__real_start__ = obj.real_start
        self.__real_end__ = obj.real_end

    def create(self, name: str, title: str = None, description: str = None) -> Collection:
        """create a new collection"""
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        body = _Collection(name=name, title=title, description=description)
        try:
            obj = pychronos._raw_collection_api_instance.app_api_collection_raw_post(space_id=self.__space_id__,
                                                                                     collection=body)

        except ApiException as e:
            if e.status == 401:
                raise Exception("Login failed; login again") from None

            elif e.status == 404:
                raise NameError("Space, {}, not found".format(self.__space_name__)) from None

            else:
                raise RuntimeError(f"Error: {e}") from None

        coll = Collection(space_name=self.__space_name__, coll_name=name)
        coll._fetch(obj)
        return coll

    def delete(self):
        """ delete space """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        try:
            pychronos._raw_space_api_instance.app_api_space_raw_delete(self.__space_id__)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with "
                f"{pychronos._configuration.host} on port {pychronos._configuration.port}"
            ) from None

        except ApiException as e:
            if e.status == 401:
                raise Exception("Login failed; login again") from None

            elif e.status == 404:
                raise NameError("Error: space, {}, not found".format(self.__space_name__)) from None

            else:
                raise RuntimeError(f"Error: {e}") from None

        self.__space_id__ = None
        self.__space_name__ = None
        self.__space_description__ = None
        self.__real_start__ = None
        self.__real_end__ = None
        self.__space_title__ = None

        return None

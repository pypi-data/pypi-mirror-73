import logging
from typing import Text, Dict
from urllib3.exceptions import MaxRetryError

import pychronos
from .base import PyChronosBase, TIME_INF
# from pychronos import _vintage_api_instance, _configuration, _raw_vintage_api_instance

from openapi_client.models.vintage_update import VintageUpdate
from openapi_client.exceptions import ApiException, ApiValueError
from openapi_client.models.space import Space as _Space
from openapi_client.models.vintage import Vintage as _Vintage

logger = logging.getLogger(__name__)


class Vintage(PyChronosBase):
    """ Vintage """

    def __init__(self, name, description=None, metadata={}):
        self.__coll_id__ = None
        self.__vid__ = None
        self.__realtime__ = None
        self.__tsids__ = None
        self.series = []  # ???? TimeSeries
        self.__vintage_name__ = name
        self.__description__ = description
        self.__metadata__ = metadata
        self.__real_start__ = None
        self.__real_end__ = None  # TIME_INF is the most up-to-date, anything else is historical

    def __repr__(self):
        return f"{self.__vintage_name__} @{ self.__realtime__} #{self.__vid__}"

    def _fetch(self, obj=None):
        """ fetch collection """
        if obj is None:
            try:
                obj = pychronos._raw_vintage_api_instance.app_api_vintages_get_raw(self.__coll_id__, self.__vid__)

            except MaxRetryError:
                raise ConnectionError(
                    f"Couldn't establish connection with "
                    f"{pychronos._configuration.host} on port {pychronos._configuration.port}"
                ) from None

            except ApiException as e:
                if e.status == 404:
                    raise ValueError("Collection, {}, not found".format(self.__coll_name__)) from None
                else:
                    raise RuntimeError(f"Error: {e}") from None

        self.__coll_id__ = obj.coll_id
        self.__vid__ = obj.vid
        self.__realtime__ = obj.realtime
        self.__vintage_name__ = obj.name
        self.__description__ = obj.description
        self.__metadata__ = obj.metadata or {}
        self.__tsids__ = obj.tsids or []
        self.__real_start__ = obj.real_start
        self.__real_end__ = obj.real_end

    def update(self, name=None, description=None, metadata=None):
        """"""
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        if self.__coll_id__ is None:
            print("Error: invalid vintage object, get vintage via timeseries.vintages()")

        data = VintageUpdate(name=name, description=description, metadata=metadata)
        try:
            res = pychronos._vintage_api_instance.app_api_vintages_put_raw(self.__coll_id__, self.__vintage_name__,
                                                                           data)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} on port {pychronos._configuration.port}") from None

        except ApiValueError as e:
            print("Error: {}".format(e))
            return None

        except ApiException as e:
            print("Error: {}".format(e))
            return None

        if name:
            self.__vintage_name__ = name
        if description:
            self.__description__ = description
        if metadata:
            self.__metadata__ = metadata

    #
    # immutable
    #
    @property
    def realtime(self):
        return self.__realtime__

    @property
    def vid(self):
        return self.__vid__

    #
    # mutable
    #
    @property
    def name(self):
        return self.__vintage_name__

    @name.setter
    def name(self, name):
        """ """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        self.update(name=name)

    @property
    def description(self):
        return self.__description__

    @description.setter
    def description(self, description: Text):
        """ """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        self.update(description=description)

    @property
    def metadata(self):
        if self.__metadata__ is None:
            self._fetch()
        return self.__metadata__

    @metadata.setter
    def metadata(self, x: Dict):
        """ """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        if not isinstance(x, dict):
            print("Error: metadata must be an jsonifiable dictionary")
        self.update(metadata=x)

    @classmethod
    def _from_response(cls, res: _Vintage, coll_id: Text = None):
        if res is None:
            return None

        obj = cls(name=res.name,
                  description=res.description,
                  metadata=res.metadata if hasattr(res, 'metadata') else None)
        obj.__coll_id__ = coll_id or res.coll_id
        obj.__vid__ = res.vid
        obj.__realtime__ = res.realtime
        obj.__tsids__ = None
        obj.series = []  # ???? TimeSeries
        obj.__vintage_name__ = res.name
        obj.__real_start__ = res.real_start
        obj.__real_end__ = res.real_end

        return obj

    def history(self, by_name=True):
        """ history of vintage properties changes """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        try:
            if by_name:
                res = pychronos._raw_vintage_api_instance.app_api_vintages_name_history_raw(self, self.__coll_id__,
                                                                                            self.__vintage_name__)
            else:
                res = pychronos._raw_vintage_api_instance.app_api_vintages_object_history_raw(self, self.__coll_id__,
                                                                                              self.__vid__)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} on port {pychronos._configuration.port}") from None

        except ApiException as e:
            print("Error {}".format(e.status))
            return None

        return [Vintage._from_response(r, cid=self.__coll_id__) for r in res]

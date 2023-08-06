# create/update/delete time series
# retrieve history
import datetime
import logging
from typing import Text, Dict, List, Union
import pandas as pd
from urllib3.exceptions import MaxRetryError

import pychronos
import pychronos.annotation
from pychronos.exceptions import api_exception_helper
from pychronos.freq import pandas_freq_to_chronos_freq
from .base import PyChronosBase, TIME_INF
from .utils_pandas import series_to_SingleTimeSeriesData, rawSingleTimeSeriesData_to_series, pandas_time_to_index
from pychronos.vintage import Vintage

from openapi_client.models.vintage_update import VintageUpdate
from openapi_client.exceptions import ApiException, ApiValueError
from openapi_client.models import TimeSeries as _TimeSeries
from openapi_client.models import TimeSeriesCore as _TimeSeriesCore
from openapi_client.models import TimeSeriesUpdate as _TimeSeriesUpdate
from openapi_client.models import RawDataPutRequest as _RawDataPutRequest
from openapi_client.models import AnnotationTarget as _AnnotationTarget
from openapi_client.models import Annotation as _Annotation

logger = logging.getLogger(__name__)


class TimeSeries(PyChronosBase):
    """ Time Series object """

    def __init__(self, space_name, coll_name, ts_name, coll_id=None, tsid=None):

        try:
            _ = _TimeSeries(space=space_name, collection=coll_name, name=ts_name)
        except ApiValueError as e:
            print("invalid value: {}".format(e))
            return None

        self.__space_name__ = space_name
        self.__coll_name__ = coll_name
        self.__ts_name__ = ts_name
        self.__tsid__ = None
        self.__title__ = None
        self.__description__ = None
        self.__coll_id__ = None
        self.__dtype__ = None
        self.__dparams__ = None
        self.__itype__ = None
        self.__freq__ = None
        self.__fparams__ = None
        self.__unit__ = None
        self.__discontinued__ = None
        self.__entity__ = None
        self.__variable__ = None

        self.__attributes__ = None

        self.last_updated = None

        self.__real_start__ = None
        self.__real_end__ = None  # TIME_INF is the most up-to-date, anything else is historical

    def __repr__(self):
        return f"{self.__ts_name__}.c:{self.__coll_name__}.s:{self.__space_name__} ({self.__tsid__})"

    def __str__(self):
        return f"ts:{self.__ts_name__}"

    def __eq__(self, x):
        return x.__tsid__ == self.__tsid__ if isinstance(x, TimeSeries) else False

    @classmethod
    def _from_core(cls, space_name: Text, coll_name: Text, ts_name: Text, core: _TimeSeriesCore):
        """ create TimeSeries from TimeSeriesCore api response"""
        obj = cls(space_name=space_name, coll_name=coll_name, ts_name=ts_name)
        obj.__tsid__ = core.tsid
        obj.__coll_id__ = core.coll_id
        obj.__dtype__ = core.dtype
        obj.__dparams__ = core.dparams
        obj.__itype__ = core.itype
        obj.__freq__ = core.freq
        obj.__fparams__ = core.fparams
        obj.__entity__ = core.entity
        obj.__variable__ = core.variable

        return obj

    @classmethod
    def _from_raw(cls, coll_id, tsid):
        obj = cls(None, None, None)
        obj.__tsid__ = tsid
        obj.__coll_id__ = coll_id

        obj._fetch_raw()

        return obj

    def __repr__(self):
        return "TS: {}(.{}.{}), {}, {}".format(self.__ts_name__, self.__coll_name__, self.__space_name__,
                                               self.__dtype__, self.__freq__)

    def _fetch_raw(self, obj=None):
        if obj is None:
            try:
                obj = pychronos._raw_timeseries_api_instance.app_api_timeseries_raw_get(self.__coll_id__, self.__tsid__)

            except MaxRetryError:
                raise ConnectionError(
                    f"Couldn't establish connection with {pychronos._configuration.host} "
                    f"on port {pychronos._configuration.port}") from None

            except ApiException as e:
                print("Error {}".format(e.status))

        self._fetch(obj)

    def _fetch(self, obj=None):
        """ fetch time series info """
        if obj is None:
            try:
                obj = pychronos._timeseries_api_instance.app_api_timeseries_get(self.__space_name__, self.__coll_name__,
                                                                                self.__ts_name__)

            except MaxRetryError:
                raise ConnectionError(
                    f"Couldn't establish connection with {pychronos._configuration.host} "
                    f"on port {pychronos._configuration.port}") from None

            except ApiException as e:
                print("Error {}".format(e.status))

        self.__tsid__ = obj.tsid
        self.__coll_id__ = obj.coll_id
        self.__dtype__ = obj.dtype
        self.__dparams__ = obj.dparams
        self.__itype__ = obj.itype
        self.__freq__ = obj.freq
        self.__fparams__ = obj.fparams
        self.__unit__ = obj.unit
        self.__discontinued__ = obj.discontinued
        self.__attributes__ = obj.attributes
        self.__entity__ = obj.entity
        self.__variable__ = obj.variable
        self.__title__ = obj.title
        self.__description__ = obj.description
        self.__real_start__ = obj.real_start
        self.__real_end__ = obj.real_end

    @property
    def info(self):
        """ display time series info """
        print(f"name: {self.__ts_name__} (.{self.__coll_name__}.{self.__space_name__})\n" +
              f"title: {self.__title__}\n" +
              f"description: {self.__description__}\n" +
              f"last updated: {self.last_updated}")

        return {
            'tsid': self.__tsid__,
            'name': self.__ts_name__,
            'title': self.__title__,
            'description': self.__description__
        }

    def update(self, name=None, title=None, description=None, attributes=None, discontinued=None, unit=None):
        """ update Time series"""
        try:
            body = _TimeSeriesUpdate(name=name,
                                     title=title,
                                     description=description,
                                     unit=unit,
                                     discontinued=discontinued,
                                     attributes=attributes)
        except ValueError as e:
            raise

        except TypeError as e:
            raise

        try:
            obj = pychronos._raw_timeseries_api_instance.app_api_timeseries_raw_put(coll_id=self.__coll_id__,
                                                                                    tsid=self.__tsid__,
                                                                                    time_series_update=body)
        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} "
                f"on port {pychronos._configuration.port}") from None

        except ApiException as e:
            if e.status == 404:
                print("Time series, {}.{}.{}, not found".format(self.__ts_name__,
                                                                self.__coll_name__,
                                                                self.__space_name__))
                return None
            else:
                print("Error: {}".format(e.reason))
                return None

        if name:
            self.__ts_name__ = name
        if title:
            self.__title__ = title
        if description:
            self.__description__ = description
        if attributes:
            self.__attributes__ = attributes
        if discontinued:
            self.__discontinued__ = discontinued
        if unit:
            self.__unit__ = unit

    def get(self, vintage: Vintage = None):
        """ return pandas object """

        realtime = None
        if vintage:
            realtime = vintage.realtime

        try:
            res = pychronos._raw_api_instance.app_api_raw_timeseries_data_get(coll_id=self.__coll_id__,
                                                                              tsids=[self.__tsid__],
                                                                              realtime=realtime)
        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} "
                f"on port {pychronos._configuration.port}") from None

        except ApiException as e:
            print("Error: {}".format(e))
            return None

        if len(res) != 1:
            raise RuntimeError("not enough/too many values were returned")

        return rawSingleTimeSeriesData_to_series(res[self.__tsid__])

    def save(self, series: pd.Series, method: Text = 'update', vintage: Vintage = None, realtime: datetime = None) -> Vintage:
        """ save observations """
        if method not in ("update", "append", "overwrite"):
            raise ValueError("invalid save method; must be either 'update', 'overwrite', or 'append'")

        series_data = series_to_SingleTimeSeriesData(series, tsid=self.__tsid__, coll_id=self.__coll_id__)

        # TODO validate
        if series_data.dtype != self.dtype:
            raise ValueError(f"invalid data type, {series_data.dtype}; {self.dtype} is required")
        if series_data.itype != self.itype:
            raise ValueError(f"invalid index type, {series_data.itype}; {self.itype} is required")
        if series_data.freq != self.freq:
            raise ValueError(f"invalid frequency, {series_data.freq}; {self.freq} is required")

        if vintage:
            _vintage = VintageUpdate(name=vintage.name,
                                     description=vintage.description,
                                     metadata=vintage.metadata)
        else:
            _vintage = None

        body = _RawDataPutRequest(series=[series_data], vintage=_vintage)
        try:
            res = pychronos._raw_api_instance.app_api_raw_timeseries_data_put(coll_id=self.__coll_id__,
                                                                              method=method,
                                                                              raw_data_put_request=body,
                                                                              realtime=realtime)
        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} "
                f"on port {pychronos._configuration.port}") from None

        except ApiException as e:
            api_exception_helper(e)

        except Exception as e:
            raise RuntimeError(e)

        return Vintage._from_response(res.vintage)

    def delete(self):
        """ delete time series """
        try:
            obj = pychronos._timeseries_api_instance.app_api_timeseries_delete(self.__space_name__,
                                                                               self.__coll_name__,
                                                                               self.__ts_name__)
        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} "
                f"on port {pychronos._configuration.port}") from None

        except ApiException as e:
            if e.status == 404:
                print("Error: collection, {}, not found".format(self.__coll_name__))
                return None
            else:
                print("Error: %s\n" % e)
                return None

        self.__ts_name__ = None
        return None

    def obs_status(self):
        pass

    def history(self, real_time=None):
        """ history of time series properties changes """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        if real_time and not isinstance(real_time, datetime.datetime):
            raise TypeError("real time must be datetime object")

        try:
            hist = pychronos._raw_timeseries_api_instance.app_api_timeseries_object_history(self.__coll_id__,
                                                                                            real_start=real_time)

        except ApiException as e:
            api_exception_helper(e)

        out = []
        for h in hist:
            c = TimeSeries(self.__space_name__, self.__coll_name__, self.__ts_name__)
            c._fetch(obj=h)
            out += [c]

        return out

    def vintages(self):
        """ history of value changes """
        res = pychronos._raw_vintage_api_instance.app_api_vintages_get_list_raw(self.__coll_id__, tsid=self.__tsid__)
        return [Vintage._from_response(r, coll_id=self.__coll_id__) for r in res]

    #
    # immutable properties
    #

    @property
    def tsid(self):
        """ timeseries id """
        return self.__tsid__

    @property
    def entity(self):
        """ entity id in panel data, e.g. household id """
        return self.__entity__

    @property
    def variable(self):
        """ variable name in panel data, e.g. income """
        return self.__variable__

    @property
    def itype(self):
        return self.__itype__

    @property
    def freq(self):
        return self.__freq__

    @property
    def dtype(self):
        return self.__dtype__

    @property
    def fparams(self):
        return self.__fparams__

    @property
    def dparams(self):
        return self.__dparams__

    #
    # mutable properties
    #

    @property
    def name(self):
        return self.__ts_name__

    @name.setter
    def name(self, _name: Text):
        """ set name """
        self.update(name=_name)

    @property
    def title(self):
        """ get description """
        if self.__tsid__ is None:
            self._fetch_raw()
        return self.__title__

    @title.setter
    def title(self, _title: Text):
        """ set title """
        self.update(title=_title)

    @property
    def description(self):
        """ get description """
        if self.__tsid__ is None:
            self._fetch_raw()
        return self.__description__

    @description.setter
    def description(self, _description: Text):
        """ set title """
        self.update(description=_description)

    @property
    def attributes(self):
        return self.__attributes__

    @attributes.setter
    def attributes(self, _attributes: Dict):
        """ """
        data = _TimeSeriesUpdate(attributes=_attributes)
        try:
            res = pychronos._timeseries_api_instance.app_api_timeseries_put(self.__space_name__,
                                                                            self.__coll_name__,
                                                                            self.__ts_name__,
                                                                            data)
        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} "
                f"on port {pychronos._configuration.port}") from None

        except ApiValueError as e:
            print("Error: {}".format(e))
            return None
        except ApiException as e:
            print("Error: {}".format(e))
            return None

        self.__attributes__ = _attributes

    #
    #   Annotation
    #
    def annotations(self):
        """
        list annotations in the collection
        :return:
        """
        res = pychronos._raw_annot_api_instance.app_api_annotation_raw_get_list(coll_id=self.__coll_id__,
                                                                                tsid=self.__tsid__)

        return pychronos.annotation.construct_annotations(self.__coll_id__, res)

    def annotate(self, text, index: Union[List[pd.Period], pd.Period], text_format=None, attributes: dict = None):
        """ annotate observations"""
        if isinstance(index, (list, tuple)):
            _index_freq = [(pandas_time_to_index(x, date_format='us'), pandas_freq_to_chronos_freq.get(index[0]),) for x
                           in index]

        elif isinstance(index, pd.Period):
            _index_freq = [
                (pandas_time_to_index(index, date_format='us'), pandas_freq_to_chronos_freq.get(index.freqstr),)]

        else:
            print(f"Error: unsupported index type; use pandas Period or list/tutple of Pandas Period's")
            return None

        targets = [_AnnotationTarget(tsid=self.__tsid__, index=inx, freq=freq, real_start=None) for inx, freq in
                   _index_freq]
        data = _Annotation(text=text, format=text_format, attributes=attributes, targets=targets)

        try:
            res = pychronos._raw_annot_api_instance.app_api_annotation_raw_create(coll_id=self.__coll_id__,
                                                                                  annotation=data)
        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} "
                f"on port {pychronos._configuration.port}") from None

        except ApiValueError as e:
            print(f"Error: {e}")
            return None
        except ApiException as e:
            print(f"Error: {e}")
            return None

        return pychronos.annotation.Annotation._from_response(res)

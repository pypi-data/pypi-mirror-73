import logging
from datetime import datetime
from typing import Text, List, Union, Optional, Tuple

import bson as bson
import pandas as pd
from pandas._libs.tslibs.period import IncompatibleFrequency
from urllib3.exceptions import MaxRetryError

import pychronos
from pychronos.annotation import Annotation
from pychronos.exceptions import api_exception_helper
from pychronos.utils import pretty_dict
from pychronos.vendor.openapi_client.models.raw_data_put_request import RawDataPutRequest
from pychronos.vendor.openapi_client.models.vintage_update import VintageUpdate
from .base import PyChronosBase, TIME_INF
from .dtype import DType
from .index import IType
from .timeseries import TimeSeries
from .utils_pandas import rawSingleTimeSeriesData_to_series, series_to_RawSingleTimeSeriesData, pandas_time_to_index, \
    index_value_to_pandas_period_value
from .freq import Freq
from pychronos.vintage import Vintage

from openapi_client.exceptions import ApiException, ApiValueError
from openapi_client.models import Collection as _Collection
from openapi_client.models import TimeSeries as _TimeSeries
from openapi_client.models import Annotation as _Annotation

logger = logging.getLogger(__name__)


class Collection(PyChronosBase):

    def __init__(self, space_name, coll_name, coll_id=None):
        self.__coll_id__ = coll_id
        self.__space_name__ = space_name
        self.__coll_name__ = coll_name
        self.__coll_title__ = None
        self.__coll_description__ = None
        self.__real_start__ = None
        self.__real_end__ = None  # TIME_INF is the most up-to-date, anything else is historical

    def __repr__(self):
        return "Collection: {}".format(self.__coll_name__)

    def _fetch(self, obj=None):
        """ fetch collection """
        if obj is None:
            try:
                if self.__coll_id__:
                    obj = pychronos._raw_collection_api_instance.app_api_collection_raw_get(coll_id=self.__coll_id__)
                else:
                    obj = pychronos._collection_api_instance.app_api_collection_get(space_name=self.__space_name__,
                                                                                    coll_name=self.__coll_name__)

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
        self.__coll_title__ = obj.title
        self.__coll_description__ = obj.description
        self.__real_start__ = obj.real_start
        self.__real_end__ = obj.real_end

    def update(self, name=None, title=None, description=None):
        """ update collection properties """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        body = _Collection(name=name, title=title, description=description)
        try:
            obj = pychronos._raw_collection_api_instance.app_api_collection_raw_put(coll_id=self.__coll_id__,
                                                                                    collection=body)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} on port "
                f"{pychronos._configuration.port}") from None

        except ApiException as e:
            if e.status == 404:
                raise ValueError(f"collection, {self.__coll_name__}, not found") from None
            else:
                raise RuntimeError(f"Error: {e}") from None

        if obj.name:
            self.__coll_name__ = obj.name
        if obj.title:
            self.__coll_title__ = obj.title
        if obj.description:
            self.__coll_description__ = obj.description
        if obj.real_start:
            self.__real_start__ = obj.real_start
        if obj.real_end:
            self.__real_end__ = obj.real_end

    @property
    def name(self):
        return self.__coll_name__

    @name.setter
    def name(self, _name: Text):
        """ set name """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        self.update(name=_name)

    @property
    def title(self):
        """ get description """
        if self.__coll_title__ is None:
            self._fetch()
        return self.__coll_title__

    @title.setter
    def title(self, _title: Text):
        """ set title """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        self.update(title=_title)

    @property
    def description(self):
        """ get description """
        if self.__coll_id__ is None:
            self._fetch()
        return self.__coll_description__

    @description.setter
    def description(self, _description: Text):
        """ set title """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        self.update(description=_description)

    def delete(self):
        """ delete collection """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        try:
            pychronos._raw_collection_api_instance.app_api_collection_raw_delete(coll_id=self.__coll_id__)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} on port "
                f"{pychronos._configuration.port}") from None

        except ApiException as e:
            if e.status == 404:
                raise ValueError(f"collection, {self.__coll_name__}, not found") from None

            else:
                raise RuntimeError(f"Error: {e}") from None

        self.__coll_id__ = None
        self.__coll_name__ = None
        self.__coll_description__ = None
        self.__real_start__ = None
        self.__real_end__ = None
        self.__coll_title__ = None

        return None

    def list_timeseries(self, display=False, details=False):
        """ list time series """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        response = pychronos._raw_timeseries_api_instance.app_api_timeseries_raw_get_list(coll_id=self.__coll_id__)
        out = [x.name for x in response]
        if display:
            if details:
                pretty_dict({k: v for k, v in response if k in ('name', 'title')})
            else:
                print(out)

        return out

    @property
    def info(self, display=True):
        """ display collection info """
        if display:
            print(f"name: {self.__coll_name__} (.{self.__space_name__})\n" +
                  f"title: {self.__coll_title__}\n" +
                  f"description: {self.__coll_description__}\n" +
                  f"created on: {self.__real_start__}")
            return None

        return {
            'name': self.__coll_name__,
            'title': self.__coll_title__,
            'description': self.__coll_description__,
            'cid': self.__coll_id__,
            'path': f"{self.__coll_name__}.{self.__space_name__}"
        }

    def __getitem__(self, name: Text) -> TimeSeries:
        """ get TimeSeries """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        try:
            if bson.objectid.ObjectId.is_valid(name):
                obj = pychronos._raw_timeseries_api_instance.app_api_timeseries_raw_get(coll_id=self.__coll_id__,
                                                                                        tsid=str(name))
            else:
                obj = pychronos._timeseries_api_instance.app_api_timeseries_get(self.__space_name__,
                                                                                self.__coll_name__,
                                                                                name)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} on port "
                f"{pychronos._configuration.port}") from None

        except ApiValueError as e:
            raise ValueError(e)

        except ApiException as e:
            api_exception_helper(e)

        ts = TimeSeries(self.__space_name__, self.__coll_name__, name)
        ts._fetch(obj)
        return ts

    def get(self, names: Union[Text, List[Text]]):
        """ get data from one or many series as series """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        if isinstance(names, str):
            _names = [names]
        elif isinstance(names, (list, tuple)):
            _names = names
        else:
            raise ValueError("argument must be a string or a list/tuple of strings corresponding to time series name")

        tsids = []
        tsid_name = {}
        for name in _names:
            try:
                ts = pychronos._timeseries_api_instance.app_api_timeseries_get(space_name=self.__space_name__,
                                                                               coll_name=self.__coll_name__,
                                                                               name=name)
                tsids += [ts.tsid]
                tsid_name[ts.tsid] = name
            except ApiException as e:
                if e.status == 404:
                    raise ValueError(f"time series, '{name}' can't be found") from None
                else:
                    raise RuntimeError(str(e)) from None

        try:
            res = pychronos._raw_api_instance.app_api_raw_timeseries_data_get(self.__coll_id__,
                                                                              tsids=tsids)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} on port "
                f"{pychronos._configuration.port}") from None

        except ApiValueError:
            print("name is invalid")

        except ApiException as e:
            if e.status == 404:
                raise ValueError("time series not found") from None
            else:
                raise RuntimeError(f"Error: {e}") from None

        objs = [rawSingleTimeSeriesData_to_series(x) for x in res.values()]
        if isinstance(names, str):
            return objs[0]

        return objs

    def to_dataframe(self, names: Union[Text, List[Text]]):
        """ get data from one or many series as dataframe """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        objs = self.get(names)
        if isinstance(objs, list):
            try:
                return pd.concat(objs, axis=1)

            except IncompatibleFrequency as e:
                raise IncompatibleFrequency(e) from None

        return pd.DataFrame(objs)

    def save(self,
             data: Union[pd.Series, List[pd.Series], Tuple[pd.Series], pd.DataFrame],
             name: str = None,
             names: List[str] = None,
             method: str = "update",
             vintage: Vintage = None,
             realtime: datetime = None) -> TimeSeries:
        """
        saves data to collection
        :return: Vintage
        """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        if method not in ("update", "append", "overwrite"):
            raise ValueError("invalid save method; must be either 'update', 'overwrite', or 'append'")

        _named_data = {}
        if isinstance(data, pd.Series):
            _name = data.name or name
            if _name is None:
                raise ValueError('no series name')
            _named_data[_name] = data
        elif isinstance(data, (list, tuple)):
            for i, x in enumerate(data):
                _name = names[i] if names else x.name
                if _name is None:
                    raise ValueError('no series name')
                # _names += [_name]
                _named_data[_name] = x

        elif isinstance(data, pd.DataFrame):
            i = 0
            for name, x in data.items():
                _name = names[i] if names else name
                _named_data[_name] = x
                i += 1
        else:
            raise TypeError("unsupported data type; use pandas' Series, List of Series, Dataframe")

        # tsids = []
        # tsid_name = {}
        # name_ts = {}
        req_data = []
        for name, x in _named_data.items():
            ts = self.__getitem__(name)
            # tsids += [ts.__tsid__]
            # tsid_name[ts.__tsid__] = name
            req_data += [series_to_RawSingleTimeSeriesData(data=x, tsid=ts.__tsid__, coll_id=ts.__coll_id__)]

        _vintage = None
        if vintage:
            _vintage = VintageUpdate(name=vintage.name,
                                     description=vintage.description,
                                     metadata=vintage.metadata)

        body = RawDataPutRequest(series=req_data, vintage=_vintage)

        try:
            res = pychronos._raw_api_instance.app_api_raw_timeseries_data_put(self.__coll_id__,
                                                                              method=method,
                                                                              raw_data_put_request=body,
                                                                              realtime=realtime)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} on port "
                f"{pychronos._configuration.port}") from None

        except ApiValueError:
            print("name is invalid")

    def create(self, name,
               freq: Freq,
               dtype: DType,
               itype: IType = IType.period,
               fparams: Optional[dict] = None,
               dparams: Optional[dict] = None,
               unit=None,
               title=None,
               description=None,
               attributes=None,
               legend=None,
               entity=None,
               variable=None):
        """create time series"""
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        # check dtype
        if isinstance(dtype, DType):
            dtype = dtype.value
        elif isinstance(dtype, str):
            dtype = DType(dtype).value
        else:
            raise TypeError(f"invalid dtype")

        # check itype
        if isinstance(itype, IType):
            itype = itype.value
        elif isinstance(itype, str):
            itype = IType(itype).value
        else:
            raise TypeError(f"invalid itype")

        # check freq
        if isinstance(freq, Freq):
            freq = freq.value
        elif isinstance(freq, str):
            freq = Freq(freq).value
        else:
            raise TypeError(f"invalid freq")

        # POST
        try:
            body = _TimeSeries(name=name,
                               title=title,
                               dtype=dtype,
                               dparams=dparams,
                               itype=itype,
                               freq=freq,
                               fparams=fparams,
                               unit=unit,
                               description=description,
                               attributes=attributes,
                               legend=legend,
                               entity=entity,
                               variable=variable
                               )
        except ApiValueError as e:
            api_exception_helper(e)

        try:
            obj = pychronos._raw_timeseries_api_instance.app_api_timeseries_raw_post(coll_id=self.__coll_id__,
                                                                                     time_series=body)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with "
                f"{pychronos._configuration.host} on port {pychronos._configuration.port}") from None

        except ApiException as e:
            api_exception_helper(e)

        ts = TimeSeries._from_core(space_name=self.__space_name__,
                                   coll_name=self.__coll_name__,
                                   ts_name=name,
                                   core=obj)

        return ts

    def annotation(self, symbol):
        """get annotation"""
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        annots = self.annotations()
        a = next((x for x in annots if x.symbol == symbol), None)
        if a is None:
            raise ValueError("symbol not found")
        return a
        # try:
        #     res = pychronos._raw_annot_api_instance.app_api_annotation_raw_get(self.__coll_id__, a.aid)
        #
        # except MaxRetryError:
        #     raise ConnectionError(
        #         f"Couldn't establish connection with "
        #         f"{pychronos._configuration.host} on port {pychronos._configuration.port}") from None
        #
        # except ApiException as e:
        #     api_exception_helper(e)
        #
        # return pychronos.annotation.construct_annotations(self.__coll_id__, [res])[0]

    def annotations(self):
        """ list annotations in a collection """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        try:
            res = pychronos._raw_annot_api_instance.app_api_annotation_raw_get_list(self.__coll_id__)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with "
                f"{pychronos._configuration.host} on port {pychronos._configuration.port}") from None

        except ApiException as e:
            api_exception_helper(e)

        return pychronos.annotation.construct_annotations(self.__coll_id__, res)

    def annotate(self, text, text_format='txt', symbol=None, attributes=None):
        """create a new annotation"""

        a = _Annotation(symbol=symbol,
                        text=text,
                        format=text_format,
                        attributes=attributes)
        res = pychronos._raw_annot_api_instance.app_api_annotation_raw_create(self.__coll_id__, annotation=a)

        return Annotation._from_response(res)

    def vintages(self):
        """ list vintages in a collection """
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        res = pychronos._raw_vintage_api_instance.app_api_vintages_get_list_raw(self.__coll_id__)

        return [Vintage._from_response(r) for r in res]

    def history(self, real_time: datetime = None):
        """fetch historical collection object"""
        if self.__real_end__ != TIME_INF:
            raise TypeError("historical object can't be modified")

        if real_time and not isinstance(real_time, datetime):
            raise TypeError("real time must be datetime object")

        try:
            hist = pychronos._raw_collection_api_instance.app_api_collection_object_history(self.__coll_id__,
                                                                                            real_start=real_time)

        except ApiException as e:
            api_exception_helper(e)

        out = []
        for h in hist:
            c = Collection(self.__space_name__, self.__coll_name__)
            c._fetch(obj=h)
            out += [c]

        return out

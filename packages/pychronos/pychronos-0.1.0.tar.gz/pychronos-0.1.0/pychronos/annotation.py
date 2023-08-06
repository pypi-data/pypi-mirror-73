# create/update/delete time series
# retrieve history
import logging
from datetime import datetime
from typing import Text, Dict, List, Optional
import pandas as pd
from urllib3.exceptions import MaxRetryError

import pychronos
import pychronos.timeseries
from pychronos.exceptions import api_exception_helper
from pychronos.freq import pandas_freq_to_chronos_freq
from .base import PyChronosBase
from .utils_pandas import pandas_time_to_index, \
    index_value_to_pandas_period_value
from pychronos.vintage import Vintage

from openapi_client.exceptions import ApiException, ApiValueError
from openapi_client.models import Annotation as _Annotation
from openapi_client.models import AnnotationUpdate as _AnnotationUpdate

logger = logging.getLogger(__name__)


class AnnotationTarget(PyChronosBase):
    """
    Annotation target,
    annotation can be pointing to several
    """

    def __init__(self, coll_id, aid, timeseries: pychronos.timeseries.TimeSeries = None, index: datetime = None,
                 real_start: datetime = None):
        self._coll_id = coll_id
        self._aid = aid
        self.timeseries = timeseries
        self.index = index
        self.real_start = real_start
        self.deleted = False

    @classmethod
    def _from_response(cls, coll_id, aid, tsid, index, freq, real_start):
        timeseries = pychronos.timeseries.TimeSeries._from_raw(coll_id=coll_id, tsid=tsid) if tsid else None
        index = index_value_to_pandas_period_value(index, freq=freq) if index else None
        obj = cls(coll_id=coll_id, aid=aid, timeseries=timeseries, index=index, real_start=real_start)
        return obj

    def delete(self):
        """delete target"""
        if self.deleted:
            raise Exception("Invalid target")

        try:
            if self.index:
                freq = pandas_freq_to_chronos_freq.get(self.index.freqstr)
                if freq is None:
                    raise ValueError(f"invalid frequency: {self.index.freqstr}")
            else:
                freq = None

            obj = pychronos._raw_annot_api_instance. \
                app_api_annotation_raw_remove_target(self._coll_id, self._aid,
                                                     tsid=self.timeseries.tsid if self.timeseries else None,
                                                     index=pandas_time_to_index(self.index) if self.index else None,
                                                     freq=freq,
                                                     real_start=self.real_start
                                                     )
            self._coll_id = None
            self._aid = None
            self.timeseries = None
            self.index = None
            self.real_start = None
            self.deleted = True

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} "
                f"on port {pychronos._configuration.port}") from None

        except ApiException as e:
            print("Error {}".format(e.status))


class Annotation(PyChronosBase):
    """ Annotation object """

    def __init__(self, coll_id, aid):

        self.__coll_id__ = coll_id
        self.__aid__ = aid
        self.__symbol__ = None
        self.__text__ = None
        self.___format__ = None
        self.__targets__ = None
        self.__attributes__ = None
        self.__real_start__ = None
        self.__real_end__ = None

        self.last_updated = None

    def __repr__(self):
        return f"{self.__aid__}.c:{self.__coll_id__}"

    def __str__(self):
        return f"annotation: {self.__symbol__} ({self.__aid__}"

    def __eq__(self, x):
        return x.__aid__ == self.__aid__ if isinstance(x, Annotation) else False

    @classmethod
    def _from_response(cls, a: _Annotation):
        """ create Annotation from Annotation api response"""
        obj = cls(coll_id=a.coll_id, aid=a.aid)

        obj.__symbol__ = a.symbol
        obj.__text__ = a.text
        obj.___format__ = a.format
        obj.__targets__ = [AnnotationTarget._from_response(coll_id=a.coll_id,
                                                           aid=a.aid,
                                                           tsid=x.tsid,
                                                           index=x.index,
                                                           freq=x.freq,
                                                           real_start=x.real_start) for x in a.targets]
        obj.__real_start__ = a.real_start
        obj.__real_end__ = a.real_end

        return obj

    def _fetch(self, obj=None):
        """ fetch time series info """
        if obj is None:
            try:
                obj = pychronos._raw_annot_api_instance.app_api_annotation_raw_get(self.__coll_id__, self.__aid__)

            except MaxRetryError:
                raise ConnectionError(
                    f"Couldn't establish connection with {pychronos._configuration.host} "
                    f"on port {pychronos._configuration.port}") from None

            except ApiException as e:
                print("Error {}".format(e.status))

        self.__coll_id__ = obj.coll_id
        self.__symbol__ = obj.symbol
        self.__aid__ = obj.aid
        self.__text__ = obj.text
        self.___format = obj.format
        self.__targets__ = [AnnotationTarget._from_response(coll_id=self.__coll_id__,
                                                            aid=self.aid,
                                                            tsid=x.tsid,
                                                            index=x.index,
                                                            freq=x.freq,
                                                            real_start=x.real_start) for x in obj.targets]
        self.__attributes__ = obj.attributes
        self.__real_start__ = obj.real_start
        self.__real_end__ = obj.real_end

    @property
    def info(self):
        """ display time series info """
        print(f"symbol: {self.__symbol__}\n" +
              f"text: {self.__text__}")

        return {
            'aid': self.__aid__,
            'symbol': self.__symbol__,
            'text': self.__text__
        }

    def update(self, symbol=None, text=None, format=None, attributes=None):
        """ update Time series"""
        try:
            body = _AnnotationUpdate(symbol=symbol,
                                     text=text,
                                     format=format,
                                     attributes=attributes)
        except ValueError as e:
            raise

        except TypeError as e:
            raise

        try:
            obj = pychronos._raw_annot_api_instance.app_api_annotation_raw_update(self.__coll_id__,
                                                                                  self.__aid__,
                                                                                  annotation_update=body)
        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} "
                f"on port {pychronos._configuration.port}") from None

        except ApiException as e:
            if e.status == 404:
                print(f"Annotation, {self.__aid__} at {self.__coll_id__}, not found")
                raise
            else:
                print("Error: {}".format(e.reason))
                raise

        # self._fetch(obj)  # TODO add return object to update

        if symbol:
            self.__symbol__ = symbol
        if text:
            self.__text__ = text
        if format:
            self.___format__ = format
        if attributes:
            self.__attributes__ = attributes

    def delete(self):
        """ delete time series """
        try:
            obj = pychronos._raw_annot_api_instance.app_api_annotation_raw_delete(coll_id=self.__coll_id__,
                                                                                  aid=self.__aid__)
        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} "
                f"on port {pychronos._configuration.port}") from None

        except ApiException as e:
            if e.status == 404:
                print("Error: annotation, {}, not found".format(self.__aid__))
                raise
            else:
                print("Error: %s\n" % e)
                raise

        return None

    def history(self):
        """ history of time series properties changes """
        pass

    #
    # immutable properties
    #

    @property
    def aid(self):
        """ annotation id """
        return self.__aid__

    @property
    def targets(self):
        """ annotation targets """
        return self.__targets__

    #
    # mutable properties
    #

    @property
    def symbol(self):
        return self.__symbol__

    @symbol.setter
    def symbol(self, _symbol: Text):
        """ set name """
        self.update(symbol=_symbol)

    @property
    def text(self):
        return self.__text__

    @text.setter
    def text(self, _text: Text):
        """ set name """
        self.update(text=_text)

    @property
    def format(self):
        """ get description """
        return self.___format__

    @format.setter
    def format(self, _format: Text):
        """ set title """
        self.update(format=_format)

    @property
    def attributes(self):
        self._fetch()
        return self.__attributes__

    @attributes.setter
    def attributes(self, _attributes: Dict):
        """ """
        self.update(attributes=_attributes)

    #
    #   Annotation
    #
    def annotate(self,
                 timeseries: pychronos.timeseries.TimeSeries = None,
                 index: Optional[pd.Period] = None,
                 vintage: Optional[Vintage] = None):
        """
        annotate an observation in time series, optionally provide
        a vintage if the annotation is limited to a vintage
        """
        params = {
            'coll_id': self.__coll_id__,
            'aid': self.__aid__,
        }

        if timeseries is None and index is None:
            raise Exception("Either timeseries or index must be specified")

        if timeseries:
            if isinstance(timeseries, pychronos.timeseries.TimeSeries):
                params['tsid'] = timeseries.tsid
            else:
                print(f"Error: unsupported index type; use pandas Period or list/tutple of Pandas Period's")
                return None

        if index:
            if isinstance(index, pd.Period):
                _index = pandas_time_to_index(index, date_format='us')
                params['index'] = _index
                if timeseries is not None:
                    params['freq'] = timeseries.freq
                else:
                    tmp = pandas_freq_to_chronos_freq.get(index.freqstr)
                    if tmp is None:
                        raise ValueError(f"invalid frequency: {index.freqstr}")
                    params['freq'] = tmp

            else:
                print(f"Error: unsupported index type; use pandas Period or list/tuple of Pandas Period's")
                return None

        if vintage:
            params['real_start'] = vintage.realtime

        try:
            res = pychronos._raw_annot_api_instance.app_api_annotation_raw_add_target(**params)

        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with {pychronos._configuration.host} "
                f"on port {pychronos._configuration.port}") from None

        except ApiValueError as e:
            print(f"Error: {e}")
            raise
        except ApiException as e:
            print(f"Error: {e}")
            raise


def construct_annotations(coll_id, annots: List[_Annotation]):
    # fetch time series for all annotations
    tsids = [x.tsid for r in annots for x in r.targets if x.tsid]

    if len(tsids) > 0:
        try:
            ts = pychronos._raw_timeseries_api_instance.app_api_timeseries_raw_get_list(coll_id=coll_id, tsids=tsids)

            ts = {x.tsid: x for x in ts}
        except MaxRetryError:
            raise ConnectionError(
                f"Couldn't establish connection with "
                f"{pychronos._configuration.host} on port {pychronos._configuration.port}") from None

        except ApiException as e:
            api_exception_helper(e)

    out = []
    for _a in annots:
        a = pychronos.annotation.Annotation(coll_id=_a.coll_id, aid=_a.aid)

        a.__symbol__ = _a.symbol
        a.__text__ = _a.text
        a.___format__ = _a.format
        a.__targets__ = [pychronos.annotation.AnnotationTarget._from_response(coll_id=_a.coll_id,
                                                                              aid=_a.aid,
                                                                              tsid=x.tsid,
                                                                              index=x.index,
                                                                              freq=x.freq,
                                                                              real_start=x.real_start)
                         for x in _a.targets]

        a.__real_start__ = _a.real_start
        a.__real_end__ = _a.real_end
        out.append(a)

    return out

from __future__ import absolute_import
import os
import sys

# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)

import logging

logger = logging.getLogger(__name__)


__version__ = "1.0.0"

import openapi_client
from openapi_client.configuration import Configuration

connection = None # Chronos object which user connected to

_chronos_host = None
_chronos_port = None
_timeout = 1  # seconds

_configuration = None
_client_instance = None
_space_api_instance = None
_raw_space_api_instance = None
_collection_api_instance = None
_raw_collection_api_instance = None
_timeseries_api_instance = None
_raw_timeseries_api_instance = None
_raw_api_instance = None
_raw_vintage_api_instance = None
_vintage_api_instance = None
_user_api_instance = None
_raw_annot_api_instance = None
_annot_api_instance = None

from pychronos.init import init
from pychronos.chronos import Chronos
from pychronos.space import Space
from pychronos.collection import Collection
from pychronos.timeseries import TimeSeries
from pychronos.vintage import Vintage
from pychronos.freq import Freq
from pychronos.dtype import DType
from pychronos.index import IType


def close():
    """close connections"""
    global _configuration, _client_instance, _space_api_instance, _collection_api_instance, _timeseries_api_instance, _raw_api_instance, _raw_vintage_api_instance, _vintage_api_instance, _user_api_instance, _raw_annot_api_instance, _annot_api_instance
    # del _vintage_api_instance
    if _client_instance:
    # del _client_instance
        _client_instance.__del__()

    connection = None

    _configuration = None
    _client_instance = None
    _space_api_instance = None
    _raw_space_api_instance = None
    _raw_collection_api_instance = None
    _collection_api_instance = None
    _timeseries_api_instance = None
    _raw_timeseries_api_instance = None
    _raw_api_instance = None
    _raw_vintage_api_instance = None
    _vintage_api_instance = None
    _user_api_instance = None
    _raw_annot_api_instance = None
    _annot_api_instance = None


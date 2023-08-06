import json
import logging

from pychronos.vendor.openapi_client.exceptions import ApiException


logger = logging.getLogger(__name__)


class ChronosError(Exception):
    pass


class NotFoundError(ChronosError):
    pass


def api_exception_helper(e: ApiException):
    if e.status == 500:
        logger.error(str(e))
        raise RuntimeError(str(e)) from None

    reply = json.loads(e.body)
    detail = reply.get('detail')
    if e.status == 400:
        logger.error(detail)
        raise ValueError(detail) from None

    elif e.status == 401:
        logger.error(detail)
        raise ValueError(detail) from None
        # raise ValueError("invalid username and/or password") from None

    elif e.status == 404:
        logger.error(detail)
        raise ValueError(detail) from None

    elif e.status == 409:
        logger.error(detail)
        raise ValueError(detail) from None

    else:
        logger.error(detail)
        raise RuntimeError(detail) from None

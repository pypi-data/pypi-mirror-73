from datetime import datetime


class PyChronosBase(object):
    """
    abstract parent of ChronosDB Classes
    """

    def _fetch(self):
        pass


TIME_INF = datetime(9999, 12, 31, 23, 59, 59)

from pprint import pprint

from .datahelper.datahelper import helper

__all__ = ["get_covid19_data"]


def get_covid19_data():
    data = helper()
    print("{:*^30}".format("FAKE DATA"))
    pprint(data)

import argparse
from .covid19getter import *


__all__ = (covid19getter.__all__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--get", help="get covid19 data", action="store_true")
    args = parser.parse_args()

    if args.get:
        get_covid19_data()
    else:
        parser.error("please use --get to get data")

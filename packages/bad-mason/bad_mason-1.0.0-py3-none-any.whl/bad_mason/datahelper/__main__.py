from datahelper import helper
print("""
    This helper is a simple module just help you to fetch the data from server with dynamic token.

    Try:

    1. run directly:
        py datahelper.zip
    2. run as module and into interaction mode:
        py -im datahelper.datahelper
        >>> helper()

    Example:

    data = helper()
    # data = {
    #     "31 Dec 2019": "Wuhan Municipal Health Commission, China, reported a cluster of cases of pneumonia in Wuhan, Hubei Province. A novel coronavirus was eventually identified.",
    #     "1 January 2020": "WHO had set up the IMST (Incident Management Support Team) across the three levels of the organization: headquarters, regional headquarters and country level, putting the organization on an emergency footing for dealing with the outbreak.",
    #     "4 January 2020": "WHO reported on social media that there was a cluster of pneumonia cases – with no deaths – in Wuhan, Hubei province."
    # }

""")

print("GET DATA from helper()")
print(helper())


__author__ = 'twolf'

import urllib
import json

"""
Retrieves chilean ip from ripe website
"""
print("running asnRipe.py")

urlCL = "https://stat.ripe.net/data/country-resource-list/data.json?resource=CL"
web = urllib.urlopen(urlCL)
json_data = json.load(web)

ipv4 = json_data["data"]["resources"]["asn"]

output = "chilean_asn1.csv"
fo = open(output, 'w')

for ip in ipv4:
    fo.write(ip+"\n")

print("asnRipe.py script finished")
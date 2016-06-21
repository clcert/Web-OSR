import requests
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

print('running ipScrapePerAsn.py')
url_base = 'http://ipinfo.io/'
as_base = 'AS'

output = open('ip_per_asn1.csv', 'w')
with open('chilean_asn1.csv') as f:
    lines = f.read().splitlines()
    for asn in lines:
        ASN = as_base + asn
        page = requests.get(url_base+ASN)
        html_doc = page.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        for link in soup.find_all('a'):
            if asn in link.get('href'):
                auxstring = '/'+as_base+asn+'/'
                line = re.sub(auxstring, '', link.get('href'))
                printstring = asn+','+line+'\n'
                if 'AS' not in printstring:
                    output.write(printstring)

print('ipScrapePerAsn.py script finished')


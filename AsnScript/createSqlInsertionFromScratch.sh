#!/bin/bash
echo "full script should run under 5 minutes"
echo "setting up virtualenv"
virtualenv -p /usr/bin/python2.7 LoadAsnEnv
source LoadAsnEnv/bin/activate
pip install -r requirements.txt
python asnRipe.py
python ipScrapePerAsn.py
python write_cymru_bulk.py
echo "running bulk whois"
time nc6 whois.cymru.com 43 < bulkWhoisInput.txt > asn_names.txt
echo "bulk whois finished"
python group_asns_to_names.py
python group_blocks.py
python group_asn_name_blocks.py
python create_tableinsertion.py

echo "uninstalling dependencies"
pip uninstall -r requirements.txt -y -y
echo "removing virtualenv"
rm -r LoadAsnEnv/
shopt -s extglob
rm !(*.py|*.sql|*.sh|requirements.txt)
shopt -u extglob
echo "work finished, final file is insert_asn_data.sql"
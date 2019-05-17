#!/usr/bin/python3
import re
import subprocess
import sys

import bs4
import requests

download_pattern = ''  # any
xml_uri = r'https://rarbg.to/rssdd.php?categories=14;48;17;44;45;47;50;51;52;42;46'  # rarbg movies
DELIMITER_LEN = 3  # assuming 'dn=' is del

if len(sys.argv) > 1:
    download_pattern = sys.argv[1]
    if len(sys.argv) > 2:
        xml_uri = sys.argv[2]


def downloadMagnet(maglink):
    subprocess.Popen(['xdg-open', maglink],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)


res = requests.get(xml_uri)
try:
    res.raise_for_status()
except Exception as e:
    print("couldn't open {}.\nError: {}".format(xml_uri, e))

soup = bs4.BeautifulSoup(res.text, features="xml")

links = []
for item in soup.find_all('item'):
    link = item.find('link')
    if re.search(download_pattern, link.text):
        links.append(link.text)

for link in links:
    textlink = (link.split('&')[1])[DELIMITER_LEN:]
    inp = input('Download "%s"? ' % textlink)
    if inp.lower() == 'y':
        downloadMagnet(link)

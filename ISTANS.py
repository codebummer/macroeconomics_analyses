from urllib.request import urlopen
from urllib.parse import urlencode
import pandas as pd
import json
import re

# url = 'http://www.istans.or.kr/su/newSuTab.do?scode=S105'
url = 'http://olympus.realpython.org/profiles/poseidon'
with urlopen(url) as response:
    byte_object = response.read()
html = byte_object.decode('utf-8')

title_index = html.find('<title>')
start_index = title_index + len('<title>')
end_index = html.find('</title>')
title = html[start_index:end_index]
print(title_index, start_index, end_index, title)

urlopen(url).read().decode('utf-8')
re.findall('ab*c', 'ABC', re.IGNORECASE)
re.search('ab*c', 'ABC', re.IGNORECASE).group()

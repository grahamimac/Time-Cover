# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup
import unicodedata
import requests
from collections import Counter

url = 'https://en.wikipedia.org/wiki/List_of_covers_of_Time_magazine'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
links = [a['href'] for a in soup.find('div', {'id':'mw-content-text'}).find('ul').find_all('a')]

base_url = 'https://en.wikipedia.org'
names = []
for i in range(len(links)):
	r = requests.get(base_url + links[i])
	soup = BeautifulSoup(r.text, 'lxml')
	if i < 7:
		all_links = soup.find('div', {'id':'mw-content-text'}).find_all('div', {'class':'div-col'})
		a = []
		for j in all_links:
			a += [k.text for k in j.find('ul').find_all('a') if k.find('img') is None]
		names += a
	else:
		all_links = soup.find('div', {'id':'mw-content-text'}).find_all('table', {'class':'wikitable'})
		a = []
		for table in all_links:
			rows = table.find_all('tr')
			for row in rows[1:]:
				col = row.find_all('td')
				if i < 9:
					if len(col) > 1:
						a += [j.text for j in col[1].find_all('a')]
				else:
					if len(col) > 0:
						a += [j.text for j in col[0].find_all('a')]
		names += a

names = [unicodedata.normalize('NFD', name.replace('\n','').replace("'s","")).encode('ascii', 'ignore') for name in names]
data = pd.DataFrame(Counter(names).items(), columns=["Person", "Time Covers"])
data.sort_values(["Time Covers", "Person"], ascending=[False, True]).to_csv('Time_Covers.csv', index = False)

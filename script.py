import csv
import re
import sys
import urllib.request
from bs4 import BeautifulSoup

pattern_one = re.compile('(?:{{[Uu][Rr][Ll]\|(.*)}})|(?:homepage\W*=\W*\[(.*)\])')
pattern_two = re.compile('(?:url\W*=\W*(.*))')
wiki_links = []
site_links = []
file = sys.argv[1]
with open(file, newline='') as readfile:
	reader = csv.reader(readfile, delimiter=' ')
	for company in reader:
		wiki_links.append(company[0])
		title = company[0].split('/')[-1]
		title = title.replace('.', '%2E')
		soup = BeautifulSoup(urllib.request.urlopen('https://en.wikipedia.org/w/index.php?title=' +  title + '&action=raw'), 'html.parser')
		text = soup.get_text()
		soup = BeautifulSoup(urllib.request.urlopen(company[0]), 'html.parser')
		sites = soup.find('table', attrs={'class':'infobox'}).find_all('a', attrs={'rel':'nofollow'})
		if len(sites)>1:
			 link = pattern_one.search(text)
			 if link != None:
			 	site = link.group().split(" ")
			 	site_link = site[-1].split('|')[-1]
			 	signs = "[]{}"
			 	for char in signs:
			 		site_link = site_link.replace(char, '')
			 	site_links.append(site_link)
			 else:
			 	link = pattern_two.search(text)
			 	if link != None:
			 		site = link.group().split(" ")
			 		site_link = site[-1].split('|')[-1]
			 		signs = "[]{}"
			 		for char in signs:
			 			site_link = site_link.replace(char, '')
			 		site_links.append(site_link)
		else:
			site_links.append(sites[0].get('href'))

data = []
with open('wikipedia_answers.csv', 'w', newline='') as writefile:
    writer = csv.writer(writefile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    data_rows = []
    for index in range(len(wiki_links)):
    	pairs = [wiki_links[index], site_links[index]]
    	data_rows.append(pairs)
    writer.writerows(data_rows)	

print('Process succesfully complete.')
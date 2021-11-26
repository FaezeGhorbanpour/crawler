
from bs4 import BeautifulSoup
import requests

languages = list()
books = dict()
country = list()

def book_page_crawl(url):
	response = requests.get(url)
	parser = BeautifulSoup(response.content, 'html.parser')
	book_dict = dict()
	infobox = parser.find('table', {'class':'infobox'})
	trs = infobox.find_all('tr')
	for tr in trs:
		th = tr.find('th')
		if th:
			if th.text == 'Country':
				td = tr.find('td').text
				if td not in country:
					country.append(td)
				book_dict['hasCountry'] = country.index(td)




def book_list_crawl(url):
	response = requests.get(url)
	parser = BeautifulSoup(response.content, 'html.parser')
	parent_table = parser.find('div', {'class':'mw-parser-output'})
	book_tables = parent_table.find_all('table', {'class':'wikitable'})
	for table in book_tables:
		trs = table.find_all('tr')
		book_dict = dict()
		for tr in trs[1:]:
			tds = tr.find_all('td')
			book_dict['HasName'] = tds[0].find('a').text
			if tds[2].text not in languages:
				languages.append(tds[2].text)
			book_dict['BookHasLanguage'] = languages.index(tds[2].text)
			book_url = base_url + tds[0].find('a').get('href')
			print(book_url)
			# extra_information = book_page_crawl(book_url)
			# book_dict = book_dict.update(extra_information)
			# books[book_url] =book_dict

			author_td = tds[1]

first_url = 'https://en.wikipedia.org/wiki/List_of_best-selling_books'
base_url = 'https://en.wikipedia.org'
# for book in book_list:
def crawler(first_url):
	book_list_crawl(first_url)


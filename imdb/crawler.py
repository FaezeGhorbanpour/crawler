from urllib.request import urlopen
from bs4 import BeautifulSoup




def movies_list_crawler(url, movies_number):
	page = '?page='
	all_movies = list()
	for i in range(1, movies_number // 100 + 1):
		response = urlopen(url + page + str(i))
		soup = BeautifulSoup(response, 'lxml')
		list_film = soup.find_all('div', {'class': 'lister-item'})
		for film in list_film:
			header = film.find('h3', {'class': 'lister-item-header'})
			href = base_url + header.find('a')['href']
			all_movies.append(movie_crawler(href))

def cast_crawler(url):
	cast_information = dict()
	return cast_information

def movie_crawler(url):
	response = urlopen(url)
	soup = BeautifulSoup(response, 'lxml')
	movie_information = dict()
	title_wrapper = soup.find('div', {'class': 'title_wrapper'})
	title = title_wrapper.find('h1')
	year = title.find('span')
	movie_information['hasName'] = title.text
	movie_information['hasReleasedDate'] = year.text

	ratings_wrapper = soup.find('div', {'class': 'title_wrapper'})
	rating = ratings_wrapper.find('strong').text
	movie_information['is_worked_by'] = cast_crawler(url)














def crawler(first_url):
	# base_url = 'https://www.imdb.com'
	# first_url = 'https://www.imdb.com/list/ls005750764/'
	movies_list_crawler(first_url, 200)



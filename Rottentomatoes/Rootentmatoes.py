import traceback

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import json


def clean(str):
    return str.replace('\n', '').replace('  ', '')


j = 144


def save_in_file(film):
    global j
    with open('films/' + str(j) + '.json', 'w') as outfile:
        json.dump(film, outfile)
    j += 1


def parse_cast_page(url):
    browser.get(url)
    cast_info = dict()
    cast_page = BeautifulSoup(browser.page_source, 'html.parser')
    if cast_page.find_all('div', class_='celebHeroImage'):
        cast_info['img'] = cast_page.find_all('div', class_='celebHeroImage')[0].get('style', None).split("'")[1]
        name = cast_page.find_all('h1', class_="bottom_divider")[0].text.split()
        cast_info['first_name'] = name[0]
        if len(name) > 1:
            cast_info['last_name'] = name[-1]
        metas = cast_page.find_all('div', class_='celeb_bio_row')
        for m in metas[2:]:
            m_info = clean(m.select('span')[0].text.replace(':', ''))
            cast_info[m_info] = clean(clean(m.text).split(':')[1])

    return cast_info


def parse_film_page(url):
    browser.get(url)
    film_page = BeautifulSoup(browser.page_source, 'html.parser')
    film_info = dict()
    title_year = clean(film_page.find_all('h1', id='movie-title')[0].text).split('(')
    film_info['title'] = title_year[0]
    film_info['year'] = title_year[1][:-1]
    film_info['summary'] = clean(film_page.find_all('div', id='movieSynopsis')[0].text)
    metas = film_page.find_all('li', class_='meta-row')
    for m in metas:
        m_info = m.select('div')
        if m_info[0].text.__contains__('Genre'):
            film_info[m_info[0].text[:-2]] = re.findall(r"[\w']+", m_info[1].text)
        else:
            film_info[m_info[0].text[:-2]] = clean(m_info[1].text)
    cast = film_page.find_all('div', class_='cast-item')

    film_info['crew'] = list()
    for c in cast:
        cast_page_url = c.select_one("a").get('href', None)
        film_info['crew'].append(parse_cast_page(base_url + cast_page_url))
    print(film_info)
    save_in_file(film_info)


def crawler(main_url):
    # main_url = "https://www.rottentomatoes.com/browse/dvd-streaming-all/"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    main_browser = webdriver.Chrome(options=options)
    browser = webdriver.Chrome(options=options)

    main_browser.get(main_url)
    main_browser.implicitly_wait(10)
    i = 144
    offset = 144
    while True:
        try:
            soup = BeautifulSoup(main_browser.page_source, 'html.parser')
            films_url = list()
            for film in soup.find_all('div', class_='mb-movie'):
                films_url.append(film.select_one("div a").get('href', None))
            base_url = "https://www.rottentomatoes.com"
            for k in range(offset, len(films_url)):
                url = films_url[k]
                i += 1
                print(k, url)
                parse_film_page(base_url + url)
            offset = i
            main_browser.find_element_by_class_name("mb-load-btn").click()
        except Exception as e:
            browser.quit()
            main_browser.quit()
            print("type error: " + str(e))
            print(traceback.format_exc())

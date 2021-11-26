from Rottentomatoes.Rootentmatoes import crawler
from goodreads.crawler import crawler
from imdb.crawler import crawler

if __name__ == '__main__':
    first_url = ''
    crawler(first_url)
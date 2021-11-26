offset = 0
while True:
    offset += 32
    base_expand_url = "http://rt-client-facade-prod.aws.prod.flixster.com/movie?expand=true&include=%5B%22movieSupplementaryInfo%22%2C%22audienceSummary%22%2C%22affiliates%22%2C%22criticSummary%22%2C%22moviePersonnel%22%2C%22moviePersonnel.actors%22%2C%22moviePersonnel.actors.person%22%5D&filter=%7B%22search%22%3A%7B%22mpaa-rating-min%22%3A%22G%22%2C%22release-year-max%22%3A2018%2C%22filter-release-date%22%3A%22false%22%2C%22offset%22%3A" + str(
        offset) + "%2C%22services%22%3A%5B%22amazon%22%2C%22hbo_go%22%2C%22itunes%22%2C%22netflix_iw%22%2C%22vudu%22%2C%22amazon_prime%22%2C%22fandango_now%22%5D%2C%22sort%22%3A%22DVD_RELEASE_DATE_DESC%22%2C%22distribution%22%3A%22ANY%22%2C%22tomatometer-min%22%3A0%2C%22mpaa-rating-max%22%3A%22UN%22%2C%22release-day-of-month-max%22%3A31%2C%22limit%22%3A32%2C%22release-month-max%22%3A12%2C%22tomatometer-max%22%3A100%2C%22use-dvd-date%22%3Atrue%2C%22status%22%3A%22LIVE%22%7D%7D"
    list_page = requests.get(base_expand_url)
    print(list_page)

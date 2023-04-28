# config.py

# Base URL for IMDb search
IMDB_URL = "https://www.imdb.com/find?q={}"
IMDB_BASE_URL = "https://www.imdb.com"
IMDB_MOVIE_BASE_URL = "https://www.imdb.com/title/"
IMDB_SUMMARY_SUFFIX = "/plotsummary?ref_=tt_stry_pl"

# HTTP headers for requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
}

# Class names that might change in the future
CLASS_NAME_MOVIE = "ipc-metadata-list-summary-item__t"
CLASS_NAME_SUMMARY = 'ipc-metadata-list-item__content-container'

# Filename for saving plot summaries
FILENAME = "{}.txt"

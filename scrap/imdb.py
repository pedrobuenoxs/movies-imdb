#imbdb.py

import requests
from scrap import scrap_config
from bs4 import BeautifulSoup

HEADERS = scrap_config.HEADERS

def get_user_input():
    film_name = input("Enter the name of a movie: ")
    film_name = film_name.replace(" ", "+")
    return film_name

def get_response(url):
    print(f"Retrieving page: {url}")
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return None

def get_movies(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    class_elements = soup.find_all('a', class_=scrap_config.CLASS_NAME_MOVIE)
    movies = []

    for a in class_elements:
        if 'title' in a['href']:
            movies.append({
                'name': a.text,
                'link': scrap_config.IMDB_BASE_URL + a['href'],
                'title_code': a['href'].split('/')[2],
                'summary': scrap_config.IMDB_MOVIE_BASE_URL +a['href'].split('/')[2]+ scrap_config.IMDB_SUMMARY_SUFFIX,
            })
    return movies

def print_movies(movies):
    print("Movies:")
    for i, movie in enumerate(movies, start=1):
        print(f"{i}. {movie['name']}")

def get_user_choice(movies):
    choice = input("\nChoose a movie or actor by entering the corresponding number, or 'q' to quit: ")

    if choice.lower() != 'q':
        choice = int(choice)
        if choice <= len(movies):
            print(f"You chose the movie: {movies[choice - 1]['name']} - {movies[choice - 1]['link']}\n")
            return movies[choice - 1]
    return None

def save_to_txt(movie_name, text, text_type):
    filename = scrap_config.FILENAME.format(movie_name)
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"Movie Name: {movie_name}\n")
        file.write(f"{text_type}:\n")
        file.write(text)
        print(f"Saved to {filename}")
        file.write("\n-------------------------\n")

def get_scrapped_data(response, chosen_movie):
    soup = BeautifulSoup(response.text, 'html.parser')
    summaries = soup.find_all('div', class_=scrap_config.CLASS_NAME_SUMMARY)
    print("Plot Summary:")
    for i, summary in enumerate(summaries):
        text = summary.get_text(separator=' ', strip=True)
        print(text)
        print("-------------------------")
        if i == len(summaries) - 1:  # if it's the last summary
            save_to_txt(chosen_movie['name'], text, "Synopsis")  # Save as a Synopsis
        else:
            save_to_txt(chosen_movie['name'], text, "Plot Summary")  # Save as a Plot Summary


def run():
    film_name = get_user_input()
    response = get_response(scrap_config.IMDB_URL.format(film_name))
    if response:
        movies = get_movies(response)
        print_movies(movies)
        chosen_movie = get_user_choice(movies)
        if chosen_movie:
            summary_response = get_response(chosen_movie['summary'])
            if summary_response:
                get_scrapped_data(summary_response, chosen_movie)

if __name__ == "__main__":
    run()


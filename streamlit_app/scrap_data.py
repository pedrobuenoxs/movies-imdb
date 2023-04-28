import streamlit as st
from scrap import imdb
from scrap import scrap_config

def main():
    st.title("Welcome to the Movie Scraping App!")

    if 'movies' not in st.session_state:
        st.session_state['movies'] = []
    if 'chosen_movie' not in st.session_state:
        st.session_state['chosen_movie'] = None

    film_name = st.text_input("Enter the name of a movie:")

    if st.button("Search"):
        if film_name:
            print(film_name)
            res = imdb.get_response(scrap_config.IMDB_URL.format(film_name))
            if res:
                st.session_state['movies'] = imdb.get_movies(res)

    # Call get_user_choice() outside of the button click event
    if st.session_state['movies']:
        movie_options = ["Select a movie..."] + [movie['name'] for movie in st.session_state['movies']]
        choice = st.selectbox("Choose a movie:", movie_options)

        if choice != "Select a movie...":
            for movie in st.session_state['movies']:
                if movie['name'] == choice:
                    st.write(f"You chose the movie: {movie['name']} - {movie['link']}\n")
                    st.session_state['chosen_movie'] = movie
                    print(st.session_state['chosen_movie'])
                    break

    if st.session_state['chosen_movie']:
        if st.button("Get Data"):
            summary_response = imdb.get_response(st.session_state['chosen_movie']['summary'])
            if summary_response:
                print(summary_response)
                print(st.session_state['chosen_movie'])
                imdb.get_scrapped_data(summary_response, st.session_state['chosen_movie'])
        else:
            st.write("Please select a movie.")

if __name__ == "__main__":
    main()

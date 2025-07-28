import requests
import streamlit as st
import pickle
import pandas as pd

# Fetch poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e1559cd35986c07898f69dda99299bc9&language=en-US"
    )
    data = response.json()
    return "http://image.tmdb.org/t/p/w500" + data['poster_path']  # ✅ fixed key: 'poster_path'

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sim[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # ✅ get movie_id from DataFrame
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
sim = pickle.load(open('sim.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommendation System')

option = st.selectbox(
    'Give me a Movie for the Suggestion',
    movies['title'].values
)

if st.button('Recommend Movies'):
    names, posters = recommend(option)

    # Create 5 columns for 5 movie suggestions
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

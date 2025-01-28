import streamlit as st
import pickle 
import pandas as pd
import requests

def fetch_poster(movie_id):
   url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

   headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZWE4YjJjNWZhNDZjMWIzODAzZTEzNTVhZjAxNjcxMCIsIm5iZiI6MTczNjcwODA4Ni40OTgsInN1YiI6IjY3ODQwZmY2OTBmNDJjMzI4MzdiNDcyZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tbZCrMVRbjepcTo7gL8tbiVhOYCUE8yC6eV1OLT_kF4"
    }

   response = requests.get(url, headers=headers).json()
   return "https://image.tmdb.org/t/p/w500/"+response['poster_path']
  

def recommend(movie):
  #find the indexes of the movies
  movie_index=movies[movies['title']==movie].index[0]
  distances=similarity[movie_index]
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
  
  recommended_movies=[]
  recommended_movies_posters=[]
  for i in movies_list:
    movie_id=movies.iloc[i[0]]['id']
    recommended_movies.append(movies.iloc[i[0]].title)
    #fetch poster from api
    recommended_movies_posters.append(fetch_poster(movie_id))
  return recommended_movies,recommended_movies_posters

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
option=st.selectbox('Select a movie',movies['title'].values)

if st.button('Recommend'):
    names,posters=recommend(option)
    cols=st.columns(5)
    for col,name,poster in zip(cols,names,posters):
       with col:
          st.text(name)
          st.image(poster)
    
       
    

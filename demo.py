import streamlit as st
import pickle
import pandas as pd
import urllib.parse
import requests
import os

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def get_fallback_poster(movie_title, genre=None):
    try:
        color_map = {
            'action': '#FF6B6B',
            'comedy': '#4ECDC4', 
            'drama': '#45B7D1',
            'horror': '#8B0000',
            'romance': '#FF69B4',
            'thriller': '#2C3E50',
            'adventure': '#F39C12',
            'animation': '#9B59B6',
            'crime': '#34495E',
            'fantasy': '#8E44AD',
            'mystery': '#7F8C8D',
            'sciencefiction': '#3498DB',
            'default': '#95A5A6'
        }
        if genre is None:
            try:
                movie_row = movies[movies['title'] == movie_title]
                if not movie_row.empty:
                    genres = movie_row['genres'].iloc[0].lower()
                    for g in color_map.keys():
                        if g in genres:
                            genre = g
                            break
            except Exception:
                pass
        
        color = color_map.get(genre, color_map['default'])
        
        poster_html = f"""
        <div style="
            width: 100%;
            height: 400px;
            background: linear-gradient(45deg, {color}, {color}AA);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            padding: 20px;
            box-sizing: border-box;
        ">
            <div>
                🎬<br>
                {movie_title[:50]}{'...' if len(movie_title) > 50 else ''}
            </div>
        </div>
        """
        return poster_html
    except Exception:
        return f'<div style="width:100%;height:400px;background:#ccc;display:flex;align-items:center;justify-content:center;">🎬 {movie_title}</div>'

def fetch_poster(movie_id, movie_title=None, use_fallback=True):
    if not use_fallback:
        url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
        headers = {
            "accept": "application/json",
            "Authorization": os.getenv("API_TOKEN")
        }
        try:
            response = requests.get(url, headers=headers, timeout=3).json()
            if 'poster_path' in response and response['poster_path']:
                return "https://image.tmdb.org/t/p/w500/" + response['poster_path']
        except Exception:
            pass
    
    if movie_title:
        return get_fallback_poster(movie_title)
    else:
        return get_fallback_poster(f"Movie ID: {movie_id}")

def build_wikipedia_link(title):
    return f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"

def recommend(movie=None, era=None, genre=None):
    if movie:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:31]
        
        recommended_df = movies.iloc[[i[0] for i in movies_list]].copy()
        recommended_df['similarity_score'] = [i[1] for i in movies_list]
    else:
        recommended_df = movies.copy()
    

    if era:
        if era == '2010 and above':
            recommended_df = recommended_df[recommended_df['release_year'] >= 2010]
        elif era == '2000-2009':
            recommended_df = recommended_df[(recommended_df['release_year'] >= 2000) & (recommended_df['release_year'] <= 2009)]
        elif era == '1990-1999':
            recommended_df = recommended_df[(recommended_df['release_year'] >= 1990) & (recommended_df['release_year'] <= 1999)]
        elif era == 'Before 1990':
            recommended_df = recommended_df[recommended_df['release_year'] < 1990]
    

    if genre and genre.lower() != 'all':
        recommended_df = recommended_df[recommended_df['genres'].str.contains(genre.lower(), na=False)]
    
    if movie:
        recommended_df = recommended_df.sort_values('similarity_score', ascending=False)
    
    top_movies = recommended_df.head(9)
    movie_titles = top_movies['title'].tolist()
    movie_ids = top_movies['id'].tolist()
    
    return movie_titles, movie_ids, top_movies

st.title("🎬 CineMatch - Movie Recommender")

demo_mode = st.sidebar.checkbox("🚀 Demo Mode (Offline Friendly)", value=True, 
                               help="Enable this for reliable demo without external API dependencies")

if demo_mode:
    st.sidebar.info("ℹ️ Demo mode enabled - using generated posters for reliable presentation")

option = st.selectbox('📽️ Choose a movie', ['None'] + sorted(movies['title'].unique()), index=0)

era = st.selectbox('🕰️ Filter by Release Year', ['All', '2010 and above', '2000-2009', '1990-1999', 'Before 1990'])

genre = st.selectbox('🎭 Filter by Genre', ['All', 'action', 'adventure', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'family', 'fantasy', 'foreign', 'history', 'horror', 'music', 'mystery', 'romance', 'sciencefiction', 'thriller', 'tvmovie', 'war', 'western'])

selected_movie = None if option == 'None' else option
era = None if era == 'All' else era
genre = None if genre == 'All' else genre

if st.button('🎯 Get Recommendations'):
    with st.spinner('Finding perfect movies for you...'):
        titles, movie_ids, movies_data = recommend(selected_movie, era, genre)
        
        if not titles:
            st.warning("No movies found with the selected filters. Please try different filters.")
        else:
            st.subheader("🌟 Recommended Movies:")
            
            for i in range(0, len(titles), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(titles):
                        with cols[j]:
                            movie_title = titles[i + j]
                            movie_id = movie_ids[i + j]                            
                            if demo_mode:
                                poster_html = fetch_poster(movie_id, movie_title, use_fallback=True)
                                st.markdown(poster_html, unsafe_allow_html=True)
                            else:
                                poster_url = fetch_poster(movie_id, movie_title, use_fallback=False)
                                if poster_url.startswith('http'):
                                    st.image(poster_url, use_column_width=True)
                                else:
                                    st.markdown(poster_url, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Project Features")
st.sidebar.markdown("""
- **Content-Based Filtering**: Uses movie similarity matrix
- **Multi-Filter Support**: Filter by era, genre, or both
- **Offline Capability**: Works without external APIs
- **Responsive Design**: Clean, modern interface
- **Wikipedia Integration**: Links to movie information
""")

st.sidebar.markdown("### 🛠️ Technical Stack")
st.sidebar.markdown("""
- **ML**: Scikit-learn, Pandas, NumPy
- **Frontend**: Streamlit
- **Data**: TMDB 5000 Movies Dataset
- **Similarity**: Cosine similarity on movie features
""")

if demo_mode:
    st.sidebar.success("✅ Using demo mode!")
else:
    st.sidebar.warning("⚠️ Requires VPN in India for TMDB API")
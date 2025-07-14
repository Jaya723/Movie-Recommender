# CineMatch - Movie Recommender 

##Note: The TMBD site is blocked for several ISP in India. Therefore this application consits of a demo mode which will work even if the api is blocked. If not able to run the code using API please enable the Demo Mode(Will show custom made posters for the movies)
## Project Overview
CineMatch is content-based movie recommendation system that suggests similar movies based on user selection. This project leverages natural language processing techniques to analyze movie metadata and generate personalized recommendations through a user-friendly Streamlit interface with various filtering options like filter by movie era and there genres.

## Features
- **Content-Based Filtering**: Recommends movies similar to user selection based on movie content (genres, keywords, cast, crew, overview)
- **Interactive UI**: Clean and intuitive Streamlit interface allowing users to select movies and view recommendations
- **Multifiltering**: Multiple filtering options like filter by movie era and genres.
- **Text Processing**: Implements NLP techniques including stemming and vectorization to process movie descriptions
- **Similarity Computation**: Uses cosine similarity to find movies with similar content characteristics
- **Demo Mode(by default enabled)**: This mode can be disabled from the sidebar of the UI when TMDB API is working for the IP address.

## Technical Implementation
### Data Processing Pipeline
1. **Data Acquisition**: Utilized the TMDB 5000 Movie Dataset and TMDB 5000 Credicts Dataset containing detailed information on around 5000 movies
2. **Data Cleaning**: Handled missing values and merged the two datasets on title
3. **Feature Extraction**:
   - Extracted relevant features from nested JSON structures
   - Parsed movie genres, keywords, cast, and crew information
4. **Text Processing**:
   - Applied stemming to reduce words to their root form
   - Removed stop words to focus on meaningful content
5. **Vectorization**: Converted processed text to numerical vectors using CountVectorizer 
6. **Similarity Calculation**: Computed cosine similarity between movie vectors

### Recommendation Algorithm
The system recommends movies by:
1. Find the index of the movie selected by the user from the dataset.
2. Retrieve the precomputed similarity scores between the selected movie and all other movies using cosine similarity on content tags.
3. Sort all movies in descending order based on similarity to the selected movie.
4. Apply Filters (Optional)
   -If selected, filter the recommended movies by:
     -Release year/era (e.g., 2010 and above, 1990s)
     -Genre (e.g., action, comedy
6. Return the top 9 most relevant and filtered movies as recommendations.

## Technologies Used
- **Python**: Primary programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical operations
- **NLTK**: Natural language processing and text manipulation
- **Scikit-learn**: Machine learning tools for vectorization and similarity calculation
- **Streamlit**: Web application framework for creating the user interface

## Future Enhancements
- Deploy the application to a cloud platform for wider accessibility
- Implement a hybrid recommendation system combining content-based and collaborative filtering approaches

## Dataset
The project uses the TMDB 5000 Movie Dataset, which includes:
- `tmdb_5000_movies.csv`: Contains movie metadata including genres, keywords, and overview
- `tmdb_5000_credits.csv`: Contains cast and crew information for each movie

##Link for downloading the datasets
- https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_credits.csv

##STEPS TO RUN THE APPLICATION
1. Go on the datasets link provided above and download the datasets from here.
2. Go to the collab notebook link given and upload the datasets there. Run the notebook and download the pkl files from there. @ pkl files will be created.(Couldn't upload on github due large file size)
3. Clone the repo in any of the editor of your choice and add the pkl files in it.
4. Download the requirements.txt by executng the command pip install -r requirements.txt
5. Create a .env file which will contain your API token generated from the TMDB site. Put that token in the .env file under the variable name API_TOKEN.
6. Save all the files and now run the application by excuting the command streamlit run demo.py.
7. Note: If you coudn't access the TMDB API results(posters) try using a VPN. Otherwise enable the Demo Mode(already enabled by default) to see the results without calling the API.
8. I have added the video regarding it please check it out.

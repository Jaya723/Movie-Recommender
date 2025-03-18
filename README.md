# Movie Recommender System

## Project Overview
A content-based movie recommendation system that suggests similar movies based on user selection. This project leverages natural language processing techniques to analyze movie metadata and generate personalized recommendations through a user-friendly Streamlit interface.

## Features
- **Content-Based Filtering**: Recommends movies similar to user selection based on movie content (genres, keywords, cast, crew, overview)
- **Interactive UI**: Clean and intuitive Streamlit interface allowing users to select movies and view recommendations
- **Text Processing**: Implements NLP techniques including stemming and vectorization to process movie descriptions
- **Similarity Computation**: Uses cosine similarity to find movies with similar content characteristics

## Technical Implementation
### Data Processing Pipeline
1. **Data Acquisition**: Utilized the TMDB 5000 Movie Dataset containing detailed information on 5000 movies
2. **Data Cleaning**: Handled missing values and standardized data formats
3. **Feature Extraction**:
   - Extracted relevant features from nested JSON structures
   - Parsed movie genres, keywords, cast, and crew information
   - Limited cast information to top 5 actors per movie for optimal results
4. **Text Processing**:
   - Tokenized text data
   - Applied stemming to reduce words to their root form
   - Removed stop words to focus on meaningful content
5. **Vectorization**: Converted processed text to numerical vectors using CountVectorizer
6. **Similarity Calculation**: Computed cosine similarity between movie vectors

### Recommendation Algorithm
The system recommends movies by:
1. Identifying the index of the selected movie
2. Retrieving the similarity scores between the selected movie and all others
3. Sorting movies by similarity score
4. Returning the top 5 most similar movies

## Technologies Used
- **Python**: Primary programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical operations
- **NLTK**: Natural language processing and text manipulation
- **Scikit-learn**: Machine learning tools for vectorization and similarity calculation
- **Streamlit**: Web application framework for creating the user interface

## Future Enhancements
- Add movie posters and additional metadata to enhance the user experience
- Deploy the application to a cloud platform for wider accessibility
- Implement a hybrid recommendation system combining content-based and collaborative filtering approaches

## Dataset
The project uses the TMDB 5000 Movie Dataset, which includes:
- `tmdb_5000_movies.csv`: Contains movie metadata including genres, keywords, and overview
- `tmdb_5000_credits.csv`: Contains cast and crew information for each movie



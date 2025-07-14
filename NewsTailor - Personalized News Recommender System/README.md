# NewsTailor - Personalized News Recommender System

## Overview

The **Personalized News Recommender System** is an intelligent application designed to curate news articles tailored to individual user preferences using advanced machine learning techniques. By learning from user interactions (likes/dislikes), the system delivers a personalized news consumption experience, ensuring users see content that aligns with their interests.

## Key Features

### 1. Smart News Curation
- **Personalized Recommendations**: Utilizes collaborative filtering to suggest articles based on your reading history.
- **Diversity Control**: Adjustable slider to balance between similar recommendations and diverse suggestions.
- **Category Filtering**: Browse news by specific categories such as business, technology, science, and more.

### 2. Comprehensive User Profile Analysis
- **Visual Analytics**:
  - Interactive charts displaying liked/disliked categories.
  - Word clouds highlighting keywords in preferred articles.
  - Time-based analysis of reading patterns.
- **Detailed Statistics**:
  - Number of liked/disliked articles.
  - Category distribution percentages.
  - Source preferences.

### 3. Advanced Content Processing
- **Natural Language Processing**:
  - Text cleaning and preprocessing.
  - TF-IDF vectorization for content analysis.
  - Keyword extraction to understand user preferences.
- **Image Validation**: Automatically checks and displays valid article images.

### 4. Data Management
- **Secure User Sessions**: Unique user IDs with persistent preferences.
- **Data Export**: Download your complete reading history as CSV or JSON.
- **Reset Functionality**: Clear your preferences at any time.

### 5. Technical Robustness
- **Error Handling**: Comprehensive logging and user-friendly error messages.
- **Performance Optimization**: Caching for faster loading times.
- **API Integration**: Connects with [NewsAPI](https://newsapi.org/) for fresh content.

## How It Works

1. **Initialization**:
   - Users provide their NewsAPI key.
   - The system fetches current news across multiple categories.
   - Articles are preprocessed (cleaning, tokenization, vectorization).

2. **User Interaction**:
   - Browse articles and mark preferences (like/dislike).
   - The system updates the user profile with each interaction.
   - The recommendation engine continuously refines suggestions.

3. **Recommendation Engine**:
   - Uses cosine similarity to find articles matching your profile.
   - Implements a diversity algorithm to prevent filter bubbles.
   - Combines content-based and collaborative filtering approaches.

4. **Profile Analysis**:
   - Aggregates reading patterns over time.
   - Identifies preferred topics and sources.
   - Visualizes preferences through interactive charts.

## Technical Implementation

### Backend
- **Python**: Core programming language.
- **Scikit-learn**: For machine learning algorithms.
- **NLTK**: For natural language processing.
- **NewsAPI**: Integration for fetching news content.
- **Streamlit**: Web application framework for the user interface.

### Algorithms
- **TF-IDF Vectorization**: Transforms text into numerical features.
- **Cosine Similarity**: Measures article similarity.
- **Nearest Neighbors**: Ensures diverse recommendations.
- **Word Clouds**: Visualizes textual patterns.

### Frontend
- Interactive dashboards with **Plotly** visualizations.
- Responsive design using **Streamlit** components.
- User-friendly interface with clear navigation.

## Why This Project Stands Out

1. **Personalization**: Understands nuanced user preferences beyond simple categorization.
2. **Transparency**: Provides detailed analytics to explain why articles are recommended.
3. **Control**: Offers fine-grained control over recommendation diversity.
4. **Insightful**: Delivers valuable analytics about reading habits.
5. **Portable**: Supports data export for external analysis.

## Practical Applications

- **Personal Use**: Curate a personalized news feed without algorithmic bias.
- **Media Companies**: Gain insights into reader preferences at an individual level.
- **Researchers**: Analyze news consumption patterns with exported data.
- **Learning Tool**: Serves as a practical example of applied machine learning.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/personalized-news-recommender.git
   cd personalized-news-recommender
   ```
2. **Install Dependencies: Ensure you have Python 3.8+ installed, then run:**
``` 
pip install -r requirements.txt
```
3. **Get a NewsAPI Key:**
 - Sign up at NewsAPI to obtain an API key.
 - Set the API key as an environment variable or input it when prompted by the application.
4. **Run the Application**
```
streamlit run app.py
```

## Usage

- Launch the application and enter your NewsAPI key.
- Browse news articles and mark them as liked or disliked.
- Use the diversity slider to adjust recommendation variety.
- Explore your profile analytics through interactive charts and word clouds.
- Export your reading history as CSV or JSON for further analysis.
- Reset preferences if desired to start fresh.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please open an issue on Github
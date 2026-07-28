# Movie Recommendation System (Collaborative Filtering)

An item-based collaborative filtering movie recommender system that pivots transactional user movie ratings into a user-item rating matrix, computes **Cosine Similarity** profiles between movies, and ranks recommendations.

## Features
- **Pivot Rating Matrix**: Converts flat ratings tables into a pivoted sparse matrix mapping user ratings.
- **Cosine Similarity Calculations**: Uses `scikit-learn` to calculate item-item similarity dimensions.
- **Top N Recommendations**: Generates ranked recommendation predictions excluding the query target movie.

## Project Structure
- `recommender.py`: Rating pivot builders, similarity engines, and recommendation functions.
- `main.py`: Command-line interface driver.
- `test_recommender.py`: Unit test suite verifying matrix pivots and cosine calculations.
- `ratings.csv`: Sample user ratings database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To get recommendations:
```bash
python main.py --input ratings.csv --movie "Toy Story" --limit 3
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_recommender.py
```

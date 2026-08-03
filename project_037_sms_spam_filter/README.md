# SMS Spam Filter (TF-IDF & Logistic Regression)

A Natural Language Processing (NLP) text classification pipeline that standardizes SMS text messages, builds a **TF-IDF sparse word matrix**, and trains a regularized **Logistic Regression** classifier to distinguish spam from ham (legitimate messages).

## Features
- **String Preprocessing**: Cleans messages by removing punctuation, lowercasing, and stripping whitespace.
- **Sparse TF-IDF Vectorization**: Extracts word features weighted by Term Frequency-Inverse Document Frequency (TF-IDF).
- **Binary Classification Pipeline**: Trains a `LogisticRegression` model with stratified training/testing splits and evaluates performance metrics.

## Project Structure
- `spam_filter.py`: String preprocessors, TF-IDF transformations, models training, and predictions.
- `main.py`: Command-line interface driver.
- `test_filter.py`: Unit test suite verifying text cleaning and classifications.
- `spam_sms.csv`: Sample SMS messages database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To fit models and run predictions:
```bash
python main.py --input spam_sms.csv --message "Win a free cash prize now!"
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_filter.py
```

from textblob import TextBlob
import random

def get_sentiment(feedback_list):
    sentiment_counts = {
        'Positive': 0,
        'Neutral': 0,
        'Negative': 0
    }

    for feedback in feedback_list:
        analysis = TextBlob(feedback)
        if analysis.sentiment.polarity > 0:
            sentiment_counts['Positive'] += 1
        elif analysis.sentiment.polarity == 0:
            sentiment_counts['Neutral'] += 1
        else:
            sentiment_counts['Negative'] += 1

    total_feedback = len(feedback_list)
    sentiment_percentages = {
        'Positive': (sentiment_counts['Positive'] / total_feedback) * 100,
        'Neutral': (sentiment_counts['Neutral'] / total_feedback) * 100,
        'Negative': (sentiment_counts['Negative'] / total_feedback) * 100
    }

    return sentiment_percentages

def sample_feedback(positive_file='positive.txt', negative_file='negative.txt'):
    with open(positive_file, 'r') as file:
        positive_feedback = [line.strip() for line in file.readlines()]
    with open(negative_file, 'r') as file:
        negative_feedback = [line.strip() for line in file.readlines()]

    # Sample 5 comments from each feedback list
    sample_positive = random.sample(positive_feedback, min(5, len(positive_feedback)))
    sample_negative = random.sample(negative_feedback, min(5, len(negative_feedback)))

    # Combine samples and calculate sentiment percentages
    feedback_samples = sample_positive + sample_negative
    return get_sentiment(feedback_samples)

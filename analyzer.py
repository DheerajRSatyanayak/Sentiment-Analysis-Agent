import praw
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import os
from dotenv import load_dotenv

load_dotenv()
nltk.download('vader_lexicon')

def analyze_sentiments(query, subreddit_name="all", limit=500):
    csv_sentiment_file = "data/reddit_sentiment.csv"
    csv_feedback_file = "data/reddit_feedback.csv"

    # Setup Reddit API
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "Itchy_Departure2341"),
    )

    posts = []
    for submission in reddit.subreddit(subreddit_name).search(query, limit=limit):
        posts.append({
            "title": submission.title,
            "selftext": submission.selftext,
            "score": submission.score,
            "url": submission.url,
            "num_comments": submission.num_comments,
            "created_utc": submission.created_utc
        })

    df = pd.DataFrame(posts)

    # Save fresh feedback CSV
    df.to_csv(csv_feedback_file, index=False)

    # Sentiment Analysis
    sia = SentimentIntensityAnalyzer()
    df['combined_text'] = df['title'].fillna('') + " " + df['selftext'].fillna('')

    def get_sentiment(text):
        if not isinstance(text, str):
            return "neutral"
        score = sia.polarity_scores(text)['compound']
        if score >= 0.05:
            return 'positive'
        elif score <= -0.05:
            return 'negative'
        else:
            return 'neutral'

    df['sentiment'] = df['combined_text'].apply(get_sentiment)

    # Save fresh sentiment CSV
    df.to_csv(csv_sentiment_file, index=False)

    # Calculate sentiment summary
    sentiment_counts = df['sentiment'].value_counts().to_dict()

    return {
        "status": "analyzed",
        "query": query,
        "posts": len(df),
        "details": f"Fetched and analyzed {len(df)} posts related to '{query}'.",
        "sentiment_breakdown": {
            "positive": sentiment_counts.get("positive", 0),
            "negative": sentiment_counts.get("negative", 0),
            "neutral": sentiment_counts.get("neutral", 0)
        }
    }

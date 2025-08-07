import pandas as pd
import requests
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

def check_and_alert(threshold=10):
    df = pd.read_csv("data/reddit_sentiment.csv")
    sentiment_counts = df['sentiment'].value_counts()
    total = len(df)
    negative_percent = (sentiment_counts.get('negative', 0) / total) * 100

    alert_sent = False
    details = f"Negative sentiment: {negative_percent:.2f}%"

    # Slack webhook URL from env or config
    slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    
    # Email credentials from env variables for security
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # your email, e.g., you@gmail.com
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # app password or real password
    EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")  # recipient email

    if negative_percent > threshold:
        # Send Slack alert
        slack_message = {"text": f"🚨 ALERT: {negative_percent:.2f}% of posts are negative!"}
        try:
            response = requests.post(slack_webhook_url, json=slack_message)
            if response.status_code == 200:
                alert_sent = True
                details += " (Slack alert sent)"
            else:
                details += f" (Slack alert failed: {response.text})"
        except Exception as e:
            details += f" (Slack alert exception: {e})"

        # Send Email alert
        if EMAIL_ADDRESS and EMAIL_PASSWORD and EMAIL_RECEIVER:
            msg = EmailMessage()
            msg["Subject"] = "⚠️ Alert: High Negative Sentiment Detected"
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = EMAIL_RECEIVER
            msg.set_content(f"""
            Hi,

            The percentage of negative Reddit posts has reached {negative_percent:.2f}%!

            Please check the sentiment analysis dashboard for details.

            Regards,
            Sentiment Analysis Agent
            """)

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.send_message(msg)
                alert_sent = True
                details += " (Email alert sent)"
            except Exception as e:
                details += f" (Email alert exception: {e})"
        else:
            details += " (Email alert skipped due to missing email config)"

    return {
        "status": "alert_checked",
        "negative_percent": round(negative_percent, 2),
        "alert_sent": alert_sent,
        "details": details
    }

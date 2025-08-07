from flask import Flask, request, jsonify
from analyzer import analyze_sentiments
from summarizer import summarize_posts
from alerter import check_and_alert

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    query = data.get("query")
    subreddit = data.get("subreddit")
    limit = data.get("limit")

    if not query or not subreddit or not limit:
        return jsonify({"error": "query, subreddit, and limit are required"}), 400

    result = analyze_sentiments(query=query, subreddit_name=subreddit, limit=limit)
    return jsonify(result)


@app.route("/summarize", methods=["POST"])
def summarize():
    # summarizer does not require input, but could be extended later
    summary = summarize_posts()
    return jsonify({'summary': summary})


@app.route("/alert", methods=["POST"])
def alert():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    threshold = data.get("threshold")
    if threshold is None:
        return jsonify({"error": "threshold is required"}), 400

    alert_result = check_and_alert(threshold=threshold)
    return jsonify(alert_result)


if __name__ == "__main__":
    app.run(debug=True)

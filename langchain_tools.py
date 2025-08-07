from typing import Optional
from langchain.tools import BaseTool


class AnalyzerTool(BaseTool):
    name: str = "Analyzer"
    description: Optional[str] = "Fetches Reddit data and performs sentiment analysis."

    def _run(self, query: str):
        from analyzer import analyze_sentiments
        return analyze_sentiments(query=query)


class SummarizerTool(BaseTool):
    name: str = "Summarizer"
    description: Optional[str] = "Summarizes analyzed Reddit posts."

    def _run(self):
        from summarizer import summarize_posts
        return summarize_posts()


class AlerterTool(BaseTool):
    name: str = "Alerter"
    description: Optional[str] = "Checks sentiment and sends an alert if required."

    def _run(self):
        from alerter import check_and_alert
        return check_and_alert()

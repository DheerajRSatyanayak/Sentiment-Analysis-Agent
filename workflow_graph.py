from typing import TypedDict
from analyzer import analyze_sentiments
from summarizer import summarize_posts
from alerter import check_and_alert
from langgraph.graph import StateGraph, END

class SentimentState(TypedDict):
    query: str
    analysis_result: dict
    summary_result: str
    alert_result: dict

def analyze_node(state: SentimentState):
    result = analyze_sentiments(query=state["query"])
    return {**state, "analysis_result": result}

def summarize_node(state: SentimentState):
    summary = summarize_posts()
    return {**state, "summary_result": summary}

def alert_node(state: SentimentState):
    alert = check_and_alert()
    return {**state, "alert_result": alert}

graph = StateGraph(SentimentState)
graph.add_node("analyze", analyze_node)
graph.add_node("summarize", summarize_node)
graph.add_node("alert", alert_node)
graph.set_entry_point("analyze")
graph.add_edge("analyze", "summarize")
graph.add_edge("summarize", "alert")
graph.add_edge("alert", END)

if __name__ == "__main__":
    app = graph.compile()
    initial_state = {"query": "Zepto delivery reviews"}
    final_state = app.invoke(initial_state)
    print(final_state)

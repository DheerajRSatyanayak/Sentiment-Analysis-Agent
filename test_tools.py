from langchain_tools import AnalyzerTool, SummarizerTool, AlerterTool  # Adjust import paths as needed

def test_tools():
    analyzer = AnalyzerTool()
    summarizer = SummarizerTool()
    alerter = AlerterTool()

    query = input("Enter a query to analyze : ")

    print("Testing AnalyzerTool...")
    result = analyzer._run(query)
    print("Analyzer result:", result)

    print("\nTesting SummarizerTool...")
    summary = summarizer._run()
    print("Summary:", summary)

    print("\nTesting AlerterTool...")
    alert_result = alerter._run()
    print("Alert result:", alert_result)

if __name__ == "__main__":
    test_tools()

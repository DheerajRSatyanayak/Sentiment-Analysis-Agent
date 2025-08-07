import pandas as pd
from transformers import pipeline, BartTokenizer

def summarize_posts():
    df = pd.read_csv("data/reddit_sentiment.csv")
    titles = df['title'].dropna().astype(str).tolist()
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", tokenizer=tokenizer)
    full_text = "\n".join(titles)
    def split_text_by_tokens(text, tokenizer, max_tokens=1024):
        sentences = text.split("\n")
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            tokens = tokenizer(current_chunk + sentence, return_tensors="pt", truncation=False)["input_ids"]
            if tokens.shape[1] > max_tokens:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + "\n"
            else:
                current_chunk += sentence + "\n"
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks
    def summarize_chunks(chunks, max_len=100, min_len=30):
        summaries = []
        for chunk in chunks:
            summary = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        return summaries
    chunks = split_text_by_tokens(full_text, tokenizer, max_tokens=1024)
    summaries = summarize_chunks(chunks, max_len=60, min_len=20)
    final_summary = "\n".join(summaries)
    with open("data/daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(final_summary)
    return final_summary

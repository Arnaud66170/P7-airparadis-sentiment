# === gradio_ui_ultimate.py ===
# Interface Gradio principale avec visualisation, feedback, historique

import gradio as gr
from shared.predict_utils import predict_single
from config import FEEDBACK_ALERT_THRESHOLD
import pandas as pd
import plotly.express as px
import random
from collections import deque

# === Globals ===
HISTORY_LIMIT = 5
feedback_tracker = deque(maxlen=10)
history = deque(maxlen=HISTORY_LIMIT)
counter_pos, counter_neg = 0, 0

# === Tweets d'exemple ===
tweet_examples = [
    "Absolutely loved the flight! Smooth and comfortable.",
    "Worst airline experience ever. Delayed and rude staff.",
    "It was okay. Nothing spectacular but not horrible either.",
    "Food was decent. Crew was polite.",
    "Three hours delay. Again. Seriously Air Paradis?"
]

# === Prediction runner ===
def run_prediction(tweet):
    global counter_pos, counter_neg
    pred = predict_single(tweet)
    history.appendleft(pred)
    if pred['label'] == 1:
        counter_pos += 1
    elif pred['label'] == 0:
        counter_neg += 1

    html_sentiment = f"<h2 style='color:{pred['color']};text-align:center;'>🧭 Sentiment: {pred['sentiment']} ({pred['proba']}%)</h2>"
    return html_sentiment, pred['emoji'], pred['proba'], update_pie_chart(), update_history()

# === Visualisation dynamique ===
def update_pie_chart():
    df = pd.DataFrame({"Sentiment": ["Positive", "Negative"], "Count": [counter_pos, counter_neg]})
    fig = px.pie(df, values='Count', names='Sentiment', title='Live Sentiment Distribution', color='Sentiment', color_discrete_map={"Positive": "green", "Negative": "red"})
    return fig

def update_history():
    df = pd.DataFrame(list(history))
    if not df.empty:
        return df[["text", "sentiment", "proba"]].rename(columns={"text": "Tweet", "sentiment": "Sentiment", "proba": "Confidence"})
    else:
        return pd.DataFrame(columns=["Tweet", "Sentiment", "Confidence"])

# === Feedback logging ===
def log_feedback(feedback, comment):
    feedback_tracker.append(feedback)
    count_bad = list(feedback_tracker).count("👎 No")
    if count_bad >= FEEDBACK_ALERT_THRESHOLD:
        return "⚠️ Too many negative feedbacks recently!", update_pie_chart(), update_history()
    return "✅ Feedback saved!", update_pie_chart(), update_history()

# === Reset ===
def reset_all():
    return "", "", 0, update_pie_chart(), update_history(), None, "", ""

# === UI ===
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    <div style="text-align: center">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Airplane_silhouette.svg/512px-Airplane_silhouette.svg.png" height="100" />
        <h1 style="color: #1E88E5;">✈️ Air Paradis - Sentiment Monitor</h1>
        <h4>Anticipate bad buzz with real-time tweet analysis</h4>
    </div>
    """)

    with gr.Row():
        tweet_input = gr.Textbox(lines=3, label="💬 Tweet to Analyze", placeholder="Enter or paste a tweet...")
        example_btn = gr.Button("🎲 Insert Example Tweet")

    with gr.Row():
        analyze_btn = gr.Button("🔍 Analyze Tweet")
        reset_btn = gr.Button("♻️ Reset")

    sentiment_output = gr.HTML()
    emoji_output = gr.Text(label="Sentiment Emoji", interactive=False)
    confidence_slider = gr.Slider(minimum=0, maximum=100, label="🔋 Confidence", interactive=False)

    with gr.Row():
        pie_plot = gr.Plot(label="📊 Sentiment Distribution")

    with gr.Accordion("🧠 Educational Panel", open=False):
        gr.Markdown("""
        **How does this model work?**
        - Tweets are cleaned and lemmatized (via spaCy)
        - Transformed into a vector using TF-IDF
        - Classified using a Logistic Regression model

        ✅ Fast and interpretable
        ❌ Not deep-learning based (but lighter and deployable)
        """)

    with gr.Accordion("🧾 History - Last 5 Tweets", open=True):
        history_display = gr.Dataframe(headers=["Tweet", "Sentiment", "Confidence"], interactive=False)

    with gr.Accordion("📩 Feedback", open=False):
        feedback = gr.Radio(["👍 Yes", "👎 No"], label="Was this prediction correct?")
        comment = gr.Textbox(label="Optional comment")
        feedback_btn = gr.Button("✅ Send Feedback")
        feedback_log = gr.Textbox(label="Feedback Status", interactive=False)

    analyze_btn.click(fn=run_prediction, inputs=tweet_input, outputs=[sentiment_output, emoji_output, confidence_slider, pie_plot, history_display])
    example_btn.click(fn=lambda: random.choice(tweet_examples), outputs=tweet_input)
    feedback_btn.click(fn=log_feedback, inputs=[feedback, comment], outputs=[feedback_log, pie_plot, history_display])
    reset_btn.click(fn=reset_all, outputs=[sentiment_output, emoji_output, confidence_slider, pie_plot, history_display, feedback, comment, feedback_log])

if __name__ == "__main__":
    demo.launch()

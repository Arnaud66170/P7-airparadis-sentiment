# === app.py ===
# Interface Gradio principale avec visualisation, feedback, historique, CSV logging, stats, thème jour/nuit

import gradio as gr
from shared.predict_utils import predict_single
from config import FEEDBACK_ALERT_THRESHOLD
import pandas as pd
import plotly.express as px
import random
from collections import deque
import csv
from datetime import datetime
import os

# === Globals ===
HISTORY_LIMIT = 5
feedback_tracker = deque(maxlen=10)
history = deque(maxlen=HISTORY_LIMIT)
counter_pos, counter_neg = 0, 0
FEEDBACK_CSV = "feedback_log.csv"
THEME_STATE = {"mode": "light"}


# === Tweets d'exemple ===
tweet_examples = [
    "Absolutely loved the flight! Smooth and comfortable.",
    "Worst airline experience ever. Delayed and rude staff.",
    "It was okay. Nothing spectacular but not horrible either.",
    "Food was decent. Crew was polite.",
    "Three hours delay. Again. Seriously Air Paradis?",
    "Why do I even bother booking here anymore?",
    "Clean cabin, quick boarding, and friendly service.",
    "Best flight I’ve had in years. Thanks, Air Paradis!",
    "Flight cancelled without warning. Zero accountability.",
    "I felt so relaxed the entire time. Loved this flight!",
    "Typical flight. Nothing stood out.",
    "Customer service doesn’t even pick up the phone.",
    "I’ll definitely fly again with Air Paradis. Great job!",
    "Arrived late, but I got home eventually.",
    "No WiFi, rude attendants, and terrible food.",
    "Seats were a bit tight, but the rest was fine.",
    "Had to wait two hours for luggage. Unacceptable.",
    "The food was edible. That's all I can say.",
    "Free snacks and warm smiles. Way to go!",
    "Very impressed with how professional the crew was.",
    "This airline is a disaster. Avoid at all costs.",
    "Service was decent. Could be better, could be worse.",
    "Not sure how I feel about this airline yet.",
    "Late again. No explanation. Classic Air Paradis.",
    "Another delay with Air Paradis. Getting ridiculous.",
    "Fantastic flight with Air Paradis today! Everything was smooth.",
    "Truly a 5-star airline experience. Keep it up!",
    "It did the job. Got me from A to B.",
    "Landed ahead of time. Comfortable seats and kind staff.",
    "They lost my suitcase and acted like it was normal.",
    "Mediocre experience. Nothing more to say.",
    "This was the worst flight of my life.",
    "Typical flight. Nothing stood out.",
    "Clean cabin, quick boarding, and friendly service.",
    "Customer service doesn’t even pick up the phone.",
    "Flight cancelled without warning. Zero accountability.",
    "Seats were a bit tight, but the rest was fine.",
    "Best flight I’ve had in years. Thanks, Air Paradis!",
    "Free snacks and warm smiles. Way to go!",
    "Landed ahead of time. Comfortable seats and kind staff.",
    "No WiFi, rude attendants, and terrible food.",
    "Service was decent. Could be better, could be worse.",
    "I’m on the fence about recommending them.",
    "Another delay with Air Paradis. Getting ridiculous.",
    "This airline is a disaster. Avoid at all costs.",
    "Not sure how I feel about this airline yet.",
    "Very impressed with how professional the crew was.",
    "I’ll definitely fly again with Air Paradis. Great job!",
    "Three hours delay. Again. Seriously Air Paradis?",
    "The food was edible. That's all I can say.",
    "Worst airline experience ever. Delayed and rude staff.",
    "Clean cabin, quick boarding, and friendly service.",
    "Fantastic flight with Air Paradis today! Everything was smooth.",
    "Why do I even bother booking here anymore?",
    "Arrived late, but I got home eventually.",
    "Customer service doesn’t even pick up the phone.",
    "Landed ahead of time. Comfortable seats and kind staff.",
    "They lost my suitcase and acted like it was normal.",
    "Free snacks and warm smiles. Way to go!",
    "Not sure how I feel about this airline yet.",
    "No complaints at all. Excellent service from Air Paradis.",
    "Service was decent. Could be better, could be worse.",
    "Seats were a bit tight, but the rest was fine.",
    "Best flight I’ve had in years. Thanks, Air Paradis!",
    "Flight cancelled without warning. Zero accountability.",
    "Another delay with Air Paradis. Getting ridiculous.",
    "Worst airline experience ever. Delayed and rude staff.",
    "Clean cabin, quick boarding, and friendly service.",
    "Arrived late, but I got home eventually.",
    "They lost my suitcase and acted like it was normal.",
    "Mediocre experience. Nothing more to say.",
    "Food was decent. Crew was polite.",
    "Flight cancelled without warning. Zero accountability.",
    "Why do I even bother booking here anymore?",
    "Truly a 5-star airline experience. Keep it up!",
    "No complaints at all. Excellent service from Air Paradis.",
    "I felt so relaxed the entire time. Loved this flight!",
    "Customer service doesn’t even pick up the phone.",
    "Another delay with Air Paradis. Getting ridiculous.",
    "Worst airline experience ever. Delayed and rude staff.",
    "Seats were a bit tight, but the rest was fine.",
    "Not sure how I feel about this airline yet.",
    "This was the worst flight of my life.",
    "I’m on the fence about recommending them.",
    "Flight cancelled without warning. Zero accountability.",
    "Free snacks and warm smiles. Way to go!",
    "Fantastic flight with Air Paradis today! Everything was smooth.",
    "Why do I even bother booking here anymore?",
    "They lost my suitcase and acted like it was normal.",
    "Late again. No explanation. Classic Air Paradis.",
    "No WiFi, rude attendants, and terrible food.",
    "Customer service doesn’t even pick up the phone.",
    "This airline is a disaster. Avoid at all costs.",
    "Service was decent. Could be better, could be worse.",
    "Seats were a bit tight, but the rest was fine.",
    "I’ll definitely fly again with Air Paradis. Great job!",
    "Clean cabin, quick boarding, and friendly service.",
    "Had to wait two hours for luggage. Unacceptable.",
    "Worst airline experience ever. Delayed and rude staff.",
    "Best flight I’ve had in years. Thanks, Air Paradis!",
    "Very impressed with how professional the crew was.",
    "This was the worst flight of my life.",
    "Three hours delay. Again. Seriously Air Paradis?",
    "Fantastic flight with Air Paradis today! Everything was smooth.",
    "No WiFi, rude attendants, and terrible food.",
    "Another delay with Air Paradis. Getting ridiculous.",
    "The food was edible. That's all I can say."
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

# === Feedback logging (enregistrement CSV) ===
def save_feedback(tweet, sentiment, confidence, feedback, comment):
    timestamp = datetime.now().isoformat()
    row = {
        "tweet": tweet,
        "predicted_label": sentiment,
        "proba": confidence,
        "user_feedback": feedback,
        "comment": comment,
        "timestamp": timestamp
    }
    file_exists = os.path.isfile(FEEDBACK_CSV)
    with open(FEEDBACK_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    return "✅ Feedback enregistré avec succès.", update_feedback_stats()

# === Feedback stats ===
def update_feedback_stats():
    if not os.path.exists(FEEDBACK_CSV):
        return "No feedback yet."
    df = pd.read_csv(FEEDBACK_CSV)
    count_yes = (df['user_feedback'] == '👍 Yes').sum()
    count_no = (df['user_feedback'] == '👎 No').sum()
    total = len(df)
    return f"👍 Yes: {count_yes} | 👎 No: {count_no} | Total: {total}"

def reset_feedback_csv():
    if os.path.exists(FEEDBACK_CSV):
        os.remove(FEEDBACK_CSV)
    return "Feedback reset."

# === Reset complet des stats ===
def reset_all():
    return "", "", 0, update_pie_chart(), update_history(), None, "", "", update_feedback_stats()

def reset_all_stats():
    global counter_pos, counter_neg, history, feedback_tracker
    counter_pos = 0
    counter_neg = 0
    history.clear()
    feedback_tracker.clear()
    return update_pie_chart(), update_history(), update_feedback_stats()

# === Changement de thème ===
def toggle_theme():
    if THEME_STATE['mode'] == 'light':
        THEME_STATE['mode'] = 'dark'
        return gr.themes.Base(text_primary="#f0f0f0", background_fill_primary="#1a1a1a")
    else:
        THEME_STATE['mode'] = 'light'
        return gr.themes.Soft()

# === UI ===
with gr.Blocks(theme=gr.themes.Soft(), title="Sentiment UI") as demo:
    theme_switch_btn = gr.Button("🌞 / 🌙 Switch Theme")

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
        reset_stats_btn = gr.Button("🧹 Reset Stats")

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
        feedback_stats = gr.Textbox(label="📊 Feedback Stats", interactive=False)
        feedback_dl = gr.File(label="⬇️ Download feedback CSV")
        feedback_reset = gr.Button("🧻 Reset Feedback Log")

    analyze_btn.click(fn=run_prediction, inputs=tweet_input, outputs=[sentiment_output, emoji_output, confidence_slider, pie_plot, history_display])
    example_btn.click(fn=lambda: random.choice(tweet_examples), outputs=tweet_input)
    feedback_btn.click(fn=save_feedback, inputs=[tweet_input, sentiment_output, confidence_slider, feedback, comment], outputs=[feedback_log, feedback_stats])
    reset_btn.click(fn=reset_all, outputs=[sentiment_output, emoji_output, confidence_slider, pie_plot, history_display, feedback, comment, feedback_log, feedback_stats])
    reset_stats_btn.click(fn=reset_all_stats, outputs=[pie_plot, history_display, feedback_stats])
    feedback_reset.click(fn=reset_feedback_csv, outputs=[feedback_log])
    feedback_dl.upload(fn=lambda x: x, inputs=[], outputs=[feedback_dl])
    theme_switch_btn.click(fn=toggle_theme, outputs=None)

if __name__ == "__main__":
    demo.launch()
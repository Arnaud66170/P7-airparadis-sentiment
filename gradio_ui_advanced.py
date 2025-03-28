import gradio as gr
import requests
import csv
import os
import pandas as pd
from datetime import datetime

# === Appel réel à l'API FastAPI LogReg (TF-IDF) ===
def predict_sentiment(tweet, model_choice):
    try:
        response = requests.post("http://localhost:8000/predict", json={"text": tweet})
        response.raise_for_status()
        data = response.json()
        label = data.get("label", 0)
        proba = data.get("proba", 0.0)

        sentiment = "Negative" if label == 0 else "Positive"
        emoji = "😠" if label == 0 else "😊"
        confidence = f"{proba * 100:.1f}%"

        return sentiment, confidence, emoji, proba * 100

    except Exception as e:
        print("❌ API Error:", e)
        return "Error", "0%", "❓", 0

# === Interface avancée ===
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # ✈️ Air Paradis - Sentiment AI ✨
    _Predict bad buzz before takeoff_
    """)

    with gr.Row():
        tweet_input = gr.Textbox(label="💬 Tweet", placeholder="Ex: My flight was delayed again...", lines=3)
        model_choice = gr.Dropdown(choices=["LogReg (TF-IDF)"], value="LogReg (TF-IDF)", label="🧠 Model")

    with gr.Row():
        submit_btn = gr.Button("🔍 Analyze Sentiment")
        reset_btn = gr.Button("♻️ Reset")

    with gr.Row():
        sentiment_out = gr.Text(label="📌 Sentiment")
        confidence_out = gr.Text(label="🎯 Confidence")
        emoji_out = gr.Text(label="😃 Emoji")

    confidence_slider = gr.Slider(label="🔋 Confidence Gauge", minimum=0, maximum=100, step=1, interactive=False)

    with gr.Accordion("📝 Feedback (Was the prediction correct?)", open=False):
        feedback = gr.Radio(["👍 Yes", "👎 No"], label="Feedback")
        comment = gr.Textbox(lines=2, placeholder="Optional comment...", label="Comment")
        submit_feedback = gr.Button("📩 Submit Feedback")

    # === Callback pour prédiction ===
    submit_btn.click(
        fn=predict_sentiment,
        inputs=[tweet_input, model_choice],
        outputs=[sentiment_out, confidence_out, emoji_out, confidence_slider]
    )

    # === Callback Feedback (sauvegarde en CSV) ===
    def log_feedback(feedback, comment):
        log_path = "feedback_log.csv"
        with open(log_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().isoformat(), feedback, comment])
        return "✅ Feedback saved!"

    feedback_result = gr.Textbox(label="✅ Confirmation", interactive=False)
    submit_feedback.click(fn=log_feedback, inputs=[feedback, comment], outputs=feedback_result)

    # === Affichage du fichier CSV ===
    with gr.Row():
        show_log_btn = gr.Button("📂 Show Feedback Log")
        feedback_table = gr.Dataframe(label="🧾 Feedback Log", visible=False)

    def load_feedback_log():
        if os.path.exists("feedback_log.csv"):
            df = pd.read_csv("feedback_log.csv", header=None)
            df.columns = ["Timestamp", "Feedback", "Comment"]
            return gr.update(visible=True), df
        else:
            return gr.update(visible=True), pd.DataFrame([["", "", ""]], columns=["Timestamp", "Feedback", "Comment"])

    show_log_btn.click(fn=load_feedback_log, inputs=[], outputs=[feedback_table, feedback_table])

    # === Reset bouton ===
    def reset_all():
        return "", "", "", 0, None, "", ""

    reset_btn.click(fn=reset_all, inputs=[], outputs=[sentiment_out, confidence_out, emoji_out, confidence_slider, feedback, comment, feedback_result])

if __name__ == "__main__":
    demo.launch()
# === gradio_ui_batch.py ===
# Interface Gradio dédiée à l'analyse par lot (multi-lignes ou fichiers)

import gradio as gr
import pandas as pd
import os
from shared.predict_utils import predict_batch
from config import DEFAULT_BATCH_COLUMN_NAMES, EXPORT_FILENAME, EXPORT_FOLDER

os.makedirs(EXPORT_FOLDER, exist_ok=True)

# === Variable globale pour stocker les derniers résultats ===
last_results = pd.DataFrame()

def update_last_results(df):
    global last_results
    last_results = df
    return df

# === Analyse via texte multi-lignes ===
def analyze_multiline(text_block):
    lines = [line.strip() for line in text_block.strip().splitlines() if line.strip()]
    results = predict_batch(lines)
    return update_last_results(results)

# === Analyse via fichier CSV ou XLSX ===
def analyze_file(file):
    if file is None:
        return pd.DataFrame()
    try:
        ext = os.path.splitext(file.name)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(file.name)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file.name)
        else:
            return pd.DataFrame([{"Error": "Unsupported file format"}])

        # Détection auto colonne texte
        col = next((c for c in df.columns if c.lower() in DEFAULT_BATCH_COLUMN_NAMES), None)
        if col is None:
            return pd.DataFrame([{"Error": "No valid column found"}])

        results = predict_batch(df[col].dropna().tolist())
        return update_last_results(results)
    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])

# === Export des derniers résultats ===
def export_csv():
    export_path = os.path.join(EXPORT_FOLDER, EXPORT_FILENAME)
    last_results.to_csv(export_path, index=False)
    return export_path

# === Export du fichier feedback global ===
def export_feedback_log():
    if os.path.exists("feedback_log.csv"):
        return "feedback_log.csv"
    else:
        return None

# === Interface Gradio ===
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📊 Batch Tweet Sentiment Analyzer
    Analyze multiple tweets via text or file input, and export results.
    """)

    with gr.Tabs():
        with gr.Tab("📝 Paste Tweets"):
            multiline_input = gr.Textbox(lines=10, label="Paste multiple tweets (one per line)")
            analyze_btn = gr.Button("🔍 Analyze All")
            output_table_1 = gr.Dataframe(label="Results")

            analyze_btn.click(fn=analyze_multiline, inputs=multiline_input, outputs=output_table_1)

        with gr.Tab("📂 Upload File"):
            file_input = gr.File(label="Upload .csv or .xlsx file")
            file_output = gr.Dataframe(label="Results")
            file_analyze_btn = gr.Button("📊 Analyze File")

            file_analyze_btn.click(fn=analyze_file, inputs=file_input, outputs=file_output)

    gr.Markdown("## 💾 Export des résultats d'analyse")
    export_btn = gr.Button("⬇️ Export Last Results")
    export_path_display = gr.File(label="Download CSV")

    export_btn.click(fn=export_csv, inputs=[], outputs=export_path_display)

    gr.Markdown("## 📝 Export Feedback Log")
    feedback_export_btn = gr.Button("📥 Télécharger feedback_log.csv")
    feedback_export_output = gr.File(label="⬇️ Cliquez pour télécharger")

    feedback_export_btn.click(
        fn=export_feedback_log,
        inputs=[],
        outputs=feedback_export_output
    )

if __name__ == "__main__":
    demo.launch()

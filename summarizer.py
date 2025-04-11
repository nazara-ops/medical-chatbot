
from fpdf import FPDF
from transformers import pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_chat(chat_history):
    full_text = "\n".join(f"Patient: {x['Patient']}\nDoctor: {x['Doctor']}" for x in chat_history)
    return summarizer(full_text, max_length=150, min_length=60)[0]['summary_text']

def generate_pdf(chat_history, patient_info, filename="patient_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Patient Summary", ln=True, align="C")
    pdf.ln(10)
    for k, v in patient_info.items():
        pdf.cell(200, 10, f"{k}: {v}", ln=True)
    pdf.ln(5)
    for chat in chat_history:
        pdf.multi_cell(0, 10, f"Patient: {chat['Patient']}\nDoctor: {chat['Doctor']}")
        pdf.ln(2)
    pdf.output(filename)
    return filename

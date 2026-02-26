import streamlit as st
import fitz
from generator import QuestionGenerator

st.title("📚 AI Practice Question Generator")

uploaded_file = st.file_uploader("Upload Academic PDF", type=["pdf"])

def extract_text(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


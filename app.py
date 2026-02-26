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

if uploaded_file:
    st.success("PDF Uploaded Successfully!")

    if st.button("Generate Questions"):
        with st.spinner("Generating Questions..."):
            text = extract_text(uploaded_file)
            generator = QuestionGenerator()
            result = generator.generate_questions(text)

        st.subheader("Generated Questions:")
        st.write(result)
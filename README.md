📚 PDF Question Generator

PDF Question Generator is an AI-powered web application that extracts text from academic PDF documents and generates university-level short-answer questions using the **FLAN-T5 Transformer model**.

The project was initially developed using Streamlit for rapid prototyping and later refactored into a structured Flask-based web application with a static HTML frontend. The application is served using the Waitress WSGI server for production readiness.

Application Flow

User uploads PDF
↓
Flask receives file via `/generate` route
↓
Text extraction using PyMuPDF (fitz)
↓
Text cleaning and preprocessing
↓
Token-aware chunking (to fit FLAN-T5 input limits)
↓
Question generation using `google/flan-t5-base`
↓
Duplicate removal and numbering
↓
Render questions in HTML template
↓
Display results in browser

🤖 AI Model Used

The system uses:

FLAN-T5 (google/flan-t5-base)

* Transformer-based text-to-text generation model
* Accessed using HuggingFace `pipeline("text2text-generation")`
* Generates short-answer academic questions
* Deterministic output (`do_sample=False`)
* Token-aware chunking ensures compatibility with model limits

🛠 Technologies Used

* Python
* Flask (Web Framework)
* Waitress (Production WSGI Server)
* HuggingFace Transformers
* FLAN-T5 (google/flan-t5-base)
* PyMuPDF (PDF text extraction)
* HTML & CSS

⚙ How It Works

1. The user uploads an academic PDF through the web interface.
2. Flask processes the file and extracts text using PyMuPDF.
3. The extracted text is cleaned and split into token-based chunks to avoid exceeding the model's maximum input size.
4. Each chunk is passed to the FLAN-T5 model to generate clear university-level short-answer questions.
5. Duplicate questions are removed and numbered automatically.
6. The final list of questions is rendered using an HTML template.
7. The application runs using Waitress for production deployment.

 🏗 Architecture Summary

Frontend (HTML)
→ Flask Backend
→ PDF Processing (PyMuPDF)
→ FLAN-T5 Question Generation
→ Post-Processing
→ HTML Rendering



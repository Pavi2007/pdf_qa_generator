from flask import Flask, render_template, request, redirect, url_for
import fitz
import os
from generator import QuestionGenerator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def extract_text_from_bytes(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    uploaded_file = request.files.get('pdf')
    if not uploaded_file:
        return redirect(url_for('index'))

    pdf_bytes = uploaded_file.read()
    text = extract_text_from_bytes(pdf_bytes)

    gen = QuestionGenerator()
    questions_text = gen.generate_questions(text)
    questions = [q for q in questions_text.split('\n') if q.strip()]

    return render_template('results.html', questions=questions)


if __name__ == '__main__':
    import socket
    from waitress import serve

    port = 8501

    def get_local_ips():
        ips = set()
        try:
            hostname = socket.gethostname()
            for ip in socket.gethostbyname_ex(hostname)[2]:
                if not ip.startswith("127."):
                    ips.add(ip)
        except Exception:
            pass

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ips.add(s.getsockname()[0])
            s.close()
        except Exception:
            pass

        if not ips:
            ips.add("127.0.0.1")

        return sorted(ips)

    ips = get_local_ips()
    print(f" * Starting server on port {port}")
    print(f" * Local: http://127.0.0.1:{port}")
    for ip in ips:
        if ip != "127.0.0.1":
            print(f" * Network: http://{ip}:{port}")

    # Start waitress server
    serve(app, host='0.0.0.0', port=port)


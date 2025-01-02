import os
from flask import Flask, render_template, request, send_file
from txt_parser import file_parser
from zebra_pdf import generate_pdf
from concat_pdf import merge_pdf
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Ensure required directories exist
os.makedirs('queue', exist_ok=True)
os.makedirs('zebras_pdf', exist_ok=True)

@app.route('/zebra-label-pdf-generator', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_content = file.read().decode('utf-8')

    # Parse the file into batches
    batch_files, now = file_parser(file_content)

    batch_files_pdf, now = generate_pdf(batch_files, now)

    # Generate PDFs for parsed batches
    pdf_files = generate_pdf(batch_files, now)

    # Merge PDFs into a single file
    merged_pdf_path = merge_pdf(pdf_files, now)

    # Use try-finally to ensure cleanup
    try:
        return send_file(merged_pdf_path, mimetype="application/pdf", as_attachment=True, download_name="zebra_labels.pdf")
    finally:
        # Cleanup files
        for file in os.listdir("queue"):
            if file.startswith(str(now)):
                os.remove(f"queue/{file}")
        for file in os.listdir("zebras_pdf"):
            if file.startswith(str(now)):
                os.remove(f"zebras_pdf/{file}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8000)
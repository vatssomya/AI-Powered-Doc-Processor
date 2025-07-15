import os, tempfile, re
from flask import Flask, render_template, request, send_file, jsonify
from pytesseract import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import pandas as pd
from transformers import pipeline

app = Flask(__name__)
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Global context for QnA
full_text_global = ""

# Document-type-specific field dictionaries
DOCUMENT_PATTERNS = {
    "invoice": [
        (r'Invoice\s*No[:\s]*([\w\-\/]+)', "Invoice No"),
        (r'Date[:\s]*([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})', "Date"),
        (r'Party\s*Name[:\s]*(.*)', "Party Name"),
        (r'Total[:\s]*Rs\.?\s*([0-9,\.]+)', "Total Amount"),
        (r'HS\s*Code[:\s]*([\d\.]+)', "HS Code")
    ],
    "passport": [
        (r'Name[:\s\n]*([A-Za-z ]+)', "Name"),
        (r'Date\s*of\s*Birth[:\s\n]*([0-9]{2}[-/][0-9]{2}[-/][0-9]{4})', "DOB"),
        (r'Nationality[:\s\n]*([A-Za-z]+)', "Nationality"),
        (r'Passport\s*No[:\s\n]*([A-Z0-9]+)', "Passport No"),
        (r'Place\s*of\s*Issue[:\s\n]*([A-Za-z ]+)', "Place of Issue"),
        (r'Date\s*of\s*Issue[:\s\n]*([0-9]{2}[-/][0-9]{2}[-/][0-9]{4})', "Date of Issue"),
        (r'Date\s*of\s*Expiry[:\s\n]*([0-9]{2}[-/][0-9]{2}[-/][0-9]{4})', "Date of Expiry")
    ],
    "medical": [
        (r'Patient\s*Name[:\s\n]*([A-Za-z ]+)', "Patient Name"),
        (r'Doctor\'s\s*Name[:\s\n]*([A-Za-z\. ]+)', "Doctor Name"),
        (r'Date[:\s\n]*([0-9]{2}[-/][0-9]{2}[-/][0-9]{4})', "Date"),
        (r'Diagnosis[:\s\n]*([A-Za-z0-9 ,\-]+)', "Diagnosis"),
        (r'Prescription[:\s\n]*([A-Za-z0-9 ,\-]+)', "Prescription"),
        (r'Next\s*Visit[:\s\n]*([0-9]{2}[-/][0-9]{2}[-/][0-9]{4})', "Next Visit"),
        (r'Hospital[:\s\n]*([A-Za-z ]+)', "Hospital")
    ]
}

def extract_fields(text, doc_type):
    patterns = DOCUMENT_PATTERNS.get(doc_type, [])
    fields = {}
    for patt, label in patterns:
        match = re.search(patt, text, re.IGNORECASE)
        if match:
            fields[label] = match.group(1).strip()
    return fields

@app.route('/', methods=['GET', 'POST'])
def index():
    global full_text_global
    all_fields = []
    all_texts = []
    summaries = []
    merged_summary = ""

    if request.method == 'POST':
        doc_type = request.form.get("doc_type", "invoice")
        files = request.files.getlist('file')

        for file in files:
            ext = file.filename.rsplit('.', 1)[-1].lower()
            images = []

            if ext == 'pdf':
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                    file.save(tmp.name)
                    images = convert_from_path(tmp.name, 300)
            else:
                images = [Image.open(file)]

            full_text = ""
            for img in images:
                full_text += pytesseract.image_to_string(img) + "\n"

            all_texts.append(full_text)

            fields = extract_fields(full_text, doc_type)
            all_fields.append(fields)

            try:
                summary = summarizer(full_text[:1024])[0]['summary_text']
            except:
                summary = "Summary could not be generated."
            summaries.append(summary)

        with open("output.txt", "w") as f:
            for i, fieldset in enumerate(all_fields):
                f.write(f"\n--- Document {i+1} ---\n")
                for k, v in fieldset.items():
                    f.write(f"{k}: {v}\n")

        pd.DataFrame(all_fields).to_excel("output.xlsx", index=False)
        pd.DataFrame(all_fields).to_csv("output.csv", index=False) 

        combined_text = "\n".join(all_texts)
        full_text_global = combined_text

        try:
            merged_summary = summarizer(combined_text[:2048])[0]['summary_text']
        except:
            merged_summary = "Merged summary could not be generated."

        return render_template("index.html",
                               extracted=all_fields,
                               summary=merged_summary,
                               summaries=summaries)

    return render_template("index.html", extracted=None)


    @app.route('/download/<filetype>')
def download(filetype):
    if filetype == "txt":
        return send_file("output.txt", as_attachment=True)
    elif filetype == "excel":
        return send_file("output.xlsx", as_attachment=True)
    elif filetype == "csv":  # ✅ Add this block
        return send_file("output.csv", as_attachment=True)
    return "File not found", 404

@app.route('/ask', methods=['POST'])
def ask():
    global full_text_global  # <-- Add this line

    question = request.form.get("question")
    if not question:
        return jsonify({"answer": "No question provided."})

    if not full_text_global.strip():
        return jsonify({"answer": "Unable to generate answer. Try re-uploading the document."})

    try:
        answer = qa_pipeline({
            'question': question,
            'context': full_text_global
        })['answer']
        return jsonify({"answer": answer})
    except Exception as e:
        print("QnA error:", str(e))
        return jsonify({"answer": "An error occurred while generating the answer."})


if __name__ == '__main__':
    app.run(debug=True)

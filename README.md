# 📄 Automated Document Processor

> Smart offline document understanding using AI — powered by Python, Flask, and Transformers.

---

## 🧩 Problem Statement

In professional workflows, users often need to extract key data from large PDFs or scanned documents like invoices, bills, or reports. Manual extraction is tedious, error-prone, and not scalable. Moreover, accessing intelligent insights like summaries or asking questions from such documents is often limited to cloud-based or premium tools.

This project solves that by building an **entirely offline, AI-powered web app** that extracts key fields, generates summaries, and allows question answering from uploaded PDFs and images.

---

## 📝 Project Description

The **Automated Document Processor** is a Flask-based offline web application that allows users to:

- Upload multiple documents (PDFs or images)
- Extract structured data fields like invoice numbers, dates, totals, etc.
- Get merged and individual summaries using NLP
- Ask smart questions about the document contents via a chatbot
- Interact through a sleek, responsive, and dark-mode-enabled UI

All processing is done **locally**, ensuring data privacy and eliminating the need for internet or cloud APIs.

---

## ✨ Features

- ✅ Upload **multiple PDFs or images**
- 📄 **Extracted Fields View** (collapsible for each doc)
- 🧠 **AI-powered Summaries**:
  - Combined (merged) summary
  - Individual doc-wise summaries (shown optionally)
- 💬 **Chatbot Q&A**: Ask questions from the combined content
- 🌗 **Dark Mode Toggle** with smooth transition
- 📥 Export to `.txt` and `.xlsx`
- 🔒 Works **100% Offline**
- 🖼️ OCR support using Tesseract for scanned images
- ⚡ Smooth animations and loading indicators

---

## 🚀 How It Works

1. Upload documents (PDFs/images)
2. Backend extracts text using OCR (Tesseract) and PDF parsers
3. Text is passed to:
   - Summarizer model (`facebook/bart-large-cnn`)
   - QnA model (`distilbert-base-cased-distilled-squad`)
4. Fields are extracted using rule-based logic (regex + AI if needed)
5. Results are displayed and downloadable

---

## 🛠 Tech Stack

| Layer       | Technology                                  |
|-------------|---------------------------------------------|
| Frontend    | HTML, CSS, JavaScript, Bootstrap 5, AOS     |
| Backend     | Flask (Python)                              |
| AI Models   | Hugging Face Transformers                   |
| OCR         | pytesseract (Tesseract OCR engine)          |
| PDF/Image   | pdf2image, Pillow                           |
| Export      | pandas (for `.xlsx`, `.txt`)                |
| Hosting     | Localhost / offline server (runs offline)   |

---

## 🧠 AI Models Used

- **Summarization:** `facebook/bart-large-cnn`
- **QnA:** `distilbert-base-cased-distilled-squad`

These models are loaded locally via Hugging Face Transformers — no internet required after setup.

---

## 🧪 Screenshots

_Adding soon_

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/automated-doc-processor.git](https://github.com/your-username/automated-doc-processor.git)
cd automated-doc-processor


### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate # On Windows
# or
source venv/bin/activate # On macOS/Linux

### 3. Install Dependencies

```bash
pip install -r requirements.txt

### 4. Install Tesseract OCR

🔗 Download from: https://github.com/tesseract-ocr/tesseract

After installing, update the path in `app.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

### 5. Run the App

```bash
python app.py

Then, open your browser and go to:
```cpp
http://127.0.0.1:5000


## 📁 Folder Structure
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── output.txt
├── output.xlsx


---

## 📦 requirements.txt

Flask==2.3.2
pytesseract==0.3.10
pdf2image==1.16.3
Pillow==9.5.0
transformers==4.40.1
torch==2.2.2
pandas==2.2.2


---

## 🔐 Offline Mode

Once installed and the models are downloaded the first time, everything works 100% offline:

❌ No external API calls

🔐 Privacy-friendly: all data stays local

🧠 Summarization and Q&A happen on-device

---

## 👨‍💻 Developer

**Somya Vats**
Student @ UPES | Developer | Tech Explorer

Built with ❤️, styled with ✨, and powered by AI.

---

## 📄 License

This project is licensed under the MIT License.

---

## 💡 Future Improvements

✅ NLP-based entity extraction using SpaCy

✅ Table extraction and processing

✅ Docker support for container deployment

✅ Voice-based Q&A (Multimodal Input)

---

⭐ If you liked this project, please star it on GitHub and share it with others!



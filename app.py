import os
import json
import uuid
import PyPDF2
import requests
from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
app = Flask(__name__)
client = Anthropic()

# Store documents in memory
documents = {}

# Memory file
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"sessions": []}

def save_memory(session):
    memory = load_memory()
    memory["sessions"].append(session)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    
    doc_id = str(uuid.uuid4())
    documents[doc_id] = text
    return jsonify({ 'success': True, 'doc_id': doc_id })

@app.route('/upload-url', methods=['POST'])
def upload_url():
    url = request.json['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    
    doc_id = str(uuid.uuid4())
    documents[doc_id] = text
    return jsonify({ 'success': True, 'doc_id': doc_id })

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']
    doc_ids = data['doc_ids']
    
    # Combine all documents
    combined_text = ""
    for doc_id in doc_ids:
        if doc_id in documents:
            combined_text += documents[doc_id] + "\n\n"
    
    # Send to Claude
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""You are an energy consultant research assistant.

Document content:
{combined_text}

Question: {question}

Answer like a consultant. Include:
1. A clear answer
2. Exact citations from the document
3. Three follow-up questions to consider"""
        }]
    )
    
    answer = response.content[0].text
    answer = response.content[0].text

# Save to memory
    save_memory({
        "question": question,
        "answer": answer,
        "doc_ids": doc_ids
    })
    return jsonify({ 'answer': answer })

@app.route('/memory', methods=['GET'])
def get_memory():
    memory = load_memory()
    return jsonify(memory)

if __name__ == '__main__':
    app.run(debug=True)




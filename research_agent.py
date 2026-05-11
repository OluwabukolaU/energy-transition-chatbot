import os
import PyPDF2
import requests
from dotenv import load_dotenv
from anthropic import Anthropic 
# Load API key
load_dotenv()
client = Anthropic()

print("=" * 50)
print(" Energy Research Agent ")
print("=" * 50)

pdf_path = input("\nEnter PDF path or URL: ")
# Extract text from PDF
def extract_pdf_text(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Scrape text from URL
def scrape_url(url):
    response = requests.get(url)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

# Extract and confirm
# Decide PDF or URL
if pdf_path.startswith("https://"):
    document_text = scrape_url(pdf_path)
else:
    document_text = extract_pdf_text(pdf_path)
print("\n✅ Document uploaded successfully!")
print(f"📄 Extracted {len(document_text)} characters")


# Question loop
while True:
    question = input("\n🔍 Ask a question about the document: ")
    
    if question.lower() == "quit":
        print("\nGoodbye! 👋")
        break
    
    # Send to Claude
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""You are an energy consultant research assistant.
                
Document content:
{document_text}

Question: {question}

Answer the question like a consultant. Include:
1. A clear answer
2. Citations from the document (quote exact phrases)
3. Three follow-up questions the user should consider"""
            }
        ]
    )
    
    print("\n" + "=" * 50)
    print(response.content[0].text)
    print("=" * 50)
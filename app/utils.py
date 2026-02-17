import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import pypdf
import os
import io

def extract_text_from_url(url):
    """
    Fetches text content from a URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Simple extraction of all paragraph text
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return text
    except Exception as e:
        return f"Error extracting text from URL: {e}"

def extract_text_from_file(file_storage):
    """
    Extracts text from a file (PDF or Text).
    file_storage is a Werkzeug FileStorage object.
    """
    filename = file_storage.filename.lower()
    try:
        if filename.endswith('.pdf'):
            reader = pypdf.PdfReader(file_storage)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        elif filename.endswith('.txt') or filename.endswith('.md'):
            return file_storage.read().decode('utf-8')
        else:
            return "Unsupported file type. Please upload PDF or Text files."
    except Exception as e:
        return f"Error extracting text from file: {e}"

def generate_artifacts(api_key, context, context_type):
    """
    Interacts with Gemini Pro to generate testing artifacts.
    """
    if not api_key:
        return "API Key is required."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        Act as an expert Quality Engineer. Based on the following {context_type}, generate a comprehensive test strategy.

        Context:
        {context}

        Please provide the output in Markdown format with the following sections:
        1. Test Strategy
        2. Test Cases (Table format)
        3. Test Conditions
        4. Boundary Test Cases
        5. Test Data
        6. Acceptance Criteria
        7. Critical Analysis
        8. Recommendations
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating artifacts: {e}"

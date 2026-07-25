import json
import os
from dotenv import load_dotenv
import pytesseract
from PIL import Image
import pdfplumber
from google import genai
from google.genai import types

# Load the API key from the .env and initialize the GenAI client
load_dotenv()
client = genai.Client()

# Extracts text from the PDF using pdfplumber and returns it as a string separated by newlines.
def extract_text_from_pdf(path: str) -> str:
    """Extract raw text from a PDF file using pdfplumber if available."""
    if pdfplumber is None:
        raise RuntimeError("pdfplumber is not installed")
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)

# NOT COMPLETED DO NOT EVEN TOUCH THIS I WILL COME TO YOUR HOUSE AND KILL YOU IF YOU TOUCH THIS
def extract_text_from_image(path: str) -> str:
    """Extract raw text from an image file using pytesseract if available."""
    if pytesseract is None or Image is None:
        raise RuntimeError("Pillow or pytesseract is not installed")
    img = Image.open(path)
    return pytesseract.image_to_string(img)

# Parses document text using Gemini 3.5 Flash Lite model to extract relevant details in strict JSON format.
def parse_document(raw_text: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"Extract all relevant details from this document into strict JSON format:\n\n{raw_text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    return response.text

if __name__ == "__main__":
    print("--- SCRIPT STARTED ---")
    
    pdf_filename = "your_invoice.pdf"
    print(f"Attempting to read: {pdf_filename}")
    
    try:
        sample_text = extract_text_from_pdf(pdf_filename)
        print("PDF read successfully! Length of text:", len(sample_text))
        
        print("Sending to Gemini...")
        json_string_response = parse_document(sample_text)
        print("Got response from Gemini!")
        
        output_file = "extracted_output.json"
        parsed_data = json.loads(json_string_response)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, indent=4, ensure_ascii=False)
            
        print(f"SUCCESS! File saved as '{output_file}'")
        
    except Exception as e:
        print(f"CRASHED WITH ERROR: {e}")
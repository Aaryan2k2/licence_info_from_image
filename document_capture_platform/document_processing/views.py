from django.shortcuts import render
import pytesseract
from PIL import Image
from django.shortcuts import redirect
from .forms import DocumentForm
from .models import Document
import re

# Specify the path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Update this for your system


def extract_info(text):
    # Define your regex patterns
    name_pattern = re.compile(
    r'(?:Name\s*:\s*|Full Name\s*:\s*|Holder Name\s*:\s*|Applicant Name\s*:\s*|Name of Holder\s*:\s*|Name of Applicant\s*:\s*|NAMES?\s*:\s*)(.*?)(?=\s*[\n;]|$)', 
    re.IGNORECASE)
    
    document_number_pattern = re.compile(r'(?:D/L\s*No\s*:\s*)([A-Z0-9\/\s-]+)(?=\s*Date)', re.IGNORECASE)
    
    expiration_date_pattern = re.compile(
    r'(?:expires?\s*:\s*|expiration\s*date\s*:\s*|valid\s*until\s*:\s*|valid\s*till\s*:\s*|to\s*:\s*|from\s*:\s*\d{2}/\d{2}/\d{4}\s*to\s*:\s*)(\d{2}/\d{2}/\d{4})', 
    re.IGNORECASE)

    
    # Search for matches
    name_match = name_pattern.search(text)
    document_number_match = document_number_pattern.search(text)
    expiration_date_match = expiration_date_pattern.search(text)

    # Extract values or set to None if not found
    name = name_match.group(1).strip() if name_match else None
    document_number = document_number_match.group(1).strip() if document_number_match else None
    expiration_date = expiration_date_match.group(1).strip() if expiration_date_match else None

    return name, document_number, expiration_date

def handle_uploaded_file(uploaded_file):
    """
    Handle file uploads and extract text from the file.
    Supports image files only.
    """
    # Use Tesseract to extract text from the image
    image = Image.open(uploaded_file)
    text = pytesseract.image_to_string(image)

    print(text)
    return text

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()

            # Perform OCR on the uploaded image
            text = handle_uploaded_file(document.document_image)

            # Extract details
            name, document_number, expiration_date = extract_info(text)

            context = {
                'form': form,
                'name': name,
                'document_number': document_number,
                'expiration_date': expiration_date,
                'text':text,
            }
            return render(request, 'result.html', context)
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})

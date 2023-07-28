from django.shortcuts import render
import pytesseract
import tempfile
from PyPDF2 import PdfReader
from PIL import Image
import os
from django.http import HttpResponse, FileResponse
from wsgiref.util import FileWrapper
from pathlib import Path
def home(request):
    if request.method == 'POST':
        if 'pdf' in request.FILES:
            pdf = request.FILES['pdf']
            text = extract_text_from_pdf(pdf)
        elif 'image' in request.FILES:
            image = request.FILES['image']
            text = extract_text_from_image(image)
        else:
            return render(request, 'ocr_app/home.html')
        if text is None:
            message = "Unable to extract text."
            return render(request, 'ocr_app/home.html', {'message': message})
        file_path = save_text_to_file(text)
        if file_path:
            return render(request, 'ocr_app/home.html', {'file_path': file_path})
        else:
            message = "Unable to save text to file."
            return render(request, 'ocr_app/home.html', {'message': message})
    return render(request, 'ocr_app/home.html')
def extract_text_from_pdf(pdf):
    try:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(pdf.read())
        with open(temp_file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    finally:
        if temp_file_path:
            os.remove(temp_file_path)
def extract_text_from_image(image):
    try:
        img = Image.open(image)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        text = pytesseract.image_to_string(img, lang='eng')
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None
def save_text_to_file(text):
    try:
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w') as temp_file:
            temp_file.write(text)

        return temp_file.name
    except Exception as e:
        print(f"Error saving text to file: {e}")
        return None
def download_text_file(request):
    file_path = request.GET.get('file_path')
    if file_path:
        try:
            path = Path(file_path)
            if path.exists():
                with path.open('rb') as file:
                    response = HttpResponse(file.read(), content_type='text/plain')
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                    response['Content-Length'] = path.stat().st_size
                    return response
            else:
                return HttpResponse("Text file not found.")
        except IOError:
            return HttpResponse("Text file not found.")
    else:
        return HttpResponse("Text file not found.")

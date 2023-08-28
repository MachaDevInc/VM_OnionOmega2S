import sys
from pdf2image import convert_from_path
from pytesseract import image_to_string

def pdf_to_text_ocr(pdf_file):
    # Convert the PDF to a list of images
    images = convert_from_path(pdf_file)

    text = ''
    # Iterate through each image (corresponding to a page)
    for i, img in enumerate(images):
        # OCR the image to get the text
        page_text = image_to_string(img)
        text += page_text + '\n'
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pdf_to_text_ocr_v2.py <PDF_file>")
    else:
        pdf_file = sys.argv[1]
        text = pdf_to_text_ocr(pdf_file)
        print(text)

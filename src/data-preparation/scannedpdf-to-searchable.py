# Import libraries
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os

'''
Converts scanned pdf into searchable pdf or text using OCR (Optical character recognition)
Pdf converted to image and content read from image are stored into text file
https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
https://pypi.org/project/pytesseract/
'''

#Explicit path for tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path of the scanned pdf
basepath = os.path.dirname(os.path.abspath(__file__))
#datapath = basepath +'/data/hugh-murray/chapter3/'
datapath = basepath +'/data/henry-yule/index/'
#PDF for each individual chapter
PDF_file = "index.pdf"

''' 
Part #1 : Converting PDF to images 
'''

# Store all the pages of the PDF files
# Specify external path of the poppler
pages = convert_from_path(datapath+PDF_file, poppler_path="E:/software/poppler-0.67.0_x86/bin/")

# One image per page of PDF
image_counter = 1

if not os.path.exists(datapath+'index-images'):
    os.makedirs(datapath+'index-images')

# Iterate through all the pages of PDF
for page in pages:
    filename = "page_" + str(image_counter) + ".jpg"

    # Save the image of the page in system
    page.save(datapath+'index-images/'+filename, 'JPEG')

    # Increment the counter to update filename
    image_counter = image_counter + 1

''' 
Part #2 - Recognizing text from the images using OCR 
'''

# Variable to get count of total number of pages
totalpages = image_counter - 1

# Creating a text file to write the output
outfile = "index-full-original.txt"

# Open the file in append mode so that
# All contents of all images are added to the same file
outfile = open(datapath+outfile, "a")

# Iterate from 1 to total number of pages
for i in range(1, totalpages + 1):
    filename = "page_" + str(i) + ".jpg"

    # Recognize the text as string in image using pytesserct
    text = str(((pytesseract.image_to_string(Image.open(datapath+'index-images/'+filename)))))
    text = text.replace('-\n', '')

    # Add processed text to text file
    outfile.write(text)

outfile.close()

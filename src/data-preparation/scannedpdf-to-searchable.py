#!/usr/bin/venv python3
# Import libraries
from PIL import Image
import pytesseract
from pathlib import Path
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

def scannedpdf_to_images(readfile,part,author):
    '''
    Part #1 : Converting PDF to images
    '''

    # Store all the pages of the PDF files
    # Specify external path of the poppler
    pages = convert_from_path(readfile, poppler_path="E:/software/poppler-0.67.0_x86/bin/")
    # One image per page of PDF
    image_counter = 1

    if not os.path.exists(datapath /'results/{}/{}/OCR/{}-images'.format(author,part,part)):
        os.makedirs(datapath /'results/{}/{}/OCR/{}-images'.format(author,part,part))

    # Iterate through all the pages of PDF
    for page in pages:
         print("{} page".format(image_counter))
         filename = "page_" + str(image_counter) + ".jpg"

         # Save the image of the page in system
         page.save(datapath /'results/{}/{}/OCR/{}-images/'.format(author,part,part) / filename, 'JPEG')

         # Increment the counter to update filename
         image_counter = image_counter + 1

    return image_counter


def images_to_text(image_counter,part,author):
    ''' 
    Part #2 - Recognizing text from the images using OCR 
    '''

    # Variable to get count of total number of pages
    totalpages = image_counter - 1

    # Creating a text file to write the output
    outfile = "{}-full-original.txt".format(part)

    # Open the file in append mode so that
    # All contents of all images are added to the same file
    outfile = open(datapath /'results/{}/{}/OCR'.format(author,part)/outfile, "a")

    # Iterate from 1 to total number of pages
    for i in range(1, totalpages + 1):
        filename = "page_" + str(i) + ".jpg"

        # Recognize the text as string in image using pytesserct
        text = str(((pytesseract.image_to_string(Image.open(datapath /'results/{}/{}/OCR/{}-images'.format(author,part,part) /filename)))))
        text = text.replace('-\n', '')

        # Add processed text to text file
        print("content addded")
        outfile.write(text)
        print("++++++++++++++++++++++")

    return outfile
    print("=============================")
    outfile.close()
    print("*****************************")


# Path of the scanned pdf
datapath = Path(__file__).resolve().parents[2]

#book = ['part1','part2','part3']
book = ['index']
author = "henry-yule"
for part in book:

    readfile = datapath / 'data/hugh-murray/{}/{}.pdf'.format(part,part)  # Input individual index files
    print(readfile)
    if not os.path.exists(datapath /'results/{}/{}'.format(author,part)):
        os.makedirs(datapath /'results/{}/{}'.format(author,part))

    if not os.path.exists(datapath /'results/{}/{}/OCR'.format(author,part)):
        os.makedirs(datapath /'results/{}/{}/OCR'.format(author,part))

    image_counter = scannedpdf_to_images(readfile,part,author)
    outfile = images_to_text(image_counter,part,author)
    outfile.close()
    print("Processing for {} has been completed".format(part))
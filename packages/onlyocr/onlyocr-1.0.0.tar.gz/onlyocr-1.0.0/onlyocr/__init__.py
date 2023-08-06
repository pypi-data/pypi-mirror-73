import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
#import sys
from tkinter import Tk
import tkinter as tk
from tkinter.filedialog import askopenfilename
#import cv2
#import numpy as np
import os
import logging
import json

logging.basicConfig(level = logging.INFO, filename = "app.log", format = '%(asctime)s %(message)s', filemode = 'w') 
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr():
	Tk().withdraw()
	inputfile = askopenfilename()
	name, ext = os.path.splitext(inputfile)
	logging.info("Extension")
	#print(ext)
	if ext == ".pdf" or ext == ".jpg" or ext == ".png" or ext == ".bmp" or ext == ".jpeg" :
		pdfFile = wi(filename = inputfile, resolution = 500) 
		image = pdfFile.convert('jpeg')
		logging.info("Conversion to jpeg")

		imageBlobs = []

		for img in image.sequence:
			imgPage = wi(image = img)
			imageBlobs.append(imgPage.make_blob('jpeg'))
			logging.info("Stored as blobs")

		extract = []

		for imgBlob in imageBlobs:
			image = Image.open(io.BytesIO(imgBlob))
			text = pytesseract.image_to_string(image, lang = 'eng')
			logging.info("Conversion to string")
			extract.append(text)
			logging.info("String stored")

		json_list = json.dumps(extract)
		#print(json_list)

		"""root = tk.Tk()
		root.title("Output")
		S = tk.Scrollbar(root)
		T = tk.Text(root, height = 25, width = 75)
		S.pack(side=tk.RIGHT, fill=tk.Y)
		T.pack(side=tk.LEFT, fill=tk.Y)
		S.config(command=T.yview)
		T.config(yscrollcommand=S.set)
		T.insert(tk.END, extract)
		tk.mainloop()
		logging.info("Output")"""

		return json_list

	else:
		"""out = "Please select a pdf or image file!"
		root = tk.Tk()
		root.title("Output")
		S = tk.Scrollbar(root)
		T = tk.Text(root, height = 25, width = 75)
		S.pack(side=tk.RIGHT, fill=tk.Y)
		T.pack(side=tk.LEFT, fill=tk.Y)
		S.config(command=T.yview)
		T.config(yscrollcommand=S.set)
		T.insert(tk.END, out)
		tk.mainloop()
		logging.info("Output")"""

		return 0
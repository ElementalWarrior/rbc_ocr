#!/usr/bin/env python3
import sys
from PIL import Image
import pyocr
from wand.image import Image as Img
import pyocr.builders
from pdf2image import convert_from_path
import cv2
import numpy as np
from matplotlib import pyplot as plt
import unicodecsv as csv
import re
import os

template = cv2.imread('divider.jpg',0)
w, h = template.shape[::-1]


tools = pyocr.get_available_tools()[0]


file=os.path.abspath(sys.argv[1])
print(file)
filename=file.split("/")[-1]
try:
    os.mkdir(".ocr")
except OSError:  
    pass

#convert pdf to img
pages = convert_from_path(file, 500)
#print(pages)
i = 0
files = []
output = []
for page in pages:
    i = i + 1
    page_filename = ".ocr/" + filename + ".%s.png" % i
    page.save(page_filename, 'PNG')
    files = files + [page_filename]
    
    #divider recognition start
    img_rgb = cv2.imread(page_filename)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    
    ret, thresh = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
    frame = cv2.GaussianBlur(img_gray, (0, 0), 10);
    thresh = cv2.addWeighted(img_gray, 1.5, frame, -0.5, 0);
    cv2.imwrite(page_filename + '.out.png',thresh)
    
    res = cv2.matchTemplate(thresh,template,cv2.TM_CCORR_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    pts = zip(*loc[::-1])
    
    # collect ycoords of separators
    ycoords = []
    for pt in pts:
    	add = True
    	y = pt[1]
    	for stored_y in ycoords:
    		if abs(y - stored_y) < 5:
    			add = False
    			break
    	if add:
    		ycoords = ycoords + [pt[1]]
    if len(ycoords) == 0:
    	continue
    #add the last row as it is missing a bottom border.
    ycoords = ycoords + [ycoords[-1] + 210 + 5]
    # print(ycoords)
    img = Image.open(page_filename + '.out.png')
    for i in range(len(ycoords)-1):
    	#crop to transaction size
    	box = img.getbbox()
    	crop_img = img.crop((415, 0, 2415, box[3]))
    	box = crop_img.getbbox()
    	
    	# crop to individual transaction
    	crop_img = crop_img.crop((0, ycoords[i]+5, box[2], ycoords[i+1]))
    	
    	#get date
    	box = crop_img.getbbox()
    	trans_date = crop_img.crop((0,box[1]+5, 240, box[3]))
    	trans_date.save("foobar.png")
    	dt = tools.image_to_string(trans_date, builder=pyocr.builders.TextBuilder())
    	
    	#get details
    	details = crop_img.crop((440, box[1], box[2], box[3]))
    	text = tools.image_to_string(details, builder=pyocr.builders.TextBuilder())
    	lines = list(filter(None, text.split("\n")))
    	dollar_pos = lines[0].find("$")
    	negative = False
    	if lines[0][dollar_pos-1] == "-":
    		negative = True
    	foreign_exchange_line = lines[2] if len(lines) > 2 else ""
    	currency = None
    	exchange_rate = None
    	extra = ""
    	if len(foreign_exchange_line) > 0:
    		foreign_exchange_line = re.sub(r'q(?!u)', 'g', foreign_exchange_line)
    		try:
    			currency = foreign_exchange_line.split("Exchange rate-")[0].replace('Foreign Currency-', '')
    			exchange_rate = foreign_exchange_line.split("Exchange rate-")[1]
    		except IndexError:
    			print("Could not find Exchange rate: IndexError")
    			extra = foreign_exchange_line
    	d = {
    		"date": dt,
    		"description": lines[0].split("$")[0],
    		"amount": ("-" if negative else "") + lines[0].split("$")[1],
    		"transaction_number": lines[1] if len(lines) > 2 else "",
    		"exchange_rate": exchange_rate if exchange_rate is not None else "",
    		"foreign_currency": currency if currency is not None else "",
    		"extra": extra
    	}
    	output = output + [d]
with open(filename.replace(".pdf", ".csv"), mode="wb") as csv_file:
    # print(output[0].keys())
    writer = csv.DictWriter(csv_file, delimiter=",", fieldnames=output[0].keys())
    writer.writeheader()
    for trans in output:
    	writer.writerow(trans)

#!/usr/bin/python
import datetime
now = datetime.datetime.now()
import os
import re
import subprocess
import time
import logging
import sys
sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys

import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont



response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
print(response)
ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)
#ping = "44"
#download = "1,4MB"
#upload = "3 MB"


try:
    epd = epd2in13_V2.EPD() # get the display
    epd.init(epd.FULL_UPDATE)           # initialize the display
    print("Clear...")    # prints to console, not the display, for debugging
    epd.Clear(0xFF)
    #Mostramos en pantalla resultados 
    title = ImageFont.truetype("pic/Font.ttc", 25)
    font = ImageFont.truetype("pic/Font.ttc", 15)
    fontlittle = ImageFont.truetype("pic/Font.ttc", 12)
    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    draw.text((55, 5), "SPEEDTEST", font = title, fill = 0)
    draw.text((75, 30), str(now.strftime("%d-%m %H:%M")), font = fontlittle, fill = 0)

    draw.text((20, 71), str(ping), font = font, fill = 0)
    draw.text((20, 90), "ping", font = fontlittle, fill = 0)

    draw.text((103, 71), str(download), font = font, fill=0)
    draw.text((103, 90), "download", font = fontlittle, fill=0)

    draw.text((180,71), str(upload), font = font, fill=0)
    draw.text((180, 90), "upload", font = fontlittle, fill=0)

    epd.display(epd.getbuffer(image))






except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()

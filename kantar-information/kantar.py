#-*- coding:utf-8 -*-
import urllib.request
from urllib.error import HTTPError
import time
from bs4 import BeautifulSoup
import csv
import re
import os
import socks
from sockshandler import SocksiPyHandler
opener = urllib.request.build_opener(SocksiPyHandler(socks.SOCKS5, "127.0.0.1", 1080))
urllib.request.install_opener(opener)

csvfile = open('csvtest.csv','r')
#reader = csv.reader(csvfile)
#writer = csv.writer(csvfile)

arrtitle = []
strtitle = []
arrtext = []
arrimage = []
data = {}

headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}

for m in range(0, 87):
	url = "http://www.informationisbeautifulawards.com/showcase?page=" + str(m) + "&type=awards" 
	page = urllib.request.Request(url, headers = headers)
	try:
		response = urllib.request.urlopen(page)
		soupkantar = BeautifulSoup(response,'lxml')

		titlekantar = soupkantar.find_all(attrs={'class':'title'})
		for title in titlekantar:
			titlecontent = title.find("a")
			arrtitle.append(titlecontent.text)
			strtitle.append(str(titlecontent.text).replace(" ",""))

		#textkantar = soupkantar.find_all(attrs={'class':'text'})
		#for textcontent in textkantar:
			#arrtext.append(textcontent.text)
			
		imgkantar = soupkantar.find_all(attrs={'class':'image'})
		for image in imgkantar:
			imgsrc = image.find("img")['src']
			arrimage.append(imgsrc.replace("medium","large"))
		
		time.sleep(10)
	except HTTPError as e:
		content = e.read()

for n in range(0, len(arrimage) + 1):
	if strtitle[n].find("png") == -1:
		urllib.request.urlretrieve(arrimage[n],(strtitle[n] + '.jpg')[:6].replace("/",""))
	else:
		urllib.request.urlretrieve(arrimage[n], (strtitle[n] + '.jpg')[:6].replace("/","")
#writer.writerow(['Title', 'Text', 'Img'])
#for line in list(zip(arrtitle,arrtext,arrimage)):
	#writer.writerow(line)

#csvfile.close()
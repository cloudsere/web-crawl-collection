#-*- coding:utf-8 -*-
import urllib.request
import csv
import time
import socks
from sockshandler import SocksiPyHandler
from urllib.error import HTTPError


opener = urllib.request.build_opener(SocksiPyHandler(socks.SOCKS5, "127.0.0.1", 1080))
#opener.addheaders=[('User-Agent','Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)')]
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

urllib.request.install_opener(opener)

csvfile = open('csvtest.csv','r')
reader = csv.reader(csvfile)

csvfile2 = open('csvtest2.csv','r')
reader2 = csv.reader(csvfile2)

imgcolumn = [row[2] for row in reader]
titlecolumn = [row[0] for row in reader2]

for n in range(1140, len(imgcolumn)):
	page = urllib.request.Request(imgcolumn[n].replace("medium","large"), headers = hdr)
	try:
		data = urllib.request.urlopen(page).read()
		filename = str(n) + " " + titlecolumn[n][:12].replace("/","").replace("-","") + '.jpg'
		with open(filename,'wb') as f:
			f.write(data)
			time.sleep(10)
	except HTTPError as e:
		content = e.read()

		#urllib.request.urlretrieve(imgcolumn[n].replace("medium","large"), str(n) + " " + titlecolumn[n][:12].replace("/","").replace("-","") + '.jpg')
		
	

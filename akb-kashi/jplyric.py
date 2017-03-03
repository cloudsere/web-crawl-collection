import urllib.request
from bs4 import BeautifulSoup
import time
import csv
import socks
from sockshandler import SocksiPyHandler
import selenium
from selenium import webdriver
opener = urllib.request.build_opener(SocksiPyHandler(socks.SOCKS5,"127.0.0.1",1080))
urllib.request.install_opener(opener)

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}

url = ["http://www.uta-net.com/search/?Aselect=1&Bselect=3&Keyword=akb48&sort=&pnum=1",
		"http://www.uta-net.com/search/?Aselect=1&Bselect=3&Keyword=akb48&sort=&pnum=2",
		"http://www.uta-net.com/search/?Aselect=1&Bselect=3&Keyword=akb48&sort=&pnum=1",
		"http://www.uta-net.com/search/?Aselect=1&Keyword=ske48&Bselect=3&x=0&y=0",
		"http://www.uta-net.com/search/?Aselect=1&Keyword=nmb48&Bselect=3&x=0&y=0",
		"http://www.uta-net.com/search/?Aselect=1&Keyword=hkt48&Bselect=3&x=0&y=0",
		"http://www.uta-net.com/search/?Aselect=1&Keyword=%94T%96%D8%8D%E2&Bselect=3&x=0&y=0"]
artist = []
songtime = []
title = []
lyric = []

csvfile = open("output.csv","a")
writer = csv.writer(csvfile)

for m in range(0,7):
	response = urllib.request.Request(url[m],headers = headers)
	page = urllib.request.urlopen(response)
	time.sleep(30)
	page = page.read()
	soup = BeautifulSoup(page,'lxml')

	bigTable = soup.find("tbody")
	if bigTable == None:
		break;
	else:
		bigRow = soup.find_all("tr")

		for smallRow in bigRow:
			if smallRow.find(attrs={"class":"td2"}) != None:
				smallArtist = smallRow.find(attrs={"class":"td2"}).text #得到歌手名
				artist.append(smallArtist)

				smallInfo = smallRow.find(attrs={"class":"side td1"})
				if smallInfo != None:
					songTitle = smallInfo.text #得到歌名
					title.append(songTitle)

					outerHref = smallInfo.find("a")['href']
					songHref =  "http://www.uta-net.com" + outerHref #得到歌词页面的超链接

					songResponse = urllib.request.Request(songHref,headers = headers)
					songPage = urllib.request.urlopen(songResponse)
					songSoup = BeautifulSoup(songPage,'lxml')

					outerTime = songSoup.find(attrs={"id":"view_amazon"})
					if outerTime != None:
						songTime = outerTime.text.split("商品")[0] #在这里得到发售时间
						songtime.append(songTime)
					else:
						songtime.append("时间未知")

					outerHref = songSoup.find(attrs={"id":"ipad_kashi"})
					midHref = outerHref.find("img")['src']
					lastHref = "http://www.uta-net.com" + midHref #得到歌词svg的地址

					kashiResponse = urllib.request.Request(lastHref,headers = headers)
					kashiPage = urllib.request.urlopen(kashiResponse)
					kashiSoup = BeautifulSoup(kashiPage,'lxml')
					lastKashi = kashiSoup.find('g').text #在这里得到歌词文本
					lyric.append(lastKashi)
	time.sleep(1)

writer.writerow(['Title','Artist','Time','Lyric'])

for line in list(zip(title,artist,songtime,lyric)):
	writer.writerow(line)
import urllib.request
from bs4 import BeautifulSoup
import csv

headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}

nianfen = ["2017","2016","2015","2011_2014","2000_2010","1990_1999","1980_1989","1964_1979"]
fufei = ["0","2"]

csvfile = open('output.csv','a')
writer = csv.writer(csvfile)

filmtitle = []
filmrole = []
filmscore = []
filmtime = []
filmfufei = []

for m in range(0,8): #首先循环年份
	for n in range(0,2):#再循环免费和付费
		for k in range(0,33):#再按页循环
			url = "http://list.iqiyi.com/www/1/------27401----" + fufei[n] + "-" + nianfen[m] + "--4-"+ str(k) +"-1-iqiyi--.html"
			response = urllib.request.Request(url,headers=headers)
			page = urllib.request.urlopen(response)
			soup = BeautifulSoup(page,'lxml')
			movieinfo = soup.find_all(attrs={"class":"site-piclist_info"})
			if movieinfo == None:
				break;
			else:
				for info in movieinfo:
					title = info.find(attrs={"class":"mod-listTitle_left"})
					if title != None:
						titleinfo = title.find("a").text
						filmtitle.append(titleinfo)
					else:
						filmtitle.append("标题为空")

					role = info.find(attrs={"class":"role_info"})
					if role != None:
						roleinfo = role.text.replace("\n","").replace("\r","").replace(" ","")
						filmrole.append(roleinfo)
					else:
						filmrole.append("演员为空")

					score = info.find(attrs={"class":"score"})
					if score != None:
						scoreinfo = score.text
						filmscore.append(scoreinfo)
					else:
						filmscore.append("评分为空")

					filmtime.append(nianfen[m])
					if n == 0:
						filmfufei.append("免费")
					else:
						filmfufei.append("付费")
						

writer.writerow(['Title', 'Role', 'Score','Year','Free'])
for line in list(zip(filmtitle,filmrole,filmscore,filmtime,filmfufei)):
	writer.writerow(line)



import re
from time import sleep
import sys
import json
import urllib
from bs4 import BeautifulSoup
from datetime import timedelta, date


news_url = 'http://orientaldaily.on.cc/cnt/'

category_id = [176, 202, 210, 204, 170, 180, 286]
category_names = ['news','finance','finance','finance','china_world','china_world','sport']


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield end_date - timedelta(n)


start_date = date(2010, 1, 1)
end_date = date(2019, 1, 14)


for date in daterange(start_date,end_date):
    i = date.strftime("%Y")+date.strftime("%m")+date.strftime("%d")
    for c_id in range(7):
        for j in range(50):

            url = news_url + category_names[c_id] + "/"+ i + "/00" + str(category_id[c_id]) + "_" + '{:03d}'.format(j) + ".html"
            print(url)

            try:
                page = urllib.request.urlopen(url)
                soup = BeautifulSoup(page, 'html.parser')
                title_box = soup.find('h1')
                content_box = soup.find_all('p')
                title = title_box.text.strip()

                if(content_box == []):
                    print("no article with this url")
                    continue
                content = ""
                index=0
                for c in content_box:
                    s = c.text.strip()
                    if(index != len(content_box)-1):
                        content = content+s+"\n"
                    index+=1
                content = content.strip()
            except:
                print("no article with this url")
                continue

            idd = i + "_" + "00" + str(category_id[c_id]) + "_" + '{:03d}'.format(j)
            a = {"id": idd, "url": url, "title": title, "content": content}

            if(c_id==0):
                f = open("OD_local.txt", "a+", encoding='utf-8')
            elif(c_id==1 or c_id==2):
                f = open("OD_fin.txt", "a+", encoding='utf-8')
            elif(c_id==3):
                f = open("OD_estate.txt", "a+", encoding='utf-8')
            elif(c_id==4):
                f = open("OD_china.txt", "a+", encoding='utf-8')
            elif(c_id==5):
                f = open("OD_inter.txt", "a+", encoding='utf-8')
            elif(c_id==6):
                f = open("OD_sports.txt", "a+", encoding='utf-8')

            f.write(json.dumps(a,ensure_ascii=False))
            f.write('\n')
            f.close()



            print("Article " + title + " saved to file")
            sleep(1)

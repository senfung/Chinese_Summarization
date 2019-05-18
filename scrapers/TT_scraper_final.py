### use this code for scraping

import re
from time import sleep
import sys
import json
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup


news_url = ["http://hd.stheadline.com/news/realtime/hk/",
           "http://hd.stheadline.com/news/realtime/fin/",
           "http://hd.stheadline.com/news/realtime/chi/",
           "http://hd.stheadline.com/news/realtime/wo/",
           "http://hd.stheadline.com/news/realtime/pp/",
           "http://hd.stheadline.com/news/realtime/spt/"]

category = ['local','finance','china','international','estate','education']


# Range: 1400500 - 1401354
# Testing Range: 1401081-1401117
for i in range(1401354,1400500,-3):
    index = 0
    found_article = False

    for category_url in news_url:

        url = category_url + str(i)
        print (url)


        while True:

            try:
                page = urllib.request.urlopen(url)
                soup = BeautifulSoup(page, 'html.parser')
                title_box = soup.find('h1')
                content_box = soup.find('div',attrs={'id':'news-content'})
                title = title_box.text.strip()
                content = content_box.text.strip()

            except urllib.error.HTTPError as err:
                    print(err.code)
                    if err.code == 410:
                        print("no article with this url")
                        index = index+1
                        print(index)
                        break
                    elif err.code == 429:
                        print("retry in 60 sec")
                        sleep(60)
                        continue


            a = {"id": i, "url": url, "title": title, "content": content}

            if(index==0):
                f = open("TT_local.txt", "a+", encoding='utf-8')
            elif(index==1):
                f = open("TT_fin.txt", "a+", encoding='utf-8')
            elif(index==2):
                f = open("TT_china.txt", "a+", encoding='utf-8')
            elif(index==3):
                f = open("TT_inter.txt", "a+", encoding='utf-8')
            elif(index==4):
                f = open("TT_estate.txt", "a+", encoding='utf-8')
            elif(index==5):
                f = open("TT_edu.txt", "a+", encoding='utf-8')

            f.write(json.dumps(a,ensure_ascii=False))
            f.write('\n')
            f.close()



            print(category[index] + " Article " + title + " saved to file")
            sleep(1)

            found_article = True
            break
        if(found_article):
            break
